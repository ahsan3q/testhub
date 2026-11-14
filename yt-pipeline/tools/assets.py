"""Generate reusable retro-style assets: background texture, card mask/shadow, TV frame, whoosh SFX, music bed."""
import os, sys, wave, numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
rng = np.random.default_rng(7)

# ---------- background texture (teal tint + stars + grain) ----------
tex = Image.new("RGBA", (W, H), (9, 46, 50, 175))
d = ImageDraw.Draw(tex)
for _ in range(70):
    x, y = rng.integers(0, W), rng.integers(0, H)
    s = int(rng.integers(5, 11)); a = int(rng.integers(40, 110))
    d.line([(x - s, y), (x + s, y)], fill=(170, 220, 215, a), width=2)
    d.line([(x, y - s), (x, y + s)], fill=(170, 220, 215, a), width=2)
grain = (rng.normal(0, 18, (H, W))).clip(-40, 40)
arr = np.array(tex).astype(np.int16)
arr[..., :3] = (arr[..., :3] + grain[..., None]).clip(0, 255)
# vignette
yy, xx = np.mgrid[0:H, 0:W]
r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
arr[..., 3] = (arr[..., 3] + (np.clip(r - 0.55, 0, 1) * 160)).clip(0, 245)
arr[..., :3] = (arr[..., :3] * (1 - np.clip(r - 0.6, 0, 1)[..., None] * 0.7)).clip(0, 255)
Image.fromarray(arr.astype(np.uint8), "RGBA").save(f"{OUT}/bg_texture.png")

# ---------- rounded card masks + shadows ----------
def card(w, h, rad, name):
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, w - 1, h - 1], rad, fill=255)
    m.save(f"{OUT}/{name}_mask.png")
    pad = 60
    sh = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 14, pad + w, pad + h + 14], rad, fill=(0, 0, 0, 200))
    sh.filter(ImageFilter.GaussianBlur(24)).save(f"{OUT}/{name}_shadow.png")
card(1180, 885, 24, "card")
card(880, 660, 22, "cardsm")

# ---------- vintage wooden TV frame ----------
TW, TH = 1500, 1000
tv = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
body = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
bd = ImageDraw.Draw(body)
bd.rounded_rectangle([0, 0, TW - 1, TH - 1], 46, fill=(120, 72, 38, 255))
# wood grain
wood = np.array(body).astype(np.int16)
gy = (np.sin(np.linspace(0, 90, TH))[:, None] * 10 + rng.normal(0, 6, (TH, TW))).astype(np.int16)
wood[..., 0] += gy; wood[..., 1] += (gy * 0.7).astype(np.int16); wood[..., 2] += (gy * 0.4).astype(np.int16)
body = Image.fromarray(wood.clip(0, 255).astype(np.uint8), "RGBA")
bd = ImageDraw.Draw(body)
bd.rounded_rectangle([6, 6, TW - 7, TH - 7], 42, outline=(70, 40, 18, 255), width=8)
# screen bezel + hole
SX, SY, SW, SH = 70, 95, 1080, 810
bd.rounded_rectangle([SX - 26, SY - 26, SX + SW + 26, SY + SH + 26], 70, fill=(28, 22, 18, 255))
# right panel
px = SX + SW + 50
bd.rounded_rectangle([px, 95, TW - 50, TH - 95], 26, fill=(205, 170, 120, 255))
for ky in (250, 440):
    cx = (px + TW - 50) // 2
    bd.ellipse([cx - 62, ky - 62, cx + 62, ky + 62], fill=(55, 38, 24, 255))
    bd.ellipse([cx - 46, ky - 46, cx + 46, ky + 46], fill=(85, 60, 38, 255))
    bd.line([(cx, ky - 40), (cx, ky - 8)], fill=(230, 210, 170, 255), width=8)
for gy_ in range(570, TH - 130, 18):
    bd.line([(px + 30, gy_), (TW - 80, gy_)], fill=(140, 105, 70, 255), width=7)
hole = Image.new("L", (TW, TH), 0)
ImageDraw.Draw(hole).rounded_rectangle([SX, SY, SX + SW, SY + SH], 60, fill=255)
a = np.array(body); a[..., 3] = np.where(np.array(hole) > 0, 0, a[..., 3])
body = Image.fromarray(a, "RGBA")
# glass glare
glare = Image.new("RGBA", (TW, TH), (0, 0, 0, 0))
ImageDraw.Draw(glare).ellipse([SX + 40, SY + 20, SX + 520, SY + 260], fill=(255, 255, 255, 22))
glare = glare.filter(ImageFilter.GaussianBlur(40))
shadow = Image.new("RGBA", (TW + 120, TH + 120), (0, 0, 0, 0))
ImageDraw.Draw(shadow).rounded_rectangle([60, 80, TW + 60, TH + 80], 46, fill=(0, 0, 0, 190))
shadow = shadow.filter(ImageFilter.GaussianBlur(30))
shadow.save(f"{OUT}/tv_shadow.png")
Image.alpha_composite(body, glare).save(f"{OUT}/tv_frame.png")
open(f"{OUT}/tv_geom.txt", "w").write(f"{TW} {TH} {SX} {SY} {SW} {SH}")

# ---------- audio ----------
SR = 44100
def wav(name, x):
    x = np.clip(x, -1, 1)
    with wave.open(f"{OUT}/{name}", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())

# whoosh: noise with moving low-pass sweep
n = int(SR * 0.75); t = np.arange(n) / SR
noise = rng.normal(0, 1, n)
out = np.zeros(n); y = 0.0
cut = 0.02 + 0.25 * np.sin(np.pi * t / t[-1]) ** 2
for i in range(n):
    y += cut[i] * (noise[i] - y); out[i] = y
env = np.sin(np.pi * np.clip(t / 0.75, 0, 1)) ** 1.5
wav("whoosh.wav", out / np.abs(out).max() * env * 0.55)

# pop / hit for countdown reveal
n = int(SR * 0.5); t = np.arange(n) / SR
hit = np.sin(2 * np.pi * (90 * np.exp(-t * 6)) * t) * np.exp(-t * 7)
wav("hit.wav", hit * 0.8)

# music bed: soft retro chords + walking bass + vinyl crackle (original, generated)
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 600
n = int(SR * dur); t = np.arange(n) / SR
chords = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 196.0, 261.63), (196.0, 246.94, 293.66)]
bar = 4.0
mus = np.zeros(n)
for ci in range(int(dur / bar) + 1):
    s = int(ci * bar * SR); e = min(n, int((ci + 1) * bar * SR))
    if s >= n: break
    tt = np.arange(e - s) / SR
    envc = np.minimum(1, tt / 0.6) * np.minimum(1, (bar - tt) / 0.8)
    ch = chords[ci % 4]
    for f in ch:
        mus[s:e] += (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt)) * envc * 0.11
    # soft plucked bass on beats
    for b in range(4):
        bs = s + int(b * SR)
        if bs >= e: break
        bt = np.arange(min(int(0.9 * SR), e - bs)) / SR
        mus[bs:bs + len(bt)] += np.sin(2 * np.pi * ch[0] / 2 * bt) * np.exp(-bt * 4) * 0.22
trem = 0.85 + 0.15 * np.sin(2 * np.pi * 0.25 * t)
crackle = np.zeros(n); idx = rng.integers(0, n, int(dur * 25)); crackle[idx] = rng.normal(0, 0.25, len(idx))
hiss = rng.normal(0, 0.006, n)
wav("music.wav", (mus * trem + crackle + hiss) * 0.8)
print("assets ok")
