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
- `creators.json` : base des créateurs. Priorité 1 (campagne de clips) d'abord, puis 2, puis 3. Alterner hommes et femmes.
- Trouver la vidéo avec `yt-dlp "ytsearch10:<recherche>" --flat-playlist --print "%(id)s|%(channel)s|%(duration)s|%(title)s"`. Ne garder que la chaîne officielle de la personne ou d'un podcast/média sérieux, en français.
- Quand la chaîne exacte est confirmée, la noter dans creators.json (`chaine`, `verifie: true`).
- JAMAIS d'extraits d'émissions TV (M6, TF1, Canal+…), jamais de fan accounts, jamais de clips déjà montés par d'autres.
- Ne jamais republier un moment déjà publié : vérifier `published.json`.

## Fabrication d'un clip (60 à 90 s)
1. Télécharger un segment : `yt-dlp --download-sections "*HH:MM:SS-HH:MM:SS" -f "best[height<=1080]" -o src.mp4 URL`.
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
