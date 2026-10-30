"""Non-destructive offline quality revision of the editable premium scene."""
import bpy, math, os, json, random
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-Premium.blend'))
random.seed(42)
scene=bpy.context.scene
def triangles():
 dg=bpy.context.evaluated_depsgraph_get(); total=0
 for ob in scene.objects:
  if ob.type=='MESH' and not ob.hide_render:
   mesh=ob.evaluated_get(dg).to_mesh(); mesh.calc_loop_triangles(); total+=len(mesh.loop_triangles); ob.evaluated_get(dg).to_mesh_clear()
 return total
before=triangles()
def curve(name,pts,r,mat):
 c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.resolution_u=24; c.bevel_depth=r; c.bevel_resolution=6
 s=c.splines.new('BEZIER'); s.bezier_points.add(len(pts)-1)
 for p,co in zip(s.bezier_points,pts): p.co=co; p.handle_left_type='AUTO'; p.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c); scene.collection.objects.link(o); c.materials.append(mat); return o
wood=bpy.data.materials['Warm walnut']; leather=bpy.data.materials['Cognac leather']
for o in list(scene.objects):
 if o.name.startswith(('Bentwood rail','Steam bent walnut hoop','Leaves')): bpy.data.objects.remove(o,do_unlink=True)
for y in [1.2,2.65,4.1,5.55,7.0]:
 for z,r in [(.77,.017),(.91,.022)]:
  curve('Continuous bentwood chair rail',[(.10-.24*math.sin(a),y+.235*math.cos(a),z) for a in [i*math.pi/12 for i in range(13)]],r,wood)
 # Welt follows each cushion perimeter, with real geometry.
 curve('Upholstery piping',[(-.12+.207*math.cos(a),y+.207*math.sin(a),.512) for a in [i*2*math.pi/32 for i in range(33)]],.002,leather)
for o in scene.objects:
 if o.type!='MESH': continue
 for m in o.modifiers:
  if m.type=='BEVEL': m.segments=8
 if o.name.startswith(('Channel tuft','Cognac seat','Padded chair cushion','Pendant globe','Sconce globe','Olive leaf')):
  sub=o.modifiers.new('Fine curved surface','SUBSURF'); sub.levels=2; sub.render_levels=2
  for p in o.data.polygons: p.use_smooth=True
 # Cylinders need real round silhouettes, especially at eye level.
 elif o.name.startswith(('Table foot','Table pedestal','Brass planter','Track spotlight','Chair leg','Chair back','Drink bottle')):
  bevel=o.modifiers.new('Machined edge radii','BEVEL'); bevel.width=.002; bevel.segments=5
  o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
def surface(name,dark,light,scale,stretch,rough,bump):
 m=bpy.data.materials[name]; n=m.node_tree.nodes; n.clear(); l=m.node_tree.links
 out=n.new('ShaderNodeOutputMaterial'); p=n.new('ShaderNodeBsdfPrincipled'); l.new(p.outputs['BSDF'],out.inputs['Surface']); p.inputs['Roughness'].default_value=rough
 tc=n.new('ShaderNodeTexCoord'); mapping=n.new('ShaderNodeVectorMath'); mapping.operation='MULTIPLY'; mapping.inputs[1].default_value=stretch; l.new(tc.outputs['Object'],mapping.inputs[0])
 noise=n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=scale; noise.inputs['Detail'].default_value=5; noise.inputs['Roughness'].default_value=.7; l.new(mapping.outputs[0],noise.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].color=(*dark,1); ramp.color_ramp.elements[1].color=(*light,1); l.new(noise.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
 fine=n.new('ShaderNodeTexNoise'); fine.inputs['Scale'].default_value=650; fine.inputs['Detail'].default_value=3; l.new(tc.outputs['Object'],fine.inputs['Vector'])
 b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.3; b.inputs['Distance'].default_value=bump; l.new(fine.outputs['Fac'],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
 rr=n.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value=rough-.08; rr.inputs['To Max'].default_value=rough+.08; l.new(noise.outputs['Fac'],rr.inputs['Value']); l.new(rr.outputs[0],p.inputs['Roughness'])
 return p
surface('Warm walnut',(.025,.009,.004),(.12,.044,.014),4,(24,24,.5),.32,.0003)
surface('Ivory lime plaster',(.34,.27,.18),(.55,.45,.32),6,(1,1,1),.83,.0006)
surface('Cream limestone',(.25,.22,.17),(.60,.52,.39),7,(1,1,1),.29,.00018)
p=surface('Cognac leather',(.105,.026,.008),(.27,.085,.023),18,(1,1,1),.43,.00025); p.inputs['Coat Weight'].default_value=.12
for name in ['Brushed stainless','Antique brass']:
 m=bpy.data.materials[name]; p=m.node_tree.nodes.get('Principled BSDF')
 for socket in ['Anisotropic IOR Level','Anisotropic']:
  if socket in p.inputs: p.inputs[socket].default_value=.45; break
art=bpy.data.materials.new('Food photography from A01 reference'); art.use_nodes=True
tex=art.node_tree.nodes.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(os.path.join(ROOT,'blender','food-artwork.png')); tex.image.pack()
art.node_tree.links.new(tex.outputs['Color'],art.node_tree.nodes.get('Principled BSDF').inputs['Base Color'])
art.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.55
for y in [2,4.7,7.1]:
 mesh=bpy.data.meshes.new('Framed photograph'); mesh.from_pydata([(1.461,y-.305,1.50),(1.461,y+.305,1.50),(1.461,y+.305,2.32),(1.461,y-.305,2.32)],[],[(0,1,2,3)]); mesh.update()
 uv=mesh.uv_layers.new()
 for loop,co in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]): loop.uv=co
 obj=bpy.data.objects.new('Reference food photograph',mesh); scene.collection.objects.link(obj); mesh.materials.append(art)
g=bpy.data.materials['Display glass'].node_tree.nodes.get('Principled BSDF'); g.inputs['Alpha'].default_value=1; g.inputs['Base Color'].default_value=(.96,.985,1,1); g.inputs['Transmission Weight'].default_value=1; g.inputs['IOR'].default_value=1.46; g.inputs['Roughness'].default_value=.035
for o in scene.objects:
 if o.type=='LIGHT':
  if o.name.startswith(('Wall wash','Dado bounce')): o.data.energy*=.28
  elif o.name.startswith('Soft entrance'): o.data.energy*=.45
  else: o.data.energy*=.75
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.055
scene.render.engine='CYCLES'; scene.cycles.samples=512; scene.cycles.adaptive_threshold=.015; scene.cycles.use_denoising=True; scene.cycles.max_bounces=12; scene.cycles.transmission_bounces=8
scene.render.threads_mode='AUTO'
scene.render.resolution_x=1920; scene.render.resolution_y=1280; scene.render.resolution_percentage=100
scene.view_settings.exposure=-.4
scene.render.image_settings.file_format='PNG'; scene.render.filepath=os.path.join(ROOT,'dist','assets','ultra-interior.png')
# Count evaluated triangles including the continuous chair curves.
after=triangles()
for o in scene.objects:
 if o.type=='CURVE':
  ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get()); me=ev.to_mesh(); me.calc_loop_triangles(); after+=len(me.loop_triangles); ev.to_mesh_clear()
scene['quality_revision']='High-detail offline Cycles master; procedural physically scaled surfaces'
scene['evaluated_triangles']=after
scene['previous_evaluated_triangles']=before
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-Ultra.blend'))
with open(os.path.join(ROOT,'blender','ultra-report.json'),'w') as f: json.dump({'before_triangles':before,'after_triangles':after,'samples':512,'resolution':[1920,1280],'note':'Interpretation of A01 reference, not a measured reconstruction. Browser export unchanged.'},f,indent=2)
print('ULTRA_SAVED',before,after,flush=True)
bpy.ops.render.render(write_still=True)
print('ULTRA_RENDER_DONE',flush=True)
