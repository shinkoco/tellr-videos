#!/usr/bin/env python3
"""Top clips par créateur, hors jeu vidéo. Usage : twitch_creators.py [LAST_DAY|LAST_WEEK] [vues_min]
Liste blanche de catégories : tout ce qui n'y figure pas (jeux) est écarté."""
import json, sys, urllib.request
period = sys.argv[1] if len(sys.argv) > 1 else "LAST_WEEK"
mini = int(sys.argv[2]) if len(sys.argv) > 2 else 50
OK = {"Just Chatting", "IRL", "Talk Shows & Podcasts", "Special Events", "Sports", "Politics", "Music", "Food & Drink",
      "Travel & Outdoors", "Art", "Makers & Crafting", "Science & Technology", "Animals, Aquariums, and Zoos",
      "Fitness & Health", "Tabletop RPGs", "Chess", "Software and Game Development"}
LOGINS = """squeezie michou inoxtag domingo zerator kamet0 etoiles mistermv joueur_du_grenier antoinedaniel jeanmassiet
hugodecrypte samueletienne ponce angledroit bagherajones ultia aminematue gotaga rivenzi sardoche zacknani wankilstudio
laink maximebiaggi doigby clemquicourt zawa_prod wissksrr mastu jltomy anyme023 littlebigwhale brucegrannec lefrenchie
trinity maghla hortyunderscore deujna joyca byilhann alphacast mynthos billy lebouseuh potatozsh sylvainlevy
chesscomfr djilsi nico_la theguill84""".split()
def gql(q):
    r = urllib.request.Request("https://gql.twitch.tv/gql", json.dumps({"query": q}).encode(), {"Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko"})
    return json.load(urllib.request.urlopen(r, timeout=30))
rows = []
for l in LOGINS:
    try:
        d = gql('query{user(login:"%s"){displayName clips(first:100,criteria:{period:%s,sort:VIEWS_DESC}){edges{node{slug title viewCount durationSeconds game{name}}}}}}' % (l, period))
        u = (d.get("data") or {}).get("user")
        for e in ((u or {}).get("clips") or {}).get("edges", []):
            n = e["node"]; g = (n.get("game") or {}).get("name")
            if g in OK and n["viewCount"] >= mini:
                rows.append((n["viewCount"], n["durationSeconds"], u["displayName"], g, n["slug"], n["title"]))
    except Exception as ex:
        print("ERR", l, ex, file=sys.stderr)
for v, s, who, g, slug, t in sorted(rows, reverse=True):
    print(f"{v:>7} | {s:>4.0f}s | {who:<18} | {g} | {slug} | {t}")
