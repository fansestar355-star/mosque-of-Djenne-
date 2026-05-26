import bpy

bpy.ops.mesh.primitive_cone_add(
    vertices=32,
    radius1=1.0,
    radius2=0.0,
    depth=2.0,
    location=(0, 0, 5)
)

cone = bpy.context.active_object
cone.name = "Cone_0_0_5"

print(f"Cône ajouté : {cone.name} à la position {cone.location[:]}")
