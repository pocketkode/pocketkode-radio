#!/bin/sh
# HELP: Internet radio and podcasts, with the screen off to save battery
# ICON: pocketkoderadio
# GRID: PocketKode Radio
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode

. /opt/muos/script/var/func.sh

APP_BIN="python3"
SETUP_APP "$APP_BIN" ""

SETUP_STAGE_OVERLAY

# -----------------------------------------------------------------------------

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$APP_DIR" || exit 1

mkdir -p "$APP_DIR/logs" "$APP_DIR/data"

# Stop the frontend background music so it doesn't play over the radio
killall -q playbgm.sh mpg123 2>/dev/null

export PYTHONDONTWRITEBYTECODE=1

# Exit code 42: the app asks to be started again (to finish an update)
while :; do
	python3 -u main.py >"$APP_DIR/logs/app.log" 2>&1
	[ $? -eq 42 ] || break
done

# If the app crashed: stop the player, turn the screen back on, undo keep-awake
pkill -f "input-ipc-server=/tmp/pkradio-mpv.sock" 2>/dev/null
if [ -f /tmp/pkradio-screenoff ]; then
	/opt/muos/script/device/bright.sh R
	rm -f /tmp/pkradio-screenoff
fi
if [ -f /tmp/pkradio-caffeine ]; then
	rm -f /run/muos/caffeine /tmp/pkradio-caffeine
fi

sync
