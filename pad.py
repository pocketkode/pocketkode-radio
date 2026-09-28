# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Buttons and sticks, read straight from the Linux input device.

Reading the device itself (instead of a game-controller mapping) gives the raw stick values
needed for drift measurement, and every button muOS knows about, including volume and menu.
The button codes and device paths come from muOS's own device description, so the same code
works on other muOS handhelds.
"""
import fcntl
import math
import os
import struct
import time

MUOS_DEVICE = os.environ.get("DC_MUOS_DEVICE", "/opt/muos/device/config")

EV_KEY, EV_ABS = 1, 3
_EVENT = struct.Struct("llHHi")  # struct input_event on 64-bit Linux
_ABSINFO = struct.Struct("6i")   # value, minimum, maximum, fuzz, flat, resolution

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


def _eviocgabs(code):
    return (2 << 30) | (_ABSINFO.size << 16) | (ord("E") << 8) | (0x40 + code)


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


class Stick:
    def __init__(self, name, xcode, ycode):
        self.name, self.xcode, self.ycode = name, xcode, ycode
        self.x = self.y = 0
        self.xrange = self.yrange = (-4096, 4096)
        self.reset_trace()

    def reset_trace(self):
        self.reach = [0.0] * 36  # furthest distance seen in each 10-degree sector

    def norm(self):
        """Position as (-1..1, -1..1), 0 = the centre of the reported range."""
        def n(v, rng):
            lo, hi = rng
            mid, half = (lo + hi) / 2, max(1, (hi - lo) / 2)
            return max(-1.2, min(1.2, (v - mid) / half))
        return n(self.x, self.xrange), n(self.y, self.yrange)

    def update_trace(self):
        nx, ny = self.norm()
        d = math.hypot(nx, ny)
        if d > 0.2:
            sector = int(((math.atan2(ny, nx) + math.pi) / (2 * math.pi)) * 36) % 36
            self.reach[sector] = max(self.reach[sector], min(d, 1.2))

    def roundness(self):
        """How far the stick reaches all the way round (0-100%), once it has been circled."""
        filled = [r for r in self.reach if r > 0]
        if len(filled) < 30:
            return None
        return 100.0 * sum(min(r, 1.0) for r in self.reach) / 36


class Pad:
    def __init__(self):
        self.codes = {}  # key code -> button name
        for name, key in BUTTONS:
            code = _cfg_int(f"input/code/button/{key}", DEFAULT_CODES.get(key, 0))
            if code:
                self.codes[code] = name
        self.dpad_x = _cfg_int("input/code/dpad/left", 16)
        self.dpad_y = _cfg_int("input/code/dpad/up", 17)
        self.sticks = [
            Stick("Left stick", _cfg_int("input/code/analog/left/left", 2), _cfg_int("input/code/analog/left/up", 3)),
            Stick("Right stick", _cfg_int("input/code/analog/right/left", 4), _cfg_int("input/code/analog/right/up", 5)),
        ]
        stick_count = _cfg_int("board/stick", 2)
        self.sticks = self.sticks[:max(0, min(2, stick_count))]
        axis = _cfg_int("input/axis", 4096)
        for s in self.sticks:
            s.xrange = s.yrange = (-axis, axis)
        # every button this device has, in a stable order (for "12 of 17 tested")
        self.names = list(DIRS) + list(dict.fromkeys(n for n, _ in BUTTONS if n in self.codes.values()))
        self.down = {}      # name -> time pressed
        self.seen = set()   # names pressed at least once (for the button test)
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
        self._read_ranges()

    def _read_ranges(self):
        for s in self.sticks:
            for axis in ("x", "y"):
                code = s.xcode if axis == "x" else s.ycode
                for fd in self.fds:
                    try:
                        buf = fcntl.ioctl(fd, _eviocgabs(code), bytes(_ABSINFO.size))
                    except OSError:
                        continue
                    value, lo, hi = _ABSINFO.unpack(buf)[:3]
                    if hi > lo:
                        setattr(s, axis, value)
                        setattr(s, axis + "range", (lo, hi))
                        break

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
        for s in self.sticks:
            s.update_trace()
        return out

    def inject(self, etype, code, value, out=None):
        """Handle one input event (also used by tests)."""
        out = out if out is not None else []
        if etype == EV_KEY and code in self.codes:
            if value == 2:
                return out  # the kernel's key repeat while held: not a new press (a held B would quit the app
                            # after "hold B to exit" closed a screen); arrows repeat on their own (REPEAT_EVERY)
            self._set(self.codes[code], value != 0, out)
        elif etype == EV_ABS:
            if code == self.dpad_x:
                self._set("LEFT", value < 0, out)
                self._set("RIGHT", value > 0, out)
            elif code == self.dpad_y:
                self._set("UP", value < 0, out)
                self._set("DOWN", value > 0, out)
            for s in self.sticks:
                if code == s.xcode:
                    s.x = value
                elif code == s.ycode:
                    s.y = value
        return out

    def _set(self, name, pressed, out):
        if pressed and name not in self.down:
            self.down[name] = time.monotonic()
            self.seen.add(name)
            out.append(name)
            if name in DIRS:
                self._repeat[name] = time.monotonic() + REPEAT_DELAY
        elif not pressed and name in self.down:
            del self.down[name]
            self._repeat.pop(name, None)

    def held_for(self, name):
        t = self.down.get(name)
        return time.monotonic() - t if t is not None else 0.0

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
