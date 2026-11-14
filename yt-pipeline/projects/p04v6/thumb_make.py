import sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageOps
F=sys.argv[1]; W,H=1280,720
im=Image.open('f_CG_300.png').convert('RGB')
bb=im.convert('L').point(lambda v:255 if v>14 else 0).getbbox(); im=im.crop(bb); w,h=im.size
im=im.crop((int(w*0.22),int(h*0.30),int(w*0.98),int(h*1.0)))
im=ImageOps.fit(im,(W,H),Image.LANCZOS,centering=(0.5,0.0))
im=ImageEnhance.Color(im).enhance(1.25); im=ImageEnhance.Contrast(im).enhance(1.08)
img=im
gr=Image.new('L',(W,H),0); gd=ImageDraw.Draw(gr)
for y in range(420,H): gd.line([(0,y),(W,y)],fill=int(235*((y-420)/(H-420))**0.9))
img.paste((0,0,0),mask=gr)
d=ImageDraw.Draw(img); f=ImageFont.truetype(F+'/Anton-Regular.ttf',190)
t1,t2="LA ","VERDAD"; w1=d.textlength(t1,font=f); w2=d.textlength(t2,font=f); x=(W-w1-w2)/2; y=500
d.text((x,y),t1,font=f,fill='white',stroke_width=8,stroke_fill='black')
d.text((x+w1,y),t2,font=f,fill=(235,20,20),stroke_width=8,stroke_fill='black')
img.save('v01_thumbnail.jpg',quality=92)
