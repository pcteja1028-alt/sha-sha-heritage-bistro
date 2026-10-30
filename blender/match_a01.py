import bpy, math, random, os, json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Reuse material corrections without running the previous render or saving over it.
src=open(os.path.join(ROOT,'blender','ultra.py')).read().split('# Count evaluated triangles')[0]
src=src.replace("sub.levels=2; sub.render_levels=2","sub.levels=1; sub.render_levels=1")
exec(compile(src,__file__,'exec'))
exec(open(os.path.join(ROOT,'blender','mesh_helpers.py')).read())
random.seed(59)
def mat(name,c,rough=.4,metal=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Roughness'].default_value=rough; p.inputs['Metallic'].default_value=metal; return m
ebony=mat('A01 dark stained bentwood',(.012,.009,.006),.28)
seatmat=mat('A01 black leather seat',(.009,.007,.005),.36)
brass=bpy.data.materials['Antique brass']; walnut=bpy.data.materials['Warm walnut']; cream=bpy.data.materials['Ivory lime plaster']; black=bpy.data.materials['Charcoal']; green=bpy.data.materials['Olive foliage']
# Remove the generic chairs, place settings, and the oversized bean-like foliage.
prefixes=('Chair ','Bentwood','Steam bent','Continuous bentwood','Padded chair','Upholstery piping','Ivory ceramic','Plate inset','Folded linen','Leaves','Olive leaf','Plant stem','Artwork inset')
for o in list(scene.objects):
 if o.name.startswith(prefixes): bpy.data.objects.remove(o,do_unlink=True)
for y in [1.2,2.65,4.1,5.55,7.0]:
 sphere('A01 black padded chair seat',(-.08,y,.47),(.235,.225,.045),seatmat)
 for z in [.79,.91]:
  curve('A01 curved elbow rail',[(.19-.28*math.sin(a),y+.25*math.cos(a),z-.05*math.sin(a)) for a in [i*math.pi/18 for i in range(19)]],.021,ebony)
 for yy in [-1,1]:
  curve('A01 rear swept leg',[(.25,y+yy*.25,.025),(.16,y+yy*.19,.45),(.18,y+yy*.24,.90)],.018,ebony)
  curve('A01 front tapered leg',[(-.31,y+yy*.22,.025),(-.27,y+yy*.17,.46)],.016,ebony)
  curve('A01 seat side rail',[(-.27,y+yy*.18,.43),(.18,y+yy*.19,.43)],.018,ebony)
 # Dense branching olive stems with thin, pointed, folded leaf surfaces.
 for k in range(22):
  a=k*2.399; origin=Vector((-.87,y,.88)); end=origin+Vector((math.cos(a)*random.uniform(.08,.16),math.sin(a)*random.uniform(.08,.16),random.uniform(.15,.32)))
  curve('Olive woody twig',[origin,origin.lerp(end,.5)+Vector((0,0,.04)),end],.0014,walnut)
  for t in [.35,.50,.65,.8,1.]:
   center=origin.lerp(end,t)
   for sign in [-1,1]:
    d=Vector((math.cos(a+sign*.8),math.sin(a+sign*.8),.55)).normalized(); side=Vector((-d.y,d.x,0))*.007
    base=center; tip=center+d*.055; mid=center+d*.026
    v=[base,mid+side,mid+Vector((0,0,.003)),mid-side,tip]
    me=bpy.data.meshes.new('Folded lanceolate leaf'); me.from_pydata(v,[],[(0,1,2),(0,2,3),(1,4,2),(2,4,3)]); me.update(); ob=bpy.data.objects.new('Olive leaf blade',me); scene.collection.objects.link(ob); me.materials.append(green)
# Leather seat panels and actual continuous edge piping.
for y in [.55+i*.49 for i in range(16)]:
 curve('Banquette stitched seat seam',[(-1.48,y,.535),(-1.18,y,.545),(-.88,y,.535)],.0012,leather)
curve('Banquette front welt',[(-.868,.45,.48),(-.868,4.35,.48),(-.868,8.25,.48)],.0025,leather)
# Separate honed stone floor from veined polished marble countertops.
marble=bpy.data.materials['Cream limestone'].copy(); marble.name='A01 veined cream marble'
n=marble.node_tree.nodes; l=marble.node_tree.links; p=n.get('Principled BSDF')
tc=n.new('ShaderNodeTexCoord'); noise=n.new('ShaderNodeTexNoise'); noise.inputs['Scale'].default_value=3.8; noise.inputs['Detail'].default_value=6; noise.inputs['Roughness'].default_value=.7; l.new(tc.outputs['Object'],noise.inputs['Vector'])
wave=n.new('ShaderNodeTexWave'); wave.wave_type='BANDS'; wave.bands_direction='DIAGONAL'; wave.inputs['Scale'].default_value=3.5; wave.inputs['Distortion'].default_value=12; wave.inputs['Detail'].default_value=5; l.new(tc.outputs['Object'],wave.inputs['Vector'])
r=n.new('ShaderNodeValToRGB'); r.color_ramp.elements[0].position=.66; r.color_ramp.elements[0].color=(.58,.49,.36,1); r.color_ramp.elements[1].position=.8; r.color_ramp.elements[1].color=(.20,.145,.085,1); l.new(wave.outputs['Color'],r.inputs[0]); l.new(r.outputs[0],p.inputs['Base Color']); p.inputs['Coat Weight'].default_value=.15
for o in scene.objects:
 if o.name.startswith(('Stone dining table','Standing ledge')): o.data.materials.clear(); o.data.materials.append(marble)
 if o.name.startswith('Stone dining table'):
  for mod in o.modifiers:
   if mod.type=='BEVEL': mod.width=.005
 if o.name.startswith('Limestone tile'):
  for mod in o.modifiers:
   if mod.type=='BEVEL': mod.width=.001
 if o.name.startswith('Channel tuft'):
  # Subtle, tight channels instead of inflated tubular cushions.
  o.scale.x=.72
 if o.name=='Ceiling': o.data.materials[0].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.012,.010,.008,1)
# Script signage on the left wall, positioned as in A01.
def label(name,body,position,size,rotation):
 cu=bpy.data.curves.new(name,'FONT'); cu.body=body; cu.align_x='CENTER'; cu.size=size; cu.extrude=.0015; cu.bevel_depth=.0006
 if body=='Sha Sha' and os.path.exists('C:/Windows/Fonts/FRSCRIPT.TTF'): cu.font=bpy.data.fonts.load('C:/Windows/Fonts/FRSCRIPT.TTF')
 ob=bpy.data.objects.new(name,cu); scene.collection.objects.link(ob); ob.location=position; ob.rotation_euler=rotation; cu.materials.append(black)
label('Left wall script branding','Sha Sha',(-1.505,2.45,1.70),.38,(math.pi/2,0,math.pi/2))
label('Left wall subtitle','SHANDAAR SHAWARMA',(-1.503,2.45,1.57),.058,(math.pi/2,0,math.pi/2))
# Emblem represented by modeled tapered spit and crown above the wordmark.
for i in range(8):
 z=2.02+i*.04; half=.025+i*.009
 curve('Wall spit emblem',[(-1.493,2.45-half,z),(-1.487,2.45,z+.012),(-1.493,2.45+half,z+.02)],.009,black)
curve('Wall crown emblem',[(-1.495,2.36,2.38),(-1.495,2.36,2.44),(-1.495,2.41,2.415),(-1.495,2.45,2.48),(-1.495,2.49,2.415),(-1.495,2.54,2.44),(-1.495,2.54,2.38)],.009,black)
# Add left-wall framed food photography, previously absent.
for y in [.65,5.25]:
 box('Left black artwork frame',(-1.49,y,1.97),(.035,.64,.91),black,.003)
 me=bpy.data.meshes.new('Left artwork'); me.from_pydata([(-1.468,y-.295,1.54),(-1.468,y+.295,1.54),(-1.468,y+.295,2.40),(-1.468,y-.295,2.40)],[],[(0,1,2,3)]); me.update(); uv=me.uv_layers.new()
 for loop,co in zip(uv.data,[(1,0),(0,0),(0,1),(1,1)]): loop.uv=co
 ob=bpy.data.objects.new('Left food print',me); scene.collection.objects.link(ob); me.materials.append(art)
# Proper fixture geometry: globe necks, canopy plates, and wall mounting discs.
for y in [1.4,3.6,5.8,8.0]:
 cyl('Pendant brass neck',(-.65,y,2.55),.033,.08,brass)
 cyl('Pendant canopy',(-.65,y,3.045),.055,.025,brass)
for o in scene.objects:
 if o.type=='LIGHT':
  if o.name.startswith('Soft entrance'): o.data.energy=45
  if o.name.startswith('Pendant pool'): o.data.energy=38
  if o.name.startswith('Wall wash'): o.data.energy=8
scene.world.node_tree.nodes.get('Background').inputs['Strength'].default_value=.025
scene.camera.location=(.52,.15,1.52); scene.camera.rotation_euler=(Vector((-.03,8.8,1.48))-scene.camera.location).to_track_quat('-Z','Y').to_euler(); scene.camera.data.lens=26
scene.camera.data.dof.use_dof=False
scene.view_settings.exposure=-.65
scene.render.threads_mode='FIXED'; scene.render.threads=6
scene.cycles.samples=256; scene.cycles.adaptive_threshold=.025; scene.cycles.max_bounces=10
scene.render.resolution_x=1800; scene.render.resolution_y=1200
scene.render.filepath=os.path.join(ROOT,'dist','assets','a01-matched.png')
# Open directly in the composed material camera view, not a gray modeling view.
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':
   area.spaces.active.region_3d.view_perspective='CAMERA'; area.spaces.active.shading.type='MATERIAL'
scene['reference']='A01 — reconstruction revision, visual validation required'
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-A01-Matched.blend'))
print('MATCHED_MASTER_SAVED',flush=True)
# Review render first. Master retains production settings above.
scene.render.resolution_percentage=50; scene.cycles.samples=32; scene.cycles.adaptive_threshold=.07
bpy.ops.render.render(write_still=True)
print('MATCHED_REVIEW_DONE',flush=True)
