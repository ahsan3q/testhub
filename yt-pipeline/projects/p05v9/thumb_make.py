import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
F=sys.argv[1]; W,H=1280,720
img=Image.new('RGB',(W,H),(246,238,220)); d=ImageDraw.Draw(img)
def load(p):
    im=Image.open(p).convert('RGB'); b=im.convert('L').point(lambda v:255 if v>18 else 0).getbbox(); return im.crop(b)
tiles=[('f_MH_20.png','PAUL LYNDE'),('f_M5_60.png','MAXWELL HOUSE'),('f_F2_25.png','FOLGERS'),
       ('f_JL_20.png','JELL-O'),('f_CC_20.png','COCA-COLA'),('f_GI_30.png','GILLETTE')]
fc=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',24)
tw,th=410,215
for i,(p,cap) in enumerate(tiles):
    x=15+(i%3)*422; y=12+(i//3)*228
    im=ImageEnhance.Color(ImageOps.fit(load(p),(tw,th),Image.LANCZOS)).enhance(1.25)
    d.rectangle((x-4,y-4,x+tw+4,y+th+4),fill='black'); img.paste(im,(x,y))
    d.multiline_text((x+10,y+8),cap,font=fc,fill=(255,236,0),stroke_width=4,stroke_fill='black',spacing=2)
d.rectangle((0,476,W,H),fill=(246,238,220)); d.line((0,476,W,476),fill='black',width=6)
f1=ImageFont.truetype(F+'/Anton-Regular.ttf',118); f2=ImageFont.truetype(F+"/Anton-Regular.ttf",84)
d.text((30,470),"COMERCIALES",font=f1,fill=(205,25,30),stroke_width=3,stroke_fill='black')
d.text((30,595),"DE LOS 60 QUE HOY NO VERÍAS",font=f2,fill=(25,35,90),stroke_width=2,stroke_fill='black')
# badge
cx,cy,r=1120,600,105; d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(255,214,0),outline='black',width=6)
fb=ImageFont.truetype(F+'/Anton-Regular.ttf',52)
for j,t in enumerate(["¿QUÉ","PASÓ?"]):
    w=d.textlength(t,font=fb); d.text((cx-w/2,cy-62+j*58),t,font=fb,fill=(205,25,30),stroke_width=2,stroke_fill='black')
img.save('v01_thumbnail.jpg',quality=92)
