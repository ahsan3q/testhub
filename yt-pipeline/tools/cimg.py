# Commons still finder: cimg.py outdir KEY "search terms" ... -> downloads first freely-licensed jpg/png per key, makes slow-zoom 30s clip KEY_still.mp4
import sys, json, time, urllib.request, urllib.parse, subprocess, os
UA={"User-Agent":"research-script/1.0"}
def get(u):
    for i in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))
        except Exception as e: time.sleep(15*(i+1)); err=e
    raise err
out=sys.argv[1]; os.makedirs(out,exist_ok=True); args=sys.argv[2:]
OK=("CC BY","CC0","Public domain","CC BY-SA","PD")
def one(k,q):
    if os.path.exists(f"{out}/{k}_still.mp4"): return
    for _ in range(6):
        s=get("https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&format=json&srlimit=8&srsearch="+urllib.parse.quote(q))
        if "query" in s: break
        time.sleep(40)
    else:
        print(k,"FAILED",q,flush=True); return
    done=False
    for r in s["query"]["search"]:
        t=r["title"]
        if not t.lower().endswith((".jpg",".jpeg",".png")): continue
        time.sleep(4)
        pj=get("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata|size&iiurlwidth=1280&format=json&titles="+urllib.parse.quote(t))
        if "query" not in pj: time.sleep(30); continue
        p=next(iter(pj["query"]["pages"].values()))
        ii=p["imageinfo"][0]; lic=ii.get("extmetadata",{}).get("LicenseShortName",{}).get("value","")
        if not lic.startswith(OK) or ii.get("width",0)<800: continue
        img=f"{out}/{k}.jpg"; time.sleep(3)
        data=None
        for i in range(5):
            try: data=urllib.request.urlopen(urllib.request.Request(ii.get("thumburl") or ii["url"],headers=UA),timeout=60).read(); break
            except Exception: time.sleep(30*(i+1))
        if not data: continue
        open(img,"wb").write(data)
        artist=ii.get("extmetadata",{}).get("Artist",{}).get("value","")
        open(f"{out}/licenses.txt","a").write(f"{k}\t{t}\t{lic}\t{ii.get('descriptionurl')}\t{artist[:120]}\n")
        subprocess.run(["ffmpeg","-v","error","-y","-loop","1","-i",img,"-t","30","-filter_complex",
          "[0:v]scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,gblur=sigma=20,eq=brightness=-0.15[bg];[0:v]scale=-2:720[fg];[bg][fg]overlay=(W-w)/2:0,zoompan=z='1+0.0008*on':d=1:s=1280x720:fps=25",
          "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",f"{out}/{k}_still.mp4"],check=True)
        print(k,t,lic,flush=True); done=True; break
    if not done: print(k,"NONE",q,flush=True)
    time.sleep(5)

for k,q in zip(args[::2],args[1::2]):
    try: one(k,q)
    except Exception as e: print(k,"ERROR",repr(e)[:150],flush=True); time.sleep(60)
