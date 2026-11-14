import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
F=sys.argv[1]; A=sys.argv[2]; W,H=1280,720
img=Image.new('RGB',(W,H),(30,20,16)); d=ImageDraw.Draw(img)
def L(p):
    im=Image.open(p).convert('RGB'); b=im.convert('L').point(lambda v:255 if v>16 else 0).getbbox(); return ImageEnhance.Color(im.crop(b)).enhance(1.3)
def tile(p,box,c=(0.5,0.4)):
    x0,y0,x1,y1=box; im=ImageOps.fit(L(p),(x1-x0,y1-y0),Image.LANCZOS,centering=c); img.paste(im,(x0,y0)); d.rectangle(box,outline=(250,240,220),width=3)
tile('f_FW_24.png',(22,22,320,266)); tile('f_CM_52.png',(320,22,624,266)); tile('f_MB2_101.png',(624,22,940,266))
tile('f_VS_184.png',(22,266,292,470)); tile('f_NP_58.png',(292,266,566,470)); tile('f_TY_17.png',(566,266,940,470))
tile('f_CH_3.png',(940,22,1258,470),(0.45,0.3))
# TV
tv=Image.open(A+'/tv_frame.png').convert('RGBA').resize((360,250),Image.LANCZOS)
scr=Image.new('RGB',(360,250),(200,200,195)); sd=ImageDraw.Draw(scr)
cx,cy,r=150,120,82
sd.ellipse([cx-r,cy-r,cx+r,cy+r],outline=(220,20,20),width=16)
sd.rectangle([cx-55,cy+5,cx+45,cy+22],fill=(20,20,20)); sd.rectangle([cx+45,cy+5,cx+60,cy+22],fill=(230,120,40))
sd.line([cx-58,cy-58,cx+58,cy+58],fill=(220,20,20),width=16)
img.paste(scr,(895,450)); img.paste(tv,(895,450),tv)
# text box
d=ImageDraw.Draw(img)
d.rectangle([70,486,880,694],fill='white',outline=(40,30,20),width=3)
def fit(t,sz,mw,font):
    f=ImageFont.truetype(F+font,sz)
    while d.textlength(t,font=f)>mw: sz-=2; f=ImageFont.truetype(F+font,sz)
    return f
f1=fit("PROHIBIDOS",120,760,'/ArchivoBlack-Regular.ttf'); f2=fit("COMERCIALES DE CIGARROS",56,760,'/Anton-Regular.ttf')
d.text((475,490),"PROHIBIDOS",font=f1,fill=(200,20,24),anchor='ma'); d.text((475,608),"COMERCIALES DE CIGARROS",font=f2,fill=(18,30,80),anchor='ma')
d.rectangle([110,682,840,688],fill=(200,20,24))
for x in range(8,W,18): d.ellipse([x-3,4,x+3,10],fill='white'); d.ellipse([x-3,H-10,x+3,H-4],fill='white')
for y in range(8,H,18): d.ellipse([4,y-3,10,y+3],fill='white'); d.ellipse([W-10,y-3,W-4,y+3],fill='white')
img.save('v01_thumbnail.jpg',quality=92)
