import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
F=sys.argv[1]; W,H=1280,720
img=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(img)
fb=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',34); ft=ImageFont.truetype(F+'/Anton-Regular.ttf',92)
t="13 TIPOS DE PAPAS FRITAS"; w=d.textlength(t,font=ft); d.text(((W-w)/2,8),t,font=ft,fill=(220,30,30),stroke_width=4,stroke_fill='black')
items=[('f_FF_140.png','Corte clásico'),('f_FF_200.png','Papas paja'),('f_HB_30.png','Rodajas'),
       ('f_HB_60.png','De camote'),('f_HB_100.png','Caseras'),('f_SC_10.png','Onduladas')]
fw,fh=390,230; mask=Image.new('L',(fw,fh),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,fw-1,fh-1),22,fill=255)
for i,(p,lab) in enumerate(items):
    x=25+(i%3)*415; y=140+(i//3)*290
    im=Image.open(p).convert('RGB'); b=im.convert('L').point(lambda v:255 if v>14 else 0).getbbox(); im=im.crop(b)
    im=ImageEnhance.Color(ImageOps.fit(im,(fw,fh),Image.LANCZOS)).enhance(1.3)
    d.rounded_rectangle((x+6,y+8,x+fw+6,y+fh+8),22,fill=(200,200,200)); img.paste(im,(x,y),mask)
    w=d.textlength(lab,font=fb); d.text((x+(fw-w)/2,y+fh+4),lab,font=fb,fill='black')
img.save('v01_thumbnail.jpg',quality=92)
