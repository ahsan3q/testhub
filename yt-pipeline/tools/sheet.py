# Contact sheet + sources.json from dl_log.txt. usage: sheet.py <project> [frames_per_clip]
import subprocess,json,os,sys
from PIL import Image,ImageDraw
P=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 6
os.chdir(P); os.makedirs('chk',exist_ok=True)
src={}
for line in open('dl_log.txt'):
    k,r=line.rstrip('\n').split('|',1)
    if not r.startswith('src/'): continue
    f=os.path.abspath(r.rsplit(' ',2)[0])
    if os.path.exists(f): src[k]=f
json.dump(src,open('sources.json','w'),indent=1)
tiles=[]
for k,f in src.items():
    d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f],capture_output=True,text=True,stdin=subprocess.DEVNULL).stdout.strip() or 0)
    print(k,round(d,1))
    for j in range(n):
        t=d*(0.03+0.94*j/(n-1)); o=f'chk/{k}_{j}.jpg'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',f,'-frames:v','1','-vf','scale=200:-2',o],stdin=subprocess.DEVNULL)
        tiles.append((f'{k} {int(t)}s',o))
W=200;H=130;cols=n if n>=6 else 6
img=Image.new('RGB',(W*cols,H*((len(tiles)+cols-1)//cols)));dr=ImageDraw.Draw(img)
for i,(k,o) in enumerate(tiles):
    if os.path.exists(o):
        im=Image.open(o);im.thumbnail((W,H-14));img.paste(im,((i%cols)*W,(i//cols)*H))
    dr.text(((i%cols)*W+3,(i//cols)*H+H-13),k,fill='yellow')
img.save('chk/sheet.jpg',quality=80)
