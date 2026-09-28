# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""In-app updates from the app's GitHub releases.

- check: reads update.json from the latest release (version, notes, size, sha256, signature, url). Nothing is
  sent but the request itself, and nothing is installed without the person choosing Update.
- download(): the package over HTTPS; its SHA-256 and PocketKode's Ed25519 signature are checked before anything
  is unpacked (the public key is below). A build of your own should use its own REPO and UPDATE_KEY, or turn
  updates off in Settings. Needs free space, and a charger or at least 20% battery. The new version is unpacked into .update/new and used the next time the app starts.
- main.py (before the app is loaded) finishes it. Files are swapped by renaming (never written over),
  so nothing that's in use is changed. config.ini, data/ and logs/ are kept. The previous version is kept once
  in .update/prev: if the new one doesn't start (confirm() isn't reached), the next start switches back.
"""
import hashlib
import json
import os
import shutil
import threading
import time
import urllib.error
import urllib.request
import zipfile

import ed25519
import net

REPO = "mahamudul87/pocketkode-radio"
LATEST = f"https://github.com/{REPO}/releases/latest/download/update.json"
# PocketKode's update signing key (public half): only packages signed with its private half are installed.
UPDATE_KEY = bytes.fromhex("fe76ade7218a09311dab9263a462555e1c7f58cd1d6003f79d2a87f77e49a2af")
KEEP = ("data", "logs", ".update", "config.ini")  # never replaced by an update
RESTART = 42          # exit code: mux_launch.sh starts the app again (to finish an update)
CHECK_EVERY = 24 * 3600
MIN_BATTERY = 20


def _vtuple(v):
    try:
        return tuple(int(x) for x in str(v).split("."))
    except ValueError:
        return (0,)


def newer(a, b):
    """Is version a newer than version b?"""
    return _vtuple(a) > _vtuple(b)


def _read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return ""


def power_ok():
    """A charger, or enough battery (unknown counts as fine)."""
    cfg = "/opt/muos/device/config"
    cap = _read(_read(os.path.join(cfg, "battery/capacity")) or "/sys/class/power_supply/axp2202-battery/capacity")
    chg = _read(_read(os.path.join(cfg, "battery/charger")) or "/sys/class/power_supply/axp2202-usb/online")
    if chg == "1" or not cap.isdigit():
        return True
    return int(cap) >= MIN_BATTERY


# ---------------------------------------------------------------------- at start
# Finishing a downloaded update (and switching back) is done by main.py itself, before any of the app's modules
# are loaded, so nothing old stays in memory. See APPLY in main.py.
def _rm(path):
    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except OSError:
        pass


def confirm(app_dir):
    """The app started fine after an update: keep it (called once the first screen is shown)."""
    _rm(os.path.join(app_dir, ".update", "applied.json"))


# ---------------------------------------------------------------------- in the app
class Updater:
    """States: None (nothing known), 'checking', 'available', 'downloading', 'ready' (restart to finish),
    'error' (see .error). .info = {version, notes, size, ...} of the latest version."""

    def __init__(self, app_dir, app_id, version):
        self.app_dir, self.app_id, self.version = app_dir, app_id, version
        self.up = os.path.join(app_dir, ".update")
        self.settings_path = os.path.join(app_dir, "data", "update.json")
        self.state, self.error, self.info = None, None, None
        self.progress = 0.0
        self._busy = False
        self._next = 0.0
        s = self._settings()
        self.enabled = s.get("check", True)  # on by default: only shows a notice
        self.just_updated = self._peek("applied.json")  # this start is the first one after an update
        self.rolled_back = self._pop_note("rolled_back.json")
        if os.path.exists(os.path.join(self.up, "ready.json")):
            self.state = "ready"

    def _peek(self, name):
        try:
            with open(os.path.join(self.up, name)) as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def _pop_note(self, name):
        p = os.path.join(self.up, name)
        try:
            with open(p) as f:
                d = json.load(f)
            os.remove(p)
            return d
        except (OSError, ValueError):
            return None

    def _settings(self):
        try:
            with open(self.settings_path) as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}

    def set_enabled(self, on):
        self.enabled = bool(on)
        os.makedirs(os.path.dirname(self.settings_path), exist_ok=True)
        with open(self.settings_path, "w") as f:
            json.dump({"check": self.enabled}, f)
        if on:
            self._next = 0.0

    def _spawn(self, fn):
        if self._busy:
            return
        self._busy = True

        def run():
            try:
                fn()
            finally:
                self._busy = False
        threading.Thread(target=run, daemon=True).start()

    def maybe_check(self, force=False):
        """Call every frame: checks at start and once a day (when online and switched on)."""
        if self._busy or self.state in ("downloading", "ready") or (not self.enabled and not force):
            return
        if not force and time.monotonic() < self._next:
            return
        self._next = time.monotonic() + (CHECK_EVERY if not force else 60)
        prev_state = self.state
        if force:
            self.state = "checking"

        def work():
            try:
                req = urllib.request.Request(LATEST, headers={"User-Agent": net.USER_AGENT})
                with urllib.request.urlopen(req, timeout=15) as r:
                    d = json.loads(r.read(65536))
                if not isinstance(d, dict):
                    raise ValueError("not an update description")
            except urllib.error.HTTPError as e:  # e.g. 404: no release yet
                self._next = time.monotonic() + 600
                self.state = "error" if force else prev_state
                self.error = f"GitHub answered with error {e.code}." if force else None
                return
            except (urllib.error.URLError, OSError, ValueError):
                self._next = time.monotonic() + 600  # offline: try again later
                self.state = "error" if force else prev_state
                self.error = "No internet connection. Turn on Wi-Fi in Configuration > Network." if force else None
                return
            if (d.get("version") and newer(d["version"], self.version) and d.get("signature") and d.get("sha256")
                    and str(d.get("url", "")).startswith("https://")):
                self.info, self.state, self.error = d, "available", None
            else:
                self.info, self.state = None, ("uptodate" if force else None)
        self._spawn(work)

    def download(self):
        if self.state != "available" or not self.info:
            return
        info = self.info
        if not power_ok():
            self.state, self.error = "error", f"Plug in the charger (or charge to {MIN_BATTERY}%) to update."
            return
        free = shutil.disk_usage(self.app_dir).free
        if free < 3 * int(info.get("size") or 0) + 16 * 2**20:
            self.state, self.error = "error", "Not enough free space on SD card 1 for the update."
            return
        self.state, self.error, self.progress = "downloading", None, 0.0

        def work():
            os.makedirs(self.up, exist_ok=True)
            part = os.path.join(self.up, "package.part")
            try:
                req = urllib.request.Request(info["url"], headers={"User-Agent": net.USER_AGENT})
                h = hashlib.sha256()
                total, got = int(info.get("size") or 0), 0
                with urllib.request.urlopen(req, timeout=30) as r, open(part, "wb") as out:
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        out.write(chunk)
                        h.update(chunk)
                        got += len(chunk)
                        self.progress = min(0.99, got / total) if total else 0.5
                digest = h.hexdigest()
                msg = f"pocketkode-update|{self.app_id}|{info['version']}|{digest}".encode()
                if digest != info.get("sha256") or not ed25519.verify(UPDATE_KEY, msg, bytes.fromhex(info["signature"])):
                    raise ValueError("The download couldn't be verified (damaged or not from PocketKode). Nothing was changed.")
                self._unpack(part, info)
                self.progress, self.state = 1.0, "ready"
            except (urllib.error.URLError, OSError) as e:
                self.state, self.error = "error", f"The download failed: {getattr(e, 'reason', e)}. Nothing was changed."
            except (ValueError, KeyError, zipfile.BadZipFile) as e:
                self.state, self.error = "error", str(e) or "The update couldn't be read. Nothing was changed."
            finally:
                _rm(part)
        self._spawn(work)

    def _unpack(self, part, info):
        new = os.path.join(self.up, "new")
        _rm(new)
        os.makedirs(new)
        top = os.path.basename(os.path.normpath(self.app_dir))
        with zipfile.ZipFile(part) as z:
            for m in z.infolist():
                name = m.filename.replace("\\", "/")
                parts = [p for p in name.split("/") if p]
                if not parts or parts[0] != top or len(parts) < 2 or ".." in parts or m.is_dir():
                    continue
                rel = "/".join(parts[1:])
                if parts[1] in KEEP:
                    continue
                dst = os.path.join(new, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                with z.open(m) as src, open(dst, "wb") as out:
                    shutil.copyfileobj(src, out)
                mode = (m.external_attr >> 16) & 0o777
                if mode:
                    os.chmod(dst, mode)
        if not os.listdir(new):
            raise ValueError("The update package is empty.")
        with open(os.path.join(self.up, "ready.json"), "w") as f:
            json.dump({"version": info["version"], "from": self.version}, f)

    def cancel_ready(self):
        """Keep the current version after all."""
        _rm(os.path.join(self.up, "new"))
        _rm(os.path.join(self.up, "ready.json"))
        self.state = "available" if self.info else None
