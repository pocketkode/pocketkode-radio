# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Stops muOS from dimming the screen / going to sleep while audio is playing.

muOS uses two mechanisms (see /opt/muos/script/mux/idle.sh and hotkey.sh):
  * /run/muos/caffeine exists      -> the idle *sleep* (suspend) is skipped
  * /run/muos/input_activity changes -> idle watcher sets idle_inhibit, so the
                                       screen is not dimmed (dimming can also mute
                                       audio and lower the CPU speed)
Both are only touched while playback is active, and caffeine is removed again
afterwards unless the user had already switched it on themselves.
"""
import os
import time

RUN_DIR = "/run/muos"
CAFFEINE = os.path.join(RUN_DIR, "caffeine")
ACTIVITY = os.path.join(RUN_DIR, "input_activity")
MARKER = "/tmp/pkradio-caffeine"  # lets mux_launch.sh clean up if the app crashes
PULSE_EVERY = 3.0


class KeepAwake:
    def __init__(self, enabled=True):
        self.enabled = enabled and os.path.isdir(RUN_DIR)
        self.active = False
        self._made_caffeine = False
        self._last_pulse = 0.0

    def start(self):
        if not self.enabled or self.active:
            return
        self.active = True
        if not os.path.exists(CAFFEINE):
            try:
                open(CAFFEINE, "w").close()
                open(MARKER, "w").close()
                self._made_caffeine = True
            except OSError as e:
                print("[keepawake] could not set caffeine:", e)
        self.pulse(force=True)

    def stop(self):
        if not self.active:
            return
        self.active = False
        if self._made_caffeine:
            for p in (CAFFEINE, MARKER):
                try:
                    os.remove(p)
                except OSError:
                    pass
            self._made_caffeine = False

    def pulse(self, force=False):
        """Call often; every few seconds it tells muOS the device is in use."""
        if not self.active:
            return
        now = time.monotonic()
        if force or now - self._last_pulse >= PULSE_EVERY:
            self._last_pulse = now
            try:
                with open(ACTIVITY, "w") as f:
                    f.write(f"{int(time.time() * 10)}\n")
            except OSError:
                pass
