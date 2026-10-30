def box(n,p,s,m,bevel=.015):
 verts=[(x*s[0]/2,y*s[1]/2,z*s[2]/2) for x,y,z in [(-1,-1,-1),(-1,-1,1),(-1,1,-1),(-1,1,1),(1,-1,-1),(1,-1,1),(1,1,-1),(1,1,1)]]
 faces=[(0,4,6,2),(1,3,7,5),(0,1,5,4),(2,6,7,3),(0,2,3,1),(4,5,7,6)]
 mesh=bpy.data.meshes.new(n); mesh.from_pydata(verts,[],faces); mesh.update(); o=bpy.data.objects.new(n,mesh); bpy.context.collection.objects.link(o); o.location=p; mesh.materials.append(m)
 if bevel:
  mod=o.modifiers.new('Soft edges','BEVEL'); mod.width=bevel; mod.segments=3; o.modifiers.new('Normals','WEIGHTED_NORMAL')
 return o
def cyl(n,p,r,d,m):
 N=32; v=[(r*math.cos(i*2*math.pi/N),r*math.sin(i*2*math.pi/N),z) for z in [-d/2,d/2] for i in range(N)]; f=[tuple(reversed(range(N))),tuple(range(N,2*N))]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)]
 mesh=bpy.data.meshes.new(n); mesh.from_pydata(v,[],f); mesh.update(); o=bpy.data.objects.new(n,mesh); bpy.context.collection.objects.link(o); o.location=p; mesh.materials.append(m)
 for face in mesh.polygons:
  if len(face.vertices)==4: face.use_smooth=True
 return o
def sphere(n,p,s,m):
 N=20; R=12; v=[(s[0]*math.sin(j*math.pi/R)*math.cos(i*2*math.pi/N),s[1]*math.sin(j*math.pi/R)*math.sin(i*2*math.pi/N),s[2]*math.cos(j*math.pi/R)) for j in range(R+1) for i in range(N)]; f=[(j*N+i,j*N+(i+1)%N,(j+1)*N+(i+1)%N,(j+1)*N+i) for j in range(R) for i in range(N)]
 mesh=bpy.data.meshes.new(n); mesh.from_pydata(v,[],f); mesh.update(); o=bpy.data.objects.new(n,mesh); bpy.context.collection.objects.link(o); o.location=p; mesh.materials.append(m)
 for face in mesh.polygons: face.use_smooth=True
 return o
