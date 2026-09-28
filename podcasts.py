# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Podcasts: search and top charts (Apple's public podcast directory), episodes from each
show's own RSS feed."""
import email.utils
import hashlib
import html
import re
import xml.etree.ElementTree as ET

import net

ITUNES = "http://www.itunes.com/dtds/podcast-1.0.dtd"


def _show(r):
    return {"feed": r.get("feedUrl"), "title": r.get("collectionName") or r.get("trackName") or "Podcast",
            "author": r.get("artistName") or "", "genre": r.get("primaryGenreName") or ""}


def search(term, country="US"):
    d = net.get_json("https://itunes.apple.com/search",
                     {"media": "podcast", "entity": "podcast", "term": term, "limit": 40, "country": country})
    return [_show(r) for r in d.get("results") or [] if r.get("feedUrl")]


def top(country="us"):
    d = net.get_json(f"https://rss.marketingtools.apple.com/api/v2/{country.lower()}/podcasts/top/50/podcasts.json")
    ids = [r.get("id") for r in (d.get("feed") or {}).get("results") or [] if r.get("id")]
    if not ids:
        return []
    found = net.get_json("https://itunes.apple.com/lookup", {"id": ",".join(ids), "entity": "podcast"})
    by_id = {str(r.get("collectionId")): r for r in found.get("results") or [] if r.get("feedUrl")}
    return [_show(by_id[i]) for i in ids if i in by_id]


def _text(el, path, ns=None):
    x = el.find(path, ns or {})
    return (x.text or "").strip() if x is not None and x.text else ""


def _duration(s):
    s = (s or "").strip()
    if not s:
        return 0
    try:
        parts = [float(p) for p in s.split(":")]
    except ValueError:
        return 0
    secs = 0.0
    for p in parts:
        secs = secs * 60 + p
    return int(secs)


def _clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def episode_key(show_feed, guid):
    return hashlib.sha1(f"{show_feed}|{guid}".encode()).hexdigest()[:16]


def feed(url):
    """(show dict, [episode dicts]) newest first."""
    data = net.get_bytes(url, timeout=25)
    try:
        root = ET.fromstring(data)
    except ET.ParseError as e:
        raise net.NetError("This podcast's feed couldn't be read.") from e
    ch = root.find("channel")
    if ch is None:
        raise net.NetError("This podcast's feed couldn't be read.")
    ns = {"itunes": ITUNES}
    show = {"feed": url, "title": _text(ch, "title") or "Podcast",
            "author": _text(ch, "itunes:author", ns) or _text(ch, "managingEditor"),
            "about": _clean(_text(ch, "description"))[:600]}
    eps = []
    for it in ch.findall("item"):
        enc = it.find("enclosure")
        if enc is None or not enc.get("url"):
            continue
        guid = _text(it, "guid") or enc.get("url")
        when = 0
        pub = _text(it, "pubDate")
        if pub:
            try:
                when = int(email.utils.parsedate_to_datetime(pub).timestamp())
            except (TypeError, ValueError, IndexError):
                when = 0
        try:
            size = int(enc.get("length") or 0)
        except ValueError:
            size = 0
        eps.append({"key": episode_key(url, guid), "title": _text(it, "title") or "Episode",
                    "url": enc.get("url"), "type": enc.get("type") or "", "size": size, "date": when,
                    "duration": _duration(_text(it, "itunes:duration", ns)),
                    "about": _clean(_text(it, "description"))[:600]})
    eps.sort(key=lambda e: e["date"], reverse=True)
    return show, eps
