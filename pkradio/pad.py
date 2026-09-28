# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Buttons and the d-pad, read straight from the Linux input device.

Reading the device itself (instead of a game-controller mapping) gives every button muOS knows
about, including menu. The button codes and device paths come from muOS's own device
description, so the same code works on other muOS handhelds.
"""
import os
import struct
import time

MUOS_DEVICE = os.environ.get("PKR_MUOS_DEVICE", "/opt/muos/device/config")

EV_KEY, EV_ABS = 1, 3
_EVENT = struct.Struct("llHHi")  # struct input_event on 64-bit Linux

# Button name -> muOS config key (input/code/button/<key>)
BUTTONS = [
    ("A", "a"), ("B", "b"), ("X", "x"), ("Y", "y"),
    ("L1", "l1"), ("L2", "l2"), ("R1", "r1"), ("R2", "r2"),
    ("L3", "l3"), ("R3", "r3"), ("SELECT", "select"), ("START", "start"),
    ("MENU", "menu_short"), ("MENU", "menu_long"),
    ("VOL+", "vol_up"), ("VOL-", "vol_down"),
]
DEFAULT_CODES = {"a": 304, "b": 305, "x": 307, "y": 306, "l1": 308, "l2": 314, "r1": 309, "r2": 315,
                 "l3": 313, "r3": 316, "select": 310, "start": 311, "menu_short": 354,
                 "menu_long": 312, "vol_up": 115, "vol_down": 114}
DIRS = ("UP", "DOWN", "LEFT", "RIGHT")
REPEAT_DELAY, REPEAT_EVERY = 0.35, 0.09


def _cfg(path, default=None):
    try:
        with open(os.path.join(MUOS_DEVICE, path)) as f:
            return f.read().strip()
    except OSError:
        return default


def _cfg_int(path, default):
    try:
        return int(_cfg(path, default))
    except (TypeError, ValueError):
        return default


class Pad:
    def __init__(self):
        self.codes = {}  # key code -> button name
        for name, key in BUTTONS:
            code = _cfg_int(f"input/code/button/{key}", DEFAULT_CODES.get(key, 0))
            if code:
                self.codes[code] = name
        self.dpad_x = _cfg_int("input/code/dpad/left", 16)
        self.dpad_y = _cfg_int("input/code/dpad/up", 17)
        self.down = {}      # name -> time pressed
        self._repeat = {}   # direction -> next repeat time
        self.fds = []
        paths = []
        for key in ("input/general", "input/volume", "input/extra"):
            p = _cfg(key)
            if p and p not in paths:
                paths.append(p)
        for p in paths or ["/dev/input/event1"]:
            try:
                fd = os.open(p, os.O_RDONLY | os.O_NONBLOCK)
                self.fds.append(fd)
            except OSError as e:
                print(f"[pad] can't open {p}: {e}")

    # ------------------------------------------------------------------ events
    def poll(self):
        """Read everything waiting. Returns menu actions: A, B, X, Y, START, SELECT, UP, DOWN…"""
        out = []
        for fd in self.fds:
            while True:
                try:
                    data = os.read(fd, _EVENT.size * 64)
                except BlockingIOError:
                    break
                except OSError:
                    break
                if not data:
                    break
                for i in range(0, len(data) - _EVENT.size + 1, _EVENT.size):
                    _, _, etype, code, value = _EVENT.unpack_from(data, i)
                    self.inject(etype, code, value, out)
        now = time.monotonic()
        for d in DIRS:
            if d in self.down and now >= self._repeat.get(d, now + 1):
                out.append(d)
                self._repeat[d] = now + REPEAT_EVERY
        return out

    def inject(self, etype, code, value, out=None):
        """Handle one input event."""
        out = out if out is not None else []
        if etype == EV_KEY and code in self.codes:
            if value == 2:
                return out  # the kernel's key repeat while held: not a new press (a held B would go back
                            # several screens); arrows repeat on their own (REPEAT_EVERY)
            self._set(self.codes[code], value != 0, out)
        elif etype == EV_ABS:
            if code == self.dpad_x:
                self._set("LEFT", value < 0, out)
                self._set("RIGHT", value > 0, out)
            elif code == self.dpad_y:
                self._set("UP", value < 0, out)
                self._set("DOWN", value > 0, out)
        return out

    def _set(self, name, pressed, out):
        if pressed and name not in self.down:
            self.down[name] = time.monotonic()
            out.append(name)
            if name in DIRS:
                self._repeat[name] = time.monotonic() + REPEAT_DELAY
        elif not pressed and name in self.down:
            del self.down[name]
            self._repeat.pop(name, None)

    def clear(self):
        self.down.clear()
        self._repeat.clear()

    def close(self):
        for fd in self.fds:
            try:
                os.close(fd)
            except OSError:
                pass
        self.fds = []
