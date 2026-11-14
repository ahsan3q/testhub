"""Animated keyframed graphics rendered frame-by-frame with PIL and piped to ffmpeg.
render_fx(spec, duration, out_mp4)
spec types:
  map:      {"type":"map","countries":["United States of America"],"states":["New York","California"],
             "pins":[{"name":"NUEVA YORK","lon":-74.0,"lat":40.7}], "route":[0,1], "view":[lon0,lat0,lon1,lat1], "title":"..."}
  counter:  {"type":"counter","value":250000,"prefix":"$","suffix":"","label":"...","sub":"..."}
  timeline: {"type":"timeline","items":[["1930","Nace Betty"],["1934","Código Hays"]],"title":"..."}
  quote:    {"type":"quote","text":"...","by":"..."}
  compare:  {"type":"compare","left":["$100,000","LO QUE PIDIERON"],"right":["$50,000","LO QUE PAGARON"],"title":"..."}
  list:     {"type":"list","title":"...","items":["...","..."]}
"""
import json, math, os, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

T = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1920, 1080, 30
FB = f"{T}/fonts/ArchivoBlack-Regular.ttf"; FS = f"{T}/fonts/AlfaSlabOne-Regular.ttf"
GOLD = (242, 182, 50); CREAM = (245, 230, 200); RED = (214, 52, 44); INK = (18, 16, 12); TEAL = (12, 52, 58)
_font = {}
def font(p, s):
    k = (p, int(s))
    if k not in _font: _font[k] = ImageFont.truetype(p, int(s))
    return _font[k]
BG = None
def bg():
    global BG
    if BG is None:
        base = Image.new("RGB", (W, H), (8, 36, 40))
        tex = Image.open(f"{T}/assets/bg_texture.png")
        base.paste(tex, (0, 0), tex); BG = base
    return BG.copy()

def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def ease_back(t):
    t = min(max(t, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def prog(t, a, b): return min(max((t - a) / (b - a), 0), 1)

def pill(d, xy, text, f, fill=GOLD, fg=INK, pad=(22, 10)):
    x, y = xy; tw = d.textlength(text, font=f); th = f.size
    d.rounded_rectangle([x, y, x + tw + 2 * pad[0], y + th + 2 * pad[1] + 4], 12, fill=fill)
    d.text((x + pad[0], y + pad[1]), text, font=f, fill=fg)

def ctext(d, cx, y, text, f, fill=CREAM, stroke=6):
    tw = d.textlength(text, font=f); d.text((cx - tw / 2, y), text, font=f, fill=fill, stroke_width=stroke, stroke_fill=INK)

def wrap(d, text, f, maxw):
    out, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: out.append(cur); cur = w
    out.append(cur); return out

def scaled_paste(img, layer, s, cx, cy, alpha=1.0):
    if s <= 0.01 or alpha <= 0: return
    L = layer.resize((max(1, int(layer.width * s)), max(1, int(layer.height * s))), Image.BICUBIC)
    if alpha < 1:
        a = L.getchannel("A").point(lambda v: int(v * alpha)); L.putalpha(a)
    img.paste(L, (int(cx - L.width / 2), int(cy - L.height / 2)), L)

# ---------------- MAP ----------------
_geo = {}
def geo(name):
    if name not in _geo: _geo[name] = json.load(open(f"{T}/geo/{name}.geojson"))["features"]
    return _geo[name]
def polys(feat):
    g = feat["geometry"]
    if g["type"] == "Polygon": return [g["coordinates"]]
    return g["coordinates"]

def frame_map(spec, t, D):
    img = bg(); base = img
    img = Image.new("RGB", (W, H), (14, 70, 78)); d = ImageDraw.Draw(img, "RGBA")
    v1 = spec.get("view", [-130, 20, -60, 52]); v0 = [-170, -58, 190, 80]
    z = ease(prog(t, 0.0, 1.6))
    lon0, lat0, lon1, lat1 = [a + (b - a) * z for a, b in zip(v0, v1)]
    # fit view into map rect with equal-ish aspect (mercator-ish y)
    mx0, my0, mx1, my1 = 120, 150, 1800, 1000
    def merc(lat): return math.degrees(math.log(math.tan(math.radians(45 + max(min(lat, 84), -84) / 2))))
    Y0, Y1 = merc(lat0), merc(lat1)
    sx = (mx1 - mx0) / (lon1 - lon0); sy = (my1 - my0) / (Y1 - Y0); s = min(sx, sy)
    cx0 = (mx0 + mx1) / 2 - s * (lon0 + lon1) / 2; cy0 = (my0 + my1) / 2 + s * (Y0 + Y1) / 2
    P = lambda lon, lat: (cx0 + s * lon, cy0 - s * merc(lat))
    hl = set(spec.get("countries", [])); hs = set(spec.get("states", []))
    hlp = prog(t, 1.2, 1.8)
    for f in geo("ne_110m_admin_0_countries"):
        nm = f["properties"].get("ADMIN") or f["properties"].get("NAME")
        on = nm in hl
        for poly in polys(f):
            pts = [P(x, y) for x, y in poly[0]]
            if len(pts) < 3: continue
            col = (232, 217, 181, 255)
            if on: col = tuple(int(a + (b - a) * hlp) for a, b in zip((232, 217, 181), GOLD)) + (255,)
            d.polygon(pts, fill=col, outline=(60, 50, 35, 255))
    if hs:
        for f in geo("ne_50m_admin_1_states_provinces"):
            if f["properties"].get("name") in hs:
                for poly in polys(f):
                    pts = [P(x, y) for x, y in poly[0]]
                    if len(pts) > 2: d.polygon(pts, fill=(214, 52, 44, int(200 * hlp)), outline=(60, 20, 15, 255))
    # clip map into rounded frame on textured bg
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([mx0 - 20, my0 - 20, mx1 + 20, my1 + 20], 26, fill=255)
    base.paste(img, (0, 0), m); img = base; d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([mx0 - 20, my0 - 20, mx1 + 20, my1 + 20], 26, outline=(200, 180, 130, 255), width=5)
    # route
    pins = spec.get("pins", [])
    if spec.get("route") and len(pins) >= 2:
        a, b = pins[spec["route"][0]], pins[spec["route"][1]]
        rp = ease(prog(t, 2.0, 3.2)); A = P(a["lon"], a["lat"]); B = P(b["lon"], b["lat"])
        n = 60; pts = []
        for i in range(int(n * rp) + 1):
            u = i / n; x = A[0] + (B[0] - A[0]) * u; y = A[1] + (B[1] - A[1]) * u - math.sin(math.pi * u) * 140
            pts.append((x, y))
        for i in range(0, len(pts) - 1, 2): d.line([pts[i], pts[i + 1]], fill=RED + (255,), width=8)
    # pins
    placed = []
    for i, p in enumerate(pins):
        pp = ease_back(prog(t, 1.5 + 0.35 * i, 2.0 + 0.35 * i))
        if pp <= 0: continue
        x, y = P(p["lon"], p["lat"]); r = 16 * pp
        d.ellipse([x - r * 1.8, y - r * 1.8, x + r * 1.8, y + r * 1.8], fill=(214, 52, 44, 70))
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED + (255,), outline=(255, 255, 255, 255), width=4)
        if pp > 0.6:
            f = font(FB, 34); tw = d.textlength(p["name"], font=f)
            lx = x + 26 if x + 26 + tw + 44 < mx1 + 10 else x - tw - 70
            ly = y - 30
            for _ in range(6):
                r = (lx, ly, lx + tw + 44, ly + 58)
                if not any(not (r[2] < q[0] or r[0] > q[2] or r[3] < q[1] or r[1] > q[3]) for q in placed): break
                ly += 62
            placed.append((lx, ly, lx + tw + 44, ly + 58))
            if ly != y - 30: d.line([(x, y), (lx, ly + 29)], fill=INK + (255,), width=3)
            pill(d, (lx, ly), p["name"], f, fill=INK, fg=CREAM)
    if spec.get("title"):
        a = ease(prog(t, 0.2, 0.8)); f = font(FB, 44)
        pill(d, (140, 40 - (1 - a) * 80), spec["title"], f, fill=RED, fg=(255, 255, 255))
    return img

# ---------------- COUNTER ----------------
def fmt_num(v): return f"{int(round(v)):,}"
def frame_counter(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    a = ease_back(prog(t, 0.0, 0.5))
    card = Image.new("RGBA", (1300, 620), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, 1299, 619], 36, fill=(10, 30, 33, 235), outline=GOLD + (255,), width=6)
    scaled_paste(img, card, 0.6 + 0.4 * a, W / 2, H / 2 + 20, alpha=min(1, a * 1.5))
    if a > 0.7:
        v = spec["value"] * ease(prog(t, 0.4, 2.2))
        txt = spec.get("prefix", "") + fmt_num(v) + spec.get("suffix", "")
        f = font(FS, 210)
        while d.textlength(txt, font=f) > 1180: f = font(FS, f.size - 10)
        ctext(d, W / 2, H / 2 - 120, txt, f, fill=GOLD, stroke=8)
        lab = spec.get("label", "")
        if lab:
            f2 = font(FB, 46); tw = d.textlength(lab, font=f2); pill(d, (W / 2 - tw / 2 - 22, 245), lab, f2, fill=RED, fg=(255, 255, 255))
        if spec.get("sub") and t > 2.3:
            sa = ease(prog(t, 2.3, 2.8)); f3 = font(FB, 52)
            ctext(d, W / 2, H / 2 + 150 + (1 - sa) * 40, spec["sub"], f3, fill=CREAM + (int(255 * sa),), stroke=5)
    return img

# ---------------- TIMELINE ----------------
def frame_timeline(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    items = spec["items"]; n = len(items); x0, x1, y = 200, 1720, 600
    lp = ease(prog(t, 0.1, 0.4 + 0.5 * n))
    d.line([(x0, y), (x0 + (x1 - x0) * lp, y)], fill=CREAM + (255,), width=10)
    if spec.get("title"): pill(d, (140, 60), spec["title"], font(FB, 44), fill=RED, fg=(255, 255, 255))
    for i, (yr, lab) in enumerate(items):
        x = x0 + (x1 - x0) * (i / max(1, n - 1)) if n > 1 else (x0 + x1) / 2
        p = ease_back(prog(t, 0.3 + 0.5 * i, 0.7 + 0.5 * i))
        if p <= 0: continue
        r = 26 * p; d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD + (255,), outline=INK + (255,), width=5)
        up = (i % 2 == 0)
        fy = font(FS, 80); fl = font(FB, 36)
        yy = y - 170 if up else y + 50
        ctext(d, x, yy + (1 - p) * 30, yr, fy, fill=GOLD, stroke=6)
        lines = wrap(d, lab, fl, 330)
        ly = (y - 70 - 44 * len(lines)) if up else y + 150
        if up: ly = y - 60 - 44 * len(lines) - 0
        for j, ln in enumerate(lines):
            ctext(d, x, (yy + 100 + j * 44) if not up else (yy - 50 - (len(lines) - 1 - j) * 44), ln, fl, fill=CREAM, stroke=4)
    return img

# ---------------- QUOTE ----------------
def frame_quote(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    a = ease(prog(t, 0, 0.5))
    d.rounded_rectangle([200, 180, 1720, 900], 40, fill=(10, 30, 33, int(235 * a)), outline=GOLD + (int(255 * a),), width=6)
    ctext(d, 330, 120, "“", font(FS, 300), fill=GOLD, stroke=0)
    f = font(FS, 66); words = spec["text"].split()
    shown = int(len(words) * ease(prog(t, 0.4, max(0.8, D * 0.55))))
    lines = wrap(d, " ".join(words), f, 1300); y = 330; k = 0
    for ln in lines:
        ws = ln.split(); vis = " ".join(ws[:max(0, shown - k)]); k += len(ws)
        tw = d.textlength(ln, font=f); d.text((W / 2 - tw / 2, y), vis, font=f, fill=CREAM, stroke_width=4, stroke_fill=INK); y += 86
    if spec.get("by") and shown >= len(words):
        ctext(d, W / 2, y + 40, "— " + spec["by"], font(FB, 44), fill=GOLD, stroke=4)
    return img

# ---------------- COMPARE ----------------
def frame_compare(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    if spec.get("title"): pill(d, (W / 2 - d.textlength(spec["title"], font=font(FB, 44)) / 2 - 22, 70), spec["title"], font(FB, 44), fill=RED, fg=(255, 255, 255))
    for i, (side, cx) in enumerate([(spec["left"], 520), (spec["right"], 1400)]):
        p = ease_back(prog(t, 0.2 + 0.6 * i, 0.8 + 0.6 * i))
        card = Image.new("RGBA", (760, 560), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, 759, 559], 32, fill=(10, 30, 33, 240), outline=(GOLD if i == 0 else RED) + (255,), width=6)
        f = font(FS, 130)
        while cd.textlength(side[0], font=f) > 680: f = font(FS, f.size - 8)
        tw = cd.textlength(side[0], font=f); cd.text((380 - tw / 2, 150), side[0], font=f, fill=GOLD if i == 0 else (255, 120, 100), stroke_width=6, stroke_fill=INK)
        for j, ln in enumerate(wrap(cd, side[1], font(FB, 40), 660)):
            tw = cd.textlength(ln, font=font(FB, 40)); cd.text((380 - tw / 2, 360 + j * 52), ln, font=font(FB, 40), fill=CREAM)
        scaled_paste(img, card, p, cx, 600, alpha=min(1, p * 1.4))
    if t > 1.6:
        a = ease_back(prog(t, 1.6, 2.0)); f = font(FS, int(110 * a) + 1); ctext(d, W / 2, 530, "VS", f, fill=(255, 255, 255), stroke=8)
    return img

# ---------------- LIST ----------------
def frame_list(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    if spec.get("title"): pill(d, (160, 90), spec["title"], font(FB, 48), fill=RED, fg=(255, 255, 255))
    y = 260
    for i, it in enumerate(spec["items"]):
        p = ease(prog(t, 0.3 + 0.45 * i, 0.7 + 0.45 * i))
        if p <= 0: continue
        x = 220 - (1 - p) * 200
        d.rounded_rectangle([x, y, x + 1480, y + 110], 22, fill=(10, 30, 33, int(235 * p)), outline=GOLD + (int(255 * p),), width=4)
        d.ellipse([x + 25, y + 25, x + 85, y + 85], fill=GOLD + (255,))
        d.text((x + 120, y + 26), it, font=font(FB, 50), fill=CREAM, stroke_width=3, stroke_fill=INK)
        y += 140
    return img

FR = dict(map=frame_map, counter=frame_counter, timeline=frame_timeline, quote=frame_quote, compare=frame_compare, list=frame_list)

def render_fx(spec, D, out):
    n = int(round(D * FPS)); fn = FR[spec["type"]]
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", "noise=alls=6:allf=t,format=yuv420p,fade=in:st=0:d=0.25", "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-r", str(FPS), out], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(fn(spec, i / FPS, D).convert("RGB").tobytes())
    p.stdin.close(); p.wait()
    if p.returncode: raise RuntimeError("fx render failed")

if __name__ == "__main__":
    import sys
    render_fx(json.loads(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
