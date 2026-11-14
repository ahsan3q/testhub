# Free YouTube transcript + channel video list via public Invidious instances (no vidIQ credits).
# usage:
#   ytx.py transcript <videoId> [lang]      -> prints "[mm:ss] text" lines
#   ytx.py popular <channelId|@handle> [n]  -> prints "views  videoId  title" (most popular)
import sys, json, re, urllib.request, urllib.parse

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
FALLBACK = ["yt.chocolatemoo53.com", "inv.nadeko.net", "invidious.nerdvpn.de", "yewtu.be",
            "invidious.privacyredirect.com", "iv.melmac.space", "inv.tux.pizza"]

def get(url, t=40):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read().decode("utf-8", "ignore")

def instances():
    hosts = []
    try:
        d = json.loads(get("https://api.invidious.io/instances.json?sort_by=health", 20))
        hosts = [x[0] for x in d if x[1].get("api") and x[1].get("type") == "https"]
    except Exception:
        pass
    return hosts + [h for h in FALLBACK if h not in hosts]

def vtt_to_text(vtt):
    auto = "<c>" in vtt
    out, last_t, prev = [], -99, ""
    for block in vtt.split("\n\n"):
        lines = block.strip().split("\n")
        m = re.match(r"(\d+):(\d+):(\d+)\.\d+ -->", lines[0]) if lines else None
        if not m:
            continue
        sec = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3])
        body = lines[1:]
        if auto:
            body = [l for l in body if "<c>" in l or re.search(r"<\d+:\d+", l)]
        txt = " ".join(re.sub(r"<[^>]+>", "", l).strip() for l in body).strip()
        if not txt or txt == prev:
            continue
        prev = txt
        if sec - last_t >= 15:
            out.append(f"\n[{sec // 60}:{sec % 60:02d}] "); last_t = sec
        out.append(txt + " ")
    return re.sub(r" +", " ", "".join(out)).strip()

def transcript(vid, lang="en"):
    for h in instances():
        try:
            v = get(f"https://{h}/api/v1/captions/{vid}?lang={lang}", 45)
            if v.startswith("WEBVTT") and len(v) > 200:
                return vtt_to_text(v), h
        except Exception:
            continue
    raise SystemExit("no instance returned captions")

def popular(ch, n=30):
    for h in instances():
        try:
            cid = ch
            if ch.startswith("@"):
                cid = json.loads(get(f"https://{h}/api/v1/resolveurl?url=" + urllib.parse.quote("https://www.youtube.com/" + ch)))["ucid"]
            d = json.loads(get(f"https://{h}/api/v1/channels/{cid}/videos?sort_by=popular", 45))
            vids = d.get("videos", d) if isinstance(d, dict) else d
            if vids:
                return [(v.get("viewCount", 0), v["videoId"], v["title"]) for v in vids[:n]], h
        except Exception:
            continue
    raise SystemExit("no instance returned the channel list")

if __name__ == "__main__":
    if sys.argv[1] == "transcript":
        t, h = transcript(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "en")
        print(f"# via {h}\n{t}")
    elif sys.argv[1] == "popular":
        rows, h = popular(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 30)
        print(f"# via {h}")
        for r in rows: print(f"{r[0]:>9}  {r[1]}  {r[2]}")
