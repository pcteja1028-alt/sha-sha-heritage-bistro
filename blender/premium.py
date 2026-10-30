import bpy, math, random, os, faulthandler
faulthandler.dump_traceback_later(90, repeat=True)
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=open(os.path.join(ROOT,'blender','build.py')).read().split('# Camera path')[0]
src=src[:src.index('def box(')]+open(os.path.join(ROOT,'blender','mesh_helpers.py')).read()+'\n'+src[src.index('def rod('):]
exec(compile(src,os.path.join(ROOT,'blender','build.py'),'exec'))
print('BASE GEOMETRY BUILT',flush=True)
# Higher-resolution rounded surfaces throughout.
for o in bpy.data.objects:
 for mod in o.modifiers:
  if mod.type=='BEVEL': mod.segments=4
# Physically scaled procedural finishes, baked for the browser below.
def finish(m,scale,c1,c2,stretch=(1,1,1),bump=.025):
 n=m.node_tree.nodes; l=m.node_tree.links; p=n.get('Principled BSDF')
 tex=n.new('ShaderNodeTexNoise'); tex.inputs['Scale'].default_value=scale; tex.inputs['Detail'].default_value=4
 coord=n.new('ShaderNodeTexCoord'); v=n.new('ShaderNodeVectorMath'); v.operation='MULTIPLY'; v.inputs[1].default_value=stretch
 l.new(coord.outputs['Object'],v.inputs[0]); l.new(v.outputs[0],tex.inputs['Vector'])
 ramp=n.new('ShaderNodeValToRGB'); ramp.color_ramp.elements[0].position=.22; ramp.color_ramp.elements[0].color=(*c1,1); ramp.color_ramp.elements[1].position=.8; ramp.color_ramp.elements[1].color=(*c2,1)
 l.new(tex.outputs['Fac'],ramp.inputs[0]); l.new(ramp.outputs[0],p.inputs['Base Color'])
 b=n.new('ShaderNodeBump'); b.inputs['Strength'].default_value=.22; b.inputs['Distance'].default_value=bump; l.new(tex.outputs['Fac'],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
finish(walnut,3,(.055,.018,.007),(.27,.12,.045),(15,15,.35),.006)
finish(cream,5,(.40,.32,.22),(.78,.69,.53),bump=.012)
finish(stone,4,(.29,.25,.19),(.72,.65,.53),bump=.004)
finish(leather,110,(.22,.055,.013),(.43,.17,.055),bump=.001)
leather.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.32
charcoal=mat('Warm charcoal ceiling',(.025,.022,.018),rough=.9)
for o in bpy.data.objects:
 if o.name=='Ceiling': o.data.materials.clear(); o.data.materials.append(charcoal)
 if o.name.startswith('Abstract botanical'): o.hide_render=True
# Full-height joinery, inset wall panels and integrated ribbons of light.
led=mat('2700K concealed lighting',(1,.54,.18),rough=.3,emit=5)
for x in [-1.49,1.49]:
 box('Concealed dado LED',(x,4.45,1.12),(.015,8.6,.018),led,.002)
 box('Ceiling cove glow',(x,4.45,2.98),(.025,8.6,.02),led,.002)
 for y in [.22,2.1,4.25,6.4,8.5]:
  box('Full height walnut pilaster',(x,y,1.95),(.065,.10,1.88),walnut,.008)
  box('Pilaster brass inlay',(x*.974,y,1.95),(.009,.015,1.83),brass,.002)
for y in [1.2,2.65,4.1,5.55,7.0]:
 # Comfortable upholstered chair seat and additional continuous bentwood rail.
 sphere('Padded chair cushion',(-.12,y,.495),(.215,.215,.035),leather)
 for h in [.76,.91]:
  pts=[(.10-.24*math.sin(a),y+.235*math.cos(a),h) for a in [i*math.pi/32 for i in range(33)]]
  for a,b in zip(pts,pts[1:]): rod('Steam bent walnut hoop',a,b,.016,walnut)
 # Table setting, napkin holder and ceramic plate.
 cyl('Ivory ceramic plate',(-.75,y-.12,.801),.135,.012,cream)
 cyl('Plate inset',(-.75,y-.12,.809),.109,.004,stone)
 box('Folded linen',(-.62,y+.15,.807),(.12,.18,.014),cream,.006)
 cyl('Brass napkin cup',(-.91,y+.17,.85),.035,.11,brass)
 for k in range(3):
  o=box('Linen fan',(-.91+k*.008,y+.17,.94),(.006,.065,.12),cream,.002); o.rotation_euler.y=(k-1)*.18
 # Branching foliage rather than clusters of balls.
 for k in range(10):
  a=k*2.4; base=Vector((-.87,y,.89)); tip=base+Vector((math.cos(a)*.10,math.sin(a)*.10,.17+random.random()*.1))
  rod('Plant stem',base,tip,.0025,green)
  for t in [.45,.7,1]:
   p=base.lerp(tip,t); leaf=sphere('Olive leaf',p,(.018,.007,.039),green); leaf.rotation_euler=(.5,a,a)
for x in [-1.03,.95]:
 box('Lighting track',(x,4.5,2.99),(.035,8.5,.035),black,.003)
 for y in [1,2.8,4.6,6.4,8.2]:
  cyl('Track spotlight',(x,y,2.88),.043,.17,black); cyl('Spot lens',(x,y,2.79),.033,.006,opal)
for y in [2.8,6.8]:
 box('AC cassette',(0,y,3.02),(.68,.68,.055),black)
 for k in range(12): box('AC louver',(-.27+k*.049,y,2.985),(.018,.54,.02),steel,.001)
for z in [1.75,2.2]:
 for y in [2,4.7,7.1]:
  box('Artwork inset',(1.453,y,z),(.015,.55,.016),brass,.002)
# Counter joinery with warm underlighting and realistic fluted timber.
for i in range(53): box('Walnut counter reed',(-1.46+i*.039,8.682,.49),(.023,.038,.87),walnut,.008)
box('Backlit counter stone',(-.43,8.65,.52),(1.25,.04,.76),stone)
for z in [.105,.94]: box('Counter concealed ribbon',(-.43,8.62,z),(2.05,.018,.018),led,.002)
for x in [-1.04,.18]: box('Counter panel halo',(x,8.62,.52),(.012,.018,.78),led,.002)
fontpath='C:/Windows/Fonts/FRSCRIPT.TTF'
if os.path.exists(fontpath):
 font=bpy.data.fonts.load(fontpath)
 for o in bpy.data.objects:
  if o.type=='FONT' and o.data.body=='Sha Sha': o.data.font=font; o.data.size*=1.3; o.location.y-=.07
# Detailed ingredients, cabinet seams, appliance controls.
for i in range(6):
 for j in range(35):
  sphere('Fresh cut garnish',(-1.28+i*.25+random.uniform(-.08,.08),9.12+random.uniform(-.12,.12),1.12+random.random()*.025),(.018,.013,.009),[green,red,cream,meat,green,red][i])
for x in [-.73,-.44,-.12,.12]:
 o=cyl('Appliance control',(x,12.64,1.08),.027,.023,black); o.rotation_euler.x=math.pi/2
for x in [-1.4,-.7,0,.7,1.4]: box('Backsplash seam',(x,13.29,1.65),(.007,.008,1.25),black,.001)
print('DETAILED GEOMETRY BUILT',flush=True)
# Replace default lamps with a calibrated architectural lighting rig.
for o in list(bpy.data.objects):
 if o.type=='LIGHT': bpy.data.objects.remove(o,do_unlink=True)
def area(n,p,target,power,size,color=(1,.73,.43),size_y=None):
 d=bpy.data.lights.new(n,'AREA'); d.energy=power; d.color=color; d.shape='RECTANGLE'; d.size=size; d.size_y=size_y or size
 o=bpy.data.objects.new(n,d); bpy.context.collection.objects.link(o); o.location=p; o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
for y in [1.4,3.6,5.8,8]:
 area('Pendant pool',(-.65,y,2.28),(-.65,y,0),65,.4)
 for x in [-1.4,1.4]:
  area('Wall wash',(x*.88,y,2.04),(x,y,1.2),40,.4)
  area('Dado bounce',(x*.96,y,1.15),(x,y,1.9),30,1.8,size_y=.08)
area('Counter halo',(-.43,8.57,.90),(-.43,8.3,.3),35,1.9,size_y=.08)
area('Soft entrance daylight',(0,-.5,2),(0,5,1),280,2.7,(.82,.9,1))
for y in [9.8,11.8,12.7]: area('Kitchen softbox',(0,y,2.95),(0,y,0),110,1.4,(1,.88,.7))
scene=bpy.context.scene; scene.render.engine='CYCLES'; scene.render.threads_mode='FIXED'; scene.render.threads=4; scene.cycles.samples=24; scene.cycles.use_denoising=True; scene.cycles.max_bounces=6
scene.world.use_nodes=True; scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.3,.35,.45,1); scene.world.node_tree.nodes.get('Background').inputs[1].default_value=.18
cam=bpy.data.objects.new('Interior camera',bpy.data.cameras.new('Interior camera')); bpy.context.collection.objects.link(cam); cam.location=(.67,.38,1.58); cam.name='Human eye level interior'; cam.rotation_euler=(Vector((-.15,7,1.45))-cam.location).to_track_quat('-Z','Y').to_euler(); cam.data.lens=23; scene.camera=cam
scene.render.resolution_x=1500; scene.render.resolution_y=1000; scene.render.resolution_percentage=100
scene.view_settings.view_transform='AgX'; scene.render.image_settings.file_format='PNG'; scene.render.filepath=os.path.join(ROOT,'dist','assets','blender-interior.png')
print('SAVING SCENE',flush=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-Premium.blend'))
print('STARTING CYCLES RENDER',flush=True)
bpy.ops.render.render(write_still=True)
print('PREMIUM_RENDER_DONE',flush=True)
# Bake diffuse surfaces with actual Cycles indirect illumination into a shared atlas.
# Keep metal and glass physically reflective in Three.js.
bpy.ops.object.select_all(action='DESELECT')
opaque=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH' and not o.hide_render and o.data.materials:
  m=o.data.materials[0]; p=m.node_tree.nodes.get('Principled BSDF')
  if p and p.inputs['Metallic'].default_value<.5 and p.inputs['Alpha'].default_value>.9 and p.inputs['Emission Strength'].default_value==0: opaque.append(o)
for o in opaque: o.select_set(True)
bpy.context.view_layer.objects.active=opaque[0]; bpy.ops.object.convert(target='MESH'); bpy.ops.object.join(); obj=bpy.context.object; obj.name='Baked architectural interior'
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.smart_project(angle_limit=1.15,island_margin=.006); bpy.ops.object.mode_set(mode='OBJECT')
img=bpy.data.images.new('Heritage baked illumination',width=4096,height=4096)
for m in obj.data.materials:
 n=m.node_tree.nodes.new('ShaderNodeTexImage'); n.image=img; m.node_tree.nodes.active=n
scene.cycles.samples=16; scene.render.bake.use_pass_direct=True; scene.render.bake.use_pass_indirect=True; scene.render.bake.use_pass_color=True; scene.render.bake.margin=8
bpy.ops.object.bake(type='DIFFUSE')
img.filepath_raw=os.path.join(ROOT,'dist','assets','interior-lighting.png'); img.file_format='PNG'; img.save()
baked=bpy.data.materials.new('Cycles baked interior'); baked.use_nodes=True; n=baked.node_tree.nodes; n.clear(); out=n.new('ShaderNodeOutputMaterial'); em=n.new('ShaderNodeEmission'); tex=n.new('ShaderNodeTexImage'); tex.image=img; baked.node_tree.links.new(tex.outputs['Color'],em.inputs[0]); baked.node_tree.links.new(em.outputs[0],out.inputs[0]); obj.data.materials.clear(); obj.data.materials.append(baked)
for poly in obj.data.polygons: poly.material_index=0
for o in list(bpy.data.objects):
 if o.hide_render: bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'dist','assets','heritage-a.glb'),export_format='GLB',export_animations=False,export_cameras=False,export_lights=False)
print('PREMIUM_EXPORT_DONE',flush=True)
