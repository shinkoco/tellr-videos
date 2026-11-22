#!/bin/bash
# TELLR — relais Mac : télécharge les vidéos YouTube demandées dans relay/queue.txt
# et les dépose en pièce jointe de la release GitHub « sources » du dépôt.
set -u
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
REPO="$HOME/tellr-videos"
LOG="$REPO/relay/relay.log"
cd "$REPO" || exit 1
git pull -q --rebase
mkdir -p "$HOME/.tellr_tmp"
gh release view sources >/dev/null 2>&1 || gh release create sources --title "Sources vidéo" --notes "Déposé par le relais Mac" >/dev/null
while read -r url; do
  [ -z "$url" ] && continue
  id=$(yt-dlp --get-id "$url" 2>/dev/null | head -1)
  [ -z "$id" ] && { echo "$(date) ERREUR id $url" >> "$LOG"; continue; }
  grep -q "^$id$" relay/done.txt 2>/dev/null && continue
  out="$HOME/.tellr_tmp/$id.mp4"
  if yt-dlp -q -f "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720]" --merge-output-format mp4 -o "$out" "$url"; then
    gh release upload sources "$out" --clobber && echo "$id" >> relay/done.txt && echo "$(date) OK $id" >> "$LOG"
    rm -f "$out"
  else
    echo "$(date) ERREUR téléchargement $url" >> "$LOG"
  fi
done < relay/queue.txt
bash "$REPO/relay/drive_relay.sh"
cd "$REPO" && git pull -q --rebase
git add relay/done.txt relay/relay.log 2>/dev/null
git commit -q -m "relais : sources du $(date +%F)" && git push -q
