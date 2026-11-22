# Installer le relais TELLR sur le Mac (une seule fois, ~10 min)

Ouvre l'app **Terminal** et colle ces commandes une par une.

0. Google Drive pour ordinateur (gratuit) : https://www.google.com/drive/download/ — se connecter avec le compte Google qui a accès à la campagne Yomi. Le Drive de la campagne apparaît dans le Finder, section « Drive partagés ».
1. Homebrew (si pas déjà installé) :
   `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Les outils : `brew install yt-dlp ffmpeg gh git`
3. Connexion GitHub (choisir GitHub.com, HTTPS, navigateur) : `gh auth login`
4. Le dépôt : `git clone https://github.com/shinkoco/tellr-videos ~/tellr-videos`
5. Premier essai : `~/tellr-videos/relay/tellr_relay.sh` puis vérifier `cat ~/tellr-videos/relay/relay.log` (doit afficher OK).
6. Automatisation (7 h et 19 h, et au démarrage du Mac) :
   `cp ~/tellr-videos/relay/com.tellr.relay.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.tellr.relay.plist`

Fonctionnement : la tâche TELLR écrit les liens YouTube voulus dans `relay/queue.txt`. Le Mac les télécharge (720p)
et les dépose dans la release GitHub « sources » (pas dans le dépôt lui-même). La tâche les récupère ensuite depuis
`https://github.com/shinkoco/tellr-videos/releases/download/sources/<id>.mp4` et monte les clips.
Le Mac doit être allumé (ou s'allumer) le matin ; sinon le relais tourne au prochain démarrage.

Sources Drive : le relais envoie aussi les MP4 du dossier « EXTRAITS YOMI » (jamais « Clips Interdits »), 10 par passage.
Correspondance nom de fichier → vidéo : relay/drive_index.tsv. Si le dossier n'est pas trouvé, mettre son chemin dans la variable TELLR_DRIVE_DIR.
