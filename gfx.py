# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Screen drawing: window, colours, text (English: the pixel font; other languages and names the pixel font can't
show: a Noto font, see ttf.py), boxes, circles and bars."""
import ctypes
import os
import unicodedata

import font
import i18n
import sdl
import ttf

W, H = 640, 480

C = {
    "bg": (15, 15, 15),
    "bar": (28, 28, 28),
    "row": (36, 36, 36),
    "sel": (62, 62, 62),
    "accent": (0, 137, 123),
    "accent_hi": (0, 190, 170),
    "text": (241, 241, 241),
    "dim": (170, 170, 170),
    "faint": (110, 110, 110),
    "key": (48, 48, 48),
    "ok": (46, 160, 67),
    "warn": (214, 150, 20),
    "bad": (210, 70, 70),
    "black": (0, 0, 0),
}


class Screen:
    def __init__(self, title=b"PocketKode Radio"):
        if sdl.Init(sdl.INIT_VIDEO) != 0:
            raise RuntimeError(f"SDL_Init failed: {sdl.GetError()}")
        sdl.SetHint(b"SDL_RENDER_SCALE_QUALITY", b"0")  # crisp pixels
        flags = sdl.WINDOW_SHOWN
        if not os.environ.get("PKR_WINDOWED"):
            flags |= sdl.WINDOW_FULLSCREEN_DESKTOP
        self.window = sdl.CreateWindow(title, sdl.WINDOWPOS_UNDEFINED, sdl.WINDOWPOS_UNDEFINED, W, H, flags)
        if not self.window:
            raise RuntimeError(f"SDL_CreateWindow failed: {sdl.GetError()}")
        self.r = sdl.CreateRenderer(self.window, -1, sdl.RENDERER_ACCELERATED) or \
            sdl.CreateRenderer(self.window, -1, sdl.RENDERER_SOFTWARE)
        if not self.r:
            raise RuntimeError(f"SDL_CreateRenderer failed: {sdl.GetError()}")
        sdl.RenderSetLogicalSize(self.r, W, H)
        sdl.SetRenderDrawBlendMode(self.r, sdl.BLENDMODE_BLEND)
        sdl.ShowCursor(0)
        self._atlas()
        self._rect = sdl.Rect()
        self._src = sdl.Rect()
        self.app_dir = None
        self.fonts = {}      # font file → ttf.Text (False if it can't be used)

    def _font(self, name):
        t = self.fonts.get(name)
        if t is None and self.app_dir:
            try:
                t = ttf.Text(self.r, self.app_dir, name)
            except Exception as e:  # noqa: BLE001 - no font or no SDL2_ttf
                print(f"[gfx] font {name} unavailable:", e, flush=True)
                t = False
            self.fonts[name] = t
        return t or None

    def language_ok(self):
        """False when the current language's font can't be used (then the app switches to English)."""
        return i18n.current() == "en" or self._font(i18n.font_file()) is not None

    def _needs(self, s):
        """s has characters the pixel font can't draw (Cyrillic, CJK, Korean…)."""
        return any(ord(ch) >= 0x370 and ch not in self.index and ch not in font._ALIASES for ch in s)

    def tt(self, s):
        """The Noto renderer for s, or None when s is drawn with the pixel font."""
        if i18n.current() == "en" and not self._needs(s):
            return None
        return self._font(ttf.KOREAN_FONT if any(ttf.is_hangul(ch) for ch in s) else i18n.font_file())

    @staticmethod
    def _px(scale):
        return 9 * scale  # font size matching the pixel font at this scale

    # ------------------------------------------------------------------ font atlas
    def _atlas(self):
        chars = font.CHARS + ["\0"]  # "\0" = the box for unknown characters
        self.index = {c: i for i, c in enumerate(chars)}
        cols = 16
        rows_n = (len(chars) + cols - 1) // cols
        aw, ah = cols * font.GW, rows_n * font.GH
        px = (ctypes.c_uint32 * (aw * ah))()
        for i, ch in enumerate(chars):
            gx, gy = (i % cols) * font.GW, (i // cols) * font.GH
            for y, line in enumerate(font.rows(ch)):
                for x, c in enumerate(line):
                    if c == "#":
                        px[(gy + y) * aw + gx + x] = 0xFFFFFFFF
        self.atlas = sdl.CreateTexture(self.r, sdl.PIXELFORMAT_ARGB8888, sdl.TEXTUREACCESS_STATIC, aw, ah)
        sdl.UpdateTexture(self.atlas, None, px, aw * 4)
        sdl.SetTextureBlendMode(self.atlas, sdl.BLENDMODE_BLEND)
        self.cols = cols

    # ------------------------------------------------------------------ basics
    def color(self, c, a=255):
        sdl.SetRenderDrawColor(self.r, c[0], c[1], c[2], a)

    def clear(self, c=None):
        self.color(c or C["bg"])
        sdl.RenderClear(self.r)

    def present(self):
        sdl.RenderPresent(self.r)

    def box(self, x, y, w, h, c, a=255):
        self.color(c, a)
        rc = self._rect
        rc.x, rc.y, rc.w, rc.h = int(x), int(y), int(w), int(h)
        sdl.RenderFillRect(self.r, ctypes.byref(rc))

    def frame(self, x, y, w, h, c, t=2):
        self.box(x, y, w, t, c)
        self.box(x, y + h - t, w, t, c)
        self.box(x, y, t, h, c)
        self.box(x + w - t, y, t, h, c)

    def bar(self, x, y, w, h, frac, c=None, back=None):
        self.box(x, y, w, h, back or C["key"])
        frac = max(0.0, min(1.0, frac))
        if frac > 0:
            self.box(x, y, max(1, int(w * frac)), h, c or C["accent"])

    # ------------------------------------------------------------------ text
    def plain(self, s):
        """For the pixel font: map characters it lacks (accents dropped, é -> e; others shown as '?')."""
        out = []
        for ch in s:
            if ch in self.index or ch == " ":
                out.append(ch)
                continue
            alias = font._ALIASES.get(ch)
            if alias:
                out.append(alias)
                continue
            base = unicodedata.normalize("NFKD", ch)
            base = "".join(c for c in base if not unicodedata.combining(c))
            if base and all(c in self.index for c in base):
                out.append(base)
            elif unicodedata.category(ch).startswith(("Z", "C")):
                out.append(" ")
            else:
                out.append("?")
        return "".join(out)

    def text_w(self, s, scale=2):
        t = self.tt(s)
        if t:
            return t.width(s, self._px(scale))
        return max(0, len(self.plain(s)) * font.ADV * scale - scale)

    def fit(self, s, max_w, scale=2):
        """s shortened with '…' so it fits in max_w pixels."""
        if not self.tt(s):
            s = self.plain(s)
            per = max(1, (max_w + scale) // (font.ADV * scale))
            return s if len(s) <= per else s[:max(1, per - 1)].rstrip() + "…"
        if self.text_w(s, scale) <= max_w:
            return s
        while s and self.text_w(s + "…", scale) > max_w:
            s = s[:-1]
        return s.rstrip() + "…"

    def text(self, x, y, s, scale=2, c=None, align="left"):
        """Draw s with its top-left at (x, y). Returns the width drawn."""
        w = self.text_w(s, scale)
        if align == "center":
            x -= w // 2
        elif align == "right":
            x -= w
        c = c or C["text"]
        f = self.tt(s)
        if f:
            px = self._px(scale)
            t = f.texture(s, px)
            if t:
                tex, tw, th = t
                sdl.SetTextureColorMod(tex, c[0], c[1], c[2])
                dst = self._rect
                # the font's baseline sits where the pixel font's letters end
                dst.x, dst.y, dst.w, dst.h = int(x), int(y) + 7 * scale - f.ascent(px), tw, th
                sdl.RenderCopy(self.r, tex, None, ctypes.byref(dst))
            return w
        s = self.plain(s)
        sdl.SetTextureColorMod(self.atlas, c[0], c[1], c[2])
        src, dst = self._src, self._rect
        src.w, src.h = font.GW, font.GH
        dst.w, dst.h = font.GW * scale, font.GH * scale
        cx = int(x)
        for ch in s:
            if ch != " ":
                i = self.index.get(ch)
                if i is None:
                    i = self.index.get(font._ALIASES.get(ch, ch), self.index["\0"])
                src.x, src.y = (i % self.cols) * font.GW, (i // self.cols) * font.GH
                dst.x, dst.y = cx, int(y)
                sdl.RenderCopy(self.r, self.atlas, ctypes.byref(src), ctypes.byref(dst))
            cx += font.ADV * scale
        return w

    def wrap(self, s, max_w, scale=2):
        """Split s into lines no wider than max_w (hard line breaks with \\n)."""
        if self.tt(s):
            return self._wrap_font(s, max_w, scale)
        s = self.plain(s)
        per = max(1, (max_w + scale) // (font.ADV * scale))
        out = []
        for para in s.split("\n"):
            line = ""
            for word in para.split(" "):
                cand = word if not line else line + " " + word
                if len(cand) <= per:
                    line = cand
                else:
                    if line:
                        out.append(line)
                    while len(word) > per:
                        out.append(word[:per])
                        word = word[per:]
                    line = word
            out.append(line)
        return out

    # Chinese and Japanese have no spaces: a line may break after any of their characters, except before closing
    # punctuation and small kana, or after an opening bracket. Other words (Latin, Cyrillic, Korean) stay whole.
    NO_START = set("、。，．・：；？！ー」』）］｝〕〉》】ゃゅょっぁぃぅぇぉャュョッァィゥェォ…%％")
    NO_END = set("「『（［｛〔〈《【")

    def _wrap_font(self, s, max_w, scale):
        out = []
        for para in s.split("\n"):
            tokens = []  # (text, is_space)
            word = ""
            for ch in para:
                if ch == " ":
                    if word:
                        tokens.append((word, False))
                        word = ""
                    tokens.append((" ", True))
                elif ttf.is_wide(ch):
                    if word:
                        tokens.append((word, False))
                        word = ""
                    if ch in self.NO_START and tokens and not tokens[-1][1]:
                        tokens[-1] = (tokens[-1][0] + ch, False)
                    elif tokens and not tokens[-1][1] and tokens[-1][0][-1] in self.NO_END:
                        tokens[-1] = (tokens[-1][0] + ch, False)
                    else:
                        tokens.append((ch, False))
                else:
                    word += ch
            if word:
                tokens.append((word, False))
            line = ""
            for text, space in tokens:
                if space and not line:
                    continue
                cand = line + text
                if not line or self.text_w(cand.rstrip(), scale) <= max_w:
                    line = cand
                else:
                    out.append(line.rstrip())
                    line = "" if space else text
            out.append(line.rstrip())
        return out

    def para(self, x, y, s, max_w, scale=2, c=None, gap=6):
        """Wrapped text; returns the y below the last line."""
        lh = font.GH * scale + gap
        for line in self.wrap(s, max_w, scale):
            self.text(x, y, line, scale, c)
            y += lh
        return y

    # ------------------------------------------------------------------ chrome
    def title_bar(self, title, right=""):
        self.box(0, 0, W, 48, C["bar"])
        self.box(0, 48, W, 2, C["accent"])
        self.text(20, 12, title, 3)
        if right:
            self.text(W - 20, 18, right, 2, C["dim"], align="right")

    def footer(self, hints):
        """hints: [("A", "Open"), ("B", "Back")]. Longer translations get less space between hints, then are shortened."""
        self.box(0, H - 40, W, 40, C["bar"])
        keys = [self.text_w(key, 2) + 14 + 8 for key, _label in hints]
        labels = [self.text_w(label, 2) for _key, label in hints]
        room = W - 32
        gap = 22
        while gap > 8 and sum(keys) + sum(labels) + gap * (len(hints) - 1) > room:
            gap -= 2
        over = sum(keys) + sum(labels) + gap * (len(hints) - 1) - room
        if over > 0:  # shorten the longest labels until everything fits
            cap = max(labels)
            while cap > 20 and sum(min(w, cap) for w in labels) > sum(labels) - over:
                cap -= 4
            labels = [min(w, cap) for w in labels]
        x = 16
        for (key, label), kw, lw in zip(hints, keys, labels):
            self.box(x, H - 31, kw - 8, 22, C["key"])
            self.text(x + 7, H - 28, key, 2)
            x += kw
            if lw < self.text_w(label, 2):
                label = self.fit(label, lw)
            self.text(x, H - 28, label, 2, C["dim"])
            x += lw + gap

    def close(self):
        for t in self.fonts.values():
            if t:
                t.close()
        if self.atlas:
            sdl.DestroyTexture(self.atlas)
        if self.r:
            sdl.DestroyRenderer(self.r)
        if self.window:
            sdl.DestroyWindow(self.window)
        sdl.Quit()

    def pixels(self):
        """The current frame as ARGB ints (for tests and screenshots)."""
        buf = (ctypes.c_uint32 * (W * H))()
        sdl.RenderReadPixels(self.r, None, sdl.PIXELFORMAT_ARGB8888, buf, W * 4)
        return buf
