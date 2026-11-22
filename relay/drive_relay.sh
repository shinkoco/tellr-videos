#!/bin/bash
# TELLR — relais Drive : envoie les MP4 du Drive de campagne (via Google Drive pour ordinateur)
# vers la release GitHub « sources ». Ignore le dossier « Clips Interdits ».
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
REPO="$HOME/tellr-videos"
LOG="$REPO/relay/relay.log"
INDEX="$REPO/relay/drive_index.tsv"
DRIVE_DIR="${TELLR_DRIVE_DIR:-$(ls -d "$HOME"/Library/CloudStorage/GoogleDrive-*/Drive*partag*/*/*EXTRAITS\ YOMI* 2>/dev/null | head -1)}"
cd "$REPO" || exit 1
git pull -q --rebase
[ -d "$DRIVE_DIR" ] || { echo "$(date) ERREUR dossier Drive introuvable : $DRIVE_DIR" >> "$LOG"; exit 1; }
gh release view sources >/dev/null 2>&1 || gh release create sources --title "Sources vidéo" --notes "Déposé par le relais Mac" >/dev/null
touch "$INDEX"
n=0
find -L "$DRIVE_DIR" -type f -iname "*.mp4" ! -path "*Interdit*" | while read -r f; do
  rel="${f#$DRIVE_DIR/}"
  grep -qF "	$rel" "$INDEX" && continue
  slug="drive_$(printf '%s' "$rel" | shasum | cut -c1-10).mp4"
  cp "$f" "/tmp/$slug" && gh release upload sources "/tmp/$slug" --clobber && printf '%s\t%s\n' "$slug" "$rel" >> "$INDEX" && echo "$(date) OK drive $rel" >> "$LOG"
  rm -f "/tmp/$slug"
  n=$((n+1)); [ $n -ge 10 ] && break
done
git add relay/drive_index.tsv relay/relay.log
git commit -q -m "relais Drive : $(date +%F)" && git push -q
