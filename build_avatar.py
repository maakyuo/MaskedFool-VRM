import bpy, math, random, os
from mathutils import Vector
random.seed(17)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
def mat(name,c,metal=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*c,1); m.use_nodes=True
 bs=m.node_tree.nodes.get('Principled BSDF')
 bs.inputs['Base Color'].default_value=(*c,1)
 bs.inputs['Metallic'].default_value=metal
 return m
skin=mat('skin',(.82,.69,.68)); hair=mat('black hair',(.035,.03,.055)); eye=mat('amber',(.9,.55,.06)); sclera=mat('sclera',(.94,.91,.88)); cloth=mat('black fabric',(.05,.04,.08)); purple=mat('violet fabric',(.24,.13,.39)); gold=mat('gold',(.7,.47,.2),.6); steel=mat('gunmetal mask',(.18,.19,.23),.55); white=mat('inner shirt',(.8,.8,.83))
def ell(name,p,s,m):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=p)
 o=bpy.context.object;o.name=name;o.scale=s;o.data.materials.append(m)
 return o
def rod(name,a,b,r,m,r2=None):
 a,b=Vector(a),Vector(b);v=b-a
 bpy.ops.mesh.primitive_cone_add(vertices=10,radius1=r,radius2=r if r2 is None else r2,depth=v.length,location=(a+b)/2)
 o=bpy.context.object;o.name=name;o.rotation_euler=v.to_track_quat('Z','Y').to_euler();o.data.materials.append(m)
 return o
def panel(name,pts,m):
 verts=[tuple(x) for x in pts]; faces=[tuple(range(len(pts)))]
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update()
 ob=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(ob);me.materials.append(m)
 ob.modifiers.new('thickness','SOLIDIFY').thickness=.015
 return ob
ell('pelvis',(0,0,.95),(.18,.12,.13),cloth)
ell('torso',(0,0,1.23),(.21,.13,.30),cloth)
ell('white shirt',(0,-.128,1.25),(.11,.018,.22),white)
rod('short neck',(0,0,1.48),(0,0,1.55),.06,skin)
ell('young face',(0,-.015,1.65),(.124,.103,.155),skin)
for s in (-1,1):
 ell('eye',(s*.052,-.106,1.675),(.035,.012,.015),sclera)
 ell('iris',(s*.052,-.119,1.675),(.013,.006,.013),eye)
 ell('ear',(s*.125,0,1.65),(.019,.024,.036),skin)
ell('wolfcut hair cap',(0,0,1.775),(.135,.119,.09),hair)
for i in range(55):
 t=i*2*math.pi/55;x=.12*math.cos(t);y=.105*math.sin(t)
 z=1.79+random.uniform(-.01,.02);length=random.uniform(.065,.15)+(0.09 if y>.03 else 0)
 rod('wolfcut strand',(x*.55,y*.55,z+.03),(x*1.23,y*1.2,z-length),random.uniform(.009,.018),hair,.001)
for i in range(14):
 x=(i-6.5)*.016
 rod('nape hair',(x,.09,1.70),(x+random.uniform(-.02,.02),.13,1.50+random.uniform(-.04,.04)),.011,hair,.001)
panel('faceted mask center',[(-.07,-.135,1.64),(.07,-.135,1.64),(.105,-.115,1.57),(0,-.151,1.51),(-.105,-.115,1.57)],steel)
for s in (-1,1):
 panel('mask cheek',[(s*.07,-.13,1.64),(s*.13,-.05,1.69),(s*.13,-.065,1.59),(s*.08,-.125,1.55)],steel)
 rod('upper arm',(s*.23,0,1.38),(s*.48,0,1.38),.065,skin)
 rod('jacket sleeve',(s*.23,0,1.38),(s*.36,0,1.38),.085,cloth)
 rod('forearm',(s*.48,0,1.38),(s*.70,0,1.38),.047,skin,.037)
 ell('glove',(s*.74,0,1.38),(.067,.042,.035),cloth)
 rod('thigh',(s*.11,0,.92),(s*.11,0,.55),.085,cloth,.073)
 rod('shin',(s*.11,0,.55),(s*.11,0,.15),.07,cloth,.055)
 ell('boot',(s*.11,-.045,.10),(.088,.16,.10),cloth)
 rod('boot trim',(s*.11,0,.20),(s*.11,0,.215),.072,gold)
rod('belt',(0,0,1.07),(0,0,1.10),.18,cloth)
ell('belt buckle',(0,-.15,1.09),(.037,.012,.027),gold)
panel('asymmetric left coat',[(-.19,.07,1.33),(-.26,.07,.98),(-.34,.10,.38),(-.13,.11,.56)],purple)
panel('short right coat',[(.19,.07,1.33),(.25,.07,1.01),(.28,.09,.77),(.12,.1,.82)],cloth)
ell('gold ornament',(.13,-.15,1.35),(.025,.01,.025),gold)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('masked_fool_v2.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.abspath('masked_fool_v2.glb'),export_format='GLB',use_selection=True)
print('Exported editable Blender blockout and GLB preview, NOT a finished VRM')
