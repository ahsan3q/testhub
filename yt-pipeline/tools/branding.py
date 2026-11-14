"""Generate channel branding: logo (800x800), banner (2560x1440), channel_info.txt per channel."""
import json, math, os, sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
T = os.path.dirname(os.path.abspath(__file__)); F = T + "/fonts"
OUT = sys.argv[1]; FRAMES = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
FS = F + "/AlfaSlabOne-Regular.ttf"; FB = F + "/ArchivoBlack-Regular.ttf"

CH = [
 dict(id="01", name="Leyendas Sin Filtro", handle="@LeyendasSinFiltro", mono="LSF", icon="star",
      c1=(120, 18, 24), c2=(242, 182, 50), tag="Las historias más auténticas de las estrellas de Hollywood",
      desc="Historias reales, anécdotas y respuestas sin filtro de las grandes leyendas del cine clásico. Actores que fueron soldados, estrellas que decían exactamente lo que pensaban y momentos que la televisión nunca volvió a repetir.\n\nEn Leyendas Sin Filtro contamos, en español, las historias detrás de las estrellas de Hollywood: sus guerras, sus películas, sus peleas y sus frases más memorables, con datos verificados y imágenes de archivo.\n\n🎬 Nuevos videos cada semana.\n🔔 Suscríbete y activa la campanita.",
      tags=["leyendas de Hollywood","historias de Hollywood","cine clásico","actores clásicos","anécdotas de famosos","celebridades","Hollywood en español","estrellas de cine","historias reales","biografías"]),
 dict(id="02", name="Voces de Hollywood", handle="@VocesDeHollywood", mono="VH", icon="mic",
      c1=(16, 30, 70), c2=(60, 230, 120), tag="Lo que las leyendas dijeron de otras leyendas",
      desc="¿Qué pensaban realmente las estrellas de Hollywood sobre sus compañeros? En Voces de Hollywood reunimos lo que dijeron las leyendas sobre otras leyendas: elogios, rivalidades, peleas y secretos de rodaje.\n\nBruce Lee, Chuck Norris, Jackie Chan, Steve McQueen y muchos más, contados en español con citas verificadas, contexto histórico e imágenes de archivo.\n\n🎙️ Nuevos videos cada semana.\n🔔 Suscríbete y dinos de qué estrella quieres el próximo video.",
      tags=["leyendas de Hollywood","celebridades","Bruce Lee","artes marciales","historias de famosos","Hollywood en español","cine de acción","actores","entrevistas a famosos","datos de celebridades"]),
 dict(id="03", name="Caricaturas Olvidadas", handle="@CaricaturasOlvidadas", mono="CO", icon="tv",
      c1=(10, 52, 58), c2=(250, 205, 40), tag="Las caricaturas que el tiempo borró",
      desc="Viajamos en el tiempo para recordar las caricaturas de corta vida que casi nadie recuerda: series de los años 40, 50 y 60, estudios que desaparecieron y personajes que merecían más.\n\nEn Caricaturas Olvidadas investigamos la historia oculta de la animación clásica, con datos verificados, imágenes de archivo y mucha nostalgia. ¿Qué año quieres que visitemos después?\n\n📺 Nuevos videos cada semana.\n🔔 Suscríbete y activa la campanita.",
      tags=["caricaturas olvidadas","caricaturas antiguas","caricaturas clásicas","dibujos animados clásicos","animación clásica","historia de la animación","nostalgia","caricaturas de los 60","caricaturas de los 40","series animadas antiguas"]),
 dict(id="04", name="El Baúl de las Caricaturas", handle="@ElBaulDeLasCaricaturas", mono="BC", icon="chest",
      c1=(70, 26, 96), c2=(255, 140, 40), tag="Datos increíbles de las caricaturas clásicas",
      desc="Abrimos el baúl de las caricaturas clásicas para contarte los datos que no sabías: Betty Boop, Los Picapiedra, Popeye, Superman y los personajes que marcaron la historia de la animación.\n\nEn El Baúl de las Caricaturas cada video trae datos verificados, historias detrás de cámaras, demandas, censura y curiosidades, contadas en español con imágenes de archivo.\n\n🧸 Nuevos videos cada semana.\n🔔 Suscríbete y dinos qué personaje quieres que investiguemos.",
      tags=["datos curiosos de caricaturas","caricaturas clásicas","Betty Boop","Los Picapiedra","dibujos animados","historia de la animación","nostalgia","caricaturas antiguas","Hanna-Barbera","Fleischer Studios"]),
 dict(id="05", name="Comerciales del Recuerdo", handle="@ComercialesDelRecuerdo", mono="CR", icon="tv",
      c1=(200, 70, 30), c2=(22, 40, 92), tag="Los anuncios que marcaron una época",
      desc="Los comerciales que todos recordamos… y la verdadera historia de por qué desaparecieron de la televisión. Jingles, mascotas, demandas, leyes y polémicas de la publicidad de los años 60, 70 y 80.\n\nEn Comerciales del Recuerdo te contamos qué pasó con los anuncios más famosos de la historia, con datos verificados y fragmentos de archivo.\n\n📺 Nuevos videos cada semana.\n🔔 Suscríbete y cuéntanos qué comercial recuerdas.",
      tags=["comerciales antiguos","comerciales clásicos","comerciales prohibidos","publicidad antigua","comerciales de los 70","comerciales de los 80","nostalgia","historia de la publicidad","televisión antigua","qué pasó"]),
 dict(id="06", name="Fracasos con Sabor", handle="@FracasosConSabor", mono="FS", icon="fork",
      c1=(20, 90, 50), c2=(240, 60, 45), tag="Las historias detrás de las marcas que fracasaron",
      desc="New Coke, Crystal Pepsi, la hamburguesa con algas y el kétchup morado. En Fracasos con Sabor contamos las historias de los productos y marcas de comida que fracasaron, y lo que realmente salió mal.\n\nNegocios, marketing, decisiones millonarias y errores épicos de la industria de la comida, explicados en español con datos verificados e imágenes de archivo.\n\n🍔 Nuevos videos cada semana.\n🔔 Suscríbete y cuéntanos qué producto extrañas.",
      tags=["fracasos de marcas","productos que fracasaron","historia de marcas","comida rápida","marketing","negocios","Coca-Cola","McDonald's","fracasos empresariales","datos curiosos"]),
]

def icon(d, kind, cx, cy, r, col, bg):
    if kind == "star":
        pts = [(cx + (r if i % 2 == 0 else r * 0.45) * math.cos(math.radians(-90 + i * 36)), cy + (r if i % 2 == 0 else r * 0.45) * math.sin(math.radians(-90 + i * 36))) for i in range(10)]
        d.polygon(pts, fill=col)
    elif kind == "mic":
        d.rounded_rectangle([cx - r * 0.38, cy - r, cx + r * 0.38, cy + r * 0.25], r * 0.38, fill=col)
        d.arc([cx - r * 0.65, cy - r * 0.5, cx + r * 0.65, cy + r * 0.55], 0, 180, fill=col, width=int(r * 0.12))
        d.line([(cx, cy + r * 0.55), (cx, cy + r * 0.9)], fill=col, width=int(r * 0.12)); d.line([(cx - r * 0.4, cy + r * 0.92), (cx + r * 0.4, cy + r * 0.92)], fill=col, width=int(r * 0.12))
    elif kind == "tv":
        d.rounded_rectangle([cx - r, cy - r * 0.65, cx + r, cy + r * 0.75], r * 0.15, fill=col)
        d.rounded_rectangle([cx - r * 0.82, cy - r * 0.48, cx + r * 0.38, cy + r * 0.58], r * 0.18, fill=bg)
        for yy in (-0.25, 0.15): d.ellipse([cx + r * 0.52, cy + r * yy - r * 0.12, cx + r * 0.76, cy + r * yy + r * 0.12], fill=bg)
        d.line([(cx - r * 0.3, cy - r * 0.65), (cx - r * 0.65, cy - r * 1.1)], fill=col, width=int(r * 0.08)); d.line([(cx + r * 0.1, cy - r * 0.65), (cx + r * 0.45, cy - r * 1.1)], fill=col, width=int(r * 0.08))
    elif kind == "chest":
        d.rounded_rectangle([cx - r, cy - r * 0.2, cx + r, cy + r * 0.8], r * 0.08, fill=col)
        d.pieslice([cx - r, cy - r * 0.95, cx + r, cy + r * 0.55], 180, 360, fill=col)
        d.line([(cx - r, cy - r * 0.2), (cx + r, cy - r * 0.2)], fill=bg, width=int(r * 0.08))
        d.rounded_rectangle([cx - r * 0.16, cy - r * 0.35, cx + r * 0.16, cy + r * 0.05], r * 0.05, fill=bg)
    elif kind == "fork":
        for k in (-0.3, -0.1, 0.1, 0.3): d.line([(cx - r * 0.45 + k * r, cy - r), (cx - r * 0.45 + k * r, cy - r * 0.35)], fill=col, width=int(r * 0.09))
        d.rounded_rectangle([cx - r * 0.82, cy - r * 0.42, cx - r * 0.08, cy - r * 0.2], r * 0.1, fill=col)
        d.rounded_rectangle([cx - r * 0.53, cy - r * 0.3, cx - r * 0.37, cy + r], r * 0.08, fill=col)
        d.ellipse([cx + r * 0.2, cy - r, cx + r * 0.7, cy - r * 0.05], fill=col)
        d.rounded_rectangle([cx + r * 0.37, cy - r * 0.2, cx + r * 0.53, cy + r], r * 0.08, fill=col)

def fit(d, text, path, size, maxw):
    while size > 10:
        f = ImageFont.truetype(path, size)
        if d.textlength(text, font=f) <= maxw: return f
        size -= 4
    return ImageFont.truetype(path, size)

for c in CH:
    od = f"{OUT}/{c['id']}"; os.makedirs(od, exist_ok=True)
    # ---- logo ----
    S = 800; L = Image.new("RGB", (S, S), c["c1"]); d = ImageDraw.Draw(L)
    for i in range(24):  # sunburst
        a0 = i * 15; pts = [(S / 2, S / 2)] + [(S / 2 + 900 * math.cos(math.radians(a)), S / 2 + 900 * math.sin(math.radians(a))) for a in (a0, a0 + 7.5)]
        d.polygon(pts, fill=tuple(min(255, int(v * 1.18 + 8)) for v in c["c1"]))
    d.ellipse([40, 40, S - 40, S - 40], outline=c["c2"], width=26)
    d.ellipse([84, 84, S - 84, S - 84], outline=(255, 245, 225), width=6)
    icon(d, c["icon"], S / 2, S / 2 - 95, 120, c["c2"], c["c1"])
    f = fit(d, c["mono"], FS, 200, 520)
    tw = d.textlength(c["mono"], font=f); d.text((S / 2 - tw / 2, S / 2 + 20), c["mono"], font=f, fill=(255, 245, 225), stroke_width=8, stroke_fill=(20, 15, 10))
    L.save(f"{od}/logo_800x800.png")
    # ---- banner ----
    BW, BH = 2560, 1440
    B = Image.new("RGB", (BW, BH), tuple(int(v * 0.55) for v in c["c1"])); bd = ImageDraw.Draw(B)
    for i in range(36):
        a0 = i * 10; pts = [(BW / 2, BH / 2)] + [(BW / 2 + 3000 * math.cos(math.radians(a)), BH / 2 + 3000 * math.sin(math.radians(a))) for a in (a0, a0 + 5)]
        bd.polygon(pts, fill=tuple(int(v * 0.7) for v in c["c1"]))
    fr = FRAMES.get(c["id"], [])
    for k, p in enumerate(fr[:6]):  # film frames on the sides (outside safe area)
        im = ImageOps.fit(Image.open(p).convert("RGB"), (330, 248)); x = 60 + (k % 3) * 0 if k < 3 else BW - 390
        x = 60 if k < 3 else BW - 390; y = 220 + (k % 3) * 340
        bd.rectangle([x - 14, y - 14, x + 344, y + 262], fill=(20, 16, 12)); B.paste(im, (x, y))
    sx0, sy0 = (BW - 1546) // 2, (BH - 423) // 2
    bd.rounded_rectangle([sx0 - 40, sy0 - 30, sx0 + 1586, sy0 + 453], 40, fill=(245, 236, 214), outline=c["c2"], width=14)
    fn = fit(bd, c["name"], FS, 170, 1440)
    tw = bd.textlength(c["name"], font=fn); bd.text((BW / 2 - tw / 2, sy0 + 40), c["name"], font=fn, fill=c["c1"], stroke_width=4, stroke_fill=(30, 20, 10))
    ft = fit(bd, c["tag"], FB, 64, 1400)
    tw = bd.textlength(c["tag"], font=ft); bd.text((BW / 2 - tw / 2, sy0 + 270), c["tag"], font=ft, fill=(30, 25, 20))
    fs2 = ImageFont.truetype(FB, 40); t3 = "NUEVOS VIDEOS CADA SEMANA"
    tw = bd.textlength(t3, font=fs2); bd.rounded_rectangle([BW / 2 - tw / 2 - 30, sy0 + 360, BW / 2 + tw / 2 + 30, sy0 + 425], 20, fill=c["c2"])
    bd.text((BW / 2 - tw / 2, sy0 + 368), t3, font=fs2, fill=(255, 255, 255) if sum(c["c2"]) < 300 else (20, 15, 10))
    B.save(f"{od}/banner_2560x1440.png")
    # ---- info ----
    info = f"""NOMBRE DEL CANAL:
{c['name']}

HANDLE SUGERIDO:
{c['handle']}
(si no está disponible, prueba agregando "TV", "Oficial" o "ES" al final)

LEMA:
{c['tag']}

DESCRIPCIÓN DEL CANAL:
{c['desc']}

PALABRAS CLAVE / TAGS DEL CANAL (YouTube Studio > Configuración > Canal):
{", ".join(c['tags'])}

PAÍS RECOMENDADO: el tuyo · IDIOMA DEL CANAL: Español
ARCHIVOS:
- logo_800x800.png → foto de perfil
- banner_2560x1440.png → imagen del banner (el texto está dentro del área segura de 1546x423)
"""
    open(f"{od}/channel_info.txt", "w").write(info)
    print("ok", c["id"], c["name"])
