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
    default=1,  # Single chain for VRoid-like physics
    min=1,
    max=100
)

bpy.types.Scene.vrm_jiggle_affect_radius = bpy.props.FloatProperty(
    name="Affect Radius",
    description="Radius for vertex selection around the bone axis",
    default=0.15,  # Suitable for upper leg
    min=0.01,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_stiffness_first = bpy.props.FloatProperty(
    name="Stiffness (First Joint)",
    description="Stiffness for the first joint in each chain",
    default=1.07,  # VRoid bust base
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_stiffness_second = bpy.props.FloatProperty(
    name="Stiffness (Second Joint)",
    description="Stiffness for the second joint in each chain",
    default=1.035,  # Interpolated
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_stiffness_third = bpy.props.FloatProperty(
    name="Stiffness (Third Joint)",
    description="Stiffness for the third joint in each chain",
    default=1.00,  # VRoid bust tip
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness_first = bpy.props.FloatProperty(
    name="Angular Stiffness (First Joint)",
    description="Angular stiffness for the first joint",
    default=0.5,  # Moderate for control
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness_second = bpy.props.FloatProperty(
    name="Angular Stiffness (Second Joint)",
    description="Angular stiffness for the second joint",
    default=0.4,  # Moderate for transition
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness_third = bpy.props.FloatProperty(
    name="Angular Stiffness (Third Joint)",
    description="Angular stiffness for the third joint",
    default=0.3,  # Low for shakiness
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_max_angle = bpy.props.FloatProperty(
    name="Max Angle (Degrees)",
    description="Maximum rotation angle for jiggle bones",
    default=30.0,  # Suitable for upper leg dynamics
    min=0.0,
    max=90.0
)

bpy.types.Scene.vrm_jiggle_drag_force_first = bpy.props.FloatProperty(
    name="Drag Force (First Joint)",
    description="Drag force for the first joint in each chain",
    default=0.01,  # VRoid bust minimum
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_drag_force_second = bpy.props.FloatProperty(
    name="Drag Force (Second Joint)",
    description="Drag force for the second joint in each chain",
    default=0.255,  # Interpolated
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_drag_force_third = bpy.props.FloatProperty(
    name="Drag Force (Third Joint)",
    description="Drag force for the third joint in each chain",
    default=0.5,  # VRoid bust tip
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_joint_radius_first = bpy.props.FloatProperty(
    name="Joint Radius (First Joint)",
    description="Collision radius for the first joint",
    default=0.04,  # VRoid bust base
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_joint_radius_second = bpy.props.FloatProperty(
    name="Joint Radius (Second Joint)",
    description="Collision radius for the second joint",
    default=0.04,  # VRoid bust base
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_joint_radius_third = bpy.props.FloatProperty(
    name="Joint Radius (Third Joint)",
    description="Collision radius for the third joint",
    default=0.0,  # VRoid bust tip
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_gravity_power = bpy.props.FloatProperty(
    name="Gravity Power",
    description="Strength of gravity for jiggle bones",
    default=0.7,  # Reduced for upper leg motion
    min=0.0,
    max=10.0
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
            stiffness_first = context.scene.vrm_jiggle_stiffness_first
            stiffness_second = context.scene.vrm_jiggle_stiffness_second
            stiffness_third = context.scene.vrm_jiggle_stiffness_third
            angular_stiffness_first = context.scene.vrm_jiggle_angular_stiffness_first
            angular_stiffness_second = context.scene.vrm_jiggle_angular_stiffness_second
            angular_stiffness_third = context.scene.vrm_jiggle_angular_stiffness_third
            max_angle = context.scene.vrm_jiggle_max_angle
            drag_force_first = context.scene.vrm_jiggle_drag_force_first
            drag_force_second = context.scene.vrm_jiggle_drag_force_second
            drag_force_third = context.scene.vrm_jiggle_drag_force_third
            joint_radius_first = context.scene.vrm_jiggle_joint_radius_first
            joint_radius_second = context.scene.vrm_jiggle_joint_radius_second
            joint_radius_third = context.scene.vrm_jiggle_joint_radius_third
            gravity_power = context.scene.vrm_jiggle_gravity_power
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

                # Generate a single forward-facing chain (VRoid-like)
                directions = [Vector((0, 0, 1))]  # Forward direction (model's looking direction, +Z)

                # Create bone chains
                for i, direction in enumerate(directions[:bone_quantity]):  # Respect bone_quantity, but default is 1
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
                        # Apply per-joint physics parameters
                        if j == 0:
                            joint.stiffness = stiffness_first
                            joint.angular_stiffness = angular_stiffness_first
                            joint.drag_force = drag_force_first
                            joint.radius = joint_radius_first
                        elif j == 1:
                            joint.stiffness = stiffness_second
                            joint.angular_stiffness = angular_stiffness_second
                            joint.drag_force = drag_force_second
                            joint.radius = joint_radius_second
                        else:  # j == 2
                            joint.stiffness = stiffness_third
                            joint.angular_stiffness = angular_stiffness_third
                            joint.drag_force = drag_force_third
                            joint.radius = joint_radius_third
                        joint.max_angle = math.radians(max_angle)  # Convert degrees to radians
                        joint.gravity_dir = Vector((0.0, 0.0, -1.0))
                        joint.gravity_power = gravity_power

            # Create vertex groups and assign vertices with custom weight falloff
            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.mode_set(mode='OBJECT')  # Ensure object mode
            mesh_data = mesh.data
            jiggle_vertex_groups = []  # Store created vertex groups for subdivision

            # Build vertex adjacency list for expanding selection
            vertex_neighbors = [set() for _ in range(len(mesh_data.vertices))]
            for edge in mesh_data.edges:
                v0, v1 = edge.vertices
                vertex_neighbors[v0].add(v1)
                vertex_neighbors[v1].add(v0)

            # Select vertices in J_Bip_C_Hips vertex group
            hips_vg = mesh.vertex_groups.get("J_Bip_C_Hips")
            if not hips_vg:
                self.report({'WARNING'}, "Vertex group J_Bip_C_Hips not found")
                hips_vertices = set()
            else:
                hips_vertices = set()
                for v in mesh_data.vertices:
                    try:
                        weight = hips_vg.weight(v.index)
                        if weight > 0.1:  # Significant weight
                            hips_vertices.add(v.index)
                    except RuntimeError:
                        continue

            # Expand the selection twice (equivalent to pressing "+" key twice)
            expanded_hips_vertices = set(hips_vertices)
            for _ in range(2):  # Expand twice
                new_selection = set(expanded_hips_vertices)
                for v_idx in expanded_hips_vertices:
                    new_selection.update(vertex_neighbors[v_idx])
                expanded_hips_vertices = new_selection

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

                # Determine the corresponding lower leg bone to exclude its vertices
                lower_leg_bone = parent_bone.replace("UpperLeg", "LowerLeg")  # e.g., J_Bip_L_UpperLeg -> J_Bip_L_LowerLeg
                lower_leg_vg = mesh.vertex_groups.get(lower_leg_bone)

                # Get parent bone's head and tail in world space for cylindrical weighting
                bone = armature.data.bones[parent_bone]
                bone_head = armature.matrix_world @ bone.head_local
                bone_tail = armature.matrix_world @ bone.tail_local
                bone_length = (bone_tail - bone_head).length
                bone_dir = (bone_tail - bone_head).normalized()
                extended_length = bone_length * 1.2  # Extend the effective length slightly

                # Find vertices in the parent bone's vertex group
                selected_verts = []
                weights = []
                for v in mesh_data.vertices:
                    try:
                        # Check if vertex is in parent vertex group
                        parent_weight = parent_vg.weight(v.index)

                        # Exclude vertices that are in the lower leg vertex group
                        if lower_leg_vg:
                            try:
                                lower_leg_weight = lower_leg_vg.weight(v.index)
                                if lower_leg_weight > 0.1:  # Significant lower leg influence
                                    continue
                            except RuntimeError:
                                pass  # Vertex not in lower leg vertex group

                        # Exclude vertices in the expanded hips selection
                        if v.index in expanded_hips_vertices:
                            continue

                        v_pos = mesh.matrix_world @ v.co

                        # Project vertex onto bone axis
                        vec_to_vertex = v_pos - bone_head
                        t = vec_to_vertex.dot(bone_dir)  # Distance along bone axis
                        closest_point = bone_head + t * bone_dir
                        radial_dist = (v_pos - closest_point).length  # Distance from bone axis

                        # Check if vertex is within the cylindrical affect radius and within extended bone length
                        if radial_dist < affect_radius and 0 <= t <= extended_length:
                            # Calculate weight based on position along bone
                            if t < 0:  # Above bone head (towards torso)
                                # Harsh exponential falloff
                                dist_above_head = -t
                                weight = math.exp(-2.0 * dist_above_head / bone_length)
                            else:  # Between head and extended tail
                                # Linear falloff towards knee for more even distribution
                                normalized_t = t / extended_length
                                weight = (1.0 - normalized_t) ** 1.0  # Linear falloff

                            # Apply radial falloff to wrap around leg
                            radial_weight = (1.0 - radial_dist / affect_radius) ** 1.0  # Linear radial falloff
                            weight *= radial_weight

                            # Boost weights to ensure more influence in the middle
                            weight *= 1.5

                            # Clamp weights between 0.0 and 1.0
                            weight = max(0.0, min(1.0, weight))
                            if weight > 0.0:  # Only include vertices with non-zero weight
                                selected_verts.append(v.index)
                                weights.append(weight)
                    except RuntimeError:
                        continue  # Vertex not in parent vertex group

                # Assign vertices to vertex group with custom weights
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

                # Rebuild vertex adjacency list after subdivision
                vertex_neighbors = [set() for _ in range(len(mesh_data.vertices))]
                for edge in mesh_data.edges:
                    v0, v1 = edge.vertices
                    vertex_neighbors[v0].add(v1)
                    vertex_neighbors[v1].add(v0)

                # Re-select J_Bip_C_Hips vertices and expand again
                hips_vertices = set()
                for v in mesh_data.vertices:
                    try:
                        weight = hips_vg.weight(v.index)
                        if weight > 0.1:
                            hips_vertices.add(v.index)
                    except RuntimeError:
                        continue

                expanded_hips_vertices = set(hips_vertices)
                for _ in range(2):  # Expand twice
                    new_selection = set(expanded_hips_vertices)
                    for v_idx in expanded_hips_vertices:
                        new_selection.update(vertex_neighbors[v_idx])
                    expanded_hips_vertices = new_selection

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

                    # Determine the corresponding lower leg bone
                    lower_leg_bone = parent_bone.replace("UpperLeg", "LowerLeg")
                    lower_leg_vg = mesh.vertex_groups.get(lower_leg_bone)

                    # Get parent bone's head and tail again
                    bone = armature.data.bones[parent_bone]
                    bone_head = armature.matrix_world @ bone.head_local
                    bone_tail = armature.matrix_world @ bone.tail_local
                    bone_length = (bone_tail - bone_head).length
                    bone_dir = (bone_tail - bone_head).normalized()
                    extended_length = bone_length * 1.2  # Extend the effective length slightly

                    selected_verts = []
                    weights = []
                    for v in mesh_data.vertices:
                        try:
                            parent_vg.weight(v.index)

                            # Exclude vertices in the lower leg vertex group
                            if lower_leg_vg:
                                try:
                                    lower_leg_weight = lower_leg_vg.weight(v.index)
                                    if lower_leg_weight > 0.1:
                                        continue
                                except RuntimeError:
                                    pass

                            # Exclude vertices in the expanded hips selection
                            if v.index in expanded_hips_vertices:
                                continue

                            v_pos = mesh.matrix_world @ v.co

                            # Project vertex onto bone axis
                            vec_to_vertex = v_pos - bone_head
                            t = vec_to_vertex.dot(bone_dir)
                            closest_point = bone_head + t * bone_dir
                            radial_dist = (v_pos - closest_point).length

                            # Check if vertex is within the cylindrical affect radius and within extended bone length
                            if radial_dist < affect_radius and 0 <= t <= extended_length:
                                if t < 0:  # Above bone head
                                    dist_above_head = -t
                                    weight = math.exp(-2.0 * dist_above_head / bone_length)
                                else:  # Between head and extended tail
                                    normalized_t = t / extended_length
                                    weight = (1.0 - normalized_t) ** 1.0  # Linear falloff

                                radial_weight = (1.0 - radial_dist / affect_radius) ** 1.0
                                weight *= radial_weight
                                weight *= 1.5  # Boost weights
                                weight = max(0.0, min(1.0, weight))
                                if weight > 0.0:
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
        layout.label(text="Stiffness Settings:")
        layout.prop(context.scene, "vrm_jiggle_stiffness_first")
        layout.prop(context.scene, "vrm_jiggle_stiffness_second")
        layout.prop(context.scene, "vrm_jiggle_stiffness_third")
        layout.label(text="Angular Stiffness Settings:")
        layout.prop(context.scene, "vrm_jiggle_angular_stiffness_first")
        layout.prop(context.scene, "vrm_jiggle_angular_stiffness_second")
        layout.prop(context.scene, "vrm_jiggle_angular_stiffness_third")
        layout.prop(context.scene, "vrm_jiggle_max_angle")
        layout.label(text="Drag Force Settings:")
        layout.prop(context.scene, "vrm_jiggle_drag_force_first")
        layout.prop(context.scene, "vrm_jiggle_drag_force_second")
        layout.prop(context.scene, "vrm_jiggle_drag_force_third")
        layout.label(text="Joint Radius Settings:")
        layout.prop(context.scene, "vrm_jiggle_joint_radius_first")
        layout.prop(context.scene, "vrm_jiggle_joint_radius_second")
        layout.prop(context.scene, "vrm_jiggle_joint_radius_third")
        layout.prop(context.scene, "vrm_jiggle_gravity_power")
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
    del bpy.types.Scene.vrm_jiggle_stiffness_first
    del bpy.types.Scene.vrm_jiggle_stiffness_second
    del bpy.types.Scene.vrm_jiggle_stiffness_third
    del bpy.types.Scene.vrm_jiggle_angular_stiffness_first
    del bpy.types.Scene.vrm_jiggle_angular_stiffness_second
    del bpy.types.Scene.vrm_jiggle_angular_stiffness_third
    del bpy.types.Scene.vrm_jiggle_max_angle
    del bpy.types.Scene.vrm_jiggle_drag_force_first
    del bpy.types.Scene.vrm_jiggle_drag_force_second
    del bpy.types.Scene.vrm_jiggle_drag_force_third
    del bpy.types.Scene.vrm_jiggle_joint_radius_first
    del bpy.types.Scene.vrm_jiggle_joint_radius_second
    del bpy.types.Scene.vrm_jiggle_joint_radius_third
    del bpy.types.Scene.vrm_jiggle_gravity_power
    del bpy.types.Scene.vrm_jiggle_subdivision_factor

if __name__ == "__main__":
    register()
