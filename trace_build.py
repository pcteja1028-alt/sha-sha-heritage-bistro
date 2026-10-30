from pathlib import Path
p=Path('heritage-walkthrough/blender/premium.py');s=p.read_text();s=s.replace('import bpy, math, random, os','import bpy, math, random, os, faulthandler\nfaulthandler.dump_traceback_later(90, repeat=True)')
s=s.replace("bpy.ops.object.camera_add(location=(.67,.38,1.58)); cam=bpy.context.object;", "cam=bpy.data.objects.new('Interior camera',bpy.data.cameras.new('Interior camera')); bpy.context.collection.objects.link(cam); cam.location=(.67,.38,1.58);")
s=s.replace("bpy.ops.wm.save_as_mainfile(filepath=", "print('SAVING SCENE',flush=True)\nbpy.ops.wm.save_as_mainfile(filepath=")
s=s.replace("bpy.ops.render.render(write_still=True)","print('STARTING CYCLES RENDER',flush=True)\nbpy.ops.render.render(write_still=True)")
s=s.replace("scene.cycles.samples=32;", "scene.render.threads_mode='FIXED'; scene.render.threads=4; scene.cycles.samples=24;")
p.write_text(s)
