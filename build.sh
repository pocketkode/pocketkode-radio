#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 PocketKode
# Builds PocketKodeRadio.muxapp (the installable muOS package) from this source folder.
#
# Usage:   ./build.sh            build dist/PocketKodeRadio.muxapp
#
# Needs: bash, zip, unzip, curl, shasum and python3. The package holds the app's Python source as it is, plus the
# Noto Sans JP, SC and KR fonts for the other languages (SIL Open Font License, downloaded here and checked against
# their SHA-256). The app uses the Python 3, SDL2, SDL2_ttf and mpv that come with muOS.
set -euo pipefail

cd "$(dirname "$0")"
SRC="$PWD"
DIST="${DIST:-$SRC/dist}"
APP_NAME="PocketKodeRadio"
STAGE="$DIST/stage/$APP_NAME"
NOTO_BASE="https://github.com/notofonts/noto-cjk/releases/download/Sans2.004"
# zip on the Noto CJK release · font file · its SHA-256
FONTS=(
	"16_NotoSansJP.zip NotoSansJP-Regular.otf dff723ba59d57d136764a04b9b2d03205544f7cd785a711442d6d2d085ac5073"
	"18_NotoSansSC.zip NotoSansSC-Regular.otf faa6c9df652116dde789d351359f3d7e5d2285a2b2a1f04a2d7244df706d5ea9"
	"17_NotoSansKR.zip NotoSansKR-Regular.otf 69975a0ac8472717870aefeab0a4d52739308d90856b9955313b2ad5e0148d68"
)
CACHE="$DIST/cache"

for tool in zip unzip curl shasum python3; do
	command -v "$tool" >/dev/null || { echo "Missing tool: $tool"; exit 1; }
done

echo "==> Fonts (Noto Sans JP, SC and KR)"
mkdir -p "$CACHE"
for entry in "${FONTS[@]}"; do
	read -r zipname file sum <<<"$entry"
	base="${file%-Regular.otf}"
	if [ ! -f "$CACHE/$file" ]; then
		echo "  downloading $zipname"
		curl -fsSL -o "$CACHE/$zipname" "$NOTO_BASE/$zipname"
		rm -rf "$CACHE/unz" && unzip -q -o "$CACHE/$zipname" "$file" LICENSE -d "$CACHE/unz"
		mv "$CACHE/unz/$file" "$CACHE/$file"
		mv "$CACHE/unz/LICENSE" "$CACHE/$base-OFL.txt"
		rm -rf "$CACHE/unz" "$CACHE/$zipname"
	fi
	echo "$sum  $CACHE/$file" | shasum -a 256 -c --quiet - || { echo "Font checksum mismatch: $file"; exit 1; }
done

echo "==> Assembling app folder"
rm -rf "$DIST/stage"
mkdir -p "$STAGE/glyph"
cp "$SRC"/*.py "$SRC/mux_launch.sh" "$SRC/README.md" "$SRC/LICENSE" "$STAGE/"
cp "$SRC"/glyph/* "$STAGE/glyph/"
mkdir -p "$STAGE/fonts" "$STAGE/licenses"
for entry in "${FONTS[@]}"; do
	read -r _zip file _sum <<<"$entry"
	cp "$CACHE/$file" "$STAGE/fonts/"
	cp "$CACHE/${file%-Regular.otf}-OFL.txt" "$STAGE/licenses/"
done
chmod +x "$STAGE/mux_launch.sh"
find "$STAGE" \( -name "__pycache__" -o -name ".DS_Store" \) -prune -exec rm -rf {} +

echo "==> Checking Python syntax"
python3 - "$STAGE" <<'EOF'
import ast, pathlib, sys
for p in pathlib.Path(sys.argv[1]).glob("*.py"):
    ast.parse(p.read_text(), str(p))
print("  ok")
EOF

echo "==> Packaging"
mkdir -p "$DIST"
rm -f "$DIST/$APP_NAME.muxapp"
(cd "$DIST/stage" && zip -qr -X "$DIST/$APP_NAME.muxapp" "$APP_NAME")
echo "Done: $DIST/$APP_NAME.muxapp ($(du -h "$DIST/$APP_NAME.muxapp" | cut -f1))"
echo "Copy it to the ARCHIVE folder on SD card 1, then install via Applications > Archive Manager."
