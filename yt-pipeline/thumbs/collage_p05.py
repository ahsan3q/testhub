import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
P = sys.argv[1]; F = sys.argv[2]
FB = F + "/ArchivoBlack-Regular.ttf"; FS = F + "/AlfaSlabOne-Regular.ttf"
W, H = 1280, 720
NAVY = (22, 40, 92); RED = (200, 28, 30); CREAM = (246, 236, 214); YEL = (250, 196, 30)
img = Image.new("RGB", (W, H), (36, 24, 18)); d = ImageDraw.Draw(img)
# sunburst right
sb = Image.new("RGB", (560, 720), (200, 70, 30)); sd = ImageDraw.Draw(sb)
cx, cy = 330, 300
for i in range(24):
    a0 = i * 15; a1 = a0 + 7.5
    pts = [(cx, cy)] + [(cx + 1200 * math.cos(math.radians(a)), cy + 1200 * math.sin(math.radians(a))) for a in (a0, a1)]
    sd.polygon(pts, fill=(240, 170, 50))
img.paste(sb, (720, 0))
def load(name):
    im = Image.open(f"{P}/{name}").convert("RGB")
    bb = ImageOps.invert(im.convert("L")).point(lambda v: 0 if v > 235 else 255).getbbox()  # crop black bars
    if bb: im = im.crop(bb)
    return ImageEnhance.Color(im).enhance(1.3)
def panel(name, title1, title2, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=CREAM, outline=(40, 30, 20), width=3)
    def fit(t, sz):
        f = ImageFont.truetype(FB, sz)
        while d.textlength(t, font=f) > (x1 - x0 - 14): sz -= 1; f = ImageFont.truetype(FB, sz)
        return f
    f1 = fit(title1, 24); f2 = fit(title2, 22)
    tw = d.textlength(title1, font=f1); d.text(((x0 + x1) / 2 - tw / 2, y0 + 8), title1, font=f1, fill=NAVY)
    tw = d.textlength(title2, font=f2); d.text(((x0 + x1) / 2 - tw / 2, y0 + 38), title2, font=f2, fill=RED)
    im = load(name); iw, ih = x1 - x0 - 16, y1 - y0 - 76
    im = ImageOps.fit(im, (iw, ih), Image.LANCZOS)
    img.paste(im, (x0 + 8, y0 + 68))
cells = [("c_FW_2.png", "LOS PICAPIEDRA", "CIGARROS WINSTON"), ("c_WB_0.png", "WENDY'S", "¿DÓNDE ESTÁ LA CARNE?"),
         ("c_CE_1.png", "CRAZY EDDIE", "¡PRECIOS DE LOCURA!"), ("c_MC2_0.png", "McDONALDLAND", "LA DEMANDA"),
         ("c_CR_2.png", "CALIFORNIA", "RAISINS"), ("c_LC_2.png", "LIFECALL", "¡ME HE CAÍDO!")]
pw, ph = 235, 230
for i, (n, a, b) in enumerate(cells):
    r, c = divmod(i, 3)
    panel(n, a, b, (22 + c * (pw + 8), 22 + r * (ph + 8), 22 + c * (pw + 8) + pw, 22 + r * (ph + 8) + ph))
# TV with text
tv = Image.open(f"{F}/../assets/tv_frame.png").convert("RGBA").resize((330, 220), Image.LANCZOS)
scr = Image.new("RGB", (330, 220), (225, 225, 215)); sdr = ImageDraw.Draw(scr)
f = ImageFont.truetype(FB, 17)
for j, (ln, col) in enumerate([("ESTOS COMERCIALES", NAVY), ("¡DESAPARECIERON", RED), ("DE LA TV!", NAVY)]):
    tw = sdr.textlength(ln, font=f); sdr.text((120 - tw / 2, 62 + j * 32), ln, font=f, fill=col)
img.paste(scr, (790, 190)); img.paste(tv, (790, 190), tv)
# bottom banner
d.rectangle([150, 512, 1060, 700], fill=CREAM, outline=(40, 30, 20), width=4)
fb = ImageFont.truetype(FS, 120)
tw = d.textlength("PROHIBIDOS", font=fb); d.text((605 - tw / 2, 500), "PROHIBIDOS", font=fb, fill=RED, stroke_width=3, stroke_fill=(120, 10, 10))
f2 = ImageFont.truetype(FB, 40); t2 = "LOS COMERCIALES MÁS GRACIOSOS"
tw = d.textlength(t2, font=f2); d.text((605 - tw / 2, 638), t2, font=f2, fill=NAVY)
# starbursts
def star(cx, cy, r, lines, size):
    pts = []
    for i in range(32):
        rr = r if i % 2 == 0 else r * 0.78
        a = math.radians(i * 360 / 32); pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=YEL, outline=(60, 40, 10)); fnt = ImageFont.truetype(FB, size)
    y = cy - len(lines) * size * 0.6
    for ln in lines:
        tw = d.textlength(ln, font=fnt); d.text((cx - tw / 2, y), ln, font=fnt, fill=(30, 20, 10)); y += size * 1.15
star(1150, 590, 120, ["¿QUÉ", "PASÓ?"], 40)
star(90, 610, 85, ["¡NO VAS", "A CREER", "ESTO!"], 19)
# bulb border
for x in range(8, W, 22):
    for y in (6, H - 8): d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 245, 210))
for y in range(8, H, 22):
    for x in (6, W - 8): d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 245, 210))
img.save(f"{P}/v01_thumbnail.jpg", quality=95); print("ok")
