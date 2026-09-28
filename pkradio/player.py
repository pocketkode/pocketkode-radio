# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
"""Audio playback with the mpv that ships with muOS, controlled over mpv's IPC socket."""
import json
import os
import shutil
import socket
import subprocess
import time

SOCK = "/tmp/pkradio-mpv.sock"
PROPS = ("time-pos", "duration", "pause", "speed", "metadata", "core-idle", "paused-for-cache")


class MpvIPC:
    def __init__(self, path):
        self.path = path
        self.sock = None
        self.buf = b""
        self.props = {}
        self._rid = 0
        self._pending = {}

    def connect(self):
        if self.sock:
            return True
        try:
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(self.path)
            s.setblocking(False)
            self.sock = s
            return True
        except OSError:
            return False

    def command(self, cmd):
        if not self.connect():
            return False
        self._rid += 1
        msg = json.dumps({"command": cmd, "request_id": self._rid}) + "\n"
        try:
            self.sock.sendall(msg.encode())
        except OSError:
            return False
        return self._rid

    def query(self, prop):
        rid = self.command(["get_property", prop])
        if rid:
            self._pending[rid] = prop

    def pump(self):
        if not self.sock:
            return
        try:
            while True:
                chunk = self.sock.recv(65536)
                if not chunk:
                    break
                self.buf += chunk
        except (BlockingIOError, InterruptedError):
            pass
        except OSError:
            return
        while b"\n" in self.buf:
            line, self.buf = self.buf.split(b"\n", 1)
            try:
                msg = json.loads(line)
            except ValueError:
                continue
            prop = self._pending.pop(msg.get("request_id"), None)
            if prop and msg.get("error") == "success":
                self.props[prop] = msg.get("data")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        self.sock = None


def find_mpv():
    for p in (os.environ.get("PKR_MPV"), "/usr/bin/mpv", shutil.which("mpv")):
        if p and os.path.exists(p):
            return p
    return None


class Player:
    """One thing playing at a time: a station (live) or an episode (seekable)."""

    def __init__(self, log_dir):
        self.log_dir = log_dir
        self.proc = None
        self.ipc = None
        self.item = None      # {"kind": "station"|"episode", "title", "sub", ...}
        self.started = 0.0
        self._last_query = 0.0
        self.error = None

    @property
    def active(self):
        return self.proc is not None and self.proc.poll() is None

    def play(self, url, item, start=0, speed=1.0):
        self.stop(forget=False)
        mpv = find_mpv()
        if not mpv:
            self.error = "mpv isn't installed on this system."
            return False
        try:
            os.remove(SOCK)
        except OSError:
            pass
        # warnings and errors, plus the lines that say what's played and which sound output is used, go to mpv.log
        args = [mpv, "--no-config", "--no-video", "--idle=no", "--term-status-msg=",
                f"--input-ipc-server={SOCK}", f"--force-media-title={item.get('title', '')}",
                "--volume=100", "--cache=yes", "--network-timeout=20",
                "--msg-level=all=warn,cplayer=info", "--user-agent=PocketKodeRadio/1.3"]
        if item.get("kind") == "episode":
            args.append(f"--speed={speed:.2f}")
            if start > 5:
                args.append(f"--start={int(start)}")
        args.append(url)
        log = open(os.path.join(self.log_dir, "mpv.log"), "w")  # only the latest playback
        print(f"[player] {item.get('kind')}: {url}", flush=True)
        try:
            self.proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=log, stderr=log)
        except OSError as e:
            self.error = f"Couldn't start the player: {e}"
            return False
        finally:
            log.close()
        self.ipc = MpvIPC(SOCK)
        self.item = item
        self.started = time.monotonic()
        self.error = None
        return True

    def poll(self):
        if not self.ipc:
            return
        self.ipc.pump()
        now = time.monotonic()
        if now - self._last_query >= 0.5:
            self._last_query = now
            for p in PROPS:
                self.ipc.query(p)
        if self.proc and self.proc.poll() is not None and self.item:
            print(f"[player] mpv stopped (exit code {self.proc.returncode})", flush=True)
            if self.proc.returncode not in (0, None) and now - self.started < 20 and not self.prop("time-pos"):
                self.error = "This couldn't be played. The station or episode may be offline."
            self.proc = None

    def prop(self, name, default=None):
        v = self.ipc.props.get(name) if self.ipc else None
        return default if v is None else v

    def now_title(self):
        """For radio: the song/show currently on air, if the station sends it."""
        md = self.prop("metadata") or {}
        return md.get("icy-title") or md.get("StreamTitle") or ""

    def cmd(self, *c):
        if self.ipc:
            self.ipc.command(list(c))

    def toggle_pause(self):
        self.cmd("cycle", "pause")

    def seek(self, secs):
        self.cmd("seek", secs, "relative")

    def set_speed(self, speed):
        self.cmd("set_property", "speed", speed)

    def stop(self, forget=True):
        """Stop playback. forget=False keeps self.item (e.g. to show what just ended)."""
        if self.proc and self.proc.poll() is None:
            self.cmd("quit")
            try:
                self.proc.wait(2)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        self.proc = None
        if self.ipc:
            self.ipc.close()
        self.ipc = None
        if forget:
            self.item = None
