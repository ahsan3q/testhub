"""usage: meta.py <project> ; reads <project>/meta.json {title, intro, outro, tags, chapters:{segIndex:name}} -> upload/*.txt"""
import json,subprocess,sys,os
P=sys.argv[1]; M=json.load(open(f'{P}/meta.json')); seg=json.load(open(f'{P}/script.json'))
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
t=0; st=[]
for i,s in enumerate(seg):
    st.append(t); t+=dur(f'{P}/vo/{i:02d}.mp3')+0.45+(0.9 if s.get('cap','').startswith('#') else 0)
fmt=lambda x:f"{int(x//60)}:{int(x%60):02d}"
chap="\n".join(f"{fmt(st[int(k)])} {v}" for k,v in sorted(M['chapters'].items(),key=lambda kv:int(kv[0])))
desc=f"{M['intro']}\n\n📌 Capítulos:\n{chap}\n\n{M['outro']}"
os.makedirs(f'{P}/upload',exist_ok=True)
open(f'{P}/upload/titulo.txt','w').write(M['title']+"\n")
open(f'{P}/upload/descripcion.txt','w').write(desc+"\n")
open(f'{P}/upload/tags.txt','w').write(", ".join(M['tags'])+"\n")
open(f'{P}/upload/guion.txt','w').write("\n\n".join(s['txt'] for s in seg)+"\n")
print(M['title']); print(chap); print(len(", ".join(M['tags'])),'tag chars')
