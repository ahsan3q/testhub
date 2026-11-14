"""Build a retro documentary-style video from script.json + per-segment voiceovers + source clips.
usage: build.py <project_dir> <sources.json>
sources.json: {"KEY": "path/to/source.mp4", ...}   ("MIX" = random among all)
"""
import json, os, sys, random, subprocess, re
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw, ImageFont

P = sys.argv[1]; SRC = json.load(open(sys.argv[2]))
T = os.path.dirname(os.path.abspath(__file__)); A = f"{T}/assets"; FONT = f"{T}/fonts"
W, H, FPS = 1920, 1080, 30
MAXSHOT = 3.8; MINSHOT = 2.4          # every clip shorter than 4 s
random.seed(11)
seg = json.load(open(f"{P}/script.json"))
os.makedirs(f"{P}/build/shots", exist_ok=True); os.makedirs(f"{P}/build/ovl", exist_ok=True)

def dur(f): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))

# ---- source info: duration + black-bar crop ----
info = {}
for k, f in SRC.items():
    d = dur(f)
    out = subprocess.run(["ffmpeg", "-hide_banner", "-ss", str(d * 0.4), "-i", f, "-t", "20", "-vf", "cropdetect=24:2:0", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"crop=(\d+:\d+:\d+:\d+)", out)
    info[k] = dict(f=f, d=d, crop=m[-1] if m else None)

# ---- fonts / overlays ----
F_CAP = ImageFont.truetype(f"{FONT}/ArchivoBlack-Regular.ttf", 66)
F_LAB = ImageFont.truetype(f"{FONT}/ArchivoBlack-Regular.ttf", 34)
F_NUM = ImageFont.truetype(f"{FONT}/AlfaSlabOne-Regular.ttf", 230)
F_NAME = ImageFont.truetype(f"{FONT}/AlfaSlabOne-Regular.ttf", 70)
GOLD = (242, 182, 50, 255); CREAM = (245, 230, 200, 255)

TVW, TVH, SX, SY, SW, SH = map(int, open(f"{A}/tv_geom.txt").read().split())
LAYOUTS = {
    "card":  dict(x=370, y=98, w=1180, h=885, mask="card"),
    "tv":    dict(x=210 + SX, y=40 + SY, w=SW, h=SH, tv=(210, 40)),
    "count": dict(x=900, y=210, w=880, h=660, mask="cardsm"),
}

def wrap(text, font, maxw, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w_
    lines.append(cur); return lines

def overlay(i, s, L, with_caption):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    cap = s.get("cap", "")
    if cap.startswith("#"):   # countdown reveal
        name = s["label"].split("·")[0].strip()
        d.text((130, 250), cap, font=F_NUM, fill=GOLD, stroke_width=6, stroke_fill=(20, 15, 10, 255))
        for j, ln in enumerate(wrap(name, F_NAME, 680, d)):
            d.text((140, 560 + j * 88), ln, font=F_NAME, fill=CREAM, stroke_width=4, stroke_fill=(20, 15, 10, 255))
        cap = ""
    if s.get("label"):
        lb = s["label"]; tw = d.textlength(lb, font=F_LAB)
        x0, y0 = L["x"] + 22, L["y"] + 20
        d.rounded_rectangle([x0, y0, x0 + tw + 40, y0 + 58], 12, fill=GOLD)
        d.text((x0 + 20, y0 + 9), lb, font=F_LAB, fill=(25, 20, 12, 255))
    if cap and with_caption:
        lines = wrap(cap, F_CAP, L["w"] - 120, d)
        y = L["y"] + L["h"] - 60 - len(lines) * 80
        for ln in lines:
            tw = d.textlength(ln, font=F_CAP)
            d.text((L["x"] + (L["w"] - tw) / 2, y), ln, font=F_CAP, fill=CREAM, stroke_width=7, stroke_fill=(15, 12, 8, 255))
            y += 80
    p = f"{P}/build/ovl/{i:02d}_{int(with_caption)}.png"; img.save(p); return p

# ---- timeline ----
GAP = 0.45
plan, t0 = [], 0.0
for i, s in enumerate(seg):
    vo = f"{P}/vo/{i:02d}.mp3"; vd = dur(vo)
    extra = 0.9 if s.get("cap", "").startswith("#") else 0
    sd = vd + GAP + extra
    layout = "count" if s.get("cap", "").startswith("#") else ("tv" if i % 3 == 1 else "card")
    # split into shots
    n = max(1, round(sd / 3.2)); shots = [sd / n] * n
    while max(shots) > MAXSHOT: n += 1; shots = [sd / n] * n
    # src: "KEY", "KEY@a-b" (seconds range), "MIX", or a list of these
    spec = s["src"] if isinstance(s["src"], list) else [s["src"]]
    keys = []
    for sp in spec:
        if sp == "MIX": keys += [(k, None) for k in SRC.keys()]
        elif "@" in sp:
            k, r = sp.split("@"); a, b = r.split("-"); keys.append((k, (float(a), float(b))))
        else: keys.append((sp, None))
    used = 0.0
    if s.get("fx"):
        fxd = sd if s["fx"].get("full") or sd < 6.5 else min(sd - 2.5, s["fx"].get("dur", 4.8))
        plan.append(dict(seg=i, j=-1, fx=s["fx"], d=fxd, first=True, cap=False, layout=layout, src=None, keys=keys))
        rest = sd - fxd; used = fxd
        n = 0 if rest < 0.5 else max(1, round(rest / 3.2)); shots = [rest / n] * n if n else []
        while shots and max(shots) > MAXSHOT: n += 1; shots = [rest / n] * n
    for j, sh in enumerate(shots):
        k, rng = keys[j % len(keys)] if len(keys) > 1 and all(r for _, r in keys) else random.choice(keys); I = info[k]
        if rng:
            lo, hi = rng[0], min(rng[1], I["d"] - 0.4)
            start = random.uniform(lo, max(lo, hi - sh))
        else:
            lo, hi = min(25, I["d"] * 0.1), max(I["d"] - 30, I["d"] * 0.6)
            start = random.uniform(lo, max(lo, min(hi - sh, I["d"] - sh - 0.4)))
        plan.append(dict(seg=i, j=j, src=k, start=start, d=sh, layout=layout, cap=(used < 5.0), first=(j == 0 and not s.get("fx")), zoomin=random.random() < 0.7, pan=random.choice([-1, 0, 1]), segstart=(j == 0)))
        used += sh
    seg[i]["_t0"], seg[i]["_vo"], seg[i]["_extra"] = t0, vo, extra
    t0 += sd
TOTAL = t0
print(f"timeline {TOTAL:.1f}s, {len(plan)} shots")

ovl_cache = {}
sys.path.insert(0, T); import fx as FX
def render(k):
    p = plan[k]
    if p.get("fx"):
        out = f"{P}/build/shots/{k:04d}.mp4"
        if os.path.exists(out): return
        spec = dict(p["fx"])
        bgp = f"{P}/build/ovl/fxbg_{k:04d}.jpg"
        try:
            kk, rng = p["keys"][0]; I = info[kk]
            tt = random.uniform(*(rng if rng else (I["d"] * 0.2, I["d"] * 0.8)))
            tt = min(tt, I["d"] - 1)
            if not os.path.exists(bgp):
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.2f}", "-i", I["f"], "-frames:v", "1", "-vf", (f"crop={I['crop']}," if I["crop"] else "") + "scale=1280:-2", bgp])
        except Exception:
            bgp = None
        if spec.get("type") == "photo" and spec.get("src"):
            kk, tt = spec["src"].split("@"); I = info[kk]; ph = f"{P}/build/ovl/photo_{k:04d}.png"
            if not os.path.exists(ph):
                subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", tt, "-i", I["f"], "-frames:v", "1", "-vf", (f"crop={I['crop']}," if I["crop"] else "") + "scale=1920:-2", ph])
            spec["_img"] = ph
        FX.render_fx(spec, p["d"], out, bgimg=bgp)
        return
    s = seg[p["seg"]]; L = LAYOUTS[p["layout"]]; I = info[p["src"]]
    key = (p["seg"], p["cap"])
    if key not in ovl_cache: ovl_cache[key] = overlay(p["seg"], s, L, p["cap"])
    ov = ovl_cache[key]; D = p["d"]; out = f"{P}/build/shots/{k:04d}.mp4"
    if os.path.exists(out): return
    crop = f"crop={I['crop']}," if I["crop"] else ""
    NF = D * FPS
    z = f"1+0.08*on/{NF:.1f}" if p["zoomin"] else f"1.08-0.08*on/{NF:.1f}"
    if p.get("segstart"):
        z = f"({z})+0.12*pow(max(0,1-on/{0.45*FPS:.1f}),2)"
    pan = p.get("pan", 0)
    xe = f"(iw-iw/zoom)*(0.5+{0.5*pan}*on/{NF:.1f})" if pan else "iw/2-(iw/zoom/2)"
    w, h = L["w"], L["h"]
    inputs = ["-ss", f"{p['start']:.2f}", "-t", f"{D:.3f}", "-i", I["f"], "-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/bg_texture.png", "-loop", "1", "-t", f"{D:.3f}", "-i", ov]
    fc = (f"[0:v]{crop}fps={FPS},setsar=1,split[a][b];"
          f"[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=28:4,eq=brightness=-0.12:saturation=0.55[bg0];"
          f"[bg0][1:v]overlay=0:0[bg];"
          f"[b]scale={int(w*1.5)}:{int(h*1.5)}:force_original_aspect_ratio=increase,crop={int(w*1.5)}:{int(h*1.5)},"
          f"zoompan=z='{z}':d=1:x='{xe}':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={FPS},eq=contrast=1.06:saturation=1.1[fg0];")
    nin = 3
    if "mask" in L:
        inputs += ["-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/{L['mask']}_mask.png", "-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/{L['mask']}_shadow.png"]
        fc += (f"[fg0]format=rgba[fgr];[{nin}:v]format=gray[m];[fgr][m]alphamerge[fg];"
               f"[bg][{nin+1}:v]overlay={L['x']-60}:{L['y']-60}[bs];[bs][fg]overlay={L['x']}:{L['y']}[c];")
    else:
        tx, ty = L["tv"]
        inputs += ["-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/tv_shadow.png", "-loop", "1", "-t", f"{D:.3f}", "-i", f"{A}/tv_frame.png"]
        fc += (f"[bg][{nin}:v]overlay={tx-60}:{ty-60}[bs];[bs][fg0]overlay={L['x']}:{L['y']}[bf];[bf][{nin+1}:v]overlay={tx}:{ty}[c];")
    fade = f",fade=in:st=0:d=0.3" if p["first"] else ""
    if p.get("segstart"):
        fc += (f"[2:v]format=rgba,fade=in:st=0.1:d=0.35:alpha=1[ov];"
               f"[c][ov]overlay=x='-260*pow(max(0,1-(t-0.1)/0.45),3)':y=0:eval=frame,noise=alls=7:allf=t,format=yuv420p{fade}[v]")
    else:
        fc += f"[c][2:v]overlay=0:0,noise=alls=7:allf=t,format=yuv420p{fade}[v]"
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + inputs + ["-filter_complex", fc, "-map", "[v]", "-r", str(FPS), "-t", f"{D:.3f}", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-an", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: raise RuntimeError(r.stderr[-1500:])

# pre-render overlays serially (PIL not thread-safe w/ fonts)
for k, p in enumerate(plan):
    if p.get("fx"): continue
    key = (p["seg"], p["cap"])
    if key not in ovl_cache: ovl_cache[key] = overlay(p["seg"], seg[p["seg"]], LAYOUTS[p["layout"]], p["cap"])
only = int(os.environ.get("ONLY", "0"))
idx = range(len(plan)) if not only else range(min(only, len(plan)))
with ThreadPoolExecutor(int(os.environ.get("JOBS", "4"))) as ex: list(ex.map(render, idx))
if only: sys.exit(0)

# ---- concat video ----
with open(f"{P}/build/list.txt", "w") as f:
    for k in range(len(plan)): f.write(f"file 'shots/{k:04d}.mp4'\n")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", f"{P}/build/list.txt", "-c", "copy", f"{P}/build/video.mp4"], check=True)

# ---- audio: voice + whoosh at each segment + hit at countdown + music bed ----
ins, flt, mix = [], [], []
n = 0
for i, s in enumerate(seg):
    ins += ["-i", s["_vo"]]; dl = int((s["_t0"] + 0.15 + s["_extra"]) * 1000)
    flt.append(f"[{n}:a]aresample=44100,adelay={dl}|{dl}[v{i}]"); mix.append(f"[v{i}]"); n += 1
    ins += ["-i", f"{A}/whoosh.wav"]; dl = int(max(0, s["_t0"] - 0.25) * 1000)
    flt.append(f"[{n}:a]aresample=44100,volume=0.55,adelay={dl}|{dl}[w{i}]"); mix.append(f"[w{i}]"); n += 1
    if s.get("fx") and not s["_extra"]:
        ins += ["-i", f"{A}/hit.wav"]; dl = int((s["_t0"] + 0.05) * 1000)
        flt.append(f"[{n}:a]aresample=44100,volume=0.32,adelay={dl}|{dl}[g{i}]"); mix.append(f"[g{i}]"); n += 1
    if s["_extra"]:
        ins += ["-i", f"{A}/hit.wav"]; dl = int((s["_t0"] + 0.1) * 1000)
        flt.append(f"[{n}:a]aresample=44100,volume=0.8,adelay={dl}|{dl}[h{i}]"); mix.append(f"[h{i}]"); n += 1
ins += ["-i", f"{A}/music.wav"]
flt.append(f"[{n}:a]aresample=44100,volume=0.20,atrim=0:{TOTAL:.2f},afade=t=out:st={TOTAL-3:.2f}:d=3[mus]"); mix.append("[mus]")
flt.append(f"{''.join(mix)}amix=inputs={len(mix)}:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[a]")
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(flt), "-map", "[a]", "-ac", "2", "-ar", "44100", "-c:a", "aac", "-b:a", "192k", f"{P}/build/audio.m4a"], check=True)
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", f"{P}/build/video.mp4", "-i", f"{P}/build/audio.m4a", "-map", "0:v", "-map", "1:a", "-c", "copy", "-shortest", "-movflags", "+faststart", f"{P}/final.mp4"], check=True)
print("done", f"{P}/final.mp4", f"{TOTAL:.1f}s")
