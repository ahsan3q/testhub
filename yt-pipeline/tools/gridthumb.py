# Grid thumbnail: white bg, 4x2 rounded frames with bold labels. Usage: gridthumb.py cfg.json out.jpg
# cfg: {"items":[["/path/frame.png","LABEL LINE1\nLINE2"],...8], "font":"/path/font.ttf"}
import sys,json
from PIL import Image,ImageDraw,ImageFont,ImageOps
cfg=json.load(open(sys.argv[1])); W,H=1280,720
img=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(img)
fw,fh=300,200; xs=[20+i*312 for i in range(4)]; ys=[14,366]
mask=Image.new('L',(fw,fh),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,fw-1,fh-1),18,fill=255)
for i,(p,lab) in enumerate(cfg['items']):
    x,y=xs[i%4],ys[i//4]
    fr=ImageOps.fit(Image.open(p).convert('RGB'),(fw,fh),centering=(0.5,0.5))
    sh=Image.new('RGBA',(fw+16,fh+16),(0,0,0,0)); ImageDraw.Draw(sh).rounded_rectangle((8,10,fw+8,fh+10),18,fill=(0,0,0,60))
    img.paste(sh,(x-8,y-8),sh); img.paste(fr,(x,y),mask)
    lines=lab.split('\n'); size=46
    while True:
        f=ImageFont.truetype(cfg['font'],size)
        if max(d.textlength(l,font=f) for l in lines)<=fw-14 or size<28: break
        size-=2
    ty=y+fh+12
    for l in lines:
        d.text((x+fw/2,ty),l,font=f,fill='black',anchor='ma'); ty+=size+4
img.save(sys.argv[2],quality=92)
