import bpy, math, random, os
from mathutils import Vector
random.seed(12)
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(n,c,metal=0,rough=.5,emit=0):
 m=bpy.data.materials.new(n); m.diffuse_color=(*c,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*c,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
 if emit: p.inputs['Emission Color'].default_value=(*c,1); p.inputs['Emission Strength'].default_value=emit
 return m
cream=mat('Ivory lime plaster',(.73,.65,.51)); walnut=mat('Warm walnut',(.16,.065,.026)); leather=mat('Cognac leather',(.39,.14,.045),0,.4); brass=mat('Antique brass',(.55,.32,.09),.72,.28); stone=mat('Cream limestone',(.68,.60,.46)); black=mat('Charcoal',(.018,.022,.022)); steel=mat('Brushed stainless',(.49,.54,.56),.78,.3); glass=mat('Display glass',(.52,.73,.72),.1,.12); opal=mat('Warm opal', (1,.77,.39),0,.2,2); green=mat('Olive foliage',(.12,.21,.045)); meat=mat('Roasted shawarma',(.43,.19,.055)); red=mat('Tomato',(.6,.035,.012)); grout=mat('Grout',(.35,.32,.26))
glass.diffuse_color=(.6,.8,.8,.17); glass.node_tree.nodes.get('Principled BSDF').inputs['Alpha'].default_value=.17; glass.surface_render_method='DITHERED'
def box(n,p,s,m,bevel=.015):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p); o=bpy.context.object; o.name=n; o.dimensions=s; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(m)
 if bevel: mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=2; o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def cyl(n,p,r,d,m):
 bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=d,location=p); o=bpy.context.object; o.name=n; o.data.materials.append(m); return o
def sphere(n,p,s,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,location=p); o=bpy.context.object; o.name=n; o.scale=s; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
def rod(n,a,b,r,m):
 a,b=Vector(a),Vector(b); o=cyl(n,(a+b)/2,r,(b-a).length,m); o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
def text(n,t,p,size,m,rot=(math.pi/2,0,0)):
 c=bpy.data.curves.new(n,'FONT'); c.body=t; c.align_x='CENTER'; c.size=size; c.extrude=.002; o=bpy.data.objects.new(n,c); bpy.context.collection.objects.link(o); o.location=p; o.rotation_euler=rot; o.data.materials.append(m)
def lamp(p,power=45):
 d=bpy.data.lights.new('Warm illumination','POINT'); d.energy=power; d.color=(1,.78,.49); d.shadow_soft_size=.35; o=bpy.data.objects.new('Warm illumination',d); bpy.context.collection.objects.link(o); o.location=p
# Coordinate system: x width, y depth, z height. Exact concept envelope 10 by 44 feet.
W=3.048; L=13.4112
box('Foundation',(0,L/2,-.13),(W+.3,L+.3,.25),grout)
for i in range(5):
 for j in range(22): box('Limestone tile',(-1.219+i*.6096,.305+j*.6096,.008),(.604,.604,.025),stone,.003)
for x in [-1.59,1.59]:
 box('Wall shell',(x,L/2,1.55),(.13,L,3.1),cream)
 box('Walnut wainscot',(x*.959,4.55,.53),(.045,9.1,1.06),walnut)
 box('Brass dado',(x*.947,4.55,1.08),(.02,9.1,.025),brass)
 for y in [i*.30 for i in range(30)]: box('Panel joint',(x*.944,y,.52),(.022,.015,1.02),black,.002)
box('Rear wall',(0,L,1.55),(W,.12,3.1),cream)
box('Ceiling',(0,L/2,3.12),(W,L,.12),cream)
for x in [-1.2,1.2]: box('Ceiling molding',(x,L/2,2.99),(.12,L,.12),walnut)
box('Banquette plinth',(-1.2,4.35,.20),(.58,7.8,.38),walnut)
box('Cognac seat',(-1.18,4.35,.46),(.64,7.8,.16),leather,.06)
for j in range(52): box('Channel tuft',(-1.43,.51+j*.15,.91),(.18,.145,.85),leather,.055)
for y in [1.2,2.65,4.1,5.55,7.0]:
 box('Stone dining table',(-.78,y,.76),(.66,.66,.055),stone,.022); cyl('Table pedestal',(-.78,y,.39),.035,.72,black); cyl('Table foot',(-.78,y,.045),.23,.045,black)
 cyl('Chair seat',(-.12,y,.46),.22,.07,black)
 for xx in [-.28,.04]:
  for yy in [y-.16,y+.16]: rod('Chair leg',(xx,yy,.04),(xx,yy,.45),.018,walnut)
 for yy in [y-.20,y+.20]: rod('Chair back',(.04,yy,.45),(.13,yy,.88),.018,walnut)
 # Curved bentwood chair back
 pts=[(.13-.16*math.sin(a),y+.21*math.cos(a),.88) for a in [i*math.pi/16 for i in range(17)]]
 for a,b in zip(pts,pts[1:]): rod('Bentwood rail',a,b,.021,walnut)
 cyl('Brass planter',(-.87,y,.84),.055,.12,brass)
 for k in range(7): sphere('Leaves',(-.87+random.uniform(-.08,.08),y+random.uniform(-.08,.08),.96+random.uniform(-.03,.06)),(.035,.025,.07),green)
for y in [1.4,3.6,5.8,8.0]:
 for x in [-1.39,1.39]:
  rod('Sconce bracket',(x,y,1.65),(x,y,2.08),.012,brass); sphere('Sconce globe',(x*.91,y,1.95),(.105,.105,.105),opal); lamp((x*.82,y,2),25)
 rod('Pendant stem',(-.65,y,3.02),(-.65,y,2.48),.012,brass); sphere('Pendant globe',(-.65,y,2.4),(.14,.14,.14),opal); lamp((-.65,y,2.4),40)
box('Standing ledge',(1.35,3.9,1.02),(.32,4.8,.06),stone)
for y in [2,4.7,7.1]:
 box('Wall art frame',(1.505,y,1.91),(.035,.71,.93),brass)
 box('Wall art canvas',(1.48,y,1.91),(.025,.65,.87),walnut)
 for k in range(3): sphere('Abstract botanical relief',(1.46,y+(k-1)*.14,1.9+math.sin(k)*.2),(.02,.075,.22),brass)
# Service zone, leave staff passage on the right
box('Customer counter',(-.43,9.1,.49),(2.12,.72,.98),walnut)
for i in range(40): box('Counter fluting',(-1.46+i*.052,8.725,.48),(.025,.025,.88),brass,.004)
box('Cream fascia',(-.43,8.70,.52),(1.25,.045,.76),cream)
text('Counter brand','Sha Sha',(-.43,8.67,.56),.22,black); text('Counter subtitle','SHANDAAR SHAWARMA',(-.43,8.66,.37),.054,black)
box('Granite counter top',(-.43,9.1,1.01),(2.2,.82,.065),black)
box('Glass sneeze guard',(-.65,8.92,1.29),(1.55,.02,.49),glass,0); box('Display glass top',(-.65,9.13,1.55),(1.55,.45,.02),glass,0)
for x in [-1.42,.12]: rod('Display frame',(x,8.92,1.04),(x,8.92,1.56),.013,brass)
for i in range(6):
 x=-1.28+i*.25; box('Ingredient pan',(x,9.12,1.065),(.22,.34,.06),steel); box('Fresh ingredients',(x,9.12,1.1),(.19,.30,.015),[green,red,cream,meat,green,red][i])
box('POS base',(.40,9.07,1.07),(.22,.25,.05),black); o=box('POS screen',(.40,9.15,1.27),(.29,.045,.23),black); o.rotation_euler.x=.25
# Cold storage on right
box('Drinks cooler',(1.18,10.30,1.08),(.62,.76,2.16),steel); box('Cooler dark opening',(1.18,9.905,1.1),(.53,.02,1.8),black)
for z in [.35,.75,1.15,1.55]:
 box('Cooler shelf',(1.18,10.0,z),(.5,.18,.025),steel)
 for x in [.99,1.15,1.31]: cyl('Drink bottle',(x,9.97,z+.13),.045,.23,green)
box('Cooler glass',(1.18,9.88,1.1),(.52,.015,1.82),glass,0)
box('Chest freezer',(1.18,11.40,.47),(.63,.92,.94),steel); box('Freezer lid',(1.18,11.4,.96),(.65,.94,.04),cream)
box('Prep refrigerator',(-1.16,11.1,.46),(.68,1.65,.87),steel); box('Prep granite',(-1.16,11.1,.92),(.71,1.7,.06),black)
for y in [10.7,11.5]: box('Prep handle',(-.8,y,.73),(.025,.32,.03),black)
# Rear hot line, left to right: shawarma, griddle, fryer, round cooker, sink
box('Hot line base',(0,12.98,.49),(2.94,.72,.88),steel); box('Hot line worktop',(0,12.97,.96),(2.98,.77,.05),steel)
for x in [-1.15,-.57,0,.57,1.15]:
 box('Cabinet door',(x,12.61,.49),(.55,.025,.74),steel); box('Cabinet handle',(x,12.58,.76),(.19,.025,.025),black)
box('Steel backsplash',(0,13.32,1.66),(3,.025,1.4),steel)
box('Extraction hood',(-.25,12.95,2.5),(2.47,.86,.44),steel)
for i in range(30): box('Hood baffle',(-1.43+i*.079,12.89,2.25),(.035,.65,.05),black)
box('Shawarma machine',(-1.17,13.17,1.43),(.49,.16,.91),steel); rod('Shawarma spit',(-1.17,12.96,.98),(-1.17,12.96,1.98),.012,steel)
for i in range(25): cyl('Shawarma layers',(-1.17,12.96,1.17+i*.025),.12+random.random()*.035,.027,meat)
box('Flat griddle',(-.59,12.96,1.08),(.5,.59,.21),steel); box('Griddle surface',(-.59,12.96,1.195),(.47,.5,.02),black)
box('Fryer',(0,12.96,1.09),(.43,.54,.23),steel); box('Fryer well',(0,12.96,1.215),(.33,.37,.02),black); rod('Basket handle',(0,12.73,1.18),(0,12.55,1.35),.018,black)
cyl('Round cooking pot',(.53,12.96,1.16),.22,.35,steel); cyl('Pot lid',(.53,12.96,1.35),.23,.025,steel); sphere('Lid handle',(.53,12.96,1.39),(.04,.04,.025),black)
box('Sink rim',(1.12,12.96,.99),(.5,.59,.04),steel); box('Sink bowl',(1.12,12.96,1.015),(.39,.44,.012),black)
rod('Faucet upright',(1.12,13.2,1),(1.12,13.2,1.4),.018,steel); rod('Faucet spout',(1.12,13.2,1.4),(1.12,13.02,1.4),.018,steel)
for y in [9.8,11.8,12.8]: lamp((0,y,2.7),95)
# Storefront
for x in [-1.52,1.52]: box('Facade jamb',(x,-.06,1.65),(.18,.25,3.3),walnut)
box('Facade signboard',(0,-.08,2.93),(3.1,.3,.61),cream)
text('Storefront brand','Sha Sha',(0,-.25,2.94),.36,brass); text('Storefront subtitle','SHANDAAR SHAWARMA',(0,-.255,2.76),.075,black)
box('Entrance threshold',(0,0,.04),(3,.2,.06),brass)
box('Pavement',(0,-1.8,-.07),(5,3.5,.12),stone)
for x in [-1.82,1.82]:
 box('Outdoor planter',(x,-.3,.32),(.36,.36,.64),black)
 for i in range(16): sphere('Outdoor foliage',(x+random.uniform(-.18,.18),-.3+random.uniform(-.18,.18),.8+random.random()*.45),(.11,.10,.18),green)
lamp((0,-.5,2.6),90)
# Camera path retained in editable Blender file.
bpy.ops.object.camera_add(location=(.65,.5,1.65)); cam=bpy.context.object; cam.name='Walkthrough camera'; bpy.context.scene.camera=cam; cam.data.lens=22
for f,pos,target in [(1,(0,-3,1.7),(0,3,1.5)),(100,(.65,.5,1.65),(-.3,6,1.5)),(220,(.65,4,1.65),(-.6,7,1.3)),(340,(.65,7.8,1.65),(-.4,9.2,1.3)),(460,(.65,10.2,1.65),(0,12.9,1.4))]:
 cam.location=pos; cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler(); cam.keyframe_insert('location',frame=f); cam.keyframe_insert('rotation_euler',frame=f)
scene=bpy.context.scene; scene.frame_end=460; scene.frame_set(100); scene.render.engine='CYCLES'; scene.cycles.samples=24; scene.world.color=(.22,.22,.22); scene.render.resolution_x=1280; scene.render.resolution_y=800; scene.render.resolution_percentage=100
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-Design-A.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.join(ROOT,'dist','assets','heritage-a.glb'),export_format='GLB',export_animations=False,export_cameras=False,export_lights=False)
print('MODEL_COMPLETE',len(bpy.data.objects))
