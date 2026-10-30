import bpy, gpu, os, json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-A01-Matched.blend'))
scene=bpy.context.scene
try:
 gpu.init()
 print('GPU_RENDERER',gpu.platform.renderer_get(),flush=True)
 print('GPU_VENDOR',gpu.platform.vendor_get(),flush=True)
except Exception as e: print('GPU_INFO',str(e),flush=True)
scene.render.engine='CYCLES'
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.refresh_devices()
report={'cycles_devices':[(d.name,d.type) for d in prefs.devices],'render_engine':'BLENDER_EEVEE','source':'Sha-Sha-A01-Matched.blend'}
scene.render.engine='BLENDER_EEVEE'
scene.eevee.taa_render_samples=128
scene.eevee.use_raytracing=True
scene.eevee.shadow_pool_size='1536'
scene.eevee.shadow_resolution_scale=.75
scene.eevee.shadow_ray_count=2
scene.render.resolution_x=1800; scene.render.resolution_y=1200; scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'; scene.view_settings.exposure=0
scene.render.image_settings.file_format='PNG'
scene['render_device_note']='Intel Iris Xe: Eevee GPU rasterization; Cycles oneAPI unavailable on this hardware.'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-GPU.blend'))
for name,position,target,lens in [('gpu-arrival',(.48,.1,1.50),(-.04,6.5,1.48),26),('gpu-dining',(.80,2.1,1.62),(-.9,3.65,1.18),24)]:
 scene.camera.location=position; scene.camera.rotation_euler=(Vector(target)-scene.camera.location).to_track_quat('-Z','Y').to_euler(); scene.camera.data.lens=lens
 scene.render.filepath=os.path.join(ROOT,'dist','assets',name+'.png')
 bpy.ops.render.render(write_still=True)
 print('GPU_RENDER_DONE',name,flush=True)
# Build a separate browser asset from this final scene; keep the editable master intact.
for ob in list(scene.objects):
 if ob.hide_render or ob.type in {'LIGHT','CAMERA'}: bpy.data.objects.remove(ob,do_unlink=True)
for ob in scene.objects:
 for mod in ob.modifiers:
  if mod.type=='SUBSURF': mod.levels=min(mod.levels,1); mod.render_levels=min(mod.render_levels,1)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.convert(target='MESH')
# Planar world-space UVs preserve physical texture scale on each surface.
scales={'Ivory lime plaster':.5,'Cognac leather':3,'A01 veined cream marble':.6,'Cream limestone':.7}
for ob in scene.objects:
 if ob.type!='MESH': continue
 uv=ob.data.uv_layers.active or ob.data.uv_layers.new(name='SurfaceUV')
 for face in ob.data.polygons:
  mat=ob.data.materials[face.material_index] if ob.data.materials else None
  if not mat or mat.name not in scales: continue
  axis=max(range(3),key=lambda i:abs((ob.matrix_world.to_3x3()@face.normal)[i])); axes=[i for i in range(3) if i!=axis]
  for li in face.loop_indices:
   co=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
   uv.data[li].uv=(co[axes[0]]*scales[mat.name],co[axes[1]]*scales[mat.name])
for mat in bpy.data.materials:
 if not mat.use_nodes: continue
 n=mat.node_tree.nodes; links=mat.node_tree.links
 p=next((x for x in n if x.type=='BSDF_PRINCIPLED'),None)
 if not p: continue
 if mat.name in scales:
  tex=next((x for x in n if x.type=='TEX_IMAGE' and x.image and x.image.colorspace_settings.name!='Non-Color'),None)
  if tex:
   for link in list(tex.inputs['Vector'].links): links.remove(link)
   tex.projection='FLAT'; links.new(tex.outputs['Color'],p.inputs['Base Color'])
   # Tint is incorporated in the PBR factor.
   p.inputs['Base Color'].default_value=(.85,.73,.58,1) if mat.name=='Ivory lime plaster' else ((1,.72,.48,1) if mat.name=='Cognac leather' else (1,1,1,1))
 for socket in ['Normal','Roughness']:
  for link in list(p.inputs[socket].links): links.remove(link)
 p.inputs['Roughness'].default_value=.82 if 'plaster' in mat.name else .4
 # Procedural Blender surfaces use a representative PBR colour in the browser.
 for link in list(p.inputs['Base Color'].links):
  if link.from_node.type!='TEX_IMAGE':
   node=link.from_node
   if node.type=='VALTORGB':
    cols=[e.color for e in node.color_ramp.elements]; p.inputs['Base Color'].default_value=tuple(sum(c[i] for c in cols)/len(cols) for i in range(4))
   links.remove(link)
bpy.ops.object.select_all(action='SELECT'); bpy.context.view_layer.objects.active=next(o for o in scene.objects if o.type=='MESH'); bpy.ops.object.join()
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'dist','assets','heritage-a01.glb'),export_format='GLB',export_animations=False,export_cameras=False,export_lights=False,export_image_format='JPEG',export_jpeg_quality=88)
report['output']='heritage-a01.glb'
with open(os.path.join(ROOT,'blender','gpu-report.json'),'w') as f: json.dump(report,f,indent=2)
print('GPU_PIPELINE_DONE',flush=True)
