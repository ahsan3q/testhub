import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps, ImageFilter
F=sys.argv[1]; W,H=1280,720
def load(p):
    im=Image.open(p).convert('RGB'); b=im.convert('L').point(lambda v:255 if v>14 else 0).getbbox(); return im.crop(b)
a=ImageOps.fit(load('f_TE_1000.png'),(800,H),Image.LANCZOS,centering=(0.5,0.4))
b=ImageOps.fit(load('f_TE_1200.png'),(480,H),Image.LANCZOS,centering=(0.42,0.5))
img=Image.new('RGB',(W,H)); img.paste(a,(0,0)); img.paste(b,(800,0))
img=ImageEnhance.Contrast(ImageEnhance.Color(img).enhance(1.25)).enhance(1.12).filter(ImageFilter.SHARPEN)
warm=Image.new('RGB',(W,H),(255,170,60)); img=Image.blend(img,warm,0.10)
d=ImageDraw.Draw(img); d.rectangle((796,0,804,H),fill=(255,214,60)); f=ImageFont.truetype(F+'/Anton-Regular.ttf',150)
t="SIN FILTRO"; w=d.textlength(t,font=f)
d.text((W-w-40,H-205),t,font=f,fill=(255,214,60),stroke_width=9,stroke_fill='black')
img.save('v01_thumbnail.jpg',quality=92)
