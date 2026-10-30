from pathlib import Path
p=Path('heritage-walkthrough/blender/premium.py'); s=p.read_text(); s=s.replace("exec(compile(src,", "src=src[:src.index('def box(')]+open(os.path.join(ROOT,'blender','mesh_helpers.py')).read()+'\\n'+src[src.index('def rod('):]\nexec(compile(src,")
s=s.replace("# Higher-resolution", "print('BASE GEOMETRY BUILT',flush=True)\n# Higher-resolution").replace("# Replace default lamps", "print('DETAILED GEOMETRY BUILT',flush=True)\n# Replace default lamps")
p.write_text(s)
