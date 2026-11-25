import json,urllib.request,sys,subprocess,urllib.parse
def gql(q):
    r=urllib.request.Request("https://gql.twitch.tv/gql",json.dumps({"query":q}).encode(),{"Client-Id":"kimne78kx3ncx6brgo4mv6wki5h1ko"})
    return json.load(urllib.request.urlopen(r,timeout=30))
for tag,slug in [a.split("=") for a in sys.argv[1:]]:
    d=gql('query{clip(slug:"%s"){videoQualities{sourceURL quality} playbackAccessToken(params:{platform:"web",playerType:"site"}){value signature}}}'%slug)["data"]["clip"]
    qs=d["videoQualities"]; u=[q for q in qs if q["quality"]=="1080"] or qs
    t=d["playbackAccessToken"]
    url=u[0]["sourceURL"]+"?sig="+t["signature"]+"&token="+urllib.parse.quote(t["value"])
    subprocess.run(["curl","-sL","-o",tag+".mp4",url])
