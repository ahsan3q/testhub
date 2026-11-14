import sys,json,urllib.request,urllib.parse,os,subprocess
UA={'User-Agent':'research-script/1.0'}
ident,out=sys.argv[1],sys.argv[2]; nmax=int(sys.argv[3]) if len(sys.argv)>3 else 1
m=json.load(urllib.request.urlopen(urllib.request.Request("https://archive.org/metadata/"+ident,headers=UA),timeout=40))
fs=[f for f in m['files'] if f['name'].lower().endswith('.mp4')]
if not fs: fs=[f for f in m['files'] if f['name'].lower().endswith(('.ogv','.mpeg','.avi','.mkv','.mov','.webm'))]
fs.sort(key=lambda f:int(f.get('size',0) or 0))
# prefer mid-size (not tiny) files
sel=[f for f in fs if int(f.get('size',0) or 0)>3e6][:nmax] or fs[:nmax]
os.makedirs(out,exist_ok=True)
for f in sel:
    url="https://archive.org/download/"+ident+"/"+urllib.parse.quote(f['name'])
    dst=os.path.join(out,ident+"__"+os.path.basename(f['name']).replace(' ','_'))
    if not os.path.exists(dst):
        subprocess.run(['curl','-sSL','--max-time','900','-A','research-script/1.0','-o',dst,url],check=True)
    print(dst, int(f.get('size',0))//1000000,'MB')
