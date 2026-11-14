import sys,json,urllib.request,urllib.parse,time
UA={'User-Agent':'research-script/1.0'}
def get(u):
    for i in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=30))
        except Exception as e:
            time.sleep(15*(i+1)); err=e
    raise err
for q in sys.argv[2:]:
    s=get("https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srlimit=1&srsearch="+urllib.parse.quote(q))
    if not s['query']['search']: print("=== NONE",q); continue
    t=s['query']['search'][0]['title']
    p=get("https://en.wikipedia.org/w/api.php?action=query&prop=extracts&explaintext=1&format=json&redirects=1&titles="+urllib.parse.quote(t))
    ex=list(p['query']['pages'].values())[0].get('extract','')
    print("=== ",q,"->",t); print(ex[:int(sys.argv[1])]); time.sleep(6)
