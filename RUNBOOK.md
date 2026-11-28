# TELLR — runbook

Chaîne TikTok **TELLR** (@tellr_fr). Signature : **« TELLR. Le live, raconté. »**
Bio : « Le live, raconté. / Les moments forts des créateurs, en 90 secondes. »

## LIGNE ÉDITORIALE (décidée le 23/11/2026 — fait foi, remplace l'ancienne idée « clips d'entrepreneurs »)
- Le meilleur du live, jeu vidéo compris QUAND C'EST UNE RÉACTION (règle du 28/11, voir CATALOGUE ÉLARGI) : moments drôles, clashs, débats, réactions à l'actu, histoires racontées en live,
  et une catégorie « argent et business » (revenus, marques, deals des streamers, entrepreneurs invités).
- Source = Twitch (seule plateforme vidéo accessible en autonomie, avec Kick à tester). YouTube, TikTok, Instagram : bloqués.
- Français en priorité ; au maximum 1 clip anglais par jour, sous-titré en français.
- DEUX FILTRES obligatoires :
  1. Demande : le clip est dans le haut de `python3 tools/twitch_top.py LAST_WEEK FR` (ou LAST_DAY) — le public l'a déjà clippé et regardé.
  2. Intérêt : après transcription, garder uniquement s'il y a un vrai enjeu (chute drôle, info, chiffre fort, clash, retournement). Sinon, jeter.
  Les clips d'une même séquence (ex. « … 1 », « … 2 », « … 3 ») peuvent être assemblés dans l'ordre pour raconter l'histoire complète.
- Exclure : gameplay pur (sans réaction), contenu sexuel, haine, harcèlement, mineurs mis en cause, drames privés, accusations non prouvées.

## CHARTE (validée le 24/11/2026)
- Couleurs : orange #EF4A23, crème #FFF6EC, encre #1A1A1A. Logo « TellR » + bulle à coins coupés : tools/brand/ (tellr_brand.json + SVG).
- Accroche (0-3 s) : phrase choc dans une GRANDE BULLE ORANGE, texte crème, ligne du haut « NOM · CATÉGORIE » (nom crème, catégorie noire). Toujours dans la zone de sécurité (haut 150 px, côtés 60 px).
- Pendant le clip : badge TellR en haut à droite, crédit « Streamer · Twitch » en haut à gauche, sous-titres en pastille crème avec mot-clé orange.
- Fin : UNIQUEMENT l'écran orange (« À retenir », badge crème + slogan, « Abonne-toi pour la suite »). L'écran crème est abandonné.
- Une seule police (Inter Display) pour tous les textes hors logo.

## RÈGLES DES TEXTES (définitives)
- Bandeau d'ouverture : citation EXACTE prononcée dans l'extrait. Jamais réécrite pour faire cliquer.
- Ligne de contexte : facultative, factuelle, sans exagération ni formule « piège à clics ».
- Noms de marques : la boisson de DJ Snake s'écrit « Oui » (jamais « Wee », erreur de transcription). Vérifier l'orthographe de toute marque citée.
- Sous-titres : fidèles aux propos, sans déformation du sens. Corriger les erreurs évidentes de transcription ; en cas de doute sur un nom propre (marque, personne), ne pas l'écrire.
- Carte de fin « À retenir » : la morale ou la leçon, reformulée par TELLR, + « TELLR. Le live, raconté. ». Aucune autre accroche.
- Toujours créditer le streamer et la plateforme (« Source : Michou · Twitch »). Retrait immédiat si un streamer le demande.

Exemple de référence : clips/tests/tellr_test2_michou.mp4 (+ .json = spec complète).

## CATALOGUE ÉLARGI (demandé par Mathieu le 28/11/2026 — fait foi)
- Raison : la demande est faible sur le périmètre habituel. On élargit les sujets.
- JEU VIDÉO AUTORISÉ pour les RÉACTIONS (rire, surprise, rage, débat, annonce, avis, histoire racontée). Le gameplay pur (action ou performance sans réaction qui porte le moment) reste exclu. Test : sans les images du jeu, le moment garde-t-il son intérêt par ce que dit ou vit le streamer ? Au montage, garder le visage du streamer bien visible (facecam).
- Un autre compte (Partners in Vice) publie du GTA 6 : avant de choisir un clip GTA, lister les posts Zernio (lecture seule) et ne jamais reprendre un moment qu'il a déjà publié ou programmé. Ne jamais modifier ses posts.
- Sujets bienvenus en plus : sport et débriefs de matchs, voyage et IRL, insolite et animaux, cuisine, culture (cinéma, séries, musique, manga), tech, art et création, coulisses de créateurs, jeux de plateau et JdR en émission, échecs (actu et réactions, pas la partie pure).
- Recherche à chaque passage : `tools/twitch_top.py` (catégories élargies) ET `tools/twitch_creators.py LAST_WEEK` (clips par créateur ; compléter sa liste LOGINS avec les nouveaux créateurs repérés). Un même clip peut sortir des deux : vérifier published.json.
- Les DEUX filtres (demande + intérêt après transcription) et les autres exclusions ne changent pas. Regarder aussi les images et écouter : la catégorie Twitch ne suffit pas à trancher entre réaction et gameplay.

---
## TOUT EN AUTOMATIQUE (confirmé par Mathieu le 26/11/2026 — fait foi)
- Plus AUCUN brouillon à publier à la main : chaque vidéo est programmée en publication automatique (draft false, jamais isDraft).
- Mathieu n'a aucune action de publication à faire : ne jamais lui demander de publier, coller une légende ou ajouter un son.
- Si la programmation échoue : réessayer, sinon le signaler dans les alertes du HUB. Ne JAMAIS se rabattre sur un brouillon.
- La charte validée ci-dessus s'applique. Ne jamais toucher aux tâches, dépôts ou comptes de Tamko et de Partners in Vice.

## Installation (chaque exécution repart de zéro)
`pip install --break-system-packages -q yt-dlp faster-whisper numpy pillow cairosvg` puis vérifier `ffmpeg` (sinon `apt-get install -y -q ffmpeg`).
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

## Publication (active depuis le 25/11/2026)
- 1er jour (25/11) : le clip 12:30 = clips/tests/tellr_test2_michou.mp4 (Michou · Oui de DJ Snake, déjà validé par Mathieu, l'ajouter à published.json). Les 2 autres sont produits normalement.
- TikTok @tellr_fr via Zernio, compte `6b060a9242fa5702dd3fa8a5`. NE JAMAIS publier sur Tamko (`6af7635df038e4d78c1b8569`) ni Partners in Vice (`6afc525031be0a779a30b36e`), qui sont sur le même Zernio.
- 3 vidéos/jour MAX, PUBLICATION AUTOMATIQUE (décidé par Mathieu le 25/11 : les brouillons n'arrivent pas) : posts programmés directement à 12:30, 18:30 et 21:30 (Europe/Paris), PAS de brouillon.
- tiktok_settings : {"draft": false, "privacyLevel": "PUBLIC_TO_EVERYONE", "allowComment": true, "allowDuet": true, "allowStitch": true, "contentPreviewConfirmed": true, "expressConsentGiven": true}. Vidéo = URL raw GitHub du fichier poussé dans clips/AAAA-MM-JJ/.
- La légende va dans le contenu du post (content). Ne PAS remplir channel.drafts dans hub/tellr.json (supprimer la clé : même une liste vide affiche la carte « Brouillons »). Légende : 1 phrase + « 🎥 <Streamer> en live sur Twitch » + 5 hashtags (dont #tellr), sans URL, jamais #shorts.
- Avant d'envoyer, lister les posts Zernio du compte TELLR : ne jamais programmer 2 posts pour le même créneau.
- Retour d'expérience Partners in Vice (22/11) : les gens décrochent vite. Ouvrir sur la phrase choc (le bandeau la porte), couper TOUS les temps morts, viser 61-75 s. Plafond ABSOLU : 90 s (promesse de la bio « en 90 secondes »), jamais au-delà, écran de fin compris.

## HUB
- Écrire hub/tellr.json (format de https://github.com/studiomgi/studiomgi.github.io/blob/main/HUB.md) : planning du jour, stats TikTok (Zernio analytics du compte TELLR, 1 appel), alertes préfixées « TELLR : ». La page studiomgi.github.io affiche l'onglet TELLR automatiquement.

## RÈGLES AJOUTÉES LE 25/11/2026 (demande de Mathieu — font foi)
- TOUJOURS 3 clips par jour. Ne jamais conclure « pas assez de bons moments » : une journée calme se compense en élargissant la recherche (LAST_WEEK, plus de catégories : Just Chatting, IRL, Talk Shows, Special Events, Sports, Music), en prenant des moments moins viraux mais intéressants, et en CHAÎNANT des clips contigus d'un même direct (tools/twitch_chain.py ; alignement par les mots, recouvrement possible entre clips).
- Durée MINIMUM 61 s (vidéo finale, écran de fin compris), plafond 90 s. Un clip Twitch fait 60 s max : prendre le clip entier + écran de fin (end_secs 4-5) ou chaîner deux clips.
- Outils : tools/twitch_top.py (liste), tools/twitch_dl.py tag=slug (téléchargement signé), tools/twitch_chain.py (clips contigus), tools/transcribe_words.py (mots horodatés ; faster-whisper reçoit un tableau numpy via ffmpeg). make_tellr.py : lancer en arrière-plan (nohup), ~2 min.
- ESPORT = catégorie à part entière (décidé par Mathieu le 25/11) : grosse actualité à sortir (transferts, annonces, clubs, résultats, réactions). Afficher « Esport » dans la bulle. Seul le gameplay pur reste exclu.

- Format HUB (vérifié sur index.html) : today = [{time, platform:"TikTok", title, status:"programmé"}] (PAS « text »). Pas de clé channel.drafts (publication automatique).

- ZONE DE SÉCURITÉ EN LIGNE (corrigée le 25/11 après capture de Mathieu : la barre « Rechercher » TikTok recouvrait le haut) : haut 300 px, côtés 120 px, bas 420 px. tools/make_tellr.py (SAFE_T/L/R) est déjà réglé ; vérifier les 4 images avec cette marge.

## HUB v2 : stats (à remplir à chaque passage, dans hub/tellr.json → "channel")
Principe : peu de stats, seulement celles qui disent si la chaîne grandit et ce que les gens veulent voir. Pas d'Instagram, pas de stats décoratives.
- Ne plus remplir kpis, engagement, best_time, keywords, followers. Garder today, warmup, upcoming, alerts.
- "growth" : followers (Zernio accounts_get_follower_stats, compte 6b060a9242fa5702dd3fa8a5), goal 1000, followers_delta (écart avec J-7), followers_note (phrase courte), views_7d et views_prev_7d (analytics_get_daily_metrics, attribution received), avg_views (vues moyennes par vidéo), avg_watch (moyenne de igReelsAvgWatchTime/1000 dans analytics_get_analytics, en secondes), avg_note. Pas de YouTube pour TELLR, donc pas de champs yt_*.
- "insights" : groups_title « Par streamer » ; streamers [{label, value, detail:"n clips"}] triés par vues moyennes décroissantes ; formats [{label, value, detail}] (court 61-70 s vs long 71-90 s, avec temps regardé et % vu en entier = completionRate) ; slots [{label:"12:30", value, detail, group:1}] en heure de Paris ; takeaways = 3 à 4 DÉCISIONS (garder / arrêter / tester), signaler si l'échantillon est trop petit (< 9 vidéos) ; top = 3 meilleures vidéos [{title, views, detail}].
- "trend" : 7 derniers jours glissants, labels "jj/mm", series.TikTok = vues par jour (recalculé à chaque passage).
- Ne jamais inventer de chiffre : si Zernio n'a pas encore synchronisé, mettre 0/null et le dire dans la note.
