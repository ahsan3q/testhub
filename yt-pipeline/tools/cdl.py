# Wikimedia Commons video downloader (CC/PD licensed). usage: cdl.py "File:Name.webm" outdir  -> prints "outdir/file NN MB"
import sys, json, os, urllib.request, urllib.parse, subprocess, time
UA = {"User-Agent": "research-script/1.0"}
def fetch(url, t=60):
    for i in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=t).read()
        except Exception as e:
            err = e; time.sleep(20 * (i + 1))
    raise err
t, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
u = "https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata&format=json&titles=" + urllib.parse.quote(t)
p = next(iter(json.loads(fetch(u))["query"]["pages"].values()))
ii = p["imageinfo"][0]; lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "?")
raw = f"{out}/commons_{abs(hash(t)) % 10**8}.src"; dst = raw[:-4] + ".mp4"
open(raw, "wb").write(fetch(ii["url"], 300))
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-an", dst], check=True); os.remove(raw)
open(f"{out}/licenses.txt", "a").write(f"{t}\t{lic}\t{ii.get('descriptionurl')}\n")
print(f"{dst} {os.path.getsize(dst) // 2**20} MB")
