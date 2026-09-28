# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Internet radio stations from the public Radio Browser directory (radio-browser.info)."""
import random

import net

FALLBACK_SERVERS = ["https://de1.api.radio-browser.info", "https://de2.api.radio-browser.info",
                    "https://fi1.api.radio-browser.info", "https://nl1.api.radio-browser.info"]
PAGE = 40


class Radio:
    def __init__(self):
        self.servers = []

    def _servers(self):
        if not self.servers:
            try:
                names = [s.get("name") for s in net.get_json("https://all.api.radio-browser.info/json/servers", timeout=10)]
                self.servers = [f"https://{n}" for n in dict.fromkeys(names) if n]
            except net.NetError:
                self.servers = []
            if not self.servers:
                self.servers = list(FALLBACK_SERVERS)
            random.shuffle(self.servers)
        return self.servers

    def _get(self, path, params=None):
        last = None
        for base in list(self._servers()):
            try:
                return net.get_json(base + path, params, timeout=15)
            except net.NetError as e:
                last = e
                self.servers.remove(base)
                self.servers.append(base)  # try the others first next time
        raise last or net.NetError("Radio directory unavailable.")

    @staticmethod
    def station(d):
        tags = [t for t in (d.get("tags") or "").split(",") if t][:3]
        return {"id": d.get("stationuuid"), "name": (d.get("name") or "").strip() or "Unnamed station",
                "url": d.get("url_resolved") or d.get("url"), "country": d.get("country") or "",
                "cc": d.get("countrycode") or "", "tags": tags, "codec": d.get("codec") or "",
                "bitrate": d.get("bitrate") or 0, "favicon": d.get("favicon") or ""}

    def _stations(self, rows):
        return [self.station(r) for r in rows if r.get("url_resolved") or r.get("url")]

    def top(self, offset=0):
        return self._stations(self._get("/json/stations/search", {"order": "clickcount", "reverse": "true",
                                                                "hidebroken": "true", "limit": PAGE, "offset": offset}))

    def search(self, name="", countrycode="", tag="", offset=0):
        params = {"order": "clickcount", "reverse": "true", "hidebroken": "true", "limit": PAGE, "offset": offset}
        if name:
            params["name"] = name
        if countrycode:
            params["countrycode"] = countrycode
        if tag:
            params["tag"] = tag
            params["tagExact"] = "true"
        return self._stations(self._get("/json/stations/search", params))

    def countries(self):
        rows = self._get("/json/countries", {"order": "stationcount", "reverse": "true", "hidebroken": "true"})
        return [{"cc": r.get("iso_3166_1"), "name": r.get("name"), "count": r.get("stationcount", 0)}
                for r in rows if r.get("iso_3166_1") and r.get("stationcount", 0) >= 5]

    def genres(self):
        rows = self._get("/json/tags", {"order": "stationcount", "reverse": "true", "hidebroken": "true", "limit": 80})
        return [{"tag": r.get("name"), "count": r.get("stationcount", 0)} for r in rows
                if r.get("name") and len(r["name"]) <= 24]

    def clicked(self, station):
        """Tell the directory a station was played (their usage guidelines ask for this)."""
        try:
            self._get(f"/json/url/{station['id']}")
        except (net.NetError, KeyError):
            pass
