#!/usr/bin/env bash
# Holt die RestedXP-Guides in genau einer Version (Git-Tag) nach vendor/rxpguides.
# Aufruf: tools/fetch_rxp.sh v4.11.23
# Die installierte Version steht im Testlog in jeder Zeile «SITZUNG … RXP v4.11.xx».
set -euo pipefail

TAG="${1:?Bitte einen RXP-Tag angeben, z. B. v4.11.23}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DIR="${RXP_DIR:-$ROOT/vendor/rxpguides}"

if [ ! -d "$DIR/.git" ]; then
  git clone --quiet --filter=blob:none https://github.com/RestedXP/RXPGuides "$DIR"
fi
git -C "$DIR" fetch --tags --force origin
git -C "$DIR" checkout -q "$TAG"
echo "RXP $TAG liegt in $DIR ($(git -C "$DIR" log -1 --format='%h %ad' --date=short))"
