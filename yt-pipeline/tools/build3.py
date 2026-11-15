"""Engine v3 — documentary-style render from script.json + vo/NN.mp3 (+ vo/NN.json word timings).
usage: build3.py <project_dir> <sources.json>

Automatic: mood detection per segment -> grade, transition, music level, speed ramps;
compositions (card / tv / full-bleed / 2.5D parallax), karaoke subtitles with keyword
highlight, kinetic keyword pop-ups, cold-open title, light leaks, vignette, grain,
J-cuts, meaningful pauses, VO cleanup chain, music ducking, SFX layer (whoosh/riser/hit/click/pop/ambient).

Manual controls (optional, per segment in script.json):
  "mood": "informative|exciting|suspense|drama"   override detected mood
  "transition": "punch|flash|whip|dip|cut"        override transition into the segment
  "layout": "card|tv|full|count"                  override composition
  "speed": "normal|ramp|slow"                     override speed treatment of its clips
  "parallax": true/false                          force / forbid a 2.5D still at segment start
  "subs": false                                   hide subtitles for the segment
  "popup": "TEXT" | false                         kinetic pop-up text (default = "cap")
  "pause": 0.6                                    extra silence after the segment
Global (optional) <project>/edit.json:
  {"subs": true, "popups": true, "grade": true, "music": 0.20, "parallax_every": 4,
   "title_hook": true, "vignette": true, "leaks": true}
Timeline: the computed plan is written to build/timeline.json; to edit clips/timing by hand,
copy it to <project>/timeline.json, change entries (src/start/d/layout/speed/transition) and re-run.
"""
import json, os, sys, random, subprocess, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont, ImageFilter

P = sys.argv[1]; SRC = json.load(open(sys.argv[2]))
T = os.path.dirname(os.path.abspath(__file__)); A = f"{T}/assets"; FONT = f"{T}/fonts"
W, H, FPS = 1920, 1080, 30
MAXSHOT = 3.6
random.seed(11)
seg = json.load(open(f"{P}/script.json"))
meta = json.load(open(f"{P}/meta.json")) if os.path.exists(f"{P}/meta.json") else {}
ED = dict(subs=True, popups=True, grade=True, music=0.20, parallax_every=4, title_hook=True, vignette=True, leaks=True)
if os.path.exists(f"{P}/edit.json"): ED.update(json.load(open(f"{P}/edit.json")))
B = f"{P}/build3"; os.makedirs(f"{B}/shots", exist_ok=True); os.makedirs(f"{B}/ovl", exist_ok=True)

def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

# ---------------- mood detection ----------------
KW = {
    "drama": ["murió", "muerte", "murieron", "muere", "cáncer", "trágic", "tragedia", "adicción", "coma", "hospital", "llorar", "lágrima",
              "despid", "quiebra", "cerró", "derrumb", "triste", "dolor", "perdió", "fracaso", "cancelad", "enfermo", "funeral", "suicid"],
    "suspense": ["secreto", "misterio", "nadie sabe", "rumor", "verdad", "pero aquí", "en realidad", "falso", "oculto", "escondid",
                 "veneno", "cianuro", "peligro", "tóxic", "demanda", "arresto", "polic", "espía", "nunca", "mentira", "prohib"],
    "exciting": ["récord", "éxito", "millones", "ganó", "óscar", "campeón", "famos", "estrella", "explot", "increíble", "número uno",
                 "primer lugar", "fenómeno", "triunf", "estreno", "premio", "emmy", "globo de oro", "gigante", "rápid"],
}
def detect(txt):
    t = txt.lower(); sc = {m: sum(t.count(k) for k in ks) for m, ks in KW.items()}
    m = max(sc, key=sc.get)
    return m if sc[m] > 0 else "informative"

MOOD = {
    "informative": dict(grade="eq=contrast=1.05:saturation=1.08,colorbalance=rh=0.03:bh=-0.03", trans="punch", music=1.0, speed="normal"),
    "exciting":    dict(grade="eq=contrast=1.10:saturation=1.25,colorbalance=rs=0.04:rh=0.05:bh=-0.05", trans="flash", music=1.3, speed="ramp"),
    "suspense":    dict(grade="eq=contrast=1.12:brightness=-0.03:saturation=0.92,colorbalance=rs=-0.07:bs=0.09:rh=0.07:bh=-0.07", trans="whip", music=0.85, speed="normal"),
    "drama":       dict(grade="eq=contrast=1.04:brightness=-0.03:saturation=0.70,colorbalance=bs=0.06:bm=0.04", trans="dip", music=0.6, speed="slow"),
}

# ---------------- sources ----------------
info = {}
for k, f in SRC.items():
    d = dur(f)
    out = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(d * 0.4), "-i", f, "-t", "20", "-vf", "cropdetect=24:2:0", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"crop=(\d+:\d+:\d+:\d+)", out)
    hh = int(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=height", "-of", "csv=p=0", f]).decode().split()[0] or 0)
    info[k] = dict(f=f, d=d, crop=m[-1] if m else None, h=hh)

# ---------------- overlays (label pill + countdown) ----------------
F_LAB = ImageFont.truetype(f"{FONT}/ArchivoBlack-Regular.ttf", 34)
F_NUM = ImageFont.truetype(f"{FONT}/AlfaSlabOne-Regular.ttf", 230)
F_NAME = ImageFont.truetype(f"{FONT}/AlfaSlabOne-Regular.ttf", 70)
GOLD = (242, 182, 50, 255); CREAM = (245, 230, 200, 255)
TVW, TVH, SX, SY, SW, SH = map(int, open(f"{A}/tv_geom.txt").read().split())
LAYOUTS = {
    "card":  dict(x=370, y=98, w=1180, h=885, mask="card"),
    "tv":    dict(x=210 + SX, y=40 + SY, w=SW, h=SH, tv=(210, 40)),
    "count": dict(x=900, y=210, w=880, h=660, mask="cardsm"),
    "full":  dict(x=0, y=0, w=W, h=H, full=True),
}
def wrap(text, font, maxw, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur); return lines
def overlay(i, s, L):
    p = f"{B}/ovl/{i:02d}_{'full' if L.get('full') else L.get('mask', 'tv')}.png"
    if os.path.exists(p): return p
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    cap = s.get("cap", "")
    if cap.startswith("#"):
        name = s["label"].split("·")[0].strip()
        d.text((130, 250), cap, font=F_NUM, fill=GOLD, stroke_width=6, stroke_fill=(20, 15, 10, 255))
        for j, ln in enumerate(wrap(name, F_NAME, 680, d)):
            d.text((140, 560 + j * 88), ln, font=F_NAME, fill=CREAM, stroke_width=4, stroke_fill=(20, 15, 10, 255))
    if s.get("label"):
        lb = s["label"]; tw = d.textlength(lb, font=F_LAB)
        x0, y0 = (60, 54) if L.get("full") else (L["x"] + 22, L["y"] + 20)
        d.rounded_rectangle([x0, y0, x0 + tw + 40, y0 + 58], 12, fill=GOLD)
        d.text((x0 + 20, y0 + 9), lb, font=F_LAB, fill=(25, 20, 12, 255))
    img.save(p); return p

# ---------------- timeline ----------------
GAP = 0.40
plan, t0 = [], 0.0
for i, s in enumerate(seg):
    vo = f"{P}/vo/{i:02d}.mp3"; vd = dur(vo)
    mood = s.get("mood") or detect(s["txt"]); s["_mood"] = mood
    cd = s.get("cap", "").startswith("#")
    extra = 1.1 if cd else 0            # room for riser + reveal
    pause = s.get("pause", 0.5 if mood == "drama" else 0)
    sd = vd + GAP + extra + pause
    layout = s.get("layout") or ("count" if cd else ["card", "tv", "full", "card", "full", "tv"][i % 6])
    trans = s.get("transition") or MOOD[mood]["trans"]
    speed = s.get("speed") or MOOD[mood]["speed"]
    spec = s["src"] if isinstance(s["src"], list) else [s["src"]]
    keys = []
    for sp in spec:
        if "@" in sp:
            k, r = sp.split("@"); a, b = r.split("-"); keys.append((k, (float(a), float(b))))
        else: keys.append((sp, None))
    used, items = 0.0, []
    if s.get("fx"):
        fxd = sd if s["fx"].get("full") or sd < 6.5 else min(sd - 2.5, s["fx"].get("dur", 4.8))
        items.append(dict(fx=s["fx"], d=fxd)); used = fxd
    elif not cd and (s.get("parallax") or (s.get("parallax") is None and ED["parallax_every"] and i % 2 == 1 and sd > 5)):
        items.append(dict(parallax=True, d=min(3.4, sd - 1.5))); used = items[-1]["d"]
    rest = sd - used
    n = 0 if rest < 0.5 else max(1, round(rest / 3.0)); shots = [rest / n] * n if n else []
    while shots and max(shots) > MAXSHOT: n += 1; shots = [rest / n] * n
    for j, sh in enumerate(shots): items.append(dict(d=sh))
    for j, it in enumerate(items):
        k, rng = keys[j % len(keys)] if len(keys) > 1 and all(r for _, r in keys) else random.choice(keys); I = info[k]
        lo, hi = (rng[0], min(rng[1], I["d"] - 0.4)) if rng else (min(25, I["d"] * 0.1), max(I["d"] - 30, I["d"] * 0.6))
        sp_ = speed if (speed != "ramp" or random.random() < 0.45) else "normal"
        need = it["d"] * {"normal": 1.0, "ramp": 1.45, "slow": 0.8}[sp_]
        start = random.uniform(lo, max(lo, min(hi - need, I["d"] - need - 0.4)))
        lay = layout if (j == 0 or cd or s.get("layout")) else ["full", layout, ("tv" if layout == "card" else "card")][j % 3]
        if lay == "full" and I["h"] < 400: lay = "card"     # low-res sources look bad full-bleed
        plan.append(dict(seg=i, j=j, src=k, start=round(start, 2), d=round(it["d"], 3), layout=lay, mood=mood,
                         transition=(trans if j == 0 else "cut"), speed=sp_, fx=it.get("fx"), parallax=it.get("parallax", False),
                         keys=keys, zoomin=random.random() < 0.65, pan=random.choice([-1, 0, 1]),
                         leak=(ED["leaks"] and j == 0 and mood in ("exciting", "informative") and i % 3 == 0)))
    s["_t0"], s["_vo"], s["_extra"], s["_sd"] = t0, vo, extra, sd
    t0 += sd
TOTAL = t0
if os.path.exists(f"{P}/timeline.json"):           # manual timeline override
    plan = json.load(open(f"{P}/timeline.json")); print("using manual timeline.json")
json.dump(plan, open(f"{B}/timeline.json", "w"), ensure_ascii=False, indent=0)
print(f"timeline {TOTAL:.1f}s, {len(plan)} shots, moods:", {m: sum(1 for s in seg if s['_mood'] == m) for m in MOOD})

sys.path.insert(0, T); import fx as FX

def still(I, t, path, width=1920):
    if not os.path.exists(path):
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", I["f"], "-frames:v", "1", "-vf",
                        (f"crop={I['crop']}," if I["crop"] else "") + f"scale={width}:-2", path])
    return path

def trans_filters(p, D):
    tr, out = p["transition"], ""
    if tr == "flash": out += ",eq=brightness='0.45*max(0,1-t/0.2)':eval=frame,gblur=sigma=16:enable='lt(t,0.08)'"
    elif tr == "whip": out += ",gblur=sigma=28:steps=2:enable='lt(t,0.12)'"
    elif tr == "dip": out += ",fade=in:st=0:d=0.4"
    return out

def render_parallax(k, p):
    out = f"{B}/shots/{k:04d}.mp4"; I = info[p["src"]]; D = p["d"]
    base = still(I, p["start"] + 0.5, f"{B}/ovl/plx_{k:04d}.jpg")
    fgp = f"{B}/ovl/plx_{k:04d}.png"
    if not os.path.exists(fgp):
        try:
            from rembg import remove
            fg = remove(Image.open(base).convert("RGB"))
            cov = sum(1 for a in fg.getchannel("A").resize((96, 54)).getdata() if a > 128) / (96 * 54)
            if not (0.04 < cov < 0.7): raise ValueError("bad mask")
            fg.save(fgp)
        except Exception:
            fgp = None
    ov = overlay(p["seg"], seg[p["seg"]], LAYOUTS["full"])
    g = MOOD[p["mood"]]["grade"] if ED["grade"] else "null"
    if fgp:
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", f"{D}", "-i", base, "-loop", "1", "-t", f"{D}", "-i", fgp, "-loop", "1", "-t", f"{D}", "-i", ov,
               "-filter_complex",
               f"[0:v]scale=2300:-2,crop=2200:1238,gblur=sigma=7,eq=brightness=-0.06[b0];"
               f"[b0]crop={W}:{H}:x='140-120*t/{D}':y=79[bg];"
               f"[1:v]scale=2050:-2,format=rgba[f0];"
               f"[bg][f0]overlay=x='-65+70*t/{D}':y='(H-h)/2+10',{g},noise=alls=6:allf=t[c];"
               f"[2:v]format=rgba,fade=in:st=0.1:d=0.3:alpha=1[o];[c][o]overlay=0:0{trans_filters(p, D)},format=yuv420p[v]",
               "-map", "[v]", "-r", str(FPS), "-t", f"{D}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out]
    else:
        NF = D * FPS
        cmd = ["ffmpeg", "-y", "-v", "error", "-loop", "1", "-t", f"{D}", "-i", base, "-loop", "1", "-t", f"{D}", "-i", ov, "-filter_complex",
               f"[0:v]scale=2880:-2,zoompan=z='1.18-0.16*on/{NF:.0f}':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},{g},noise=alls=6:allf=t[c];"
               f"[c][1:v]overlay=0:0{trans_filters(p, D)},format=yuv420p[v]",
               "-map", "[v]", "-r", str(FPS), "-t", f"{D}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-1200:])

def render(k):
    p = plan[k]; out = f"{B}/shots/{k:04d}.mp4"
    if os.path.exists(out): return
    if p.get("fx"):
        spec = dict(p["fx"]); bgp = None
        try:
            kk, rng = p["keys"][0]; I = info[kk]
            tt = min(random.uniform(*(rng if rng else (I["d"] * 0.2, I["d"] * 0.8))), I["d"] - 1)
            bgp = still(I, tt, f"{B}/ovl/fxbg_{k:04d}.jpg", 1280)
        except Exception: pass
        if spec.get("type") == "photo" and spec.get("src"):
            kk, tt = spec["src"].split("@"); spec["_img"] = still(info[kk], float(tt), f"{B}/ovl/photo_{k:04d}.png")
        FX.render_fx(spec, p["d"], out, bgimg=bgp); return
    if p.get("parallax"): return render_parallax(k, p)
    s = seg[p["seg"]]; L = LAYOUTS[p["layout"]]; I = info[p["src"]]
    ov = overlay(p["seg"], s, L); D = p["d"]
    crop = f"crop={I['crop']}," if I["crop"] else ""
    NF = D * FPS
    z = f"1+0.09*on/{NF:.1f}" if p["zoomin"] else f"1.09-0.09*on/{NF:.1f}"
    if p["transition"] in ("punch", "flash", "whip"): z = f"({z})+0.13*pow(max(0,1-on/{0.45*FPS:.1f}),2)"
    pan = p.get("pan", 0)
    xe = f"(iw-iw/zoom)*(0.5+{0.5*pan}*on/{NF:.1f})" if pan else "iw/2-(iw/zoom/2)"
    w, h = L["w"], L["h"]
    srclen = D * {"normal": 1.0, "ramp": 1.45, "slow": 0.8}[p["speed"]]
    inputs = ["-ss", f"{p['start']:.2f}", "-t", f"{srclen + 0.1:.3f}", "-i", I["f"], "-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/bg_texture.png",
              "-loop", "1", "-t", f"{D:.3f}", "-i", ov]
    if p["speed"] == "ramp":     # fast first 40% (2x), then real-time
        a1 = 0.8 * D
        head = (f"[0:v]{crop}setsar=1,split[r1][r2];[r1]trim=0:{a1:.3f},setpts=(PTS-STARTPTS)/2[q1];"
                f"[r2]trim={a1:.3f}:{srclen:.3f},setpts=PTS-STARTPTS[q2];[q1][q2]concat=n=2:v=1:a=0,fps={FPS},split[a][b];")
    elif p["speed"] == "slow":
        head = f"[0:v]{crop}setsar=1,setpts=(PTS-STARTPTS)/0.8,fps={FPS},split[a][b];"
    else:
        head = f"[0:v]{crop}fps={FPS},setsar=1,split[a][b];"
    g = ("," + MOOD[p["mood"]]["grade"]) if ED["grade"] else ""
    if L.get("full"):
        fc = head + (f"[a]nullsink;[b]scale={int(W*1.3)}:{int(H*1.3)}:force_original_aspect_ratio=increase,crop={int(W*1.3)}:{int(H*1.3)},"
                     f"zoompan=z='{z}':d=1:x='{xe}':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}[c];")
    else:
        fc = head + (f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:4,eq=brightness=-0.12:saturation=0.55[bg0];"
                     f"[bg0][1:v]overlay=0:0[bg];"
                     f"[b]scale={int(w*1.5)}:{int(h*1.5)}:force_original_aspect_ratio=increase,crop={int(w*1.5)}:{int(h*1.5)},"
                     f"zoompan=z='{z}':d=1:x='{xe}':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={FPS}[fg0];")
        nin = 3
        if "mask" in L:
            inputs += ["-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/{L['mask']}_mask.png", "-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/{L['mask']}_shadow.png"]
            fc += (f"[fg0]format=rgba[fgr];[{nin}:v]format=gray[m];[fgr][m]alphamerge[fg];"
                   f"[bg][{nin+1}:v]overlay={L['x']-60}:{L['y']-60}[bs];[bs][fg]overlay={L['x']}:{L['y']}[c];")
        else:
            tx, ty = L["tv"]
            inputs += ["-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/tv_shadow.png", "-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/tv_frame.png"]
            fc += (f"[bg][{nin}:v]overlay={tx-60}:{ty-60}[bs];[bs][fg0]overlay={L['x']}:{L['y']}[bf];[bf][{nin+1}:v]overlay={tx}:{ty}[c];")
    li = len([x for x in inputs if x == "-i"])
    leak = ""
    if p.get("leak"):
        inputs += ["-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/leak{p['seg'] % 2}.png"]
        leak = f"[{li}:v]format=rgba,fade=in:st=0:d=0.25:alpha=1,fade=out:st=0.5:d=0.7:alpha=1[lk];"
    fc += f"[c]null{g}[cg];"
    if p["transition"] != "cut":
        fc += f"[2:v]format=rgba,fade=in:st=0.1:d=0.35:alpha=1[ov];[cg][ov]overlay=x='-260*pow(max(0,1-(t-0.1)/0.45),3)':y=0:eval=frame[c2];"
    else:
        fc += "[cg][2:v]overlay=0:0[c2];"
    if leak:
        fc += leak + "[c2][lk]overlay=0:0[c3];"; last = "c3"
    else: last = "c2"
    fc += f"[{last}]noise=alls=6:allf=t{trans_filters(p, D) if p['transition'] != 'cut' else ''},format=yuv420p[v]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-r", str(FPS), "-t", f"{D:.3f}",
                                                                            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-an", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-1500:])

only = int(os.environ.get("ONLY", "0"))
idx = range(len(plan)) if not only else range(min(only, len(plan)))
if os.environ.get("PICK"): idx = [int(x) for x in os.environ["PICK"].split(",")]; only = 1
with ThreadPoolExecutor(int(os.environ.get("JOBS", "4"))) as ex: list(ex.map(render, idx))
if only: sys.exit(0)

# ---------------- subtitles (ASS): karaoke words + keyword pop-ups + title hook ----------------
def ts(x): x = max(0, x); return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
def esc(t): return t.replace("{", "(").replace("}", ")").replace("\\", "")
NUMW = re.compile(r"\d")
ass = ["[Script Info]", "ScriptType: v4.00+", f"PlayResX: {W}", f"PlayResY: {H}", "WrapStyle: 0", "",
       "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Sub,Archivo Black,52,&H00F5F5F5,&H0032B6F2,&H00101010,&H96000000,0,0,0,0,100,100,0,0,1,5,2,2,120,120,34,1",
       "Style: Pop,Anton,104,&H0032E6FF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,60,60,0,1",
       "Style: Hook,Anton,84,&H00FFFFFF,&H00FFFFFF,&H00101010,&H96000000,0,0,0,0,100,100,1,0,1,7,4,5,80,80,0,1",
       "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
for i, s in enumerate(seg):
    s["_vos"] = s["_t0"] + s["_extra"] + (0.15 if i == 0 else -0.05)      # J-cut: voice leads the picture slightly
for i, s in enumerate(seg):
    js = f"{P}/vo/{i:02d}.json"
    keyw = set(w.strip(".,;:¡!¿?").lower() for w in (s.get("cap", "") if not s.get("cap", "").startswith("#") else "").split())
    if ED["subs"] and s.get("subs", True) and os.path.exists(js):
        words = json.load(open(js)); chunks, cur = [], []
        toks = s["txt"].split(); ti = 0                      # restore punctuation from the script text
        for w in words:
            bare = re.sub(r"\W", "", w["w"].lower())
            for look in range(ti, min(ti + 4, len(toks))):
                if re.sub(r"\W", "", toks[look].lower()) == bare:
                    w["w"] = toks[look]; ti = look + 1; break
        for w in words:
            cur.append(w)
            if len(cur) >= 6 or re.search(r"[.,;:?!]$", w["w"]) or (len(cur) >= 4 and len(" ".join(x["w"] for x in cur)) > 34):
                chunks.append(cur); cur = []
        if cur: chunks.append(cur)
        for ci, ch in enumerate(chunks):
            nxt = chunks[ci + 1][0]["s"] if ci + 1 < len(chunks) else 1e9
            for wi, w in enumerate(ch):
                st = s["_vos"] + w["s"]; en = s["_vos"] + (ch[wi + 1]["s"] if wi + 1 < len(ch) else min(w["e"] + 0.25, nxt))
                parts = []
                for wj, x in enumerate(ch):
                    tx = esc(x["w"]); bare = x["w"].strip(".,;:¡!¿?").lower()
                    hot = NUMW.search(x["w"]) or (bare in keyw and len(bare) > 3)
                    if wj == wi: parts.append("{\\c&H0032B6F2&\\fscx114\\fscy114}" + tx + "{\\c&H00F5F5F5&\\fscx100\\fscy100}")
                    elif hot: parts.append("{\\c&H004A7BFF&}" + tx + "{\\c&H00F5F5F5&}")
                    else: parts.append(tx)
                ass.append(f"Dialogue: 0,{ts(st)},{ts(en)},Sub,,0,0,0,,{' '.join(parts)}")
    pop = s.get("popup", s.get("cap", ""))
    if ED["popups"] and pop and not str(pop).startswith("#") and not s.get("fx") and pop is not False:
        st = s["_t0"] + 0.45
        ass.append(f"Dialogue: 1,{ts(st)},{ts(st + 2.3)},Pop,,0,0,0,,{{\\pos(960,820)\\fad(80,250)\\fscx35\\fscy35\\frz-4\\t(0,180,\\fscx108\\fscy108\\frz0)\\t(180,320,\\fscx100\\fscy100)}}{esc(str(pop))}")
        s["_pop"] = st
if ED["title_hook"] and meta.get("title"):
    ass.append(f"Dialogue: 2,{ts(0.4)},{ts(3.6)},Hook,,0,0,0,,{{\\pos(960,840)\\fad(200,400)\\fscx80\\fscy80\\t(0,400,\\fscx100\\fscy100)}}{esc(meta['title'])}")
open(f"{B}/subs.ass", "w").write("\n".join(ass) + "\n")

# ---------------- video: concat + finishing pass ----------------
with open(f"{B}/list.txt", "w") as f:
    for k in range(len(plan)): f.write(f"file 'shots/{k:04d}.mp4'\n")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{B}/list.txt", "-c", "copy", f"{B}/video_raw.mp4"], check=True)
vf = []
if ED["vignette"]: vf.append("vignette=angle=PI/5.5")
vf.append(f"ass={B}/subs.ass:fontsdir={FONT}")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", f"{B}/video_raw.mp4", "-vf", ",".join(vf),
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", f"{B}/video.mp4"], check=True)

# ---------------- audio: VO chain + music (mood volume, ducked) + SFX ----------------
ins, flt = [], []; n = 0; vo_lbl, sfx_lbl = [], []
VOCHAIN = "highpass=f=75,afftdn=nf=-28,equalizer=f=200:t=q:w=1:g=-2,equalizer=f=3500:t=q:w=1.2:g=2.5,deesser=i=0.35,acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2"
def add(path, vol, at, lbl, extra=""):
    global n
    ins.extend(["-i", path]); dl = int(max(0, at) * 1000)
    flt.append(f"[{n}:a]aresample=44100{extra},volume={vol},adelay={dl}|{dl}[{lbl}]"); n += 1; return f"[{lbl}]"
for i, s in enumerate(seg):
    vo_lbl.append(add(s["_vo"], 1.0, s["_vos"], f"v{i}", "," + VOCHAIN))
    tr = next((p["transition"] for p in plan if p["seg"] == i), "punch")
    if tr != "dip": sfx_lbl.append(add(f"{A}/whoosh.wav", 0.55 if tr != "flash" else 0.7, s["_t0"] - 0.25, f"w{i}"))
    if s["_extra"]:
        sfx_lbl.append(add(f"{A}/riser.wav", 0.45, s["_t0"] - 1.6, f"r{i}"))
        sfx_lbl.append(add(f"{A}/hit.wav", 0.85, s["_t0"] + 0.1, f"h{i}"))
    elif s.get("fx"):
        sfx_lbl.append(add(f"{A}/hit.wav", 0.3, s["_t0"] + 0.05, f"g{i}"))
        sfx_lbl.append(add(f"{A}/click.wav", 0.35, s["_t0"] + 0.6, f"c{i}"))
    if s.get("_pop"): sfx_lbl.append(add(f"{A}/pop.wav", 0.35, s["_pop"], f"p{i}"))
# music with mood-driven level automation
lv = "+".join(f"between(t,{s['_t0']:.2f},{s['_t0'] + s['_sd']:.2f})*{MOOD[s['_mood']]['music']}" for s in seg)
ins.extend(["-stream_loop", "-1", "-i", f"{A}/music.wav"])
flt.append(f"[{n}:a]aresample=44100,atrim=0:{TOTAL:.2f},volume='{ED['music']}*max(0.5,{lv})':eval=frame,afade=t=in:d=1.5,afade=t=out:st={TOTAL-3:.2f}:d=3[mus0]"); n += 1
ins.extend(["-stream_loop", "-1", "-i", f"{A}/ambient.wav"])
flt.append(f"[{n}:a]aresample=44100,atrim=0:{TOTAL:.2f},volume=0.5[amb]"); n += 1
flt.append(f"{''.join(vo_lbl)}amix=inputs={len(vo_lbl)}:normalize=0,asplit=2[vob][key]")
flt.append("[mus0][key]sidechaincompress=threshold=0.04:ratio=5:attack=25:release=450:makeup=1[mus]")
flt.append(f"[vob][mus][amb]{''.join(sfx_lbl)}amix=inputs={3 + len(sfx_lbl)}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(flt), "-map", "[a]", "-ac", "2", "-ar", "44100",
                "-c:a", "aac", "-b:a", "192k", f"{B}/audio.m4a"], check=True)
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", f"{B}/video.mp4", "-i", f"{B}/audio.m4a", "-map", "0:v", "-map", "1:a",
                "-c", "copy", "-shortest", "-movflags", "+faststart", f"{P}/final.mp4"], check=True)
print("done", f"{P}/final.mp4", f"{TOTAL:.1f}s")
