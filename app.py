# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""PocketKode Radio screens: radio, podcasts, now playing, keyboard, settings."""
import ctypes
import os
import subprocess
import threading
import time

import lang
import net
import podcasts
import sdl
import updater
from gfx import C, H, W, Screen
from keepawake import KeepAwake
from lang import _, tr
from pad import Pad
from player import Player
from radio import Radio
from store import Downloads, Store
from update_screen import UpdateScreen

APP_VERSION = "1.3.0"
ROW_H = 58
LIST_TOP = 60
FOOT = 40
MINI = 30  # mini player bar height
BRIGHT = "/opt/muos/script/device/bright.sh"
SCREEN_MARK = "/tmp/pkradio-screenoff"
SPEEDS = [0.75, 1.0, 1.25, 1.5, 1.75, 2.0]
SLEEP_STEPS = [0, 15, 30, 45, 60, 90]
PODCAST_REGIONS = [("us", "United States"), ("gb", "United Kingdom"), ("ca", "Canada"), ("au", "Australia"),
                   ("in", "India"), ("jp", "Japan"), ("de", "Germany"), ("fr", "France"), ("es", "Spain"),
                   ("br", "Brazil"), ("mx", "Mexico"), ("it", "Italy"), ("nl", "Netherlands"), ("se", "Sweden")]


def fmt_time(sec):
    sec = int(max(0, sec or 0))
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def fmt_date(ts):
    return lang.date(ts) if ts else ""


def stations(n):
    return _("1 station") if n == 1 else _("{n} stations", n=n)


def episodes(n):
    return _("1 episode") if n == 1 else _("{n} episodes", n=n)


def fmt_mb(n):
    return f"{n / (1 << 20):.0f} MB" if n < (1 << 30) else f"{n / (1 << 30):.1f} GB"


# ---------------------------------------------------------------------- base views
class View:
    TITLE = ""

    def __init__(self, app):
        self.app = app

    def handle(self, action):
        if action == "B":
            self.app.pop()

    def update(self):
        pass

    def right(self):
        return ""

    def hints(self):
        return [("B", _("Back"))]

    def draw(self, s):
        pass


class Menu(View):
    """A scrolling list. rows() -> [(key, title, subtitle, colour or None, right text)]"""

    def __init__(self, app):
        super().__init__(app)
        self.sel = 0
        self.top = 0
        self.flash = ""
        self.flash_until = 0.0

    def rows(self):
        return []

    def say(self, msg, secs=2.5):
        self.flash, self.flash_until = msg, time.monotonic() + secs

    def handle(self, action):
        rows = self.rows()
        n = len(rows)
        if action in ("UP", "DOWN") and n:
            self.sel = (self.sel + (1 if action == "DOWN" else -1)) % n
        elif action in ("L1", "R1") and n:
            self.sel = max(0, min(n - 1, self.sel + (-5 if action == "L1" else 5)))
        elif action == "B":
            self.app.pop()
        elif n and 0 <= self.sel < n:
            self.act(action, rows[self.sel][0])

    def act(self, action, key):
        if action == "A":
            self.choose(key)

    def choose(self, key):
        pass

    def empty_text(self):
        return _("Nothing here yet.")

    def draw(self, s):
        s.title_bar(s.fit(self.TITLE, 400, 3), self.right())
        rows = self.rows()
        bottom = H - FOOT - (MINI if self.app.player.item and not isinstance(self, NowPlaying) else 0)
        if not rows:
            s.para(24, LIST_TOP + 20, self.empty_text(), W - 48, 2, C["dim"])
        self.sel = min(self.sel, max(0, len(rows) - 1))
        visible = max(1, (bottom - LIST_TOP) // ROW_H)
        if self.sel < self.top:
            self.top = self.sel
        elif self.sel >= self.top + visible:
            self.top = self.sel - visible + 1
        for i, (key, title, sub, colour, right) in enumerate(rows[self.top:self.top + visible]):
            y = LIST_TOP + i * ROW_H
            if self.top + i == self.sel:
                s.box(8, y + 2, W - 16, ROW_H - 4, C["sel"])
                s.box(8, y + 2, 5, ROW_H - 4, C["accent"])
            rw = s.text_w(right, 2) + 12 if right else 0
            s.text(26, y + 9, s.fit(title, W - 52 - rw), 2)
            if right:
                s.text(W - 22, y + 9, right, 2, C["accent_hi"], align="right")
            if sub:
                s.text(26, y + 33, s.fit(sub, W - 52), 2, colour or C["dim"])
        if len(rows) > visible:
            track = bottom - LIST_TOP
            h = max(20, track * visible // len(rows))
            s.box(W - 5, LIST_TOP + (track - h) * self.top // max(1, len(rows) - visible), 3, h, C["faint"])
        if self.flash and time.monotonic() < self.flash_until:
            s.box(40, bottom - 44, W - 80, 36, C["bar"])
            s.frame(40, bottom - 44, W - 80, 36, C["accent"])
            s.text(W // 2, bottom - 35, s.fit(self.flash, W - 100), 2, align="center")
        s.footer(self.hints())


class Loading(View):
    """Runs fn() in the background, then shows make_view(result)."""

    def __init__(self, app, title, fn, make_view):
        super().__init__(app)
        self.TITLE, self.fn, self.make_view = title, fn, make_view
        self.result = self.error = None
        self.done = False
        self.t0 = time.monotonic()
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        try:
            self.result = self.fn()
        except net.NetError as e:
            self.error = str(e)
        except Exception as e:  # noqa: BLE001 - shown on screen
            self.error = _("Something went wrong: {e}", e=e)
        self.done = True

    def update(self):
        if self.done and not self.error:
            self.app.replace(self.make_view(self.result))

    def handle(self, action):
        if action == "B":
            self.app.pop()
        elif action == "A" and self.error:
            self.app.replace(Loading(self.app, self.TITLE, self.fn, self.make_view))

    def draw(self, s):
        s.title_bar(s.fit(self.TITLE, 560, 3))
        if self.error:
            s.para(24, 90, tr(self.error), W - 48, 2, C["warn"])
            s.footer([("A", _("Try again")), ("B", _("Back"))])
        else:
            dots = "." * (1 + int((time.monotonic() - self.t0) * 3) % 3)
            s.text(W // 2, 200, _("Loading") + dots, 3, C["dim"], align="center")
            s.footer([("B", _("Back"))])


class Keyboard(View):
    ROWS = ["1234567890", "qwertyuiop", "asdfghjkl'", "zxcvbnm,.-"]
    SHIFT = ["!?&#()@:/+", "QWERTYUIOP", "ASDFGHJKL\"", "ZXCVBNM;_="]

    def __init__(self, app, title, on_done, text=""):
        super().__init__(app)
        self.TITLE, self.on_done, self.text = title, on_done, text
        self.r = self.c = 0
        self.shift = False

    def handle(self, action):
        grid = self.SHIFT if self.shift else self.ROWS
        if action == "UP":
            self.r = (self.r - 1) % 4
        elif action == "DOWN":
            self.r = (self.r + 1) % 4
        elif action == "LEFT":
            self.c = (self.c - 1) % 10
        elif action == "RIGHT":
            self.c = (self.c + 1) % 10
        elif action == "A" and len(self.text) < 60:
            self.text += grid[self.r][self.c]
        elif action == "B":
            self.text = self.text[:-1]
        elif action == "Y":
            self.text += " "
        elif action == "X":
            self.shift = not self.shift
        elif action == "L1":
            self.text = ""
        elif action == "SELECT":
            self.app.pop()
        elif action == "START" and self.text.strip():
            self.app.pop()
            self.on_done(self.text.strip())

    def draw(self, s):
        s.title_bar(self.TITLE)
        s.box(24, 70, W - 48, 44, C["row"])
        s.text(36, 83, s.fit(self.text, W - 90) + ("_" if int(time.monotonic() * 2) % 2 else " "), 2)
        grid = self.SHIFT if self.shift else self.ROWS
        kw, kh, gap = 54, 50, 6
        x0 = (W - (10 * kw + 9 * gap)) // 2
        for r, row in enumerate(grid):
            for c, ch in enumerate(row):
                x, y = x0 + c * (kw + gap), 134 + r * (kh + gap)
                s.box(x, y, kw, kh, C["accent"] if (r, c) == (self.r, self.c) else C["key"])
                s.text(x + kw // 2, y + 16, ch, 2, align="center")
        s.footer([("A", _("Type")), ("B", _("Del")), ("Y", _("Space")), ("X", "Abc"), ("START", _("Go")), ("SELECT", _("Esc"))])


# ---------------------------------------------------------------------- home
class Home(Menu):
    TITLE = "PocketKode Radio"

    def rows(self):
        out = []
        p = self.app.player
        if p.item:
            out.append(("now", _("Now playing"), p.item.get("title", ""), C["accent_hi"], "▶" if p.active else ""))
            out.append(("screenoff", _("Turn off the screen"), _("Keeps playing · press MENU to turn it back on"), None, ""))
        subs = len(self.app.store.d["subs"])
        u = self.app.updater
        if u.state in ("available", "downloading", "ready") and u.info:
            sub = {"available": _("What's new · A to update"), "downloading": _("Downloading {n}%", n=int(u.progress * 100)),
                   "ready": _("Downloaded · restart to finish")}[u.state]
            out.insert(0, ("update", _("Update available: {v}", v=u.info['version']), sub, C["accent_hi"], ""))
        out += [("radio", _("Radio"), _("Stations from around the world"), None, ""),
                ("pod", _("Podcasts"), _("{n} subscribed", n=subs) if subs else _("Search, subscribe, download"), None, ""),
                ("settings", _("Settings"), _("Your country, podcast region, downloads, language"), None, ""),
                ("about", _("About"), _("Version {v}", v=APP_VERSION), None, "")]
        return out

    def hints(self):
        return [("A", _("Open")), ("B", _("Quit"))]

    def right(self):
        return f"v{APP_VERSION}"

    def handle(self, action):
        if action == "B":
            self.app.running = False
        else:
            super().handle(action)

    def choose(self, key):
        a = self.app
        if key == "screenoff":
            a.set_screen(False)
            return
        if key == "update":
            a.push(UpdateScreen(a, a.updater, "PocketKode Radio"))
            return
        {"now": lambda: a.push(NowPlaying(a)), "radio": lambda: a.push(RadioHome(a)),
         "pod": lambda: a.push(PodcastHome(a)), "settings": lambda: a.push(Settings(a)),
         "about": lambda: a.push(About(a))}[key]()


# ---------------------------------------------------------------------- radio
class RadioHome(Menu):
    TITLE = "Radio"

    def draw(self, s):
        self.TITLE = _("Radio")
        super().draw(s)

    def rows(self):
        st = self.app.store
        cc = st.settings.get("country")
        out = [("fav", _("Favourites"), stations(len(st.d["favourites"])), None, "★"),
               ("recent", _("Recently played"), stations(len(st.d["recent"])), None, ""),
               ("top", _("Top stations"), _("Most played worldwide"), None, "")]
        if cc:
            out.append(("mine", _("Stations in {country}", country=st.settings.get('country_name', cc)), _("Most played first"),
                        None, ""))
        out += [("countries", _("By country"), _("Choose a country"), None, ""),
                ("genres", _("By genre"), _("Pop, rock, news, jazz, talk…"), None, ""),
                ("search", _("Search"), _("Find a station by name"), None, "")]
        return out

    def choose(self, key):
        a, r, st = self.app, self.app.radio, self.app.store
        if key == "fav":
            a.push(Stations(a, _("Favourites"), static=st.d["favourites"], kind="fav"))
        elif key == "recent":
            a.push(Stations(a, _("Recently played"), static=st.d["recent"], kind="recent"))
        elif key == "top":
            a.push(Stations.loading(a, _("Top stations"), lambda off: r.top(off)))
        elif key == "mine":
            cc = st.settings["country"]
            a.push(Stations.loading(a, st.settings.get("country_name", cc), lambda off: r.search(countrycode=cc, offset=off)))
        elif key == "countries":
            a.push(Loading(a, _("Countries"), r.countries, lambda rows: Countries(a, rows)))
        elif key == "genres":
            a.push(Loading(a, _("Genres"), r.genres, lambda rows: Genres(a, rows)))
        elif key == "search":
            a.push(Keyboard(a, _("Search stations"),
                            lambda q: a.push(Stations.loading(a, f"“{q}”", lambda off: r.search(name=q, offset=off)))))


class Stations(Menu):
    def __init__(self, app, title, static=None, fetch=None, first=None, kind=""):
        super().__init__(app)
        self.TITLE, self.kind = title, kind
        self.static = static            # a list kept by the store (favourites / recent)
        self.fetch = fetch              # fetch(offset) -> more stations
        self.items = list(first or [])
        self.more = bool(fetch) and len(self.items) >= 40
        self.loading_more = False

    @classmethod
    def loading(cls, app, title, fetch):
        return Loading(app, title, lambda: fetch(0), lambda rows: cls(app, title, fetch=fetch, first=rows))

    def list(self):
        return self.static if self.static is not None else self.items

    def rows(self):
        st = self.app.store
        out = []
        for i, s in enumerate(self.list()):
            bits = [s.get("country") or s.get("cc")] + s.get("tags", [])[:2]
            if s.get("bitrate"):
                bits.append(f"{s['bitrate']} kbps")
            out.append((i, s["name"], " · ".join(b for b in bits if b), None, "★" if st.is_fav(s) else ""))
        return out

    def empty_text(self):
        return {"fav": _("No favourites yet. Press Y on a station to add it."),
                "recent": _("Stations you play appear here.")}.get(self.kind, _("No stations found."))

    def hints(self):
        return [("A", _("Play")), ("Y", _("Favourite")), ("B", _("Back"))]

    def update(self):
        if self.more and not self.loading_more and self.sel >= len(self.items) - 5:
            self.loading_more = True
            threading.Thread(target=self._more, daemon=True).start()

    def _more(self):
        try:
            got = self.fetch(len(self.items))
            known = {s["id"] for s in self.items}
            self.items += [s for s in got if s["id"] not in known]
            self.more = len(got) >= 40
        except net.NetError:
            self.more = False
        self.loading_more = False

    def act(self, action, i):
        items = self.list()
        if not 0 <= i < len(items):
            return
        s = items[i]
        if action == "A":
            self.app.play_station(s)
            self.app.push(NowPlaying(self.app))
        elif action == "Y":
            self.say(_("Added to favourites") if self.app.store.toggle_fav(s) else _("Removed from favourites"))


class Countries(Menu):
    def __init__(self, app, rows):
        super().__init__(app)
        self.items = rows
        self.TITLE = _("By country")

    def rows(self):
        mine = self.app.store.settings.get("country")
        return [(i, c["name"], stations(c["count"]), None, "★" if c["cc"] == mine else "")
                for i, c in enumerate(self.items)]

    def hints(self):
        return [("A", _("Open")), ("Y", _("My country")), ("B", _("Back"))]

    def act(self, action, i):
        c = self.items[i]
        a = self.app
        if action == "A":
            a.push(Stations.loading(a, c["name"], lambda off: a.radio.search(countrycode=c["cc"], offset=off)))
        elif action == "Y":
            a.store.settings.update(country=c["cc"], country_name=c["name"])
            a.store.changed()
            self.say(_("{country} set as your country", country=c['name']))


class Genres(Menu):
    def __init__(self, app, rows):
        super().__init__(app)
        self.items = rows
        self.TITLE = _("By genre")

    def rows(self):
        return [(i, g["tag"].title(), stations(g["count"]), None, "") for i, g in enumerate(self.items)]

    def choose(self, i):
        g = self.items[i]
        a = self.app
        a.push(Stations.loading(a, g["tag"].title(), lambda off: a.radio.search(tag=g["tag"], offset=off)))


# ---------------------------------------------------------------------- podcasts
class PodcastHome(Menu):
    def draw(self, s):
        self.TITLE = _("Podcasts")
        super().draw(s)

    def rows(self):
        st = self.app.store
        region = _(dict(PODCAST_REGIONS).get(st.settings.get("podcast_country", "us"), ""))
        n = len(st.downloads())
        return [("subs", _("My podcasts"), _("{n} subscribed", n=len(st.d['subs'])), None, ""),
                ("dl", _("Downloads"), _("1 episode on this handheld") if n == 1 else _("{n} episodes on this handheld", n=n),
                 None, ""),
                ("top", _("Top podcasts"), _("Charts: {region}", region=region), None, ""),
                ("search", _("Search"), _("Find a podcast by name or topic"), None, "")]

    def choose(self, key):
        a = self.app
        region = a.store.settings.get("podcast_country", "us")
        if key == "subs":
            a.push(Shows(a, _("My podcasts"), list(a.store.d["subs"].values()), mine=True))
        elif key == "dl":
            a.push(DownloadsView(a))
        elif key == "top":
            a.push(Loading(a, _("Top podcasts"), lambda: podcasts.top(region), lambda rows: Shows(a, _("Top podcasts"), rows)))
        elif key == "search":
            a.push(Keyboard(a, _("Search podcasts"), lambda q: a.push(
                Loading(a, f"“{q}”", lambda: podcasts.search(q, region.upper()), lambda rows: Shows(a, f"“{q}”", rows)))))


class Shows(Menu):
    def __init__(self, app, title, items, mine=False):
        super().__init__(app)
        self.TITLE, self.items, self.mine = title, items, mine

    def rows(self):
        st = self.app.store
        items = list(st.d["subs"].values()) if self.mine else self.items
        self.items = items
        return [(i, sh["title"], sh.get("author") or sh.get("genre") or "", None, "✓" if st.is_sub(sh["feed"]) else "")
                for i, sh in enumerate(items)]

    def empty_text(self):
        return (_("No subscriptions yet. Find a podcast in Search or Top podcasts and press Y to subscribe.")
                if self.mine else _("No podcasts found."))

    def hints(self):
        return [("A", _("Episodes")), ("Y", _("Subscribe")), ("B", _("Back"))]

    def act(self, action, i):
        sh = self.items[i]
        a = self.app
        if action == "A":
            a.push(Loading(a, sh["title"], lambda: podcasts.feed(sh["feed"]), lambda res: Episodes(a, *res)))
        elif action == "Y":
            self.say(_("Subscribed") if a.store.toggle_sub(sh) else _("Unsubscribed"))


class Episodes(Menu):
    def __init__(self, app, show, eps):
        super().__init__(app)
        self.show, self.eps = show, eps
        self.TITLE = show["title"]

    def right(self):
        return _("✓ subscribed") if self.app.store.is_sub(self.show["feed"]) else ""

    def rows(self):
        st, dl = self.app.store, self.app.downloads
        out = []
        for i, ep in enumerate(self.eps):
            e = st.peek(ep["key"]) or {}
            bits = [fmt_date(ep["date"])]
            if ep["duration"]:
                bits.append(_("{m} min", m=ep['duration'] // 60))
            state = dl.state(ep["key"])
            colour = None
            if e.get("played"):
                bits.append(_("✓ played"))
                colour = C["faint"]
            elif e.get("pos", 0) > 30:
                left = (e.get("dur") or ep["duration"] or 0) - e["pos"]
                bits.append(_("{t} left", t=fmt_time(left)) if left > 0 else _("started"))
                colour = C["accent_hi"]
            right = {"done": "↓", "queued": "…", "error": "!"}.get(state, "")
            if state == "loading":
                d, t = dl.progress.get(ep["key"], (0, 0))
                right = f"{100 * d // t}%" if t else fmt_mb(d)
            out.append((i, ep["title"], " · ".join(b for b in bits if b), colour, right))
        return out

    def hints(self):
        return [("A", _("Play")), ("X", _("Download")), ("Y", _("Played")), ("START", _("Subscribe"))]

    def handle(self, action):
        if action == "START":
            self.say(_("Subscribed") if self.app.store.toggle_sub(self.show) else _("Unsubscribed"))
        else:
            super().handle(action)

    def act(self, action, i):
        ep = self.eps[i]
        a = self.app
        if action == "A":
            a.play_episode(ep, self.show)
            a.push(NowPlaying(a))
        elif action == "X":
            state = a.downloads.state(ep["key"])
            if state == "done":
                a.push(Confirm(a, _("Delete download?"), ep["title"], lambda: a.downloads.delete(ep["key"])))
            elif state in ("queued", "loading"):
                a.downloads.cancel(ep["key"])
                self.say(_("Download cancelled"))
            else:
                a.downloads.add(ep, self.show)
                self.say(_("Downloading…"))
        elif action == "Y":
            e = a.store.ep(ep, self.show)
            e["played"] = not e.get("played")
            if not e["played"]:
                e["pos"] = 0
            a.store.changed()


class DownloadsView(Menu):
    def draw(self, s):
        self.TITLE = _("Downloads")
        super().draw(s)

    def rows(self):
        out = []
        for key, e in self.app.store.downloads():
            size = os.path.getsize(e["file"]) if os.path.exists(e["file"]) else 0
            out.append((key, e.get("title", ""), " · ".join(b for b in (e.get("show"), fmt_mb(size),
                        _("✓ played") if e.get("played") else "") if b), None, ""))
        return out

    def empty_text(self):
        return _("No downloads yet. In a podcast's episode list, press X to download an episode.")

    def hints(self):
        return [("A", _("Play")), ("X", _("Delete")), ("B", _("Back"))]

    def act(self, action, key):
        a = self.app
        e = a.store.peek(key)
        if not e:
            return
        if action == "A":
            ep = {"key": key, "title": e.get("title", ""), "url": e.get("url"), "duration": e.get("dur", 0), "date": e.get("date", 0)}
            a.play_episode(ep, {"title": e.get("show", ""), "feed": e.get("feed", "")})
            a.push(NowPlaying(a))
        elif action == "X":
            a.push(Confirm(a, _("Delete download?"), e.get("title", ""), lambda: a.downloads.delete(key)))


# ---------------------------------------------------------------------- now playing
class NowPlaying(View):
    TITLE = "Now playing"

    def right(self):
        left = self.app.sleep_left()
        return _("Sleep in {t}", t=fmt_time(left)) if left else ""

    def handle(self, action):
        a, p = self.app, self.app.player
        item = p.item or {}
        ep = item.get("kind") == "episode"
        if action == "B":
            a.pop()
        elif action == "A":
            if p.active:
                p.toggle_pause()
            elif item:
                a.replay()
        elif action == "X":
            a.stop_playback()
        elif action == "UP":
            p.add_volume(5)
        elif action == "DOWN":
            p.add_volume(-5)
        elif action == "LEFT" and ep:
            p.seek(-15)
        elif action == "RIGHT" and ep:
            p.seek(30)
        elif action in ("L1", "R1") and ep:
            cur = p.prop("speed", 1.0)
            i = min(range(len(SPEEDS)), key=lambda k: abs(SPEEDS[k] - cur))
            i = max(0, min(len(SPEEDS) - 1, i + (1 if action == "R1" else -1)))
            p.set_speed(SPEEDS[i])
            a.store.settings["speed"] = SPEEDS[i]
            a.store.changed()
        elif action == "Y":
            a.cycle_sleep()
        elif action == "SELECT":
            a.set_screen(False)
        elif action == "START" and ep and item.get("ep"):  # download the episode that's playing
            state = a.downloads.state(item["key"])
            if state in (None, "error"):
                a.downloads.add(item["ep"], item.get("show") or {})
                a.toast(_("Downloading…"))
        elif action == "START" and item.get("kind") == "station":
            a.store.toggle_fav(item["station"])

    def draw(self, s):
        a, p = self.app, self.app.player
        s.title_bar(_("Now playing"), self.right())
        item = p.item
        if not item:
            s.text(W // 2, 180, _("Nothing playing"), 3, C["dim"], align="center")
            s.footer([("B", _("Back"))])
            return
        ep = item.get("kind") == "episode"
        s.text(24, 76, _("PODCAST") if ep else _("RADIO"), 2, C["accent_hi"])
        y = 104
        for line in s.wrap(item.get("title", ""), W - 48, 3)[:2]:
            s.text(24, y, line, 3)
            y += 34
        sub = item.get("sub", "")
        if item.get("kind") == "episode":  # "<show> · downloaded/streaming": the last part in the app's language
            show, _sep, how = sub.rpartition(" · ")
            sub = f"{show} · {_(how)}" if show else _(how)
        s.text(24, y + 2, s.fit(sub, W - 48), 2, C["dim"])
        y += 36
        if p.error:
            s.para(24, y, tr(p.error), W - 48, 2, C["warn"])
        elif not ep:
            song = p.now_title()
            if song:
                s.text(24, y, _("On air:"), 2, C["faint"])
                s.para(24, y + 24, song, W - 48, 2, C["text"])
        status = _("Stopped") if not p.active else _("Paused") if p.prop("pause") else \
            _("Loading…") if p.prop("paused-for-cache") or p.prop("time-pos") is None else _("Playing")
        pos, dur = p.prop("time-pos", 0) or 0, p.prop("duration", 0) or 0
        if ep:
            s.bar(24, 300, W - 48, 10, pos / dur if dur else 0)
            s.text(24, 318, fmt_time(pos), 2)
            s.text(W - 24, 318, fmt_time(dur) if dur else "", 2, C["dim"], align="right")
            spd = p.prop("speed", 1.0) or 1.0
            s.text(W // 2, 318, f"{status} · {spd:g}x", 2, C["accent_hi"], align="center")
        else:
            s.text(24, 318, f"{status}" + (f" · {fmt_time(pos)}" if pos else ""), 2, C["accent_hi"])
            if item.get("station") and a.store.is_fav(item["station"]):
                s.text(W - 24, 318, _("★ favourite"), 2, C["accent_hi"], align="right")
        vol = p.prop("volume")
        if vol is not None:
            s.text(W - 24, 76, _("Volume {n}%", n=int(vol)), 2, C["dim"], align="right")
        keys = [("A", _("Pause")), ("X", _("Stop")), ("↑↓", _("Volume")), ("Y", _("Sleep")), ("SELECT", _("Screen off (MENU wakes)"))]
        if ep:
            keys = [("A", _("Pause")), ("←→", "-15/+30s"), ("L1 R1", _("Speed")), ("Y", _("Sleep")),
                    ("SELECT", _("Screen off (MENU wakes)"))]
            state = a.downloads.state(item.get("key"))
            if state == "loading":
                d, t = a.downloads.progress.get(item["key"], (0, 0))
                keys.insert(1, ("↓", _("Downloading {n}%", n=100 * d // t) if t else fmt_mb(d)))
            elif state == "queued":
                keys.insert(1, ("↓", _("Downloading…")))
            elif state in (None, "error") and item.get("ep"):
                keys.insert(1, ("START", _("Download")))
        else:
            keys.insert(2, ("START", _("Favourite")))
        lines, line = [], ""
        for k, v in keys:  # as many hints per line as fit (translations can be longer)
            part = f"{k} {v}"
            if line and s.text_w(line + "  " + part, 2) > W - 48:
                lines.append(line)
                line = part
            else:
                line = f"{line}  {part}" if line else part
        lines.append(line)
        y0, gap = (346, 22) if len(lines) > 2 else (356, 24)  # three lines fit between the time row and the footer
        for i, line in enumerate(lines[:3]):
            s.text(24, y0 + i * gap, line, 2, C["faint"])
        s.footer([("B", _("Back (keeps playing)")), ("X", _("Stop"))])


class Confirm(View):
    def __init__(self, app, title, text, yes):
        super().__init__(app)
        self.TITLE, self.text, self.yes = title, text, yes

    def handle(self, action):
        if action == "A":
            self.app.pop()
            self.yes()
        elif action == "B":
            self.app.pop()

    def draw(self, s):
        s.title_bar(self.TITLE)
        s.para(24, 90, self.text, W - 48)
        s.footer([("A", _("Yes")), ("B", _("No"))])


# ---------------------------------------------------------------------- settings / about
class Settings(Menu):
    def draw(self, s):
        self.TITLE = _("Settings")
        super().draw(s)

    def rows(self):
        st = self.app.store
        size = sum(os.path.getsize(e["file"]) for _k, e in st.downloads() if os.path.exists(e["file"]))
        return [("country", _("My country"), st.settings.get("country_name") or _("Not set (choose in Radio > By country)"), None, ""),
                ("region", _("Podcast charts"), _(dict(PODCAST_REGIONS).get(st.settings.get("podcast_country", "us"), "United States")),
                 None, ""),
                ("language", _("Language"), lang.label(), None, ""),
                ("clear", _("Delete all downloads"), f"{episodes(len(st.downloads()))} · {fmt_mb(size)}", None, ""),
                ("updates", _("Check for updates"), _("On · a notice when a new version is out") if self.app.updater.enabled
                 else _("Off"), None, ""),
                ("checknow", _("Check now"), _("You have version {v}", v=APP_VERSION), None, "")]

    def hints(self):
        return [("A", _("Change")), ("B", _("Back"))]

    def act(self, action, key):
        if key == "language" and action in ("LEFT", "RIGHT", "A"):
            lang.cycle(-1 if action == "LEFT" else 1)
            if not self.app.screen.language_ok():
                lang.unavailable()  # no font for it: English
        elif action == "A":
            self.choose(key)

    def choose(self, key):
        a = self.app
        if key == "country":
            a.push(Loading(a, _("Countries"), a.radio.countries, lambda rows: Countries(a, rows)))
        elif key == "region":
            a.push(Regions(a))
        elif key == "updates":
            a.updater.set_enabled(not a.updater.enabled)
        elif key == "checknow":
            if a.updater.state not in ("available", "downloading", "ready"):
                a.updater.state, a.updater.info = None, None
            a.push(UpdateScreen(a, a.updater, "PocketKode Radio"))
        elif key == "clear":
            a.push(Confirm(a, _("Delete all downloads?"), _("Downloaded episodes are removed from the handheld. "
                           "Your subscriptions and listening progress are kept."),
                           lambda: [a.downloads.delete(k) for k, _ in a.store.downloads()]))


class Regions(Menu):
    def draw(self, s):
        self.TITLE = _("Podcast charts")
        super().draw(s)

    def rows(self):
        cur = self.app.store.settings.get("podcast_country", "us")
        return [(cc, _(name), "", None, "✓" if cc == cur else "") for cc, name in PODCAST_REGIONS]

    def choose(self, cc):
        self.app.store.settings["podcast_country"] = cc
        self.app.store.changed()
        self.app.pop()


class About(View):
    def handle(self, action):
        if action == "B":
            self.app.pop()
        elif action == "A":
            self.app.push(Privacy(self.app))

    def draw(self, s):
        s.title_bar(_("About"))
        s.text(24, 76, f"PocketKode Radio {APP_VERSION}", 3)
        y = s.para(24, 120, _("Internet radio and podcasts for muOS handhelds. Stations come from the "
                              "community Radio Browser directory (radio-browser.info). Podcast search and charts come "
                              "from Apple's public podcast directory, and episodes from each show's own feed. "
                              "Nothing is recorded or re-shared."), W - 48, gap=2) + 8
        for line, c in [(_("Free and open source (MIT License). See LICENSE in the app folder."), C["text"]),
                        ("github.com/" + updater.REPO, C["dim"]),
                        ("feedback@pocketkode.com", C["dim"])]:
            y = s.para(24, y, line, W - 48, 2, c, gap=2)
        s.footer([("A", _("Privacy")), ("B", _("Back"))])


# ---------------------------------------------------------------------- privacy
PRIVACY = [
    "PocketKode Radio never reads or sends your files, and doesn't record anything.",
    "For updates it reads the latest release on GitHub (you can turn this off in Settings). It sends nothing about you or the handheld.",
    "Stations come from Radio Browser, podcasts from Apple's podcast directory, and the sound from each station or show itself. Your searches go to those services. When you play a station, Radio Browser is told that the station was played (an anonymous count that keeps its Top list up to date).",
    'Your favourites, subscriptions and history stay on the handheld. No ads, no analytics, no tracking.',
]


class Privacy(View):
    """What this app sends, and what it never does (also in the README). ▲▼ scroll."""

    def __init__(self, app):
        super().__init__(app)
        self.scroll, self.height = 0, 0

    def handle(self, action):
        room = H - 44 - 62
        if action == "DOWN":
            self.scroll = min(max(0, self.height - room), self.scroll + 48)
        elif action == "UP":
            self.scroll = max(0, self.scroll - 48)
        elif action == "B":
            self.app.pop()

    def draw(self, s):
        y = 62 - self.scroll
        for para in PRIVACY:
            y = s.para(24, y, _(para), W - 48, 2, C["text"] if para is PRIVACY[0] else C["dim"]) + 8
        self.height = y + self.scroll - 62
        s.title_bar(_("Privacy"))  # drawn after the text, so scrolled lines go under the bars
        more = self.height > H - 44 - 62
        s.footer(([("↑↓", _("Scroll"))] if more else []) + [("B", _("Back"))])


class Notice(View):
    """A short message (e.g. after an update)."""

    def __init__(self, app, title, body):
        super().__init__(app)
        self.title, self.body = title, body

    def handle(self, action):
        if action in ("A", "B"):
            self.app.pop()

    def draw(self, s):
        s.title_bar(_(self.title))
        s.para(24, 90, self.body, W - 48, 2, C["dim"])
        s.footer([("A", "OK")])


# ---------------------------------------------------------------------- app
def _forget_licence(app_dir):
    """Versions before 1.3.0 had an activation: its saved licence (with a handheld ID) isn't needed any more."""
    try:
        os.remove(os.path.join(app_dir, "data", "license.json"))
    except OSError:
        pass


class App:
    def __init__(self, app_dir):
        self.app_dir = app_dir
        os.makedirs(os.path.join(app_dir, "logs"), exist_ok=True)
        lang.setup(app_dir)  # the app's choice, else muOS's language (see lang.py)
        self.screen = Screen()
        self.screen.app_dir = app_dir
        if not self.screen.language_ok():
            lang.unavailable()
        self.pad = Pad()
        self.awake = KeepAwake()
        self.store = Store(app_dir)
        self.radio = Radio()
        self.player = Player(os.path.join(app_dir, "logs"))
        self.downloads = Downloads(self.store)
        self.downloads.start()
        _forget_licence(app_dir)
        self.stack = [Home(self)]
        self.running = True
        self._toast = ("", 0.0)
        self.restart = False  # "Restart now" after an update: main.py returns 42, mux_launch.sh starts again
        # Updates from GitHub releases (checked at start and daily when online; nothing installs by itself)
        self.updater = updater.Updater(app_dir, "pocketkode-radio", APP_VERSION)
        self._confirmed = False
        if self.updater.just_updated:
            self.push(Notice(self, "Updated", _("PocketKode Radio is now version {v}. Your stations, podcasts "
                                                "and settings were kept.", v=APP_VERSION)))
        elif self.updater.rolled_back:
            self.push(Notice(self, "Update undone", _("Version {bad} didn't start, so PocketKode Radio went back to {v}. "
                                                      "Please email feedback@pocketkode.com.",
                                                      bad=self.updater.rolled_back.get('version'), v=APP_VERSION)))
        self.screen_on = True
        self.sleep_at = 0.0
        self.last_url = None
        self._event = ctypes.create_string_buffer(64)
        self._last_pos_save = 0.0

    def toast(self, text, secs=4.0):
        self._toast = (text, time.monotonic() + secs)

    # navigation
    def push(self, view):
        self.pad.clear()
        self.stack.append(view)

    def pop(self):
        self.pad.clear()
        if len(self.stack) > 1:
            self.stack.pop()

    def replace(self, view):
        self.stack[-1] = view

    # playback
    def play_station(self, st):
        self.store.played_station(st)
        item = {"kind": "station", "title": st["name"], "station": st,
                "sub": " · ".join(b for b in [st.get("country")] + st.get("tags", [])[:2] if b)}
        self._play(st["url"], item)
        threading.Thread(target=self.radio.clicked, args=(st,), daemon=True).start()

    def play_episode(self, ep, show):
        e = self.store.ep(ep, show)
        if e.get("played"):
            e["played"], e["pos"] = False, 0
        src = e["file"] if e.get("file") and os.path.exists(e["file"]) else ep["url"]
        item = {"kind": "episode", "title": ep["title"], "key": ep["key"], "ep": ep, "show": show,
                "sub": show.get("title", "") + (" · downloaded" if src != ep["url"] else " · streaming")}  # translated when drawn
        self._play(src, item, start=e.get("pos", 0))

    def _play(self, url, item, start=0):
        self.last_url = (url, item)
        self.player.play(url, item, start=start, speed=self.store.settings.get("speed", 1.0),
                         volume=self.store.settings.get("volume", 80))
        self.awake.start()

    def replay(self):
        if self.last_url:
            url, item = self.last_url
            start = 0
            if item.get("kind") == "episode":
                start = (self.store.peek(item["key"]) or {}).get("pos", 0)
            self.player.play(url, item, start=start, speed=self.store.settings.get("speed", 1.0),
                             volume=self.store.settings.get("volume", 80))
            self.awake.start()

    def stop_playback(self):
        self._save_position(force=True)
        self.player.stop(forget=False)
        self.awake.stop()

    def _save_position(self, force=False):
        p = self.player
        item = p.item
        now = time.monotonic()
        if not item or not p.active or (not force and now - self._last_pos_save < 5):
            return
        self._last_pos_save = now
        vol = p.prop("volume")
        if vol is not None and int(vol) != self.store.settings.get("volume"):
            self.store.settings["volume"] = int(vol)
            self.store.changed()
        if item.get("kind") != "episode":
            return
        e = self.store.peek(item["key"])
        pos, dur = p.prop("time-pos"), p.prop("duration")
        if e is not None and pos is not None:
            e["pos"] = float(pos)
            if dur:
                e["dur"] = float(dur)
                e["played"] = pos >= dur - 60
            self.store.changed()

    # sleep timer and screen
    def cycle_sleep(self):
        left = self.sleep_left() / 60
        nxt = next((m for m in SLEEP_STEPS if m > left + 0.5), 0)
        self.sleep_at = time.monotonic() + nxt * 60 if nxt else 0.0

    def sleep_left(self):
        return max(0.0, self.sleep_at - time.monotonic()) if self.sleep_at else 0.0

    def set_screen(self, on):
        if on == self.screen_on:
            return
        self.screen_on = on
        try:  # lets mux_launch.sh turn the screen back on if the app crashes
            if on:
                os.remove(SCREEN_MARK)
            else:
                open(SCREEN_MARK, "w").close()
        except OSError:
            pass
        if os.path.exists(BRIGHT):
            try:
                subprocess.run([BRIGHT, "R" if on else "0"], timeout=5,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except (OSError, subprocess.SubprocessError):
                pass

    # loop
    def dispatch(self, action):
        if not self.screen_on:
            if action == "MENU":
                self.set_screen(True)  # only MENU wakes the screen (a button pressed in a bag or pocket doesn't)
            return
        if action == "MENU" and self.player.item and not isinstance(self.stack[-1], NowPlaying):
            self.push(NowPlaying(self))
            return
        self.stack[-1].handle(action)

    def step(self):
        while sdl.PollEvent(self._event):
            if int.from_bytes(self._event.raw[:4], "little") == sdl.QUIT:
                self.running = False
        for action in self.pad.poll():
            self.dispatch(action)
        self.player.poll()
        self._save_position()
        if self.player.item and not self.player.active and self.awake.active:
            self._save_position(force=True)
            self.awake.stop()
        if self.player.active:
            self.awake.pulse()
        if self.sleep_at and time.monotonic() >= self.sleep_at:
            self.sleep_at = 0.0
            self.stop_playback()
            self.set_screen(True)
        self.stack[-1].update()
        self.store.save()
        self.updater.maybe_check()
        s = self.screen
        s.clear()
        if self.screen_on:
            self.stack[-1].draw(s)
            self._mini(s)
            text, until = self._toast
            if text and time.monotonic() < until:
                s.box(0, H - 40, W, 40, C["bar"])  # over the footer for a few seconds
                s.text(W // 2, H - 28, text, 2, C["ok"] if text.startswith("✓") else C["text"], align="center")
        s.present()
        if not self._confirmed:  # the first screen is up: an update that was just installed works
            self._confirmed = True
            updater.confirm(self.app_dir)

    def _mini(self, s):
        p = self.player
        if not p.item or isinstance(self.stack[-1], (NowPlaying, Keyboard)):
            return
        y = H - FOOT - MINI
        s.box(0, y, W, MINI, C["row"])
        s.box(0, y, 4, MINI, C["accent"] if p.active else C["faint"])
        state = ("▶ " if not p.prop("pause") else "|| ") if p.active else "■ "
        hint = _("MENU: open")
        s.text(14, y + 7, s.fit(state + p.item.get("title", ""), W - 44 - s.text_w(hint, 2)), 2)
        s.text(W - 14, y + 7, hint, 2, C["faint"], align="right")

    def run(self):
        try:
            while self.running:
                self.step()
                sdl.Delay(33 if self.screen_on else 100)
        finally:
            self._save_position(force=True)
            self.set_screen(True)
            self.player.stop()
            self.downloads.stop()
            self.awake.stop()
            self.store.save(force=True)
            self.pad.close()
            self.screen.close()
