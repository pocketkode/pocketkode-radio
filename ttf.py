# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Text in other languages (and names the pixel font can't show): drawn with the Noto Sans JP, SC or KR font
(fonts/, SIL Open Font License) through the SDL2_ttf library that ships with muOS (nothing else is bundled).
English keeps the app's own pixel font."""
import ctypes
import ctypes.util
import os
from collections import OrderedDict

import sdl

_CANDIDATES = [
    os.environ.get("PKR_SDL2_TTF_LIB", ""),
    "/usr/lib/libSDL2_ttf-2.0.so.0",
    "/usr/lib/libSDL2_ttf.so",
    "/usr/lib/aarch64-linux-gnu/libSDL2_ttf-2.0.so.0",
    ctypes.util.find_library("SDL2_ttf") or "",
]
FONT_FILE = "NotoSansJP-Regular.otf"
KOREAN_FONT = "NotoSansKR-Regular.otf"
# symbols the Noto fonts don't have, drawn as close ones they do have
_SUBST = str.maketrans({"✗": "×", "✘": "×", "✔": "✓"})


class _Color(ctypes.Structure):
    _fields_ = [("r", ctypes.c_uint8), ("g", ctypes.c_uint8), ("b", ctypes.c_uint8), ("a", ctypes.c_uint8)]


class _Surface(ctypes.Structure):  # the first fields of SDL_Surface
    _fields_ = [("flags", ctypes.c_uint32), ("format", ctypes.c_void_p), ("w", ctypes.c_int), ("h", ctypes.c_int)]


def is_wide(ch):
    """Japanese (and other CJK) characters, and full-width punctuation: the pixel font doesn't have them."""
    o = ord(ch)
    return 0x2E80 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF


def is_hangul(ch):
    o = ord(ch)
    return 0xAC00 <= o <= 0xD7A3 or 0x1100 <= o <= 0x11FF or 0x3130 <= o <= 0x318F


def needs(s):
    return any(is_wide(ch) for ch in s)


class Text:
    """Renders strings with the font into textures (kept in a small cache: screens redraw 30 times a second)."""

    def __init__(self, renderer, app_dir, font_file=FONT_FILE):
        self.r = renderer
        self.fonts = {}
        self.cache = OrderedDict()
        self.sizes = {}
        self.path = os.path.join(app_dir, "fonts", font_file)
        if not os.path.exists(self.path):
            raise OSError(f"missing {self.path}")
        lib = None
        for p in _CANDIDATES:
            if p:
                try:
                    lib = ctypes.CDLL(p)
                    break
                except OSError:
                    continue
        if lib is None:
            raise OSError("SDL2_ttf library not found")
        f = lib.TTF_Init
        f.restype = ctypes.c_int
        if f() != 0:
            raise OSError("TTF_Init failed")
        self._open = lib.TTF_OpenFont
        self._open.restype, self._open.argtypes = ctypes.c_void_p, [ctypes.c_char_p, ctypes.c_int]
        self._size = lib.TTF_SizeUTF8
        self._size.restype = ctypes.c_int
        self._size.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
        self._render = lib.TTF_RenderUTF8_Blended
        self._render.restype, self._render.argtypes = ctypes.c_void_p, [ctypes.c_void_p, ctypes.c_char_p, _Color]
        self._ascent = lib.TTF_FontAscent
        self._ascent.restype, self._ascent.argtypes = ctypes.c_int, [ctypes.c_void_p]
        self._close = lib.TTF_CloseFont
        self._close.argtypes = [ctypes.c_void_p]
        self._to_tex = sdl.lib.SDL_CreateTextureFromSurface
        self._to_tex.restype, self._to_tex.argtypes = ctypes.c_void_p, [ctypes.c_void_p, ctypes.c_void_p]
        self._free = sdl.lib.SDL_FreeSurface
        self._free.argtypes = [ctypes.c_void_p]
        self.font(18)  # fails here (not while drawing) if the font can't be opened

    def font(self, px):
        f = self.fonts.get(px)
        if f is None:
            f = self._open(self.path.encode(), px)
            if not f:
                raise OSError(f"can't open {self.path}")
            self.fonts[px] = f
        return f

    def ascent(self, px):
        return self._ascent(self.font(px))

    def width(self, s, px):
        key = (s, px)
        w = self.sizes.get(key)
        if w is None:
            cw, ch = ctypes.c_int(), ctypes.c_int()
            self._size(self.font(px), s.translate(_SUBST).encode(), ctypes.byref(cw), ctypes.byref(ch))
            w = self.sizes[key] = cw.value
            if len(self.sizes) > 4000:
                self.sizes.clear()
        return w

    def texture(self, s, px):
        """(texture, w, h) of s in white; tinted when drawn."""
        key = (s, px)
        hit = self.cache.get(key)
        if hit:
            self.cache.move_to_end(key)
            return hit
        surf = self._render(self.font(px), s.translate(_SUBST).encode(), _Color(255, 255, 255, 255))
        if not surf:
            return None
        sp = ctypes.cast(surf, ctypes.POINTER(_Surface)).contents
        w, h = sp.w, sp.h
        tex = self._to_tex(self.r, surf)
        self._free(surf)
        if not tex:
            return None
        sdl.SetTextureBlendMode(tex, sdl.BLENDMODE_BLEND)
        self.cache[key] = (tex, w, h)
        while len(self.cache) > 300:
            _, (old, _w, _h) = self.cache.popitem(last=False)
            sdl.DestroyTexture(old)
        return self.cache[key]

    def close(self):
        for tex, _w, _h in self.cache.values():
            sdl.DestroyTexture(tex)
        self.cache.clear()
        for f in self.fonts.values():
            self._close(f)
        self.fonts.clear()
