# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Web requests: JSON, feeds and episode downloads, with messages people can understand."""
import json
import os
import socket
import ssl
import urllib.error
import urllib.parse
import urllib.request

USER_AGENT = "PocketKodeRadio/1.3 (+https://github.com/mahamudul87/pocketkode-radio)"


class NetError(Exception):
    pass


def friendly(e):
    reason = getattr(e, "reason", e)
    low = str(reason).lower()
    if isinstance(e, urllib.error.HTTPError):
        return f"The server said no (error {e.code}). Try again later."
    if isinstance(reason, (socket.timeout, TimeoutError)) or "timed out" in low:
        return "The connection timed out. Check Wi-Fi and try again."
    if isinstance(reason, ssl.SSLError) or "certificate" in low:
        return "Secure connection failed. Check the handheld's date and time."
    if isinstance(reason, socket.gaierror) or "name or service" in low or "resolution" in low:
        return "No internet connection. Turn on Wi-Fi in Configuration > Network."
    return f"Connection problem: {reason}"


def open_url(url, timeout=20, headers=None):
    h = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    h.update(headers or {})
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=timeout)
    except (urllib.error.URLError, OSError, ValueError) as e:
        raise NetError(friendly(e)) from e


def get_bytes(url, timeout=20, limit=16 << 20):
    with open_url(url, timeout) as r:
        try:
            data = r.read(limit + 1)
        except (OSError, ValueError) as e:
            raise NetError(friendly(e)) from e
    if len(data) > limit:
        raise NetError("That feed is too large to load.")
    return data


def get_json(url, params=None, timeout=20):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params)
    try:
        return json.loads(get_bytes(url, timeout))
    except ValueError as e:
        raise NetError("The server sent something the app couldn't read.") from e


def download(url, path, progress=None, cancelled=None, timeout=30):
    """Save url to path (via path + '.part', resuming a partial file). progress(done, total)."""
    part = path + ".part"
    have = os.path.getsize(part) if os.path.exists(part) else 0
    headers = {"Range": f"bytes={have}-"} if have else {}
    r = open_url(url, timeout, headers)
    try:
        if have and getattr(r, "status", 200) != 206:
            have = 0  # the server ignored the range: start again
        total = r.headers.get("Content-Length")
        total = int(total) + have if total and total.isdigit() else 0
        with open(part, "ab" if have else "wb") as f:
            done = have
            while True:
                if cancelled and cancelled():
                    return False
                try:
                    chunk = r.read(256 * 1024)
                except (OSError, ValueError) as e:
                    raise NetError(friendly(e)) from e
                if not chunk:
                    break
                f.write(chunk)
                done += len(chunk)
                if progress:
                    progress(done, total)
    finally:
        r.close()
    os.replace(part, path)
    return True
