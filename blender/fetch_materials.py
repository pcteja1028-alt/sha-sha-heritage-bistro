import requests, pathlib, concurrent.futures, json
root=pathlib.Path(__file__).parent/'textures'; root.mkdir(exist_ok=True)
def fetch(asset):
 d=requests.get('https://api.polyhaven.com/files/'+asset,timeout=45).json(); result={}
 for kind,keys in [('color',['diff','Diffuse']),('rough',['rough','Rough']),('height',['disp','Displacement'])]:
  key=next((k for k in keys if k in d),None)
  if not key: continue
  formats=d[key]['2k']; fmt=next(k for k in ['jpg','png'] if k in formats); url=formats[fmt]['url']; path=root/(asset+'_'+kind+'.'+fmt)
  r=requests.get(url,timeout=90); r.raise_for_status(); path.write_bytes(r.content); result[kind]=str(path)
 return asset,result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: manifest=dict(pool.map(fetch,['beige_wall_001','brown_leather','marble_01']))
(root/'manifest.json').write_text(json.dumps(manifest,indent=2))
(root/'SOURCES.md').write_text('Powered by Poly Haven. CC0 texture assets.\n'+''.join('https://polyhaven.com/a/'+a+'\n' for a in manifest))
print('Downloaded',manifest.keys())
