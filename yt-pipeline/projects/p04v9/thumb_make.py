import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter
F = sys.argv[1]; W, H = 1280, 720
bg = ImageOps.fit(Image.open('f_FF_30.png').convert('L'), (W, H), Image.LANCZOS)
bg = ImageOps.colorize(ImageEnhance.Contrast(bg).enhance(0.8), (60, 45, 30), (235, 220, 190)).filter(ImageFilter.GaussianBlur(2))
img = bg.convert('RGB'); d = ImageDraw.Draw(img)
f = ImageFont.truetype(F + '/Anton-Regular.ttf', 230)
t = "OLVIDADO"; w = d.textlength(t, font=f)
d.text(((W - w) / 2, -40), t, font=f, fill=(255, 226, 0), stroke_width=10, stroke_fill='black')
fx = Image.open('f_BK_30.png').convert('RGB'); fw, fh = fx.size
fx = fx.crop((int(fw * 0.25), int(fh * 0.05), int(fw * 0.85), int(fh * 0.98)))
fx = ImageEnhance.Contrast(fx).enhance(1.15); fx = ImageEnhance.Color(fx).enhance(1.2)
th = 470; fx = fx.resize((int(fx.width * th / fx.height), th), Image.LANCZOS)
x = (W - fx.width) // 2; y = H - th - 20
d.rounded_rectangle((x - 12, y - 12, x + fx.width + 12, y + th + 12), 24, fill='black')
m = Image.new('L', fx.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, fx.width, th), 18, fill=255)
img.paste(fx, (x, y), m)
fb = ImageFont.truetype(F + '/Anton-Regular.ttf', 66)
for (tx, ty, s) in [(40, 330, "1919"), (W - 230, 330, "1933")]:
    d.rectangle((tx - 10, ty, tx + 190, ty + 90), fill=(205, 25, 30), outline='black', width=5)
    ww = d.textlength(s, font=fb); d.text((tx + 90 - ww / 2, ty + 2), s, font=fb, fill='white', stroke_width=3, stroke_fill='black')
img.save('v01_thumbnail.jpg', quality=92)
