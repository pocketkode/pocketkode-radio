# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio - internet radio and podcasts for muOS handhelds. Entry point."""
import json
import os
import shutil
import sys
import traceback

APP_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------------- finishing an update
# An update downloaded in the app (checked: SHA-256 and PocketKode's signature) waits in .update/new. It's
# swapped in here, before any of the app's modules are loaded: files are renamed, never written over, and the
# previous version is kept in .update/prev. If the updated app doesn't come up (it confirms once its first
# screen is shown), the next start switches back. config.ini, data/ and logs/ are never touched.
def _rm(path):
    try:
        if os.path.isdir(path) and not os.path.islink(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
    except OSError:
        pass


def apply_update(app_dir):
    up = os.path.join(app_dir, ".update")
    applied, ready = os.path.join(up, "applied.json"), os.path.join(up, "ready.json")
    try:
        if os.path.exists(applied):  # the updated version didn't confirm: back to the previous one
            info = json.load(open(applied))
            for rel in info.get("added", []):
                _rm(os.path.join(app_dir, rel))
            for rel in info.get("replaced", []):
                src = os.path.join(up, "prev", rel)
                if os.path.exists(src):
                    os.replace(src, os.path.join(app_dir, rel))
            os.remove(applied)
            with open(os.path.join(up, "rolled_back.json"), "w") as fh:
                json.dump({"version": info.get("version"), "back_to": info.get("from")}, fh)
            print("[update]", info.get("version"), "didn't start: back to", info.get("from"), flush=True)
        elif os.path.exists(ready):
            info = json.load(open(ready))
            new, prev = os.path.join(up, "new"), os.path.join(up, "prev")
            _rm(prev)
            added, replaced = [], []
            for root, dirs, files in os.walk(new):
                rel_dir = os.path.relpath(root, new)
                for d in dirs:
                    os.makedirs(os.path.join(app_dir, rel_dir, d), exist_ok=True)
                for f in files:
                    rel = os.path.normpath(os.path.join(rel_dir, f))
                    dst = os.path.join(app_dir, rel)
                    if os.path.exists(dst):
                        os.makedirs(os.path.dirname(os.path.join(prev, rel)), exist_ok=True)
                        os.replace(dst, os.path.join(prev, rel))
                        replaced.append(rel)
                    else:
                        added.append(rel)
                    os.replace(os.path.join(root, f), dst)
            with open(applied, "w") as fh:
                json.dump({"version": info.get("version"), "from": info.get("from"), "added": added, "replaced": replaced}, fh)
            os.remove(ready)
            _rm(new)
            print("[update] installed", info.get("version"), "(was", info.get("from"), ")", flush=True)
    except Exception as e:  # noqa: BLE001 - never stop the app from starting
        print("[update] couldn't finish:", e, flush=True)


def drop_compiled(app_dir):
    """Versions before 1.3.0 were compiled (app.so, lang.so…). Python loads a .so before a .py of the same name, so
    after installing this version over one of them the old files must go. Right after an in-app update they're kept
    in .update/prev with the other replaced files, so switching back to the previous version still works."""
    if not os.path.exists(os.path.join(app_dir, "pkradio", "app.py")):  # switched back to a compiled version: keep it
        return
    old = [f for f in os.listdir(app_dir) if f.endswith(".so")]
    if not old:
        return
    up = os.path.join(app_dir, ".update")
    applied = os.path.join(up, "applied.json")
    info = None
    try:
        with open(applied) as fh:
            info = json.load(fh)
    except (OSError, ValueError):
        pass
    for f in old:
        try:
            if info is not None:
                os.makedirs(os.path.join(up, "prev"), exist_ok=True)
                os.replace(os.path.join(app_dir, f), os.path.join(up, "prev", f))
                info.setdefault("replaced", []).append(f)
            else:
                os.remove(os.path.join(app_dir, f))
        except OSError as e:
            print("[update] couldn't remove", f, e, flush=True)
    if info is not None:
        with open(applied, "w") as fh:
            json.dump(info, fh)
    print("[update] removed the compiled files of the previous version:", len(old), flush=True)


apply_update(APP_DIR)  # before any of the app's modules are loaded
drop_compiled(APP_DIR)
sys.path.insert(0, APP_DIR)

if os.path.exists(os.path.join(APP_DIR, "pkradio", "app.py")):
    from pkradio.app import App  # noqa: E402
else:  # just switched back to a version before 1.3.0 (compiled, in the app folder itself)
    from app import App  # noqa: E402


def main():
    try:
        app = App(APP_DIR)
        app.run()
        if getattr(app, "restart", False):
            return 42  # mux_launch.sh starts the app again (to finish an update)
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
