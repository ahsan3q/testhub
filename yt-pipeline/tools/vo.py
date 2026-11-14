import json,subprocess,os,sys
from concurrent.futures import ThreadPoolExecutor
P,voice,rate=sys.argv[1],sys.argv[2],sys.argv[3]
seg=json.load(open(f'{P}/script.json')); os.makedirs(f'{P}/vo',exist_ok=True)
env=dict(os.environ,SSL_CERT_FILE='/root/.ccr/ca-bundle.crt')
def run(i):
    out=f'{P}/vo/{i:02d}.mp3'
    for k in range(4):
        r=subprocess.run(['edge-tts','--proxy',os.environ['HTTPS_PROXY'],'--voice',voice,f'--rate={rate}','--text',seg[i]['txt'],'--write-media',out],env=env,capture_output=True)
        if r.returncode==0 and os.path.getsize(out)>1000: return 'ok'
    return r.stderr[-300:]
with ThreadPoolExecutor(4) as ex:
    for i,s in enumerate(ex.map(run,range(len(seg)))):
        if s!='ok': print('FAIL',i,s)
tot=sum(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{P}/vo/{i:02d}.mp3'])) for i in range(len(seg)))
w=sum(len(s['txt'].split()) for s in seg); print('segs',len(seg),'sec',round(tot),'wpm',round(w/tot*60))
