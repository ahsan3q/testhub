# Split thumbnail: left/right frames, optional green-framed center inset, optional bottom text.
# usage: splitthumb.py cfg.json out.jpg
# cfg: {"left": {"img": p, "cx": 0.5, "cy": 0.4, "zoom": 1.0}, "right": {...},
#       "center": {"img": p, "cx":.5, "cy":.4, "zoom":1.0} (optional),
#       "lines": ["¿LÍNEA 1", "LÍNEA 2?"] (optional), "font": path}
import sys, json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

C = json.load(open(sys.argv[1])); W, H = 1280, 720
img = Image.new("RGB", (W, H), "black")

def crop(spec, w, h):
    im = Image.open(spec["img"]).convert("RGB")
    z = spec.get("zoom", 1.0)
    s = max(w / im.width, h / im.height) * z
    im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
    cx, cy = spec.get("cx", 0.5) * im.width, spec.get("cy", 0.45) * im.height
    x0 = int(min(max(cx - w / 2, 0), im.width - w)); y0 = int(min(max(cy - h / 2, 0), im.height - h))
    im = im.crop((x0, y0, x0 + w, y0 + h))
    im = ImageEnhance.Contrast(im).enhance(1.12); im = ImageEnhance.Color(im).enhance(1.2)
    return ImageEnhance.Sharpness(im).enhance(1.4)

img.paste(crop(C["left"], W // 2, H), (0, 0))
img.paste(crop(C["right"], W // 2, H), (W // 2, 0))
d = ImageDraw.Draw(img)
d.rectangle((W // 2 - 3, 0, W // 2 + 2, H), fill="white")
if C.get("center"):
    cw, ch = 270, 360; x, y = W // 2 - cw // 2, 70
    d.rectangle((x - 7, y - 7, x + cw + 6, y + ch + 6), fill=(60, 255, 90))
    img.paste(crop(C["center"], cw, ch), (x, y))
lines = C.get("lines") or []
if lines:
    f = ImageFont.truetype(C["font"], 96)
    y = H - 30 - len(lines) * 104
    for ln in lines:
        size = 96
        while d.textlength(ln, font=f) > W - 80 and size > 50:
            size -= 4; f = ImageFont.truetype(C["font"], size)
        d.text((W / 2, y), ln, font=f, fill="white", anchor="ma", stroke_width=9, stroke_fill="black")
        y += 104
img.save(sys.argv[2], quality=92)
