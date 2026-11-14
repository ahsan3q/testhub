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
CTX = {}
_bgcache = {}
def _texture():
    global BG
    if BG is None:
        base = Image.new("RGB", (W, H), (8, 36, 40))
        tex = Image.open(f"{T}/assets/bg_texture.png")
        base.paste(tex, (0, 0), tex); BG = base
    return BG
def bg():
    """Background: blurred, tinted still from the segment's own footage (slow Ken Burns), else texture."""
    path = CTX.get("bg")
    if not path or not os.path.exists(path):
        return _texture().copy()
    if path not in _bgcache:
        im = Image.open(path).convert("RGB")
        im = im.resize((int(W * 1.12), int(H * 1.12)), Image.BICUBIC).filter(ImageFilter.GaussianBlur(22))
        a = np.asarray(im).astype(np.float32) / 255
        tint = np.array([0.05, 0.20, 0.22], np.float32)
        a = a * 0.62 + tint * 0.30
        yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
        v = 1 - 0.55 * np.clip(np.sqrt(((xx - a.shape[1] / 2) / a.shape[1]) ** 2 + ((yy - a.shape[0] / 2) / a.shape[0]) ** 2) * 1.6 - 0.25, 0, 1)
        a = a * v[..., None]
        im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
        tex = Image.open(f"{T}/assets/bg_texture.png")
        tex = tex.resize(im.size)
        im.paste(tex, (0, 0), tex)
        _bgcache[path] = im
    im = _bgcache[path]
    u = CTX.get("t", 0) / max(CTX.get("D", 1), 0.1)
    s = 1.0 - 0.07 * u
    w, h = int(im.width * s), int(im.height * s)
    x0 = int((im.width - w) * (0.5 + 0.3 * (u - 0.5))); y0 = int((im.height - h) / 2)
    return im.crop((x0, y0, x0 + w, y0 + h)).resize((W, H), Image.BILINEAR)

def camera(img, t, D):
    """Global keyframe: subtle push-in over the whole graphic."""
    s = 1.0 + 0.035 * ease_io(min(t / max(D, 0.1), 1))
    if s <= 1.001: return img
    w, h = int(W / s), int(H / s)
    return img.crop(((W - w) // 2, (H - h) // 2, (W - w) // 2 + w, (H - h) // 2 + h)).resize((W, H), Image.BILINEAR)

def ease(t): t = min(max(t, 0), 1); return 1 - (1 - t) ** 3
def ease_back(t):
    t = min(max(t, 0), 1); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def ease_io(t):
    t = min(max(t, 0), 1); return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2
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
    base = bg()
    img = Image.new("RGB", (W, H), (16, 62, 74)); d = ImageDraw.Draw(img, "RGBA")
    v1 = spec.get("view", [-130, 20, -60, 52]); v0 = spec.get("from", [-170, -58, 190, 80])
    z = ease_io(prog(t, 0.0, 2.0))
    # keep pushing in slowly after arriving (keyframed drift)
    push = 0.06 * prog(t, 2.0, D)
    lon0, lat0, lon1, lat1 = [a + (b - a) * z for a, b in zip(v0, v1)]
    cl, ct = (lon0 + lon1) / 2, (lat0 + lat1) / 2
    lon0, lon1 = cl + (lon0 - cl) * (1 - push), cl + (lon1 - cl) * (1 - push)
    lat0, lat1 = ct + (lat0 - ct) * (1 - push), ct + (lat1 - ct) * (1 - push)
    mx0, my0, mx1, my1 = 110, 140, 1810, 1010
    def merc(lat): return math.degrees(math.log(math.tan(math.radians(45 + max(min(lat, 84), -84) / 2))))
    Y0, Y1 = merc(lat0), merc(lat1)
    sx = (mx1 - mx0) / (lon1 - lon0); sy = (my1 - my0) / (Y1 - Y0); sc = min(sx, sy)
    cx0 = (mx0 + mx1) / 2 - sc * (lon0 + lon1) / 2; cy0 = (my0 + my1) / 2 + sc * (Y0 + Y1) / 2
    P = lambda lon, lat: (cx0 + sc * lon, cy0 - sc * merc(lat))
    # graticule
    step = 30 if (lon1 - lon0) > 120 else (10 if (lon1 - lon0) > 30 else 5)
    for g in range(-180, 181, step):
        x = P(g, 0)[0]; d.line([(x, my0 - 40), (x, my1 + 40)], fill=(255, 255, 255, 22), width=1)
    for g in range(-80, 81, step):
        y = P(0, g)[1]; d.line([(mx0 - 40, y), (mx1 + 40, y)], fill=(255, 255, 255, 22), width=1)
    hl = set(spec.get("countries", [])); hs = set(spec.get("states", []))
    hlp = prog(t, 1.3, 2.0)
    glow = []
    for f in geo("ne_110m_admin_0_countries"):
        nm = f["properties"].get("ADMIN") or f["properties"].get("NAME")
        on = nm in hl
        for poly in polys(f):
            pts = [P(x, y) for x, y in poly[0]]
            if len(pts) < 3: continue
            col = (226, 212, 178, 255)
            if on:
                col = tuple(int(a + (b - a) * hlp) for a, b in zip((226, 212, 178), GOLD)) + (255,)
                glow.append(pts)
            d.polygon(pts, fill=col, outline=(70, 58, 40, 255))
    if hs:
        for f in geo("ne_50m_admin_1_states_provinces"):
            if f["properties"].get("name") in hs:
                for poly in polys(f):
                    pts = [P(x, y) for x, y in poly[0]]
                    if len(pts) > 2:
                        d.polygon(pts, fill=(214, 52, 44, int(190 * hlp)), outline=(90, 20, 15, 255))
                        glow.append(pts)
    # pulsing outline on highlighted areas
    if glow and hlp > 0:
        pw = 3 + 3 * (0.5 + 0.5 * math.sin(t * 5))
        for pts in glow: d.line(pts + [pts[0]], fill=(255, 245, 210, int(200 * hlp)), width=int(pw))
    m = Image.new("L", (W, H), 0); ImageDraw.Draw(m).rounded_rectangle([mx0 - 20, my0 - 20, mx1 + 20, my1 + 20], 26, fill=255)
    base.paste(img, (0, 0), m); img = base; d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([mx0 - 20, my0 - 20, mx1 + 20, my1 + 20], 26, outline=(205, 185, 135, 255), width=5)
    pins = spec.get("pins", [])
    # multi-leg route with travelling marker
    route = spec.get("route") or []
    if len(route) >= 2 and len(pins) >= 2:
        legs = list(zip(route[:-1], route[1:])); nl = len(legs)
        rp_all = ease_io(prog(t, 2.0, min(D - 0.6, 2.0 + 1.4 * nl)))
        for li, (ia, ib) in enumerate(legs):
            lp = min(max(rp_all * nl - li, 0), 1)
            if lp <= 0: continue
            A = P(pins[ia]["lon"], pins[ia]["lat"]); B = P(pins[ib]["lon"], pins[ib]["lat"])
            dist = math.hypot(B[0] - A[0], B[1] - A[1]); arc = min(160, dist * 0.25)
            n = 80; pts = []
            for i in range(int(n * lp) + 1):
                u = i / n; pts.append((A[0] + (B[0] - A[0]) * u, A[1] + (B[1] - A[1]) * u - math.sin(math.pi * u) * arc))
            if len(pts) > 1:
                d.line(pts, fill=(255, 255, 255, 230), width=12)
                d.line(pts, fill=RED + (255,), width=7)
                hx, hy = pts[-1]
                if lp < 1:
                    d.ellipse([hx - 14, hy - 14, hx + 14, hy + 14], fill=(255, 255, 255, 255))
                    d.ellipse([hx - 8, hy - 8, hx + 8, hy + 8], fill=RED + (255,))
    placed = []
    for i, p in enumerate(pins):
        pp = ease_back(prog(t, 1.6 + 0.4 * i, 2.1 + 0.4 * i))
        if pp <= 0: continue
        x, y = P(p["lon"], p["lat"]); y -= (1 - min(pp, 1)) * 70
        # expanding pulse rings (loop)
        for k in range(2):
            ph = ((t - 1.6 - 0.4 * i) * 0.9 + k * 0.5) % 1.0
            rr = 18 + 60 * ph
            d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=(214, 52, 44, int(200 * (1 - ph))), width=4)
        r = 17 * pp
        d.ellipse([x - r, y - r, x + r, y + r], fill=RED + (255,), outline=(255, 255, 255, 255), width=5)
        if pp > 0.6:
            f = font(FB, 34); full = p["name"]
            nchar = int(len(full) * ease(prog(t, 2.0 + 0.4 * i, 2.6 + 0.4 * i)))
            txt = full[:max(1, nchar)]
            tw = d.textlength(full, font=f)
            lx = x + 30 if x + 30 + tw + 44 < mx1 + 10 else x - tw - 74
            ly = y - 30
            for _ in range(6):
                rct = (lx, ly, lx + tw + 44, ly + 58)
                if not any(not (rct[2] < q[0] or rct[0] > q[2] or rct[3] < q[1] or rct[1] > q[3]) for q in placed): break
                ly += 62
            placed.append((lx, ly, lx + tw + 44, ly + 58))
            if ly != y - 30: d.line([(x, y), (lx, ly + 29)], fill=INK + (255,), width=3)
            d.rounded_rectangle([lx, ly, lx + tw + 44, ly + 58], 12, fill=INK + (235,))
            d.text((lx + 22, ly + 10), txt, font=f, fill=CREAM)
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

# ---------------- BARS (animated bar chart) ----------------
def frame_bars(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    items = spec["items"]; n = len(items)
    if spec.get("title"):
        a = ease(prog(t, 0.0, 0.5)); pill(d, (140, 60 - (1 - a) * 80), spec["title"], font(FB, 44), fill=RED, fg=(255, 255, 255))
    vmax = max(v for _, v in items) or 1
    top, rowh = 230, min(150, 720 // max(n, 1))
    x0, xmax = 520, 1360
    for i, (lab, v) in enumerate(items):
        y = top + i * rowh
        p = ease_io(prog(t, 0.3 + 0.35 * i, 1.5 + 0.35 * i))
        f = font(FB, 44)
        lw = d.textlength(lab, font=f)
        d.text((x0 - 30 - lw, y + rowh * 0.5 - 30), lab, font=f, fill=CREAM, stroke_width=3, stroke_fill=INK)
        bw = (xmax - x0) * (v / vmax) * p
        col = spec.get("colors", [GOLD, RED, (90, 180, 170), (230, 140, 60)])[i % 4]
        d.rounded_rectangle([x0, y + rowh * 0.18, x0 + max(bw, 6), y + rowh * 0.82], 14, fill=tuple(col) + (245,))
        val = spec.get("prefix", "") + fmt_num(v * p) + spec.get("suffix", "")
        fv = font(FS, 54)
        d.text((x0 + bw + 20, y + rowh * 0.5 - 36), val, font=fv, fill=(255, 255, 255), stroke_width=5, stroke_fill=INK)
    if spec.get("note") and t > 1.2 + 0.35 * n:
        a = ease(prog(t, 1.2 + 0.35 * n, 1.7 + 0.35 * n))
        ctext(d, W / 2, 960 + (1 - a) * 30, spec["note"], font(FB, 40), fill=CREAM, stroke=4)
    return img

# ---------------- HEADLINE (newspaper clipping) ----------------
_paper = {}
def paper_card(w, h):
    if (w, h) not in _paper:
        rng = np.random.default_rng(3)
        a = np.ones((h, w, 3), np.float32) * np.array([0.93, 0.89, 0.80], np.float32)
        a += rng.normal(0, 0.025, (h, w, 1)).astype(np.float32)
        yy, xx = np.mgrid[0:h, 0:w]
        a *= (1 - 0.18 * (((xx - w / 2) / w) ** 2 + ((yy - h / 2) / h) ** 2))[..., None]
        _paper[(w, h)] = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    return _paper[(w, h)].copy()

def frame_headline(spec, t, D):
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    cw, chh = 1300, 760
    card = paper_card(cw, chh); cd = ImageDraw.Draw(card)
    fp = font(FS, 70); name = spec.get("paper", "EL DIARIO")
    tw = cd.textlength(name, font=fp); cd.text((cw / 2 - tw / 2, 40), name, font=fp, fill=(30, 26, 20))
    cd.line([(60, 140), (cw - 60, 140)], fill=(30, 26, 20), width=4); cd.line([(60, 150), (cw - 60, 150)], fill=(30, 26, 20), width=2)
    fd = font(FB, 30); dt = spec.get("date", "")
    if dt: tw = cd.textlength(dt, font=fd); cd.text((cw / 2 - tw / 2, 162), dt, font=fd, fill=(60, 50, 40))
    words = spec["headline"].split()
    shown = int(len(words) * ease(prog(t, 0.7, 0.7 + 0.18 * len(words))))
    fh = font(FS, 92); lines = wrap(cd, spec["headline"], fh, cw - 140)
    while len(lines) > 3: fh = font(FS, fh.size - 8); lines = wrap(cd, spec["headline"], fh, cw - 140)
    y = 230; k = 0
    for ln in lines:
        ws = ln.split(); vis = " ".join(ws[:max(0, shown - k)]); k += len(ws)
        lw = cd.textlength(ln, font=fh); cd.text((cw / 2 - lw / 2, y), vis, font=fh, fill=(20, 16, 12)); y += fh.size + 16
    if spec.get("sub") and shown >= len(words):
        fs2 = font(FB, 36)
        for j, ln in enumerate(wrap(cd, spec["sub"], fs2, cw - 200)[:3]):
            lw = cd.textlength(ln, font=fs2); cd.text((cw / 2 - lw / 2, y + 20 + j * 48), ln, font=fs2, fill=(70, 60, 48))
    for k2 in range(3):
        yy = chh - 130 + k2 * 26; cd.line([(80, yy), (cw - 80, yy)], fill=(150, 140, 120), width=8)
    a = ease_back(prog(t, 0.0, 0.6))
    rot = -3 + 2 * (1 - a)
    big = card.rotate(rot, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", big.size, (0, 0, 0, 0)); sh.putalpha(big.getchannel("A").point(lambda v: int(v * 0.5)))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    scaled_paste(img, sh, 0.7 + 0.3 * a, W / 2 + 18, H / 2 + 34, alpha=min(1, a))
    scaled_paste(img, big, 0.7 + 0.3 * a, W / 2, H / 2 + 10, alpha=min(1, a * 1.3))
    if spec.get("stamp") and t > 1.2 + 0.18 * len(words):
        sp = ease_back(prog(t, 1.2 + 0.18 * len(words), 1.6 + 0.18 * len(words)))
        fs = font(FB, 64); txt = spec["stamp"]; tw = d.textlength(txt, font=fs)
        st = Image.new("RGBA", (int(tw + 80), 130), (0, 0, 0, 0)); sd2 = ImageDraw.Draw(st)
        sd2.rounded_rectangle([4, 4, st.width - 4, 126], 16, outline=RED + (255,), width=8)
        sd2.text((40, 26), txt, font=fs, fill=RED + (255,))
        st = st.rotate(12, expand=True, resample=Image.BICUBIC)
        scaled_paste(img, st, 1.6 - 0.6 * sp, W / 2 + 380, H / 2 + 250, alpha=min(1, sp))
    return img

# ---------------- PHOTO (keyframed zoom + highlight on a real frame) ----------------
_ph = {}
def frame_photo(spec, t, D):
    path = spec.get("_img")
    if not path or not os.path.exists(path): return bg()
    if path not in _ph: _ph[path] = Image.open(path).convert("RGB")
    src = _ph[path]
    fx, fy = spec.get("focus", [0.5, 0.45]); zmax = spec.get("zoom", 1.6)
    u = ease_io(prog(t, 0.2, D * 0.75))
    z = 1.0 + (zmax - 1.0) * u
    sw, sh = src.width / z, src.height / z
    cx = src.width * (0.5 + (fx - 0.5) * u); cy = src.height * (0.5 + (fy - 0.5) * u)
    x0 = min(max(cx - sw / 2, 0), src.width - sw); y0 = min(max(cy - sh / 2, 0), src.height - sh)
    fr = src.crop((int(x0), int(y0), int(x0 + sw), int(y0 + sh))).resize((1500, 844), Image.BICUBIC)
    img = bg(); d = ImageDraw.Draw(img, "RGBA")
    m = Image.new("L", fr.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, fr.width - 1, fr.height - 1], 28, fill=255)
    ox, oy = (W - fr.width) // 2, 140
    d.rounded_rectangle([ox - 10, oy - 10, ox + fr.width + 10, oy + fr.height + 10], 32, fill=(0, 0, 0, 120))
    img.paste(fr, (ox, oy), m); d = ImageDraw.Draw(img, "RGBA")
    if spec.get("circle", True):
        cp = ease(prog(t, D * 0.55, D * 0.75))
        if cp > 0:
            px = ox + (src.width * fx - x0) / sw * fr.width; py = oy + (src.height * fy - y0) / sh * fr.height
            r = spec.get("r", 150)
            d.arc([px - r, py - r * 0.8, px + r, py + r * 0.8], -90, -90 + 360 * cp, fill=RED + (255,), width=10)
    if spec.get("label"):
        a = ease(prog(t, 0.3, 0.8)); f = font(FB, 44)
        pill(d, (ox + 20, oy + fr.height - 30 + (1 - a) * 60), spec["label"], f, fill=GOLD, fg=INK)
    if spec.get("title"):
        a = ease(prog(t, 0.1, 0.6)); pill(d, (140, 36 - (1 - a) * 80), spec["title"], font(FB, 44), fill=RED, fg=(255, 255, 255))
    return img

FR = dict(map=frame_map, counter=frame_counter, timeline=frame_timeline, quote=frame_quote, compare=frame_compare, list=frame_list,
          bars=frame_bars, headline=frame_headline, photo=frame_photo)

def render_fx(spec, D, out, bgimg=None):
    n = int(round(D * FPS)); fn = FR[spec["type"]]
    CTX["bg"] = bgimg or spec.get("_bg"); CTX["D"] = D
    p = subprocess.Popen(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", f"noise=alls=6:allf=t,format=yuv420p,fade=in:st=0:d=0.25,fade=out:st={max(0, D - 0.22):.2f}:d=0.22", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", str(FPS), out], stdin=subprocess.PIPE)
    for i in range(n):
        CTX["t"] = i / FPS
        fr = fn(spec, i / FPS, D).convert("RGB")
        p.stdin.write(camera(fr, i / FPS, D).tobytes())
    p.stdin.close(); p.wait()
    if p.returncode: raise RuntimeError("fx render failed")

if __name__ == "__main__":
    import sys
    render_fx(json.loads(sys.argv[1]), float(sys.argv[2]), sys.argv[3])
