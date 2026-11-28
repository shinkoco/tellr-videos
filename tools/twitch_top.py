#!/usr/bin/env python3
"""Top clips Twitch FR hors jeu vidéo. Usage: twitch_top.py [LAST_DAY|LAST_WEEK] [FR|EN] [categorie]"""
import json, sys, urllib.request
period = sys.argv[1] if len(sys.argv) > 1 else "LAST_DAY"
lang = sys.argv[2] if len(sys.argv) > 2 else "FR"
cats = sys.argv[3:] or ["Just Chatting", "Talk Shows & Podcasts", "Special Events", "Politics", "Sports", "Music", "Food & Drink", "IRL",
    "Travel & Outdoors", "Tabletop RPGs", "Chess", "Art", "Animals, Aquariums, and Zoos", "Makers & Crafting", "Science & Technology"]
def gql(q):
    r = urllib.request.Request("https://gql.twitch.tv/gql", json.dumps({"query": q}).encode(), {"Client-Id": "kimne78kx3ncx6brgo4mv6wki5h1ko"})
    return json.load(urllib.request.urlopen(r, timeout=30))
for c in cats:
    q = '''query{game(name:"%s"){name clips(first:25,criteria:{period:%s,languages:[%s],sort:VIEWS_DESC}){edges{node{slug title viewCount durationSeconds createdAt broadcaster{displayName} videoOffsetSeconds video{id}}}}}}''' % (c, period, lang)
    try: d = gql(q)
    except Exception as e: print("ERR", c, e); continue
    g = (d.get("data") or {}).get("game")
    if not g: print("--", c, d.get("errors")); continue
    for e in (g.get("clips") or {}).get("edges",[]):
        n = e["node"]
        print(f'{n["viewCount"]:>7} | {n["durationSeconds"]:>4.0f}s | {n["broadcaster"]["displayName"]:<18} | {g["name"]} | {n["slug"]} | {n["title"]}')
