import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from rembg import remove
F=sys.argv[1]; W,H=1280,720
img=Image.new('RGB',(W,H),'white')
def cut(p,crop=None):
    im=Image.open(p).convert('RGB')
    if crop: w,h=im.size; im=im.crop((int(w*crop[0]),int(h*crop[1]),int(w*crop[2]),int(h*crop[3])))
    c=remove(im); bb=c.getchannel('A').point(lambda v:255 if v>40 else 0).getbbox(); return c.crop(bb)
def place(c,h,cx,yb,shadow=True):
    s=h/c.height; c=c.resize((int(c.width*s),h),Image.LANCZOS)
    x=int(cx-c.width/2); y=yb-h
    if shadow:
        sh=Image.new('RGBA',c.size,(0,0,0,0)); sh.paste((0,0,0,90),mask=c.getchannel('A')); sh=sh.filter(ImageFilter.GaussianBlur(10))
        img.paste(sh,(x+10,y+12),sh)
    img.paste(c,(x,y),c)
place(cut('g_HB_636.png',(0,0,0.78,1)),540,930,725)
place(cut('g_GR_460.png',(0.12,0,0.88,1)),600,420,730)
d=ImageDraw.Draw(img)
f=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',80)
t1,t2="CARICATURAS ","SECRETAS"
w1=d.textlength(t1,font=f); w2=d.textlength(t2,font=f); x=(W-w1-w2)/2; y=18
for dx,dy in [(8,10)]:
    d.text((x+dx,y+dy),t1+t2,font=f,fill='black',stroke_width=10,stroke_fill='black')
d.text((x,y),t1,font=f,fill='white',stroke_width=8,stroke_fill='black')
d.text((x+w1,y),t2,font=f,fill=(255,230,0),stroke_width=8,stroke_fill='black')
img.save('v01_thumbnail.jpg',quality=92)
