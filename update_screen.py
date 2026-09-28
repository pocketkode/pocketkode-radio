# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""The update screen: what's new, download, restart to finish."""
import time

from gfx import C, W
from lang import _, tr


class UpdateScreen:
    """A new version from GitHub: what's new, then download (checked: SHA-256 and PocketKode's signature)
    and restart to finish. Nothing is installed unless the person chooses Update."""

    def __init__(self, app, updater, app_name):
        self.app, self.up, self.app_name = app, updater, app_name
        if updater.state is None and not updater.info:
            updater.maybe_check(force=True)  # opened from "Check for updates"

    def handle(self, action):
        st = self.up.state
        if action == "A" and st == "available":
            self.up.download()
        elif action == "A" and st == "ready":
            self.app.restart = True  # mux_launch.sh starts the app again; main.py finishes the update first
            self.app.running = False
        elif action == "A" and st == "error":
            if self.up.info:
                self.up.state = "available"
                self.up.download()
            else:
                self.up.maybe_check(force=True)
        elif action == "B":
            self.app.pop()

    def update(self):
        pass

    def draw(self, s):
        u = self.up
        s.title_bar(_("Update"), f"{self.app_name} {u.version}")
        info = u.info or {}
        new = info.get("version", "")
        if u.state == "checking":
            s.text(24, 90, _("Checking for updates") + "." * (1 + int(time.monotonic() * 2) % 3), 2, C["accent_hi"])
            s.footer([("B", _("Back"))])
            return
        if u.state == "uptodate" or (u.state is None and not info):
            s.text(24, 90, _("You have the latest version."), 3, C["ok"])
            s.footer([("B", _("Back"))])
            return
        if u.state == "ready":
            s.text(24, 84, _("✓ Version {v} is ready", v=new), 3, C["ok"])
            s.para(24, 130, _("Downloaded and checked. Restart the app to finish; your settings and data stay. "
                              "If you choose Later, it's installed the next time you open the app."), W - 48, 2, C["dim"])
            s.footer([("A", _("Restart now")), ("B", _("Later"))])
            return
        if u.state == "error" and not info:  # the check itself failed: there is no new version to show
            s.para(24, 90, tr(u.error) or _("Something went wrong."), W - 48, 2, C["warn"])
            s.footer([("A", _("Try again")), ("B", _("Back"))])
            return
        s.text(24, 76, _("Version {v} is available", v=new), 3)
        s.text(24, 116, _("You have {v}", v=u.version) + (f" · {info['size'] / 2**20:.1f} MB" if info.get("size") else ""), 2, C["dim"])
        y = 150
        s.text(24, y, _("What's new:"), 2, C["text"])
        y += 28
        for note in (info.get("notes") or [])[:5]:
            y = s.para(40, y, "· " + str(note), W - 64, 2, C["dim"]) + 2
            if y > 330:
                break
        if u.state == "downloading":
            s.text(24, 360, _("Downloading {n}%", n=int(u.progress * 100)), 2, C["accent_hi"])
            s.bar(24, 390, W - 48, 10, u.progress)
            s.footer([("B", _("Back (keeps downloading)"))])
        elif u.state == "error":
            s.para(24, 350, tr(u.error) or _("Something went wrong."), W - 48, 2, C["warn"])
            s.footer([("A", _("Try again")), ("B", _("Back"))])
        else:
            s.para(24, 350, _("Your settings and data are kept. Needs Wi-Fi."), W - 48, 2, C["faint"])
            s.footer([("A", _("Update")), ("B", _("Later"))])
