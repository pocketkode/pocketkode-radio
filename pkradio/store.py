# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Everything the app remembers: favourite and recent stations, subscriptions, where each
episode was stopped, downloads, settings. Saved as data/state.json."""
import json
import os
import threading
import time

from . import net

RECENT_MAX = 15


class Store:
    def __init__(self, app_dir):
        self.dir = os.path.join(app_dir, "data")
        self.dl_dir = os.path.join(self.dir, "podcasts")
        os.makedirs(self.dl_dir, exist_ok=True)
        self.path = os.path.join(self.dir, "state.json")
        self.d = {"favourites": [], "recent": [], "subs": {}, "eps": {},
                  "settings": {"country": "", "podcast_country": "us"}}
        try:
            with open(self.path) as f:
                saved = json.load(f)
            for k in self.d:
                if isinstance(saved.get(k), type(self.d[k])):
                    self.d[k] = saved[k] if k != "settings" else {**self.d[k], **saved[k]}
        except (OSError, ValueError):
            pass
        self.d["settings"].pop("volume", None)  # before 1.3.0 the app had its own volume; now it's the handheld's
        self.dirty = False
        self._last_save = 0.0
        for key, e in list(self.d["eps"].items()):  # forget downloads whose file is gone
            if e.get("file") and not os.path.exists(e["file"]):
                e["file"] = None

    # ------------------------------------------------------------------ saving
    def changed(self):
        self.dirty = True

    def save(self, force=False):
        if not self.dirty or (not force and time.monotonic() - self._last_save < 5):
            return
        tmp = self.path + ".tmp"
        try:
            with open(tmp, "w") as f:
                json.dump(self.d, f)
            os.replace(tmp, self.path)
            self.dirty = False
            self._last_save = time.monotonic()
        except OSError as e:
            print("[store] save failed:", e)

    @property
    def settings(self):
        return self.d["settings"]

    # ------------------------------------------------------------------ stations
    def is_fav(self, st):
        return any(s["id"] == st["id"] for s in self.d["favourites"])

    def toggle_fav(self, st):
        favs = self.d["favourites"]
        if self.is_fav(st):
            favs[:] = [s for s in favs if s["id"] != st["id"]]
        else:
            favs.append(st)
        self.changed()
        return self.is_fav(st)

    def played_station(self, st):
        rec = [s for s in self.d["recent"] if s["id"] != st["id"]]
        self.d["recent"] = [st] + rec[:RECENT_MAX - 1]
        self.changed()

    # ------------------------------------------------------------------ podcasts
    def is_sub(self, feed):
        return feed in self.d["subs"]

    def toggle_sub(self, show):
        if show["feed"] in self.d["subs"]:
            del self.d["subs"][show["feed"]]
        else:
            self.d["subs"][show["feed"]] = {k: show.get(k, "") for k in ("feed", "title", "author")}
        self.changed()
        return self.is_sub(show["feed"])

    def ep(self, ep, show=None):
        """The saved state of an episode (created on first use)."""
        e = self.d["eps"].get(ep["key"])
        if e is None:
            e = self.d["eps"][ep["key"]] = {"pos": 0, "dur": ep.get("duration", 0), "played": False, "file": None}
        e.update(title=ep.get("title", e.get("title", "")), url=ep.get("url", e.get("url")), date=ep.get("date", e.get("date", 0)))
        if show:
            e.update(show=show.get("title", ""), feed=show.get("feed", ""))
        return e

    def peek(self, key):
        return self.d["eps"].get(key)

    def downloads(self):
        return sorted(((k, e) for k, e in self.d["eps"].items() if e.get("file")),
                      key=lambda kv: kv[1].get("date", 0), reverse=True)


class Downloads(threading.Thread):
    """Downloads episodes one after another in the background."""

    def __init__(self, store):
        super().__init__(daemon=True)
        self.store = store
        self.queue = []
        self.current = None  # key being downloaded
        self.progress = {}   # key -> (done, total)
        self.errors = {}     # key -> message
        self._cancel = set()
        self._wake = threading.Event()
        self.running = True

    def add(self, ep, show):
        e = self.store.ep(ep, show)
        if e.get("file") or ep["key"] in self.queue or ep["key"] == self.current:
            return
        self.errors.pop(ep["key"], None)
        e["dl_url"] = ep["url"]
        e["dl_ext"] = _ext(ep)
        self.queue.append(ep["key"])
        self._wake.set()

    def cancel(self, key):
        if key in self.queue:
            self.queue.remove(key)
        if key == self.current:
            self._cancel.add(key)

    def state(self, key):
        """'done', 'queued', 'loading', 'error' or None."""
        e = self.store.peek(key)
        if e and e.get("file"):
            return "done"
        if key == self.current:
            return "loading"
        if key in self.queue:
            return "queued"
        if key in self.errors:
            return "error"
        return None

    def delete(self, key):
        self.cancel(key)
        e = self.store.peek(key)
        if e and e.get("file"):
            try:
                os.remove(e["file"])
            except OSError:
                pass
            e["file"] = None
            self.store.changed()

    def run(self):
        while self.running:
            if not self.queue:
                self._wake.wait(1.0)
                self._wake.clear()
                continue
            key = self.current = self.queue.pop(0)
            e = self.store.peek(key)
            path = os.path.join(self.store.dl_dir, key + e.get("dl_ext", ".mp3"))
            try:
                ok = net.download(e["dl_url"], path, lambda d, t: self.progress.__setitem__(key, (d, t)),
                                  lambda: key in self._cancel or not self.running)
                if ok:
                    e["file"] = path
                    self.store.changed()
            except (net.NetError, OSError) as ex:
                self.errors[key] = str(ex)
            finally:
                self._cancel.discard(key)
                self.progress.pop(key, None)
                self.current = None

    def stop(self):
        self.running = False
        self._wake.set()


def _ext(ep):
    url = (ep.get("url") or "").split("?")[0].lower()
    for ext in (".mp3", ".m4a", ".aac", ".ogg", ".opus", ".mp4", ".wav"):
        if url.endswith(ext):
            return ext
    t = ep.get("type") or ""
    return {"audio/mpeg": ".mp3", "audio/mp4": ".m4a", "audio/x-m4a": ".m4a", "audio/ogg": ".ogg"}.get(t, ".mp3")
