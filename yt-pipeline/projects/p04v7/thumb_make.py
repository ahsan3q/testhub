import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
F=sys.argv[1]; W,H=1280,720
im=Image.open('f_PE_311.png').convert('RGB'); b=im.convert('L').point(lambda v:255 if v>14 else 0).getbbox(); im=im.crop(b)
img=ImageOps.fit(im,(W,H),Image.LANCZOS,centering=(0.45,0.15)); img=ImageEnhance.Color(img).enhance(1.25)
d=ImageDraw.Draw(img); f=ImageFont.truetype(F+'/Anton-Regular.ttf',210)
t="SE ACABÓ"; w=d.textlength(t,font=f)
d.text(((W-w)/2+8,H-300+10),t,font=f,fill='black',stroke_width=12,stroke_fill='black')
d.text(((W-w)/2,H-300),t,font=f,fill=(255,236,0),stroke_width=10,stroke_fill='black')
img.save('v01_thumbnail.jpg',quality=92)
