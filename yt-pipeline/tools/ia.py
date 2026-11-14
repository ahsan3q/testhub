import sys,json,urllib.request,urllib.parse
UA={'User-Agent':'research-script/1.0'}
q=sys.argv[1]; n=int(sys.argv[2]) if len(sys.argv)>2 else 8
u="https://archive.org/advancedsearch.php?"+urllib.parse.urlencode({'q':q+' AND mediatype:movies','fl[]':['identifier','title','downloads','year'],'rows':n,'sort[]':'downloads desc','output':'json'},doseq=True)
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40))
for d in r['response']['docs']: print(d.get('identifier'),'|',str(d.get('title'))[:80],'|',d.get('year'),'|',d.get('downloads'))
