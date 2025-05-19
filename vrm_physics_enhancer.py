import bpy
from mathutils import Vector
import math

bl_info = {
    "name": "VRM Physics Enhancer",
    "blender": (3, 0, 0),
    "category": "3D View",
    "author": "Meringue Rouge",
    "version": (1, 0),
    "location": "View3D > Sidebar > VRM Physics Enhancer",
    "description": "Adds physics colliders and jiggle bones to VRM models",
    "warning": "",
    "doc_url": "",
}

# Define scene properties for Jiggle Bones parameters
bpy.types.Scene.vrm_jiggle_bone_pair = bpy.props.EnumProperty(
    name="Bone Pair",
    description="Select the bone pair or single bone to apply jiggle physics to",
    items=[
        ('UPPER_LEG', "Upper Leg", "J_Bip_L_UpperLeg and J_Bip_R_UpperLeg"),
        ('LOWER_LEG', "Lower Leg", "J_Bip_L_LowerLeg and J_Bip_R_LowerLeg"),
        ('SPINE', "Spine", "J_Bip_C_Spine"),
        ('BUST', "Bust", "J_Bip_L_Bust and J_Bip_R_Bust"),
        ('CHEST', "Chest", "J_Bip_C_Chest"),
        ('UPPER_ARM', "Upper Arm", "J_Bip_L_UpperArm and J_Bip_R_UpperArm"),
        ('LOWER_ARM', "Lower Arm", "J_Bip_L_LowerArm and J_Bip_R_LowerArm"),
    ],
    default='UPPER_LEG'
)

bpy.types.Scene.vrm_jiggle_bone_quantity = bpy.props.IntProperty(
    name="Bone Quantity",
    description="Number of jiggle bone chains per bone",
    default=4,
    min=1,
    max=100
)

bpy.types.Scene.vrm_jiggle_affect_radius = bpy.props.FloatProperty(
    name="Affect Radius",
    description="Radius for vertex selection",
    default=0.1,
    min=0.01,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_stiffness = bpy.props.FloatProperty(
    name="Stiffness",
    description="Stiffness for all joints",
    default=0.5,  # Reduced for softer jiggle
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness = bpy.props.FloatProperty(
    name="Angular Stiffness",
    description="Stiffness for angular constraints",
    default=0.5,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_max_angle = bpy.props.FloatProperty(
    name="Max Angle (Degrees)",
    description="Maximum rotation angle for jiggle bones",
    default=30.0,
    min=0.0,
    max=90.0
)

bpy.types.Scene.vrm_jiggle_drag_force_first = bpy.props.FloatProperty(
    name="Drag Force (First Two Joints)",
    description="Drag force for the first two joints in each chain",
    default=0.2,  # Increased for more damping
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_drag_force_end = bpy.props.FloatProperty(
    name="Drag Force (End Joint)",
    description="Drag force for the third joint in each chain",
    default=0.7,  # Increased for more damping
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_subdivision_factor = bpy.props.IntProperty(
    name="Subdivision Factor",
    description="Number of subdivision iterations for jiggle bone areas (0 for no subdivision)",
    default=1,
    min=0,
    max=3
)

class VRM_OT_Add_Breast_Physics_Colliders(bpy.types.Operator):
    """Adds breast physics colliders to VRM models"""
    bl_idname = "vrm.add_breast_physics"
    bl_label = "Add Breast Physics Colliders"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'MOD_PHYSICS'

    def execute(self, context):
        try:
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            bpy.context.view_layer.objects.active = armature
            sb = armature.data.vrm_addon_extension.spring_bone1

            left_collider = sb.colliders.add()
            left_collider.node.bone_name = "J_Sec_L_Bust1"
            left_collider.shape.sphere.radius = 0.07
            left_collider.shape.sphere.offset = [-0.13, -0.052, 0.018]

            right_collider = sb.colliders.add()
            right_collider.node.bone_name = "J_Sec_R_Bust1"
            right_collider.shape.sphere.radius = 0.07
            right_collider.shape.sphere.offset = [0.13, -0.052, 0.018]

            new_group = sb.collider_groups.add()
            new_group.vrm_name = "Breasts"

            new_group.colliders.add().collider_name = "J_Sec_L_Bust1"
            new_group.colliders.add().collider_name = "J_Sec_R_Bust1"

            for spring in sb.springs:
                if "Hair" in spring.vrm_name:
                    spring.collider_groups.add().collider_group_name = "Breasts"

            self.report({'INFO'}, "Breast physics colliders added successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VRM_OT_Add_Long_Hair_Collider(bpy.types.Operator):
    """Adds a long hair body penetration prevention collider"""
    bl_idname = "vrm.add_long_hair_collider"
    bl_label = "Add Long Hair Body Penetration Prevention"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'OUTLINER_OB_FORCE_FIELD'

    def execute(self, context):
        try:
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            bpy.context.view_layer.objects.active = armature
            sb = armature.data.vrm_addon_extension.spring_bone1

            capsule_collider = sb.colliders.add()
            capsule_collider.node.bone_name = "J_Bip_C_Chest"
            capsule_collider.shape_type = "Capsule"
            capsule_collider.shape.capsule.radius = 0.12
            capsule_collider.shape.capsule.offset = [0.0, -0.08, 0.0]
            capsule_collider.shape.capsule.tail = [0.0, 0.14, 0.0]

            new_group = sb.collider_groups.add()
            new_group.vrm_name = "LongHairHelper"
            new_group.colliders.add().collider_name = "J_Bip_C_Chest"

            for spring in sb.springs:
                if "Hair" in spring.vrm_name:
                    spring.collider_groups.add().collider_group_name = "LongHairHelper"

            self.report({'INFO'}, "Long Hair Body Penetration Prevention added successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VRM_OT_Add_Arm_Hand_Colliders(bpy.types.Operator):
    """Adds arm and hand colliders for physics interactions"""
    bl_idname = "vrm.add_arm_hand_colliders"
    bl_label = "Add Arms/Hand Colliders"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'VIEW_PAN'

    def execute(self, context):
        try:
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            bpy.context.view_layer.objects.active = armature
            sb = armature.data.vrm_addon_extension.spring_bone1

            arm_colliders = [
                ("J_Bip_L_UpperArm", "Capsule", 0.043, [0, 0, 0], [0, 0.2, 0]),
                ("J_Bip_L_LowerArm", "Capsule", 0.041, [0, 0, 0], [0, 0.2, 0]),
                ("J_Bip_L_Hand", "Sphere", 0.054, [0.000003, 0.08, 0], None),
                ("J_Bip_R_UpperArm", "Capsule", 0.043, [0, 0, 0], [0, 0.2, 0]),
                ("J_Bip_R_LowerArm", "Capsule", 0.041, [0, 0, 0], [0, 0.2, 0]),
                ("J_Bip_R_Hand", "Sphere", 0.054, [0.000003, 0.08, 0], None),
            ]

            left_group = sb.collider_groups.add()
            left_group.vrm_name = "LeftArmColliders"
            right_group = sb.collider_groups.add()
            right_group.vrm_name = "RightArmColliders"

            for bone, shape, radius, offset, tail in arm_colliders:
                collider = sb.colliders.add()
                collider.node.bone_name = bone

                if shape == "Capsule":
                    collider.shape.capsule.radius = radius
                    collider.shape.capsule.offset = offset
                    collider.shape.capsule.tail = tail
                else:
                    collider.shape.sphere.radius = radius
                    collider.shape.sphere.offset = offset

                if "L_" in bone:
                    left_group.colliders.add().collider_name = bone
                else:
                    right_group.colliders.add().collider_name = bone

            for spring in sb.springs:
                if "Hair" in spring.vrm_name:
                    spring.collider_groups.add().collider_group_name = "LeftArmColliders"
                    spring.collider_groups.add().collider_group_name = "RightArmColliders"

            self.report({'INFO'}, "Arms and hand colliders added successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VRM_OT_Add_Jiggle_Bones(bpy.types.Operator):
    """Adds jiggle bone chains to selected bones for VRM models and assigns vertex groups"""
    bl_idname = "vrm.add_jiggle_bones"
    bl_label = "Add Jiggle Bones"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'BONE_DATA'

    def execute(self, context):
        try:
            # Retrieve scene properties
            bone_pair = context.scene.vrm_jiggle_bone_pair
            bone_quantity = context.scene.vrm_jiggle_bone_quantity
            affect_radius = context.scene.vrm_jiggle_affect_radius
            stiffness = context.scene.vrm_jiggle_stiffness
            angular_stiffness = context.scene.vrm_jiggle_angular_stiffness
            max_angle = context.scene.vrm_jiggle_max_angle
            drag_force_first = context.scene.vrm_jiggle_drag_force_first
            drag_force_end = context.scene.vrm_jiggle_drag_force_end
            subdivision_factor = context.scene.vrm_jiggle_subdivision_factor

            # Define bone pairs based on selection
            bone_pairs = {
                'UPPER_LEG': ["J_Bip_L_UpperLeg", "J_Bip_R_UpperLeg"],
                'LOWER_LEG': ["J_Bip_L_LowerLeg", "J_Bip_R_LowerLeg"],
                'SPINE': ["J_Bip_C_Spine"],
                'BUST': ["J_Bip_L_Bust", "J_Bip_R_Bust"],
                'CHEST': ["J_Bip_C_Chest"],
                'UPPER_ARM': ["J_Bip_L_UpperArm", "J_Bip_R_UpperArm"],
                'LOWER_ARM': ["J_Bip_L_LowerArm", "J_Bip_R_LowerArm"],
            }
            selected_bones = bone_pairs.get(bone_pair, ["J_Bip_L_UpperLeg", "J_Bip_R_UpperLeg"])

            # Find the armature and mesh
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            mesh = next(obj for obj in armature.children if obj.type == 'MESH')  # Assuming mesh is a child of the armature

            # Set active object to armature and enter edit mode
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')

            # Access edit bones
            edit_bones = armature.data.edit_bones
            jiggle_length = 0.05  # Length of each jiggle bone segment

            # Create jiggle bone chains for each selected bone
            jiggle_bone_positions = {}  # Store first bone names and their head positions
            jiggle_bone_chains = {}  # Store bone chains for spring joints
            for bone_name in selected_bones:
                if bone_name not in edit_bones:
                    self.report({'WARNING'}, f"Bone {bone_name} not found in armature")
                    continue
                bone = edit_bones[bone_name]
                matrix = bone.matrix
                length = bone.length
                midpoint_local = Vector((0, length / 2, 0))
                midpoint_world = matrix @ midpoint_local

                # Generate directions based on bone_quantity
                directions = []
                for i in range(bone_quantity):
                    angle = 2 * math.pi * i / bone_quantity
                    direction = Vector((math.cos(angle), 0, math.sin(angle)))  # Around Y-axis
                    directions.append(direction)

                # Create bone chains for each direction
                for i, direction in enumerate(directions):
                    head_local = midpoint_local + 0.05 * direction  # Radius is fixed to 0.05
                    head_world = matrix @ head_local
                    direction_world = matrix.to_3x3() @ direction

                    # Create chain of three bones
                    chain_bones = []
                    prev_bone = None
                    for j in range(3):
                        bone_suffix = f"_{i+1}" if j == 0 else f"_{i+1}_{j+1}"
                        new_bone_name = f"Jiggle_{bone_name}{bone_suffix}"
                        new_bone = edit_bones.new(new_bone_name)

                        if j == 0:
                            # First bone in chain
                            new_bone.head = head_world
                            new_bone.tail = head_world + jiggle_length * direction_world
                            new_bone.parent = bone
                            jiggle_bone_positions[new_bone_name] = armature.matrix_world @ head_world
                        else:
                            # Subsequent bones in chain
                            new_bone.head = prev_bone.tail
                            new_bone.tail = new_bone.head + jiggle_length * direction_world
                            new_bone.parent = prev_bone

                        chain_bones.append(new_bone_name)
                        prev_bone = new_bone

                    jiggle_bone_chains[f"Jiggle_{bone_name}_{i+1}"] = chain_bones

            # Switch back to object mode
            bpy.ops.object.mode_set(mode='OBJECT')

            # Add spring physics to jiggle bones
            sb = armature.data.vrm_addon_extension.spring_bone1
            for bone_name in selected_bones:
                for i in range(bone_quantity):
                    jiggle_bone_name = f"Jiggle_{bone_name}_{i+1}"
                    if jiggle_bone_name not in armature.data.bones:
                        self.report({'WARNING'}, f"Jiggle bone {jiggle_bone_name} not created")
                        continue
                    if jiggle_bone_name not in jiggle_bone_chains:
                        self.report({'WARNING'}, f"No chain found for {jiggle_bone_name}")
                        continue
                    new_spring = sb.springs.add()
                    new_spring.vrm_name = f"{jiggle_bone_name}_Spring"
                    # Add three joints for the bone chain
                    for j, chain_bone_name in enumerate(jiggle_bone_chains[jiggle_bone_name]):
                        joint = new_spring.joints.add()
                        joint.node.bone_name = chain_bone_name
                        joint.stiffness = stiffness
                        joint.angular_stiffness = angular_stiffness
                        joint.max_angle = math.radians(max_angle)  # Convert degrees to radians
                        joint.gravity_dir = Vector((0.0, 0.0, -1.0))
                        joint.drag_force = drag_force_first if j < 2 else drag_force_end

            # Create vertex groups and assign vertices with distance-based weights
            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.mode_set(mode='OBJECT')  # Ensure object mode
            mesh_data = mesh.data
            jiggle_vertex_groups = []  # Store created vertex groups for subdivision

            for jiggle_bone_name, head_pos in jiggle_bone_positions.items():
                if jiggle_bone_name not in armature.data.bones:
                    self.report({'WARNING'}, f"Jiggle bone {jiggle_bone_name} not found in armature")
                    continue
                # Create vertex group (only for the first bone in the chain)
                if jiggle_bone_name not in mesh.vertex_groups:
                    vg = mesh.vertex_groups.new(name=jiggle_bone_name)
                    jiggle_vertex_groups.append(jiggle_bone_name)
                else:
                    jiggle_vertex_groups.append(jiggle_bone_name)

                # Determine the parent bone
                parent_bone = None
                for bone in selected_bones:
                    if bone in jiggle_bone_name:
                        parent_bone = bone
                        break
                if not parent_bone:
                    self.report({'WARNING'}, f"Could not determine parent bone for {jiggle_bone_name}")
                    continue

                # Get the vertex group for the parent bone
                parent_vg = mesh.vertex_groups.get(parent_bone)
                if not parent_vg:
                    self.report({'WARNING'}, f"Vertex group {parent_bone} not found for {jiggle_bone_name}")
                    continue

                # Find vertices in the parent bone's vertex group within the affect radius
                selected_verts = []
                weights = []
                for v in mesh_data.vertices:
                    try:
                        parent_vg.weight(v.index)  # Check if vertex is in group
                        v_pos = mesh.matrix_world @ v.co
                        dist = (v_pos - head_pos).length
                        if dist < affect_radius:
                            # Calculate weight based on distance (linear falloff)
                            weight = 1.0 - (dist / affect_radius)
                            weight = max(0.1, weight)  # Ensure minimum weight
                            selected_verts.append(v.index)
                            weights.append(weight)
                    except RuntimeError:
                        continue  # Vertex not in parent vertex group

                # Assign vertices to vertex group with distance-based weights
                if selected_verts:
                    self.report({'INFO'}, f"Selected {len(selected_verts)} vertices for {jiggle_bone_name}")
                    for vert_idx, weight in zip(selected_verts, weights):
                        vg.add([vert_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices selected for {jiggle_bone_name} in {parent_bone} group")

            # Subdivide mesh in jiggle bone areas if subdivision_factor > 0
            if subdivision_factor > 0 and jiggle_vertex_groups:
                bpy.context.view_layer.objects.active = mesh
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

                # Select vertices in all jiggle vertex groups
                for vg_name in jiggle_vertex_groups:
                    vg = mesh.vertex_groups.get(vg_name)
                    if vg:
                        for v in mesh_data.vertices:
                            try:
                                vg.weight(v.index)  # Check if vertex is in group
                                v.select = True
                            except RuntimeError:
                                continue

                # Subdivide selected vertices
                bpy.ops.object.mode_set(mode='EDIT')
                for _ in range(subdivision_factor):
                    bpy.ops.mesh.subdivide(smoothness=0.0)
                bpy.ops.object.mode_set(mode='OBJECT')

                # Reassign vertices to vertex groups to account for new vertices
                for vg_name in jiggle_vertex_groups:
                    vg = mesh.vertex_groups.get(vg_name)
                    if not vg:
                        continue
                    parent_bone = None
                    for bone in selected_bones:
                        if bone in vg_name:
                            parent_bone = bone
                            break
                    if not parent_bone:
                        continue
                    parent_vg = mesh.vertex_groups.get(parent_bone)
                    if not parent_vg:
                        continue
                    head_pos = jiggle_bone_positions.get(vg_name)
                    if not head_pos:
                        continue
                    selected_verts = []
                    weights = []
                    for v in mesh_data.vertices:
                        try:
                            parent_vg.weight(v.index)
                            v_pos = mesh.matrix_world @ v.co
                            dist = (v_pos - head_pos).length
                            if dist < affect_radius:
                                weight = 1.0 - (dist / affect_radius)
                                weight = max(0.1, weight)  # Ensure minimum weight
                                selected_verts.append(v.index)
                                weights.append(weight)
                        except RuntimeError:
                            continue
                    if selected_verts:
                        for vert_idx, weight in zip(selected_verts, weights):
                            vg.add([vert_idx], weight, 'REPLACE')

            self.report({'INFO'}, f"Jiggle bone chains for {bone_pair.lower().replace('_', ' ')} added successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VRM_PT_Physics_Enhancer_Panel(bpy.types.Panel):
    """Creates a panel for VRM Physics Enhancer"""
    bl_label = "VRM Physics Enhancer"
    bl_idname = "VRM_PT_Physics_Enhancer"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VRM Physics Enhancer"

    def draw(self, context):
        layout = self.layout
        layout.operator("vrm.add_breast_physics", icon='MOD_PHYSICS')
        layout.label(text="Manually adjust the Collider Sizes + Positions using the VRM Add-on:")
        layout.label(text="Spring Bone → Spring Bone Colliders →")
        layout.label(text="J_Sec_L_Bust1 Collider or J_Sec_R_Bust1 Collider")
        layout.operator("vrm.add_long_hair_collider", icon='OUTLINER_OB_FORCE_FIELD')
        layout.operator("vrm.add_arm_hand_colliders", icon='VIEW_PAN')
        layout.label(text="Jiggle Bones Parameters:")
        layout.prop(context.scene, "vrm_jiggle_bone_pair")
        layout.prop(context.scene, "vrm_jiggle_bone_quantity")
        layout.prop(context.scene, "vrm_jiggle_affect_radius")
        layout.prop(context.scene, "vrm_jiggle_stiffness")
        layout.prop(context.scene, "vrm_jiggle_angular_stiffness")
        layout.prop(context.scene, "vrm_jiggle_max_angle")
        layout.prop(context.scene, "vrm_jiggle_drag_force_first")
        layout.prop(context.scene, "vrm_jiggle_drag_force_end")
        layout.prop(context.scene, "vrm_jiggle_subdivision_factor")
        layout.operator("vrm.add_jiggle_bones", icon='BONE_DATA')

def register():
    bpy.utils.register_class(VRM_OT_Add_Breast_Physics_Colliders)
    bpy.utils.register_class(VRM_OT_Add_Long_Hair_Collider)
    bpy.utils.register_class(VRM_OT_Add_Arm_Hand_Colliders)
    bpy.utils.register_class(VRM_OT_Add_Jiggle_Bones)
    bpy.utils.register_class(VRM_PT_Physics_Enhancer_Panel)

def unregister():
    bpy.utils.unregister_class(VRM_OT_Add_Breast_Physics_Colliders)
    bpy.utils.unregister_class(VRM_OT_Add_Long_Hair_Collider)
    bpy.utils.unregister_class(VRM_OT_Add_Arm_Hand_Colliders)
    bpy.utils.unregister_class(VRM_OT_Add_Jiggle_Bones)
    bpy.utils.unregister_class(VRM_PT_Physics_Enhancer_Panel)
    del bpy.types.Scene.vrm_jiggle_bone_pair
    del bpy.types.Scene.vrm_jiggle_bone_quantity
    del bpy.types.Scene.vrm_jiggle_affect_radius
    del bpy.types.Scene.vrm_jiggle_stiffness
    del bpy.types.Scene.vrm_jiggle_angular_stiffness
    del bpy.types.Scene.vrm_jiggle_max_angle
    del bpy.types.Scene.vrm_jiggle_drag_force_first
    del bpy.types.Scene.vrm_jiggle_drag_force_end
    del bpy.types.Scene.vrm_jiggle_subdivision_factor

if __name__ == "__main__":
    register()
