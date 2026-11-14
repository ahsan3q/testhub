import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
F=sys.argv[1]; W,H=1280,720
NAVY=(18,36,90); RED=(196,24,28)
def L(n,box=None):
    im=Image.open(n).convert('RGB')
    bb=im.convert('L').point(lambda v:255 if v>22 else 0).getbbox()
    if bb: im=im.crop(bb)
    if box:
        w,h=im.size; im=im.crop((int(w*box[0]),int(h*box[1]),int(w*box[2]),int(h*box[3])))
    return im
bg=ImageOps.fit(L('g_SA_19.png',(0.0,0.0,1,0.8)),(W,H)).filter(ImageFilter.GaussianBlur(6))
bg=ImageEnhance.Brightness(bg).enhance(0.75); img=bg.copy(); d=ImageDraw.Draw(img)
def card(im,box,size,rot=0):
    im=ImageEnhance.Color(im).enhance(1.25); im=ImageOps.fit(im,size,Image.LANCZOS)
    fr=Image.new('RGB',(size[0]+12,size[1]+12),'white'); fr.paste(im,(6,6))
    fr=fr.convert('RGBA').rotate(rot,expand=True,resample=Image.BICUBIC)
    sh=Image.new('RGBA',fr.size,(0,0,0,0)); sh.paste((0,0,0,120),mask=fr.split()[3])
    sh=sh.filter(ImageFilter.GaussianBlur(8)); img.paste(sh,(box[0]+8,box[1]+10),sh); img.paste(fr,box,fr)
# woman right
wm=ImageOps.fit(L('g_TB2_13.png',(0.0,0.0,1,1)),(470,720),Image.LANCZOS,centering=(0.45,0.5))
wm=ImageEnhance.Color(wm).enhance(1.2)
mask=Image.new('L',(470,720),255); md=ImageDraw.Draw(mask)
for i in range(60): md.line([(i,0),(i,720)],fill=int(255*i/60))
img.paste(wm,(810,0),mask)
card(L('g_PR_29.png',(0.06,0.02,0.94,0.5)),(250,70),(250,160),-4)
card(L('g_TB_29.png',(0.28,0.0,0.72,0.66)),(520,40),(170,230),3)
card(L('g_WC2_26.png',(0.2,0.05,0.8,0.85)),(40,240),(230,200),-3)
card(L('g_HO_28.png',(0.06,0.3,0.94,0.75)),(300,270),(250,140),2)
card(L('g_RB3_29.png',(0.12,0.05,0.88,0.7)),(580,290),(200,170),-2)
# text box
d=ImageDraw.Draw(img)
d.rounded_rectangle([34,478,850,692],12,fill='white')
fb=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',74)
t1="COMIDAS DE LOS 80"; t2="PROHIBIDAS O PERDIDAS"
def fit(t,sz,maxw):
    f=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',sz)
    while d.textlength(t,font=f)>maxw: sz-=2; f=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',sz)
    return f
f1=fit(t1,86,780); f2=fit(t2,80,780)
d.text((442,488),t1,font=f1,fill=NAVY,anchor='ma'); d.text((442,592),t2,font=f2,fill=RED,anchor='ma')
# dotted border
for x in range(8,W,18): d.ellipse([x-3,7,x+3,13],fill='white'); d.ellipse([x-3,H-13,x+3,H-7],fill='white')
for y in range(8,H,18): d.ellipse([7,y-3,13,y+3],fill='white'); d.ellipse([W-13,y-3,W-7,y+3],fill='white')
img.save('v01_thumbnail.jpg',quality=92)
