# usage: clamp.py <proj>  -- clamp KEY@a-b ranges in mk.py to source durations from sheet.log; reruns mk.py
import re,sys,subprocess,os
P=sys.argv[1]; dur={}
for ln in open(f"{P}/sheet.log"):
    m=re.match(r"^([A-Z0-9]{2}) ([0-9.]+)$",ln.strip())
    if m: dur[m.group(1)]=float(m.group(2))
s=open(f"{P}/mk.py").read(); miss=set()
def f(m):
    k,a,b=m.group(1),int(m.group(2)),int(m.group(3))
    if k not in dur: miss.add(k); return m.group(0)
    d=int(dur[k])-int(sys.argv[2] if len(sys.argv)>2 else 3)
    if b>d: b=d
    if a>b-25: a=max(1,b-max(25,int(d*0.4)))
    return f"{k}@{a}-{b}"
s=re.sub(r"\b([A-Z][A-Z0-9])@(\d+)-(\d+)",f,s)
s=re.sub(r'src="([A-Z][A-Z0-9])@',lambda m:m.group(0),s)
open(f"{P}/mk.py","w").write(s)
print("missing keys:",sorted(miss))
subprocess.run(["python3","mk.py"],cwd=P)
