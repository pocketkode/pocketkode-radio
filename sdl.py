# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""The few SDL2 functions the app needs, called directly from the SDL2 library that ships with
muOS (nothing is bundled). Only video is used: buttons and sticks are read from the input
device itself (see pad.py)."""
import ctypes
import ctypes.util
import os

_CANDIDATES = [
    os.environ.get("PKR_SDL2_LIB", ""),
    "/usr/lib/libSDL2-2.0.so.0",
    "/usr/lib/libSDL2.so",
    "/usr/lib/aarch64-linux-gnu/libSDL2-2.0.so.0",
    ctypes.util.find_library("SDL2") or "",
]


def _load():
    for path in _CANDIDATES:
        if path:
            try:
                return ctypes.CDLL(path)
            except OSError:
                continue
    raise OSError("SDL2 library not found")


lib = _load()

INIT_VIDEO = 0x00000020
WINDOW_SHOWN = 0x00000004
WINDOW_FULLSCREEN_DESKTOP = 0x00001001
WINDOWPOS_UNDEFINED = 0x1FFF0000
RENDERER_SOFTWARE = 0x01
RENDERER_ACCELERATED = 0x02
BLENDMODE_BLEND = 1
PIXELFORMAT_ARGB8888 = 0x16362004
TEXTUREACCESS_STATIC = 0
QUIT = 0x100


class Rect(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int), ("w", ctypes.c_int), ("h", ctypes.c_int)]


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]


_p = ctypes.c_void_p
_u8 = ctypes.c_uint8
_i = ctypes.c_int
_RP = ctypes.POINTER(Rect)


def _fn(name, res, *args):
    f = getattr(lib, name)
    f.restype = res
    f.argtypes = list(args)
    return f


Init = _fn("SDL_Init", _i, ctypes.c_uint32)
Quit = _fn("SDL_Quit", None)
GetError = _fn("SDL_GetError", ctypes.c_char_p)
SetHint = _fn("SDL_SetHint", _i, ctypes.c_char_p, ctypes.c_char_p)
CreateWindow = _fn("SDL_CreateWindow", _p, ctypes.c_char_p, _i, _i, _i, _i, ctypes.c_uint32)
DestroyWindow = _fn("SDL_DestroyWindow", None, _p)
CreateRenderer = _fn("SDL_CreateRenderer", _p, _p, _i, ctypes.c_uint32)
DestroyRenderer = _fn("SDL_DestroyRenderer", None, _p)
RenderSetLogicalSize = _fn("SDL_RenderSetLogicalSize", _i, _p, _i, _i)
SetRenderDrawBlendMode = _fn("SDL_SetRenderDrawBlendMode", _i, _p, _i)
SetRenderDrawColor = _fn("SDL_SetRenderDrawColor", _i, _p, _u8, _u8, _u8, _u8)
RenderClear = _fn("SDL_RenderClear", _i, _p)
RenderFillRect = _fn("SDL_RenderFillRect", _i, _p, _RP)
RenderDrawLine = _fn("SDL_RenderDrawLine", _i, _p, _i, _i, _i, _i)
RenderDrawPoints = _fn("SDL_RenderDrawPoints", _i, _p, ctypes.POINTER(Point), _i)
RenderPresent = _fn("SDL_RenderPresent", None, _p)
RenderCopy = _fn("SDL_RenderCopy", _i, _p, _p, _RP, _RP)
RenderReadPixels = _fn("SDL_RenderReadPixels", _i, _p, _RP, ctypes.c_uint32, _p, _i)
CreateTexture = _fn("SDL_CreateTexture", _p, _p, ctypes.c_uint32, _i, _i, _i)
UpdateTexture = _fn("SDL_UpdateTexture", _i, _p, _RP, _p, _i)
DestroyTexture = _fn("SDL_DestroyTexture", None, _p)
SetTextureBlendMode = _fn("SDL_SetTextureBlendMode", _i, _p, _i)
SetTextureColorMod = _fn("SDL_SetTextureColorMod", _i, _p, _u8, _u8, _u8)
ShowCursor = _fn("SDL_ShowCursor", _i, _i)
PollEvent = _fn("SDL_PollEvent", _i, _p)
Delay = _fn("SDL_Delay", None, ctypes.c_uint32)
