import bpy
import numpy as np

# Grille 10x10 SRTM autour du Tombeau des Askia (Gao, Mali 16.2872N, -0.0400E)
elev = np.array([
    [251,251,252,256,257,250,254,253,254,255],
    [249,255,254,257,252,252,252,254,254,250],
    [258,257,255,256,257,254,258,253,255,254],
    [255,254,256,259,252,254,253,255,260,256],
    [257,256,256,254,254,253,257,256,259,261],
    [253,255,255,252,255,257,254,256,260,258],
    [245,253,254,250,255,255,259,254,256,259],
    [250,245,252,257,257,257,255,258,256,254],
    [250,251,246,253,251,251,256,255,255,253],
    [250,251,245,249,250,249,249,252,249,251],
], dtype=float)

elev = elev[::-1, :]  # ligne 0=sud, ligne 9=nord

model = bpy.data.objects.get("Mesh_0")
model_bottom_z = model.location.z + model.bound_box[0][2] * model.scale[2]

tx, ty = 22.0, 12.0
e_min = elev.min()
e_range = float(elev.max() - elev.min())
elev_norm = (elev - e_min) / max(e_range, 1.0)
relief_scale = 1.5

tomb_x = 0.2 * tx - tx / 2
tomb_y = 0.889 * ty - ty / 2
tomb_z_norm = float(elev_norm[8, 2])
terrain_z_offset = model_bottom_z - tomb_z_norm * relief_scale

rows, cols = 10, 10
verts = []
for r in range(rows):
    for c in range(cols):
        x = (c / (cols - 1)) * tx - tx / 2
        y = (r / (rows - 1)) * ty - ty / 2
        z = terrain_z_offset + float(elev_norm[r, c]) * relief_scale
        verts.append((x, y, z))

faces = []
for r in range(rows - 1):
    for c in range(cols - 1):
        v0 = r * cols + c
        v1 = r * cols + c + 1
        v2 = (r + 1) * cols + c + 1
        v3 = (r + 1) * cols + c
        faces.append((v0, v1, v2, v3))

old = bpy.data.objects.get("Topographie_Askia")
if old:
    bpy.data.objects.remove(old, do_unlink=True)

mesh = bpy.data.meshes.new("Topographie_Askia")
mesh.from_pydata(verts, [], faces)
mesh.update()
obj_topo = bpy.data.objects.new("Topographie_Askia", mesh)
bpy.context.collection.objects.link(obj_topo)

mat_topo = bpy.data.materials.new("Mat_Topo")
mat_topo.use_nodes = True
bsdf = mat_topo.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.55, 0.40, 0.22, 1.0)
bsdf.inputs["Roughness"].default_value = 0.9
obj_topo.data.materials.append(mat_topo)

model.location.x = tomb_x
model.location.y = tomb_y
tomb_terrain_z = terrain_z_offset + elev_norm[8, 2] * relief_scale
model.location.z = float(tomb_terrain_z) + abs(float(model.bound_box[0][2]) * float(model.scale[2]))

for area in bpy.context.screen.areas:
    area.tag_redraw()

print("Topographie_Askia creee avec succes")
print("Tombeau positionne sur la topo")
print("Relief SRTM: " + str(round(e_min)) + "m - " + str(round(float(elev.max()))) + "m")
