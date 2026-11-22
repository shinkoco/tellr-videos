# TELLR — runbook

Chaîne TikTok **TELLR** (@tellr_fr) : clips d'entrepreneurs et de business en français.
Dépôt : shinkoco/tellr-videos. Vidéos servies par `https://raw.githubusercontent.com/shinkoco/tellr-videos/main/<chemin>`.

## État au 22/11/2026
- Phase TEST : produire des clips dans `clips/tests/`, NE RIEN PUBLIER, ne pas toucher à Zernio.
- Charte graphique PROVISOIRE (orange #FF6A1A, Inter Display). Mathieu dessine le logo : ne pas inventer de charte.
- Ne jamais toucher aux tâches, dépôts ou comptes de Tamko et de Partners in Vice.

## Installation (chaque exécution repart de zéro)
`pip install --break-system-packages -q yt-dlp faster-whisper numpy pillow` puis vérifier `ffmpeg` (sinon `apt-get install -y -q ffmpeg`).
Les polices Inter Display sont attendues dans /usr/share/fonts/opentype/inter (sinon les télécharger dans tools/fonts/).

## Sources
- SOURCE PRINCIPALE = release GitHub « sources » (vidéos officielles déposées par Mathieu, ex. Drive de la campagne Yomi Denzel). Lister : `curl -s https://api.github.com/repos/shinkoco/tellr-videos/releases/tags/sources` (champ assets[].name / browser_download_url), puis `curl -L -o src.mp4 <browser_download_url>`. Noter dans published.json la vidéo et les passages déjà utilisés pour ne jamais refaire le même moment. Le relais Mac (relay/) est une option, pas un prérequis.
- SOURCE N°1 = vidéos officielles du Drive de la campagne Yomi Denzel, relayées par le Mac. Liste : relay/drive_index.tsv (nom dans la release → chemin d'origine). Télécharger : `curl -L -o src.mp4 https://github.com/shinkoco/tellr-videos/releases/download/sources/<slug>.mp4`. Le dossier « Clips Interdits » du Drive est exclu : ne jamais utiliser ces passages, même trouvés ailleurs.
- YouTube est BLOQUÉ depuis les serveurs : ne pas télécharger YouTube directement. Passer par le RELAIS MAC (relay/INSTALL.md) :
  1. Trouver les vidéos via la recherche web (URL youtube.com/watch?v=…), les ajouter dans `relay/queue.txt`, commit + push.
  2. Le Mac les dépose dans la release « sources » (7 h et 19 h). Liste : relay/done.txt.
  3. Télécharger avec `curl -L -o src.mp4 https://github.com/shinkoco/tellr-videos/releases/download/sources/<id>.mp4`.
  4. Si une vidéo n'est pas encore relayée, prendre une autre déjà dans done.txt, ou attendre l'exécution suivante (le signaler dans le récap).
- `creators.json` : base des créateurs. Priorité 1 (campagne de clips) d'abord, puis 2, puis 3. Alterner hommes et femmes.
- Trouver la vidéo avec `yt-dlp "ytsearch10:<recherche>" --flat-playlist --print "%(id)s|%(channel)s|%(duration)s|%(title)s"`. Ne garder que la chaîne officielle de la personne ou d'un podcast/média sérieux, en français.
- Quand la chaîne exacte est confirmée, la noter dans creators.json (`chaine`, `verifie: true`).
- JAMAIS d'extraits d'émissions TV (M6, TF1, Canal+…), jamais de fan accounts, jamais de clips déjà montés par d'autres.
- Ne jamais republier un moment déjà publié : vérifier `published.json`.

## Fabrication d'un clip (60 à 90 s)
1. Récupérer la vidéo depuis la release « sources » (voir Sources), puis couper le segment avec ffmpeg.
2. Transcrire (faster-whisper `small`, int8, language="fr", word_timestamps=True).
3. Choisir un passage qui se suffit à lui-même (une idée, une histoire, une leçon), 60 à 90 s, coupé sur des fins de phrase.
4. Repérer le visage sur une image du segment pour le `crop` 9:16 si le cadrage centré coupe la personne.
5. Écrire `spec.json` (voir la docstring de `tools/make_tellr.py`) :
   - `hook` = une VRAIE phrase prononcée dans l'extrait, mot pour mot. Jamais inventée, jamais résumée entre guillemets.
   - `context` = une ligne écrite par TELLR (qui parle, pourquoi c'est intéressant). Factuelle.
   - `captions` = transcription fidèle, 3 à 6 mots par bloc, 1 mot-clé entre *astérisques* par bloc maximum.
   - `zooms` = 2 à 4 punch-ins sur les phrases fortes.
   - `takeaway` = la leçon reformulée par TELLR, sans promesse de gains.
6. Rendu : `python3 tools/make_tellr.py spec.json out.mp4`. Extraire 4 images (début, milieu, zoom, fin) et vérifier : texte lisible, visage non coupé, rien dans les 150 px de droite ni en bas sous la source.

## Règles éditoriales
- Citations fidèles : ne jamais couper une phrase si ça en change le sens. Personnalités controversées OK, légendes neutres (« Il affirme que… »).
- Toujours créditer l'invité et la source (à l'écran et dans la légende).
- Aucune promesse de gains, aucun conseil d'investissement présenté comme tel.
- Ne jamais laisser croire qu'un invité est partenaire de TELLR.

## Publication (plus tard, après validation de Mathieu)
- TikTok via Zernio en BROUILLON, 3 vidéos/jour maximum, espacées de 3 h. Légendes dans le HUB (hub/tellr.json), sans URL, 5 hashtags, jamais #shorts.
- Zernio : 3e compte payant (6 $/mois) — à connecter par Mathieu.
