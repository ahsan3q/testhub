import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
F=sys.argv[1]; W,H=1280,720
img=Image.new('RGB',(W,H),(30,20,16)); d=ImageDraw.Draw(img)
def L(p):
    im=Image.open(p).convert('RGB'); b=im.convert('L').point(lambda v:255 if v>16 else 0).getbbox(); im=im.crop(b); w,h=im.size; im=im.crop((0,0,w,int(h*0.88))); return ImageEnhance.Color(im).enhance(1.3)
def tile(p,box,c=(0.5,0.45)):
    x0,y0,x1,y1=box; im=ImageOps.fit(L(p),(x1-x0,y1-y0),Image.LANCZOS,centering=c); img.paste(im,(x0,y0)); d.rectangle(box,outline=(250,240,220),width=3)
tile('f_EL2_8.png',(22,22,310,266)); tile('f_BR_14.png',(310,22,600,266),(0.75,0.6)); tile('f_SU_34.png',(600,22,870,266))
tile('f_MR_85.png',(22,266,300,470)); tile('f_EG_22.png',(300,266,580,470)); tile('f_PF_5.png',(580,266,870,470))
tile('f_MJ_20.png',(870,22,1258,698),(0.47,0.3))
d=ImageDraw.Draw(img)
d.rectangle([22,484,862,698],fill='white',outline=(40,30,20),width=3)
fn=ImageFont.truetype(F+'/ArchivoBlack-Regular.ttf',190)
d.text((40,478),"13",font=fn,fill=(205,24,28))
def fit(t,sz,mw,font):
    f=ImageFont.truetype(F+font,sz)
    while d.textlength(t,font=f)>mw: sz-=2; f=ImageFont.truetype(F+font,sz)
    return f
f1=fit("COMERCIALES MÁS RAROS",70,560,'/ArchivoBlack-Regular.ttf'); f2=fit("DE LOS AÑOS 70",72,520,'/ArchivoBlack-Regular.ttf')
d.text((570,512),"COMERCIALES MÁS RAROS",font=f1,fill=(18,36,90),anchor='ma'); d.text((570,600),"DE LOS AÑOS 70",font=f2,fill=(205,24,28),anchor='ma')
for x in range(8,W,18): d.ellipse([x-3,4,x+3,10],fill='white'); d.ellipse([x-3,H-10,x+3,H-4],fill='white')
for y in range(8,H,18): d.ellipse([4,y-3,10,y+3],fill='white'); d.ellipse([W-10,y-3,W-4,y+3],fill='white')
img.save('v01_thumbnail.jpg',quality=92)
