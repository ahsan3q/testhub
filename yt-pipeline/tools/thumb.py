"""Retro cartoon thumbnail: night-blue bg + cut-out characters left + 3-line text stack right.
usage: thumb.py config.json out.png
config: {"bg": path, "chars": [{"img": path, "h": px, "x": px, "y_bottom": px}], "lines": [{"text":..., "style": "yellow|cyan|red"}]}
"""
import json, sys, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

C = json.load(open(sys.argv[1])); OUT = sys.argv[2]
F = __file__.rsplit("/", 1)[0] + "/fonts/LuckiestGuy-Regular.ttf"
W, H = 1280, 720
random.seed(3)

# --- background: blurred frame tinted night blue + moon glow ---
bg = Image.open(C["bg"]).convert("RGB")
bw, bh = bg.size; s = max(W / bw, H / bh)
bg = bg.resize((int(bw * s) + 1, int(bh * s) + 1), Image.LANCZOS).crop((0, 0, W, H)).filter(ImageFilter.GaussianBlur(6))
a = np.asarray(bg).astype(float) / 255
lum = a.mean(axis=2, keepdims=True)
night = np.array([0.10, 0.20, 0.48]) * (0.35 + 1.1 * lum) + a * 0.25
yy, xx = np.mgrid[0:H, 0:W]
moon = np.exp(-(((xx - 230) ** 2 + (yy - 120) ** 2) / (2 * 140 ** 2)))[..., None] * np.array([0.35, 0.45, 0.6])
vig = (1 - 0.55 * np.clip(np.sqrt(((xx - W * 0.35) / W) ** 2 + ((yy - H / 2) / H) ** 2) - 0.2, 0, 1))[..., None]
img = Image.fromarray((np.clip((night + moon) * vig, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
d = ImageDraw.Draw(img)
d.ellipse([170, 60, 290, 180], fill=(205, 220, 240, 230))
img = img.filter(ImageFilter.GaussianBlur(1))

# --- characters with white outline glow ---
for ch in C["chars"]:
    c = Image.open(ch["img"]).convert("RGBA")
    bb = c.getchannel("A").point(lambda v: 255 if v > 40 else 0).getbbox(); c = c.crop(bb)
    sc = ch["h"] / c.height; c = c.resize((int(c.width * sc), int(c.height * sc)), Image.LANCZOS)
    c = ImageEnhance.Color(c).enhance(1.35); c = ImageEnhance.Contrast(c).enhance(1.12)
    al = c.getchannel("A").point(lambda v: 255 if v > 90 else 0)
    c.putalpha(al.filter(ImageFilter.GaussianBlur(0.8)))
    pad = 14
    glow = Image.new("RGBA", (c.width + 2 * pad, c.height + 2 * pad), (0, 0, 0, 0))
    m = Image.new("L", glow.size, 0); m.paste(al, (pad, pad)); m = m.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2))
    glow.paste((255, 255, 255, 255), (0, 0), m)
    x, y = ch["x"], ch["y_bottom"] - c.height
    img.alpha_composite(glow, (x - pad, y - pad)); img.alpha_composite(c, (x, y))

# --- text stack ---
def brush(w, h, color):
    b = Image.new("RGBA", (w + 80, h + 60), (0, 0, 0, 0)); dd = ImageDraw.Draw(b)
    pts = []
    for i in range(24):  # top edge jagged
        pts.append((40 + i * w / 23, 30 + random.uniform(-10, 6)))
    for i in range(24):
        pts.append((40 + w - i * w / 23, 30 + h + random.uniform(-6, 10)))
    dd.polygon(pts, fill=color)
    for _ in range(14):  # bristle streaks at ends
        yv = random.uniform(34, 26 + h); L = random.uniform(15, 40)
        dd.line([(40 - L, yv), (44, yv)], fill=color, width=random.randint(3, 7))
        dd.line([(36 + w, yv), (40 + w + L, yv)], fill=color, width=random.randint(3, 7))
    return b

layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
STY = {"yellow": ((250, 214, 30, 255), (255, 255, 255)), "red": ((226, 30, 36, 255), (255, 255, 255)), "cyan": (None, (64, 226, 240))}
x0, x1 = C.get("text_x", 640), C.get("text_x1", 1250); maxw = x1 - x0
y = C.get("text_y", 60)
for ln in C["lines"]:
    col, fg = STY[ln["style"]]
    size = ln.get("size", 150)
    f = ImageFont.truetype(F, size)
    while True:
        tb = layer.getbbox() if False else None
        bx = ImageDraw.Draw(layer).textbbox((0, 0), ln["text"], font=f, stroke_width=10)
        if bx[2] - bx[0] <= maxw - (60 if col else 0) or size < 50: break
        size -= 4; f = ImageFont.truetype(F, size)
    tw, th = bx[2] - bx[0], bx[3] - bx[1]
    t = Image.new("RGBA", (tw + 60, th + 60), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((30 - bx[0] + 8, 30 - bx[1] + 10), ln["text"], font=f, fill=(0, 0, 0, 255), stroke_width=12, stroke_fill=(0, 0, 0, 255))
    ImageDraw.Draw(t).text((30 - bx[0], 30 - bx[1]), ln["text"], font=f, fill=fg + (255,), stroke_width=10, stroke_fill=(15, 15, 20, 255))
    blk = Image.new("RGBA", (maxw + 40, th + 100), (0, 0, 0, 0))
    if col: blk.alpha_composite(brush(min(maxw - 30, tw + 50), th + 26, col), (max(0, (maxw - tw) // 2 - 45), 8))
    blk.alpha_composite(t, ((maxw + 40 - t.width) // 2, 20))
    blk = blk.rotate(ln.get("rot", -4), resample=Image.BICUBIC, expand=True)
    layer.alpha_composite(blk, (x0 + (maxw - blk.width) // 2 + 10, int(y)))
    y += th + ln.get("gap", 40)

# sparkle lines
dl = ImageDraw.Draw(layer)
for (cx, cy, colr) in C.get("sparks", [[600, 330, (250, 214, 30)], [1235, 270, (250, 214, 30)], [610, 430, (226, 30, 36)], [1240, 380, (226, 30, 36)]]):
    for ang in (-25, 0, 25):
        r = np.deg2rad(ang + (180 if cx < 900 else 0)); L1, L2 = 18, 58
        dl.line([(cx + L1 * np.cos(r), cy + L1 * np.sin(r)), (cx + L2 * np.cos(r), cy + L2 * np.sin(r))], fill=tuple(colr) + (255,), width=9)
img.alpha_composite(layer)
img.convert("RGB").save(OUT, quality=95)
print("thumb ok", OUT)
