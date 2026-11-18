import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
F=sys.argv[1]; W,H=1280,720
def load(p):
    im=Image.open(p).convert('RGB'); b=im.convert('L').point(lambda v:255 if v>14 else 0).getbbox(); return im.crop(b)
bg=ImageOps.fit(load('f_MS_330.png'),(W,H),Image.LANCZOS,centering=(0.5,0.35)); bg=ImageEnhance.Color(bg).enhance(1.3)
img=bg.copy(); d=ImageDraw.Draw(img)
ins=ImageOps.fit(load('f_PG_400.png'),(560,330),Image.LANCZOS)
x,y=640,60; d.rounded_rectangle((x-10,y-10,x+570,y+340),22,fill='white'); img.paste(ins,(x,y))
# yellow arrow pointing to inset
d.line((420,520,610,330),fill=(255,230,0),width=34); d.polygon([(650,290),(560,320),(625,385)],fill=(255,230,0))
d.rectangle((0,H-165,W,H),fill='black')
f=ImageFont.truetype(F+'/Anton-Regular.ttf',150); t="“NADIE LO NOTÓ...”"; w=d.textlength(t,font=f)
d.text(((W-w)/2,H-185),t,font=f,fill=(255,236,0),stroke_width=6,stroke_fill='black')
img.save('v01_thumbnail.jpg',quality=92)
