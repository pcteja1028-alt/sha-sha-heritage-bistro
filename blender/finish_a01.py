import bpy,os,json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-A01-Matched.blend'))
scene=bpy.context.scene
manifest=json.load(open(os.path.join(ROOT,'blender','textures','manifest.json')))
def scanned(name,asset,scale,tint=None):
 m=bpy.data.materials[name]; n=m.node_tree.nodes; n.clear(); l=m.node_tree.links
 out=n.new('ShaderNodeOutputMaterial'); p=n.new('ShaderNodeBsdfPrincipled'); l.new(p.outputs[0],out.inputs[0])
 tc=n.new('ShaderNodeTexCoord'); v=n.new('ShaderNodeVectorMath'); v.operation='SCALE'; v.inputs[3].default_value=scale; l.new(tc.outputs['Object'],v.inputs[0])
 for kind,path in manifest[asset].items():
  im=bpy.data.images.load(path,check_existing=True); im.pack()
  if kind!='color': im.colorspace_settings.name='Non-Color'
  tex=n.new('ShaderNodeTexImage'); tex.image=im; tex.projection='BOX'; tex.projection_blend=.2; l.new(v.outputs[0],tex.inputs[0])
  if kind=='color':
   if tint:
    mix=n.new('ShaderNodeMixRGB'); mix.blend_type='MULTIPLY'; mix.inputs[0].default_value=1; mix.inputs[2].default_value=(*tint,1); l.new(tex.outputs['Color'],mix.inputs[1]); l.new(mix.outputs[0],p.inputs['Base Color'])
   else: l.new(tex.outputs['Color'],p.inputs['Base Color'])
  elif kind=='rough':
   rem=n.new('ShaderNodeMapRange'); rem.inputs['To Min'].default_value=.25 if asset!='beige_wall_001' else .7; rem.inputs['To Max'].default_value=.5 if asset!='beige_wall_001' else .9; l.new(tex.outputs[0],rem.inputs[0]); l.new(rem.outputs[0],p.inputs['Roughness'])
  else:
   b=n.new('ShaderNodeBump'); b.inputs['Distance'].default_value=.0006; b.inputs['Strength'].default_value=.35; l.new(tex.outputs[0],b.inputs['Height']); l.new(b.outputs[0],p.inputs['Normal'])
scanned('Ivory lime plaster','beige_wall_001',.5,(.85,.73,.58))
scanned('Cognac leather','brown_leather',3,(1,.72,.48))
scanned('A01 veined cream marble','marble_01',.6)
scanned('Cream limestone','marble_01',.7,(.70,.66,.59))
# A01 has a shallower visible depth than the earlier assumed 44-foot layout.
for ob in scene.objects:
 if ob.type in {'MESH','CURVE','FONT'}:
  ob.location.y*=.74; ob.scale.y*=.74
 elif ob.type=='LIGHT': ob.location.y*=.74
 if ob.name.startswith('Concealed dado LED'): ob.location.z=1.37
 if ob.name.startswith('Dado bounce'): ob.location.z=1.40; ob.data.energy=6
 if ob.name.startswith('Brass dado'): ob.location.z=1.345
 if ob.name.startswith('Stone dining table'): ob.scale.y/= .74
scene.camera.location=(.48,.1,1.50); scene.camera.rotation_euler=(Vector((-.04,6.5,1.48))-scene.camera.location).to_track_quat('-Z','Y').to_euler(); scene.camera.data.lens=26
scene['reference']='A01; visible depth calibrated to image, not measured dimensions'
scene['materials']='Packed 2K Poly Haven scanned color, roughness and height maps; CC0'
scene.render.filepath=os.path.join(ROOT,'dist','assets','a01-matched.png')
scene.render.resolution_percentage=100; scene.cycles.samples=256
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'blender','Sha-Sha-A01-Matched.blend'))
scene.render.resolution_percentage=60; scene.cycles.samples=48; scene.cycles.adaptive_threshold=.05
bpy.ops.render.render(write_still=True)
print('A01_FINISHED',flush=True)
