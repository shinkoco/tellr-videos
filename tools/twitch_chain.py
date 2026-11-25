import json,urllib.request
def gql(q):
    r=urllib.request.Request("https://gql.twitch.tv/gql",json.dumps({"query":q}).encode(),{"Client-Id":"kimne78kx3ncx6brgo4mv6wki5h1ko"})
    return json.load(urllib.request.urlopen(r,timeout=30))
for login in ["kamet0","jltomy","anyme023","youladecadd","domingo","michou","helydia","squeezie","gotaga","zerator","inoxtag","mister_mv","lestream"]:
    try: d=gql('query{user(login:"%s"){clips(first:100,criteria:{period:LAST_WEEK,sort:VIEWS_DESC}){edges{node{slug title viewCount durationSeconds videoOffsetSeconds game{name} video{id}}}}}}'%login)
    except Exception as e: print(login,e); continue
    u=d["data"]["user"]
    if not u: continue
    cl=[e["node"] for e in u["clips"]["edges"] if e["node"]["video"]]
    cl=[n for n in cl if (n["game"] or {}).get("name") in ("Just Chatting","IRL","Special Events","Talk Shows & Podcasts",None)]
    byv={}
    for n in cl: byv.setdefault(n["video"]["id"],[]).append(n)
    for v,l in byv.items():
        l.sort(key=lambda n:n["videoOffsetSeconds"])
        for i,a in enumerate(l):
            for b in l[i+1:]:
                gap=b["videoOffsetSeconds"]-(a["videoOffsetSeconds"]+a["durationSeconds"])
                if -30<=gap<=8 and a["viewCount"]+b["viewCount"]>=300:
                    print(login,v,a["viewCount"],a["durationSeconds"],a["videoOffsetSeconds"],a["slug"],"|",a["title"][:30],"->",b["viewCount"],b["durationSeconds"],b["videoOffsetSeconds"],b["slug"],"|",b["title"][:30],"gap",gap)
