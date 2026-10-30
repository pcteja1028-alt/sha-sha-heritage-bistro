from pathlib import Path
import struct,json
p=Path('heritage-walkthrough/dist/assets/heritage-a.glb')
data=p.read_bytes(); magic,version,total=struct.unpack_from('<4sII',data); length,kind=struct.unpack_from('<II',data,12); g=json.loads(data[20:20+length])
assert magic==b'glTF' and version==2 and total==len(data)
print(json.dumps({'size_mb':round(len(data)/1048576,2),'meshes':len(g.get('meshes',[])),'materials':len(g.get('materials',[])),'images':len(g.get('images',[])),'extensions':g.get('extensionsUsed',[])},indent=2))
