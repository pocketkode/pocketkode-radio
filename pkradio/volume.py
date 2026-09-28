# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""The handheld's own volume, which muOS sets with the VOL+ / VOL- buttons. Read (never changed) with PipeWire's
wpctl, in the background, so Now playing can say when the sound is off."""
import re
import shutil
import subprocess
import threading
import time


class HandheldVolume:
    def __init__(self):
        self.wpctl = shutil.which("wpctl")
        self.level = None   # 0-100, or None when it can't be read
        self.muted = False
        self._next = 0.0
        self._busy = False

    @property
    def off(self):
        return self.level is not None and (self.muted or self.level == 0)

    def poll(self, every=1.0):
        """Call often: reads the volume at most once per `every` seconds."""
        if not self.wpctl or self._busy or time.monotonic() < self._next:
            return
        self._next, self._busy = time.monotonic() + every, True
        threading.Thread(target=self._read, daemon=True).start()

    def _read(self):
        try:
            out = subprocess.run([self.wpctl, "get-volume", "@DEFAULT_AUDIO_SINK@"], capture_output=True,
                                 text=True, timeout=3).stdout  # e.g. "Volume: 0.40 [MUTED]"
            m = re.search(r"Volume:\s*([\d.]+)", out)
            self.level = round(float(m.group(1)) * 100) if m else None
            self.muted = "MUTED" in out
        except (OSError, subprocess.SubprocessError, ValueError):
            self.level = None
        finally:
            self._busy = False
