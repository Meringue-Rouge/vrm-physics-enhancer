import bpy
from mathutils import Vector
import math

bl_info = {
    "name": "VRM Physics Enhancer",
    "blender": (5, 5, 1),
    "category": "3D View",
    "author": "Meringue Rouge",
    "version": (2, 0),
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

# Add new scene property for gravity power
bpy.types.Scene.vrm_breast_gravity_power = bpy.props.FloatProperty(
    name="Gravity Power",
    description="Gravity power for breast physics spring joints (third joint or end in 3-bone case)",
    default=0.15,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_scale_factor = bpy.props.FloatProperty(
    name="Scale Factor",
    description="Factor to scale the model and adjust physics parameters",
    default=20.0,
    min=0.1,
    max=100.0
)

# Define scene properties for Breast Physics Tweaker parameters
bpy.types.Scene.vrm_breast_weight_increase = bpy.props.FloatProperty(
    name="Weight Increase Factor",
    description="Factor to increase weights for non-blue regions in J_Sec_L_Bust2 and J_Sec_R_Bust2",
    default=1.5,
    min=1.0,
    max=10.0
)

bpy.types.Scene.vrm_breast_end_shrink_factor = bpy.props.FloatProperty(
    name="End Shrink Factor",
    description="Factor to shrink the influence area for J_Sec_L_Bust2_end and J_Sec_R_Bust2_end",
    default=0.7,
    min=0.1,
    max=1.0
)

bpy.types.Scene.vrm_breast_end_weight_reduction = bpy.props.FloatProperty(
    name="End Weight Reduction",
    description="Factor to reduce overall weights for J_Sec_L_Bust2_end and J_Sec_R_Bust2_end",
    default=0.5,
    min=0.1,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_bone_quantity = bpy.props.IntProperty(
    name="Bone Quantity",
    description="Number of jiggle bone chains per bone",
    default=1,
    min=1,
    max=100
)

bpy.types.Scene.vrm_jiggle_affect_radius = bpy.props.FloatProperty(
    name="Affect Radius",
    description="Radius for vertex selection around the bone axis",
    default=0.15,
    min=0.01,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_stiffness_first = bpy.props.FloatProperty(
    name="Stiffness (First Joint)",
    description="Stiffness for the first joint in each chain",
    default=1.07,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_stiffness_second = bpy.props.FloatProperty(
    name="Stiffness (Second Joint)",
    description="Stiffness for the second joint in each chain",
    default=1.035,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_stiffness_third = bpy.props.FloatProperty(
    name="Stiffness (Third Joint)",
    description="Stiffness for the third joint in each chain",
    default=1.00,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness_first = bpy.props.FloatProperty(
    name="Angular Stiffness (First Joint)",
    description="Angular stiffness for the first joint",
    default=0.5,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness_second = bpy.props.FloatProperty(
    name="Angular Stiffness (Second Joint)",
    description="Angular stiffness for the second joint",
    default=0.4,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_angular_stiffness_third = bpy.props.FloatProperty(
    name="Angular Stiffness (Third Joint)",
    description="Angular stiffness for the third joint",
    default=0.3,
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
    name="Drag Force (First Joint)",
    description="Drag force for the first joint in each chain",
    default=0.01,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_drag_force_second = bpy.props.FloatProperty(
    name="Drag Force (Second Joint)",
    description="Drag force for the second joint in each chain",
    default=0.255,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_drag_force_third = bpy.props.FloatProperty(
    name="Drag Force (Third Joint)",
    description="Drag force for the third joint in each chain",
    default=0.5,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_joint_radius_first = bpy.props.FloatProperty(
    name="Joint Radius (First Joint)",
    description="Collision radius for the first joint",
    default=0.04,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_joint_radius_second = bpy.props.FloatProperty(
    name="Joint Radius (Second Joint)",
    description="Collision radius for the second joint",
    default=0.04,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_joint_radius_third = bpy.props.FloatProperty(
    name="Joint Radius (Third Joint)",
    description="Collision radius for the third joint",
    default=0.0,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_jiggle_gravity_power = bpy.props.FloatProperty(
    name="Gravity Power",
    description="Strength of gravity for jiggle bones",
    default=0.7,
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

# Collapsible toggle for Jiggle Physics parameters
bpy.types.Scene.vrm_jiggle_params_collapsed = bpy.props.BoolProperty(
    name="Show Jiggle Parameters",
    description="Show or hide advanced jiggle physics parameters",
    default=True
)

bpy.types.Scene.vrm_dress_subdivision_count = bpy.props.IntProperty(
    name="Dress Subdivision Count",
    description="Number of subdivision iterations for skirt vertex groups",
    default=1,
    min=0,
    max=3
)

bpy.types.Scene.vrm_dress_subdivision_smoothness = bpy.props.FloatProperty(
    name="Dress Subdivision Smoothness",
    description="Smoothness factor for skirt subdivision (0.0 for no smoothing, 1.0 for full smoothing)",
    default=1.0,
    min=0.0,
    max=1.0
)

# Define scene properties for Long Dress Collision parameters
bpy.types.Scene.vrm_dress_collider_radius = bpy.props.FloatProperty(
    name="Collider Radius",
    description="Radius for lower leg and foot colliders",
    default=0.09,
    min=0.01,
    max=1.0
)

bpy.types.Scene.vrm_upper_leg_collider_multiplier = bpy.props.FloatProperty(
    name="Upper Leg Collider Multiplier",
    description="Multiplier for the upper leg collider radius",
    default=3.0,
    min=0.1,
    max=10.0
)

bpy.types.Scene.vrm_skirt_hit_radius_first = bpy.props.FloatProperty(
    name="Hit Radius (First Joint)",
    description="Collision radius for the first joint in Skirt springs",
    default=0.07,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_hit_radius_second = bpy.props.FloatProperty(
    name="Hit Radius (Second Joint)",
    description="Collision radius for the second joint in Skirt springs",
    default=0.2,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_hit_radius_third = bpy.props.FloatProperty(
    name="Hit Radius (Third Joint)",
    description="Collision radius for the third joint in Skirt springs",
    default=0.3,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_hit_radius_fourth = bpy.props.FloatProperty(
    name="Hit Radius (Fourth+ Joint)",
    description="Collision radius for the fourth and subsequent joints in Skirt springs",
    default=0.1,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_gravity_power_first = bpy.props.FloatProperty(
    name="Gravity Power (First Joint)",
    description="Gravity power for the first joint in Skirt springs",
    default=0.0,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_gravity_power_rest = bpy.props.FloatProperty(
    name="Gravity Power (Rest)",
    description="Gravity power for the second and subsequent joints in Skirt springs",
    default=1.0,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_drag_force_first = bpy.props.FloatProperty(
    name="Drag Force (First Joint)",
    description="Drag force for the first joint in Skirt springs",
    default=0.8,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_drag_force_second = bpy.props.FloatProperty(
    name="Drag Force (Second Joint)",
    description="Drag force for the second joint in Skirt springs",
    default=0.6,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_drag_force_third = bpy.props.FloatProperty(
    name="Drag Force (Third Joint)",
    description="Drag force for the third joint in Skirt springs",
    default=0.4,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_drag_force_fourth = bpy.props.FloatProperty(
    name="Drag Force (Fourth Joint)",
    description="Drag force for the fourth joint in Skirt springs",
    default=0.2,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_drag_force_fifth = bpy.props.FloatProperty(
    name="Drag Force (Fifth+ Joint)",
    description="Drag force for the fifth and subsequent joints in Skirt springs",
    default=0.0,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_stiffness_first = bpy.props.FloatProperty(
    name="Stiffness (First Joint)",
    description="Stiffness for the first joint in Skirt springs",
    default=2.0,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_stiffness_second = bpy.props.FloatProperty(
    name="Stiffness (Second Joint)",
    description="Stiffness for the second joint in Skirt springs",
    default=0.8,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_stiffness_third = bpy.props.FloatProperty(
    name="Stiffness (Third Joint)",
    description="Stiffness for the third joint in Skirt springs",
    default=0.5,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_stiffness_fourth = bpy.props.FloatProperty(
    name="Stiffness (Fourth+ Joint)",
    description="Stiffness for the fourth and subsequent joints in Skirt springs",
    default=0.2,
    min=0.0,
    max=10.0
)

bpy.types.Scene.vrm_skirt_angular_stiffness_first = bpy.props.FloatProperty(
    name="Angular Stiffness (First Joint)",
    description="Angular stiffness for the first joint in Skirt springs",
    default=0.6,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_angular_stiffness_second = bpy.props.FloatProperty(
    name="Angular Stiffness (Second Joint)",
    description="Angular stiffness for the second joint in Skirt springs",
    default=0.5,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_angular_stiffness_third = bpy.props.FloatProperty(
    name="Angular Stiffness (Third Joint)",
    description="Angular stiffness for the third joint in Skirt springs",
    default=0.4,
    min=0.0,
    max=1.0
)

bpy.types.Scene.vrm_skirt_angular_stiffness_fourth = bpy.props.FloatProperty(
    name="Angular Stiffness (Fourth+ Joint)",
    description="Angular stiffness for the fourth and subsequent joints in Skirt springs",
    default=0.3,
    min=0.0,
    max=1.0
)

# Collapsible toggle for Long Dress parameters
bpy.types.Scene.vrm_dress_params_collapsed = bpy.props.BoolProperty(
    name="Show Dress Parameters",
    description="Show or hide advanced dress physics parameters",
    default=True
)


# Add new scene property for bone count
bpy.types.Scene.vrm_breast_bone_count = bpy.props.EnumProperty(
    name="Breast Bone Count",
    description="Number of bones per breast for physics simulation",
    items=[
        ('3', "3 Bones (Default)", "Use 3 bones per breast (J_Sec_X_Bust2, _end)"),
        ('4', "4 Bones (Advanced)", "Use 4 bones per breast (J_Sec_X_Bust2, _end, _3)"),
    ],
    default='3'
)

# Add new scene property for physics presets
bpy.types.Scene.vrm_breast_physics_preset = bpy.props.EnumProperty(
    name="Physics Preset",
    description="Select a preset to adjust breast physics parameters",
    items=[
        ('DISCRETE', "Discrete", "Subtle physics with 3 bones"),
        ('BOUNCY', "Bouncy", "Exaggerated physics with 4 bones"),
    ],
    default='DISCRETE'
)

class VRM_OT_Scale_Model_Physics(bpy.types.Operator):
    """Scales the model and adjusts physics parameters for VRM models"""
    bl_idname = "vrm.scale_model_physics"
    bl_label = "Scale Model with Scaled Physics"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'MODIFIER'

    def execute(self, context):
        try:
            # Get the selected armature
            armature = bpy.context.object
            if armature.type != 'ARMATURE':
                self.report({'ERROR'}, "Selected object is not an armature")
                return {'CANCELLED'}

            # Get the scale factor from scene properties
            scale_factor = context.scene.vrm_scale_factor
            scale_factor_1_4 = scale_factor ** 1.4  # For stiffness and drag_force (others)
            scale_factor_0_9 = scale_factor ** 0.9  # For stiffness (non-end bust)
            scale_factor_0_8 = scale_factor ** 0.8  # For stiffness (end bust)
            scale_factor_0_7 = scale_factor ** 0.7  # For stiffness (third bust)
            scale_factor_0_2 = scale_factor ** 0.2  # For drag_force (end bust)
            scale_factor_0_1 = scale_factor ** 0.1  # For drag_force (third bust)
            scale_factor_0_001 = scale_factor ** 0.001  # For drag_force (non-end bust)

            # Define bust joint names
            bust_joints = [
                "J_Sec_L_Bust1", "J_Sec_L_Bust2", "J_Sec_R_Bust1", "J_Sec_R_Bust2",
                "J_Sec_L_Bust2_end", "J_Sec_R_Bust2_end", "J_Sec_L_Bust3", "J_Sec_R_Bust3"
            ]

            # Scale the armature
            armature.scale = (scale_factor, scale_factor, scale_factor)

            # Get VRM extension
            vrm_extension = armature.data.vrm_addon_extension

            # Adjust SpringBone settings for VRM 1.0
            if hasattr(vrm_extension, 'spring_bone1') and hasattr(vrm_extension.spring_bone1, 'springs'):
                for spring in vrm_extension.spring_bone1.springs:
                    # Adjust joint properties
                    if hasattr(spring, 'joints'):
                        for joint in spring.joints:
                            # Get joint name (if available)
                            joint_name = getattr(joint.node, 'bone_name', None) if hasattr(joint, 'node') else None
                            
                            # Scale stiffness
                            if hasattr(joint, 'stiffness'):
                                if joint_name in ["J_Sec_L_Bust1", "J_Sec_L_Bust2", "J_Sec_R_Bust1", "J_Sec_R_Bust2"]:
                                    joint.stiffness *= scale_factor_0_9  # S^0.9 for non-end bust
                                elif joint_name in ["J_Sec_L_Bust2_end", "J_Sec_R_Bust2_end"]:
                                    joint.stiffness *= scale_factor_0_8  # S^0.8 for end bust
                                elif joint_name in ["J_Sec_L_Bust3", "J_Sec_R_Bust3"]:
                                    joint.stiffness *= scale_factor_0_7  # S^0.7 for third bust
                                else:
                                    joint.stiffness *= scale_factor_1_4  # S^1.4 for others

                            # Scale drag_force
                            if hasattr(joint, 'drag_force'):
                                if joint_name in ["J_Sec_L_Bust1", "J_Sec_L_Bust2", "J_Sec_R_Bust1", "J_Sec_R_Bust2"]:
                                    joint.drag_force *= scale_factor_0_001  # S^0.001 for non-end bust
                                elif joint_name in ["J_Sec_L_Bust2_end", "J_Sec_R_Bust2_end"]:
                                    joint.drag_force *= scale_factor_0_2  # S^0.2 for end bust
                                elif joint_name in ["J_Sec_L_Bust3", "J_Sec_R_Bust3"]:
                                    joint.drag_force *= scale_factor_0_1  # S^0.1 for third bust
                                else:
                                    joint.drag_force *= scale_factor_1_4  # S^1.4 for others

                            # Keep gravity_power unchanged
                            if hasattr(joint, 'gravity_power'):
                                pass  # No scaling

                            # Scale hit_radius linearly
                            if hasattr(joint, 'radius'):
                                joint.radius *= scale_factor

                    # Scale collider radii linearly
                    if hasattr(spring, 'collider_groups'):
                        for collider_group in spring.collider_groups:
                            if hasattr(collider_group, 'colliders'):
                                for collider_ref in collider_group.colliders:
                                    # Find the actual collider in vrm_extension.spring_bone1.colliders
                                    collider = next((c for c in vrm_extension.spring_bone1.colliders if c.node.bone_name == collider_ref.collider_name), None)
                                    if collider:
                                        if hasattr(collider.shape, 'sphere') and hasattr(collider.shape.sphere, 'radius'):
                                            collider.shape.sphere.radius *= scale_factor
                                        elif hasattr(collider.shape, 'capsule') and hasattr(collider.shape.capsule, 'radius'):
                                            collider.shape.capsule.radius *= scale_factor

            # Apply the scale to make it permanent
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            self.report({'INFO'}, "Model scaled and physics settings adjusted successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VRM_OT_Set_Breast_Physics_Preset(bpy.types.Operator):
    """Sets breast physics parameters based on selected preset"""
    bl_idname = "vrm.set_breast_physics_preset"
    bl_label = "Apply Breast Physics Preset"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'PRESET'

    def execute(self, context):
        preset = context.scene.vrm_breast_physics_preset
        if preset == 'DISCRETE':
            context.scene.vrm_breast_weight_increase = 1.5
            context.scene.vrm_breast_end_shrink_factor = 0.7
            context.scene.vrm_breast_end_weight_reduction = 0.5
            context.scene.vrm_breast_bone_count = '3'
        elif preset == 'BOUNCY':
            context.scene.vrm_breast_weight_increase = 6.0
            context.scene.vrm_breast_end_shrink_factor = 0.9
            context.scene.vrm_breast_end_weight_reduction = 0.8
            context.scene.vrm_breast_bone_count = '4'
        self.report({'INFO'}, f"Applied {preset} preset to breast physics parameters")
        return {'FINISHED'}

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

class VRM_OT_Breast_Physics_Tweaker(bpy.types.Operator):
    """Tweaks breast physics by adjusting vertex group weights for J_Sec_L_Bust2 and J_Sec_R_Bust2, and creating adjusted _end and optionally _3 groups"""
    bl_idname = "vrm.breast_physics_tweaker"
    bl_label = "Breast Physics Tweaker"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'MOD_PHYSICS'

    def execute(self, context):
        try:
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            mesh = next(obj for obj in armature.children if obj.type == 'MESH')
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = armature.data.edit_bones

            # Define bones to process
            bust_bones = ["J_Sec_L_Bust2", "J_Sec_R_Bust2"]
            end_bone_names = ["J_Sec_L_Bust2_end", "J_Sec_R_Bust2_end"]
            third_bone_names = ["J_Sec_L_Bust3", "J_Sec_R_Bust3"]
            bone_count = int(context.scene.vrm_breast_bone_count)

            # Add new end bones if they don't exist
            for bust_bone, end_bone_name in zip(bust_bones, end_bone_names):
                if end_bone_name not in edit_bones:
                    source_bone = edit_bones.get(bust_bone)
                    if not source_bone:
                        self.report({'WARNING'}, f"Bone {bust_bone} not found")
                        continue
                    new_bone = edit_bones.new(end_bone_name)
                    bone_length = source_bone.length
                    direction = (source_bone.tail - source_bone.head).normalized()
                    new_bone.head = source_bone.tail
                    new_bone.tail = new_bone.head + bone_length * direction
                    new_bone.parent = source_bone
                    new_bone.use_deform = True
                    self.report({'INFO'}, f"Created bone {end_bone_name}")

            # Add new third bones if bone_count is 4
            if bone_count == 4:
                for end_bone_name, third_bone_name in zip(end_bone_names, third_bone_names):
                    end_bone = edit_bones.get(end_bone_name)
                    if not end_bone:
                        self.report({'WARNING'}, f"Bone {end_bone_name} not found")
                        continue
                    if third_bone_name not in edit_bones:
                        new_bone = edit_bones.new(third_bone_name)
                        bone_length = end_bone.length
                        direction = (end_bone.tail - end_bone.head).normalized()
                        new_bone.head = end_bone.tail
                        new_bone.tail = new_bone.head + bone_length * direction
                        new_bone.parent = end_bone
                        new_bone.use_deform = True
                        self.report({'INFO'}, f"Created bone {third_bone_name}")

            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.view_layer.objects.active = mesh
            mesh_data = mesh.data

            # Get user-defined parameters
            weight_increase = context.scene.vrm_breast_weight_increase
            end_shrink_factor = context.scene.vrm_breast_end_shrink_factor
            end_weight_reduction = context.scene.vrm_breast_end_weight_reduction
            gravity_power = context.scene.vrm_breast_gravity_power

            # Create or get vertex groups for _end and _3 bones
            for end_bone in end_bone_names:
                if end_bone not in mesh.vertex_groups:
                    mesh.vertex_groups.new(name=end_bone)
                    self.report({'INFO'}, f"Created vertex group {end_bone}")
            if bone_count == 4:
                for third_bone in third_bone_names:
                    if third_bone not in mesh.vertex_groups:
                        mesh.vertex_groups.new(name=third_bone)
                        self.report({'INFO'}, f"Created vertex group {third_bone}")

            # Add or update spring bone settings for VRM
            sb = armature.data.vrm_addon_extension.spring_bone1
            for spring in sb.springs:
                if any(b in spring.vrm_name for b in ["Bust", "Breast"]):
                    # Determine the side of the spring (left or right)
                    is_left = "L" in spring.vrm_name or any("J_Sec_L_Bust" in joint.node.bone_name for joint in spring.joints)
                    is_right = "R" in spring.vrm_name or any("J_Sec_R_Bust" in joint.node.bone_name for joint in spring.joints)
                    
                    # Skip if spring side is ambiguous
                    if not (is_left or is_right) or (is_left and is_right):
                        self.report({'WARNING'}, f"Spring {spring.vrm_name} has ambiguous side, skipping joint assignment")
                        continue

                    # Select bones for this spring based on side
                    side_bust_bone = "J_Sec_L_Bust2" if is_left else "J_Sec_R_Bust2"
                    side_end_bone = "J_Sec_L_Bust2_end" if is_left else "J_Sec_R_Bust2_end"
                    side_third_bone = "J_Sec_L_Bust3" if is_left else "J_Sec_R_Bust3"

                    # Check if joints for bust, end, and third bones exist
                    bust_joint_exists = any(joint.node.bone_name == side_bust_bone for joint in spring.joints)
                    end_joint_exists = any(joint.node.bone_name == side_end_bone for joint in spring.joints)
                    third_joint_exists = any(joint.node.bone_name == side_third_bone for joint in spring.joints)

                    # Update or add bust joint
                    if not bust_joint_exists:
                        joint = spring.joints.add()
                        joint.node.bone_name = side_bust_bone
                        joint.stiffness = 0.9
                        joint.drag_force = 0.25
                        joint.radius = 0.06
                        joint.gravity_power = gravity_power * (0.75 if bone_count == 3 else 0.5)
                        joint.gravity_dir = Vector((0.0, 0.0, -1.0))
                        self.report({'INFO'}, f"Added spring joint for {side_bust_bone} in {spring.vrm_name}")
                    else:
                        for joint in spring.joints:
                            if joint.node.bone_name == side_bust_bone:
                                joint.gravity_power = gravity_power * (0.75 if bone_count == 3 else 0.5)
                                self.report({'INFO'}, f"Updated gravity_power for {side_bust_bone} in {spring.vrm_name} to {joint.gravity_power}")

                    # Update or add end joint
                    if not end_joint_exists:
                        joint = spring.joints.add()
                        joint.node.bone_name = side_end_bone
                        joint.stiffness = 0.8
                        joint.drag_force = 0.2
                        joint.radius = 0.05
                        joint.gravity_power = gravity_power * (1.0 if bone_count == 3 else 0.75)
                        joint.gravity_dir = Vector((0.0, 0.0, -1.0))
                        self.report({'INFO'}, f"Added spring joint for {side_end_bone} in {spring.vrm_name}")
                    else:
                        for joint in spring.joints:
                            if joint.node.bone_name == side_end_bone:
                                joint.gravity_power = gravity_power * (1.0 if bone_count == 3 else 0.75)
                                self.report({'INFO'}, f"Updated gravity_power for {side_end_bone} in {spring.vrm_name} to {joint.gravity_power}")

                    # Update or add third joint if bone_count is 4
                    if bone_count == 4:
                        if not third_joint_exists:
                            joint = spring.joints.add()
                            joint.node.bone_name = side_third_bone
                            joint.stiffness = 0.7
                            joint.drag_force = 0.15
                            joint.radius = 0.04
                            joint.gravity_power = gravity_power
                            joint.gravity_dir = Vector((0.0, 0.0, -1.0))
                            self.report({'INFO'}, f"Added spring joint for {side_third_bone} in {spring.vrm_name}")
                        else:
                            for joint in spring.joints:
                                if joint.node.bone_name == side_third_bone:
                                    joint.gravity_power = gravity_power
                                    self.report({'INFO'}, f"Updated gravity_power for {side_third_bone} in {spring.vrm_name} to {joint.gravity_power}")

            for bone_name, end_bone_name, third_bone_name in zip(bust_bones, end_bone_names, third_bone_names):
                source_vg = mesh.vertex_groups.get(bone_name)
                end_vg = mesh.vertex_groups.get(end_bone_name)
                third_vg = mesh.vertex_groups.get(third_bone_name) if bone_count == 4 else None

                if not source_vg:
                    self.report({'WARNING'}, f"Vertex group {bone_name} not found")
                    continue
                if not end_vg:
                    self.report({'WARNING'}, f"Vertex group {end_bone_name} not found")
                    continue
                if bone_count == 4 and not third_vg:
                    self.report({'WARNING'}, f"Vertex group {third_bone_name} not found")
                    continue

                # Get bone position for distance calculation
                bone = armature.data.bones.get(bone_name)
                if not bone:
                    self.report({'WARNING'}, f"Bone {bone_name} not found in armature")
                    continue
                bone_head = armature.matrix_world @ bone.head_local
                bone_tail = armature.matrix_world @ bone.tail_local
                bone_center = (bone_head + bone_tail) / 2

                # Process vertices for source vertex group (increase non-blue weights)
                selected_verts = []
                increased_weights = []
                for v in mesh_data.vertices:
                    try:
                        weight = source_vg.weight(v.index)
                        if weight > 0.0 and weight < 0.2:  # Non-pure blue (assuming blue is low weight < 0.2)
                            v_pos = mesh.matrix_world @ v.co
                            dist = (v_pos - bone_center).length
                            # Increase weight more at center, less at edges
                            weight_factor = weight_increase - 0.5 * dist
                            new_weight = weight * weight_factor
                            new_weight = max(0.0, min(1.0, new_weight))
                            if new_weight > 0.0:
                                selected_verts.append(v.index)
                                increased_weights.append(new_weight)
                    except RuntimeError:
                        continue

                # Assign increased weights to source vertex group
                if selected_verts:
                    self.report({'INFO'}, f"Adjusted {len(selected_verts)} vertices for {bone_name}")
                    for v_idx, weight in zip(selected_verts, increased_weights):
                        source_vg.add([v_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices adjusted for {bone_name}")

                # Process vertices for _end vertex group (shrunk and reduced)
                end_verts = []
                end_weights = []
                for v in mesh_data.vertices:
                    try:
                        weight = source_vg.weight(v.index)
                        if weight > 0.0:
                            v_pos = mesh.matrix_world @ v.co
                            dist = (v_pos - bone_center).length
                            # Shrink influence by user-defined factor
                            if dist < 0.3:
                                new_weight = weight * end_shrink_factor * end_weight_reduction
                                new_weight = max(0.0, min(1.0, new_weight))
                                if new_weight > 0.0:
                                    end_verts.append(v.index)
                                    end_weights.append(new_weight)
                    except RuntimeError:
                        continue

                # Assign weights to _end vertex group
                if end_verts:
                    self.report({'INFO'}, f"Assigned {len(end_verts)} vertices to {end_bone_name}")
                    for v_idx, weight in zip(end_verts, end_weights):
                        end_vg.add([v_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices assigned to {end_bone_name}")

                # Process vertices for _3 vertex group (further shrunk and reduced) if bone_count is 4
                if bone_count == 4:
                    third_verts = []
                    third_weights = []
                    for v in mesh_data.vertices:
                        try:
                            weight = source_vg.weight(v.index)
                            if weight > 0.0:
                                v_pos = mesh.matrix_world @ v.co
                                dist = (v_pos - bone_center).length
                                # Further shrink influence for _3 (tighter radius, more reduction)
                                if dist < 0.2:
                                    new_weight = weight * end_shrink_factor * 0.5 * end_weight_reduction
                                    new_weight = max(0.0, min(1.0, new_weight))
                                    if new_weight > 0.0:
                                        third_verts.append(v.index)
                                        third_weights.append(new_weight)
                        except RuntimeError:
                            continue

                    # Assign weights to _3 vertex group
                    if third_verts:
                        self.report({'INFO'}, f"Assigned {len(third_verts)} vertices to {third_bone_name}")
                        for v_idx, weight in zip(third_verts, third_weights):
                            third_vg.add([v_idx], weight, 'REPLACE')
                    else:
                        self.report({'WARNING'}, f"No vertices assigned to {third_bone_name}")

            self.report({'INFO'}, f"Breast physics tweaked successfully with {bone_count} bones per breast")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            bpy.ops.object.mode_set(mode='OBJECT')
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

class VRM_OT_Add_Long_Dress_Collision(bpy.types.Operator):
    """Adds accurate long dress collision colliders for lower legs, feet, and upper legs, adjusts Skirt Spring Bone properties, and applies weight painting"""
    bl_idname = "vrm.add_long_dress_collision"
    bl_label = "Add Accurate Long Dress Collision"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'OUTLINER_OB_FORCE_FIELD'

    def execute(self, context):
        try:
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            mesh = next(obj for obj in armature.children if obj.type == 'MESH')
            bpy.context.view_layer.objects.active = armature
            sb = armature.data.vrm_addon_extension.spring_bone1

            # Define the leg and foot bones
            upper_leg_bones = ["J_Bip_L_UpperLeg", "J_Bip_R_UpperLeg"]
            lower_leg_bones = ["J_Bip_L_LowerLeg", "J_Bip_R_LowerLeg"]
            foot_bones = ["J_Bip_L_Foot", "J_Bip_R_Foot"]
            collider_configs = [
                {"offset": [0.0, 0.0, 0.019], "suffix": ""},
                {"offset": [0.0, 0.15, 0.019], "suffix": "_Offset1"},
                {"offset": [0.0, 0.3, 0.019], "suffix": "_Offset2"},
                {"offset": [0.0, 0.45, 0.019], "suffix": "_Offset3"},
            ]
            foot_collider_config = [
                {"offset": [0.0, 0.0, 0.019], "suffix": ""}
            ]

            # Create or modify colliders for upper leg bones
            created_colliders = {bone: [] for bone in upper_leg_bones + lower_leg_bones + foot_bones}
            upper_leg_collider_radius = context.scene.vrm_upper_leg_collider_multiplier * context.scene.vrm_dress_collider_radius
            for bone in upper_leg_bones:
                # Check for existing colliders
                existing_colliders = [c for c in sb.colliders if c.node.bone_name == bone]
                if existing_colliders:
                    for collider in existing_colliders:
                        if collider.shape_type == "Sphere":
                            collider.shape.sphere.radius *= context.scene.vrm_upper_leg_collider_multiplier
                        elif collider.shape_type == "Capsule":
                            collider.shape.capsule.radius *= context.scene.vrm_upper_leg_collider_multiplier
                        created_colliders[bone].append(collider.node.bone_name)
                        self.report({'INFO'}, f"Multiplied radius of existing collider for {bone} by {context.scene.vrm_upper_leg_collider_multiplier}")
                else:
                    # Create new sphere collider
                    collider = sb.colliders.add()
                    collider_name = f"{bone}_UpperLeg"
                    collider.node.bone_name = bone
                    collider.shape.sphere.radius = upper_leg_collider_radius
                    collider.shape.sphere.offset = [0.0, 0.0, 0.0]  # Center at bone head
                    created_colliders[bone].append(collider_name)
                    self.report({'INFO'}, f"Created new collider for {bone} with radius {upper_leg_collider_radius}")

            # Create colliders for lower leg bones
            for bone in lower_leg_bones:
                for config in collider_configs:
                    collider = sb.colliders.add()
                    collider_name = f"{bone}{config['suffix']}"
                    collider.node.bone_name = bone
                    collider.shape.sphere.radius = context.scene.vrm_dress_collider_radius
                    collider.shape.sphere.offset = config['offset']
                    created_colliders[bone].append(collider_name)

            # Create colliders for foot bones
            for bone in foot_bones:
                for config in foot_collider_config:
                    collider = sb.colliders.add()
                    collider_name = f"{bone}{config['suffix']}"
                    collider.node.bone_name = bone
                    collider.shape.sphere.radius = context.scene.vrm_dress_collider_radius
                    collider.shape.sphere.offset = config['offset']
                    created_colliders[bone].append(collider_name)

            # Create collider groups for each bone
            for bone in upper_leg_bones + lower_leg_bones + foot_bones:
                group = sb.collider_groups.add()
                group.vrm_name = bone
                for collider_name in created_colliders[bone]:
                    group_collider = group.colliders.add()
                    group_collider.collider_name = collider_name

            # Assign collider groups to springs containing "Skirt" but not "SkirtBack" in their name
            for spring in sb.springs:
                if "Skirt" in spring.vrm_name and "SkirtBack" not in spring.vrm_name:
                    for bone in upper_leg_bones + lower_leg_bones + foot_bones:
                        collider_group = spring.collider_groups.add()
                        collider_group.collider_group_name = bone

            # Update properties for Skirt Spring Bone Springs, excluding SkirtBack
            for spring in sb.springs:
                if "Skirt" in spring.vrm_name and "SkirtBack" not in spring.vrm_name:
                    for idx, joint in enumerate(spring.joints):
                        if idx == 0:
                            joint.radius = context.scene.vrm_skirt_hit_radius_first
                            joint.drag_force = min(max(context.scene.vrm_skirt_drag_force_first, 0.0), 1.0)
                            joint.stiffness = context.scene.vrm_skirt_stiffness_first
                            joint.angular_stiffness = min(max(context.scene.vrm_skirt_angular_stiffness_first, 0.3), 1.0)
                        elif idx == 1:
                            joint.radius = context.scene.vrm_skirt_hit_radius_second
                            joint.drag_force = min(max(context.scene.vrm_skirt_drag_force_second, 0.0), 1.0)
                            joint.stiffness = context.scene.vrm_skirt_stiffness_second
                            joint.angular_stiffness = min(max(context.scene.vrm_skirt_angular_stiffness_second, 0.3), 1.0)
                        elif idx == 2:
                            joint.radius = context.scene.vrm_skirt_hit_radius_third
                            joint.drag_force = min(max(context.scene.vrm_skirt_drag_force_third, 0.0), 1.0)
                            joint.stiffness = context.scene.vrm_skirt_stiffness_third
                            joint.angular_stiffness = min(max(context.scene.vrm_skirt_angular_stiffness_third, 0.3), 1.0)
                        else:
                            joint.radius = context.scene.vrm_skirt_hit_radius_fourth
                            joint.drag_force = min(max(context.scene.vrm_skirt_drag_force_fifth, 0.0), 1.0)
                            joint.stiffness = context.scene.vrm_skirt_stiffness_fourth
                            joint.angular_stiffness = min(max(context.scene.vrm_skirt_angular_stiffness_fourth, 0.3), 1.0)
                        joint.gravity_power = context.scene.vrm_skirt_gravity_power_first if idx == 0 else context.scene.vrm_skirt_gravity_power_rest

            # Weight painting for skirt and lower leg vertex groups
            bpy.context.view_layer.objects.active = mesh
            mesh_data = mesh.data

            # Define skirt vertex group pairs (0_01 and 1_01), excluding SkirtBack
            skirt_vg_pairs = [
                ("J_Sec_R_SkirtFront0_01", "J_Sec_R_SkirtFront1_01"),
                ("J_Sec_L_SkirtFront0_01", "J_Sec_L_SkirtFront1_01"),
            ]

            # Process skirt vertex groups (0_01 to 1_01)
            for target_vg_name, source_vg_name in skirt_vg_pairs:
                source_vg = mesh.vertex_groups.get(source_vg_name)
                target_vg = mesh.vertex_groups.get(target_vg_name)

                if not source_vg:
                    self.report({'WARNING'}, f"Source vertex group {source_vg_name} not found")
                    continue
                if not target_vg:
                    target_vg = mesh.vertex_groups.new(name=target_vg_name)
                    self.report({'INFO'}, f"Created vertex group {target_vg_name}")

                # Attempt to find the closest matching bone by removing suffixes
                bone_name_base = source_vg_name.replace("J_Sec_", "J_Sec_").replace("1_01", "")
                bone = None
                for b in armature.data.bones:
                    if bone_name_base in b.name:
                        bone = b
                        break
                if not bone:
                    self.report({'WARNING'}, f"No matching bone found for {source_vg_name} (tried {bone_name_base})")
                    continue

                bone_head = armature.matrix_world @ bone.head_local
                bone_tail = armature.matrix_world @ bone.tail_local
                z_min = min(bone_head.z, bone_tail.z)
                z_max = max(bone_head.z, bone_tail.z)
                z_range = z_max - z_min

                # Collect vertices from source vertex group
                selected_verts = []
                weights = []
                for v in mesh_data.vertices:
                    try:
                        weight = source_vg.weight(v.index)
                        if weight > 0.0:
                            v_pos = mesh.matrix_world @ v.co
                            # Base weight is middling (0.5)
                            new_weight = 0.5
                            # Apply falloff for vertices below the bone
                            if v_pos.z < z_min:
                                dist_below = z_min - v_pos.z
                                falloff = math.exp(-dist_below / (0.1 * z_range))
                                new_weight *= falloff
                            new_weight = max(0.0, min(1.0, new_weight))
                            if new_weight > 0.0:
                                selected_verts.append(v.index)
                                weights.append(new_weight)
                    except RuntimeError:
                        continue

                # Assign weights to target vertex group
                if selected_verts:
                    self.report({'INFO'}, f"Assigned {len(selected_verts)} vertices to {target_vg_name}")
                    for v_idx, weight in zip(selected_verts, weights):
                        target_vg.add([v_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices assigned to {target_vg_name}")

            # Find skirt end vertex groups (containing "Skirt" and "end_01", excluding "SkirtBack")
            skirt_end_vertex_groups = [vg for vg in mesh.vertex_groups if "Skirt" in vg.name and "end_01" in vg.name and "SkirtBack" not in vg.name]
            if not skirt_end_vertex_groups:
                self.report({'WARNING'}, "No vertex groups containing 'Skirt' and 'end_01' (excluding 'SkirtBack') found")
                return {'CANCELLED'}

            # Transfer weights to _end_01 vertex groups from their corresponding _01 groups
            for end_vg in skirt_end_vertex_groups:
                # Derive the source vertex group name by replacing "end_01" with "01"
                source_vg_name = end_vg.name.replace("end_01", "01")
                source_vg = mesh.vertex_groups.get(source_vg_name)

                if not source_vg:
                    self.report({'WARNING'}, f"Source vertex group {source_vg_name} not found for {end_vg.name}")
                    continue

                # Attempt to find the closest matching bone
                bone_name_base = source_vg_name.replace("J_Sec_", "J_Sec_").replace("_01", "")
                bone = None
                for b in armature.data.bones:
                    if bone_name_base in b.name:
                        bone = b
                        break
                if not bone:
                    self.report({'WARNING'}, f"No matching bone found for {source_vg_name} (tried {bone_name_base})")
                    continue

                bone_head = armature.matrix_world @ bone.head_local
                bone_tail = armature.matrix_world @ bone.tail_local
                z_min = min(bone_head.z, bone_tail.z)
                z_max = max(bone_head.z, bone_tail.z)
                z_range = z_max - z_min
                z_mid = (z_min + z_max) / 2  # Midpoint for selection threshold

                # Collect vertices from source vertex group, but only those below the Z midpoint
                selected_verts = []
                weights = []
                for v in mesh_data.vertices:
                    try:
                        weight = source_vg.weight(v.index)
                        if weight > 0.0:
                            v_pos = mesh.matrix_world @ v.co
                            # Only select vertices below the Z midpoint
                            if v_pos.z <= z_mid:
                                normalized_z = (z_mid - v_pos.z) / (z_mid - z_min) if (z_mid - z_min) != 0 else 0.0
                                # Use a fourth-power falloff for a smoother gradient
                                new_weight = (normalized_z ** 4) * 0.1 + 0.03
                                new_weight = max(0.0, min(1.0, new_weight))
                                if new_weight > 0.0:
                                    selected_verts.append(v.index)
                                    weights.append(new_weight)
                    except RuntimeError:
                        continue

                # Assign weights to the _end_01 vertex group
                if selected_verts:
                    self.report({'INFO'}, f"Assigned {len(selected_verts)} vertices to {end_vg.name}")
                    for v_idx, weight in zip(selected_verts, weights):
                        end_vg.add([v_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices assigned to {end_vg.name}")

                # Smooth the weights for _end_01 vertex group
                bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
                bpy.context.object.data.use_paint_mask_vertex = True
                bpy.ops.object.vertex_group_smooth(group_select_mode='ACTIVE', factor=0.5, repeat=3, expand=0.0)
                bpy.ops.object.mode_set(mode='OBJECT')

            # Get or create lower leg vertex groups
            left_leg_vg = mesh.vertex_groups.get("J_Bip_L_LowerLeg")
            if not left_leg_vg:
                left_leg_vg = mesh.vertex_groups.new(name="J_Bip_L_LowerLeg")
                self.report({'INFO'}, "Created vertex group J_Bip_L_LowerLeg")
            right_leg_vg = mesh.vertex_groups.get("J_Bip_R_LowerLeg")
            if not right_leg_vg:
                right_leg_vg = mesh.vertex_groups.new(name="J_Bip_R_LowerLeg")
                self.report({'INFO'}, "Created vertex group J_Bip_R_LowerLeg")

            # Get lower leg bone positions
            left_bone = armature.data.bones.get("J_Bip_L_LowerLeg")
            right_bone = armature.data.bones.get("J_Bip_R_LowerLeg")
            if not left_bone or not right_bone:
                self.report({'WARNING'}, "Lower leg bones not found")
                return {'CANCELLED'}

            left_bone_head = armature.matrix_world @ left_bone.head_local
            left_bone_tail = armature.matrix_world @ left_bone.tail_local
            left_bone_dir = (left_bone_tail - left_bone_head).normalized()
            right_bone_head = armature.matrix_world @ right_bone.head_local
            right_bone_tail = armature.matrix_world @ right_bone.tail_local
            right_bone_dir = (right_bone_tail - right_bone_head).normalized()

            # Parameters for weight gradient and selection radius
            selection_radius = 0.3  # Increased to widen affected area
            decay_factor = 0.15     # Adjusted for smoother falloff

            # Process vertices from skirt end vertex groups
            left_leg_verts = []
            left_leg_weights = []
            right_leg_verts = []
            right_leg_weights = []
            for vg in skirt_end_vertex_groups:
                self.report({'INFO'}, f"Processing skirt end vertex group: {vg.name}")
                vg_verts = []
                for v in mesh_data.vertices:
                    try:
                        weight = vg.weight(v.index)
                        if weight > 0.0:
                            vg_verts.append(v)
                    except RuntimeError:
                        continue
                self.report({'INFO'}, f"Found {len(vg_verts)} vertices with weight > 0 in {vg.name}")

                for v in vg_verts:
                    v_pos = mesh.matrix_world @ v.co

                    # Compute distance to left leg bone
                    vec_to_vertex_left = v_pos - left_bone_head
                    t_left = vec_to_vertex_left.dot(left_bone_dir)
                    t_left = max(0, min(t_left, (left_bone_tail - left_bone_head).length))
                    closest_point_left = left_bone_head + t_left * left_bone_dir
                    dist_left = (v_pos - closest_point_left).length

                    # Compute distance to right leg bone
                    vec_to_vertex_right = v_pos - right_bone_head
                    t_right = vec_to_vertex_right.dot(right_bone_dir)
                    t_right = max(0, min(t_right, (right_bone_tail - right_bone_head).length))
                    closest_point_right = right_bone_head + t_right * right_bone_dir
                    dist_right = (v_pos - closest_point_right).length

                    # Select leg based on closer distance, use X-coordinate as tiebreaker
                    if dist_left < dist_right or (dist_left == dist_right and v_pos.x > 0):
                        if dist_left <= selection_radius:
                            new_weight = math.exp(-dist_left / decay_factor)
                            new_weight = max(0.0, min(1.0, new_weight))
                            if new_weight > 0.0:
                                left_leg_verts.append(v.index)
                                left_leg_weights.append(new_weight)
                                self.report({'INFO'}, f"Vertex {v.index} assigned to left leg, distance: {dist_left:.3f}, weight: {new_weight:.3f}")
                    else:
                        if dist_right <= selection_radius:
                            new_weight = math.exp(-dist_right / decay_factor)
                            new_weight = max(0.0, min(1.0, new_weight))
                            if new_weight > 0.0:
                                right_leg_verts.append(v.index)
                                right_leg_weights.append(new_weight)
                                self.report({'INFO'}, f"Vertex {v.index} assigned to right leg, distance: {dist_right:.3f}, weight: {new_weight:.3f}")

            # Assign weights to lower leg vertex groups
            if left_leg_verts:
                self.report({'INFO'}, f"Assigned weights to {len(left_leg_verts)} vertices in J_Bip_L_LowerLeg")
                for v_idx, w in zip(left_leg_verts, left_leg_weights):
                    left_leg_vg.add([v_idx], w, 'REPLACE')
                # Smooth the weights for the left leg vertex group
                bpy.context.object.vertex_groups.active = left_leg_vg
                bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
                bpy.context.object.data.use_paint_mask_vertex = True
                bpy.ops.object.vertex_group_smooth(group_select_mode='ACTIVE', factor=0.5, repeat=3, expand=0.0)
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                self.report({'WARNING'}, "No vertices assigned to J_Bip_L_LowerLeg")

            if right_leg_verts:
                self.report({'INFO'}, f"Assigned weights to {len(right_leg_verts)} vertices in J_Bip_R_LowerLeg")
                for v_idx, w in zip(right_leg_verts, right_leg_weights):
                    right_leg_vg.add([v_idx], w, 'REPLACE')
                # Smooth the weights for the right leg vertex group
                bpy.context.object.vertex_groups.active = right_leg_vg
                bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
                bpy.context.object.data.use_paint_mask_vertex = True
                bpy.ops.object.vertex_group_smooth(group_select_mode='ACTIVE', factor=0.5, repeat=3, expand=0.0)
                bpy.ops.object.mode_set(mode='OBJECT')
            else:
                self.report({'WARNING'}, "No vertices assigned to J_Bip_R_LowerLeg")

            self.report({'INFO'}, "Long dress collision colliders, Skirt Spring Bone properties, and weight painting updated successfully")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            return {'CANCELLED'}

class VRM_OT_Improve_Long_Dress_Topology(bpy.types.Operator):
    """Improves long dress topology by subdividing skirt vertex groups and adjusting weight painting"""
    bl_idname = "vrm.improve_long_dress_topology"
    bl_label = "Improve Long Dress Topology"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'MESH_DATA'

    def execute(self, context):
        try:
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            mesh = next(obj for obj in armature.children if obj.type == 'MESH')
            bpy.context.view_layer.objects.active = mesh
            mesh_data = mesh.data
            subdivision_count = context.scene.vrm_dress_subdivision_count
            subdivision_smoothness = context.scene.vrm_dress_subdivision_smoothness
            skirt_vertex_groups = [vg for vg in mesh.vertex_groups if "Skirt" in vg.name]

            if not skirt_vertex_groups:
                self.report({'WARNING'}, "No vertex groups containing 'Skirt' found")
                return {'CANCELLED'}

            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='VERT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')

            for vg in skirt_vertex_groups:
                for v in mesh_data.vertices:
                    try:
                        vg.weight(v.index)
                        v.select = True
                    except RuntimeError:
                        continue

            if subdivision_count > 0:
                bpy.ops.object.mode_set(mode='EDIT')
                for _ in range(subdivision_count):
                    bpy.ops.mesh.subdivide(smoothness=subdivision_smoothness)
                bpy.ops.object.mode_set(mode='OBJECT')
                self.report({'INFO'}, f"Subdivided skirt vertex groups {subdivision_count} time(s) with smoothness {subdivision_smoothness}")

            sides = ["L", "R"]
            directions = ["Front", "Back"]
            target_groups = [f"J_Sec_{side}_Skirt{direction}2_end_01" for side in sides for direction in directions]
            source_groups = [f"J_Sec_{side}_Skirt{direction}2_01" for side in sides for direction in directions]

            for target_vg_name, source_vg_name in zip(target_groups, source_groups):
                source_vg = mesh.vertex_groups.get(source_vg_name)
                target_vg = mesh.vertex_groups.get(target_vg_name)

                if not source_vg:
                    self.report({'WARNING'}, f"Source vertex group {source_vg_name} not found")
                    continue
                if not target_vg:
                    target_vg = mesh.vertex_groups.new(name=target_vg_name)
                    self.report({'INFO'}, f"Created vertex group {target_vg_name}")

                z_coords = []
                source_vertices = []
                source_weights = []
                for v in mesh_data.vertices:
                    try:
                        weight = source_vg.weight(v.index)
                        if weight > 0.0:
                            v_pos = mesh.matrix_world @ v.co
                            z_coords.append(v_pos.z)
                            source_vertices.append(v.index)
                            source_weights.append(weight)
                    except RuntimeError:
                        continue

                if not z_coords:
                    self.report({'WARNING'}, f"No vertices found in {source_vg_name}")
                    continue

                z_min = min(z_coords)
                z_max = max(z_coords)
                z_mid = (z_min + z_max) / 2
                z_bound = z_mid

                selected_verts = []
                weights = []
                for v_idx, source_weight in zip(source_vertices, source_weights):
                    v = mesh_data.vertices[v_idx]
                    v_pos = mesh.matrix_world @ v.co
                    if v_pos.z <= z_bound:
                        normalized_z = (z_bound - v_pos.z) / (z_bound - z_min) if z_bound != z_min else 0.0
                        new_weight = normalized_z
                        new_weight = max(0.0, min(1.0, new_weight))
                        if new_weight > 0.0:
                            selected_verts.append(v_idx)
                            weights.append(new_weight)

                if selected_verts:
                    self.report({'INFO'}, f"Assigned {len(selected_verts)} vertices to {target_vg_name}")
                    for v_idx, weight in zip(selected_verts, weights):
                        target_vg.add([v_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices assigned to {target_vg_name}")

            if subdivision_count == 0:
                self.report({'INFO'}, "Subdivision count is 0, only weight painting applied")

            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error: {str(e)}")
            bpy.ops.object.mode_set(mode='OBJECT')
            return {'CANCELLED'}

class VRM_OT_Add_Jiggle_Bones(bpy.types.Operator):
    """Adds jiggle bone chains to selected bones for VRM models and assigns vertex groups"""
    bl_idname = "vrm.add_jiggle_bones"
    bl_label = "Add Jiggle Bones"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'BONE_DATA'

    def execute(self, context):
        try:
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
            armature = next(obj for obj in bpy.data.objects if obj.type == 'ARMATURE')
            mesh = next(obj for obj in armature.children if obj.type == 'MESH')
            bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='EDIT')
            edit_bones = armature.data.edit_bones
            jiggle_length = 0.05

            jiggle_bone_positions = {}
            jiggle_bone_chains = {}
            for bone_name in selected_bones:
                if bone_name not in edit_bones:
                    self.report({'WARNING'}, f"Bone {bone_name} not found in armature")
                    continue
                bone = edit_bones[bone_name]
                matrix = bone.matrix
                length = bone.length
                midpoint_local = Vector((0, length / 2, 0))
                midpoint_world = matrix @ midpoint_local
                directions = [Vector((0, 0, 1))]

                for i, direction in enumerate(directions[:bone_quantity]):
                    head_local = midpoint_local + 0.05 * direction
                    head_world = matrix @ head_local
                    direction_world = matrix.to_3x3() @ direction
                    chain_bones = []
                    prev_bone = None
                    for j in range(3):
                        bone_suffix = f"_{i+1}" if j == 0 else f"_{i+1}_{j+1}"
                        new_bone_name = f"Jiggle_{bone_name}{bone_suffix}"
                        new_bone = edit_bones.new(new_bone_name)
                        if j == 0:
                            new_bone.head = head_world
                            new_bone.tail = head_world + jiggle_length * direction_world
                            new_bone.parent = bone
                            jiggle_bone_positions[new_bone_name] = armature.matrix_world @ head_world
                        else:
                            new_bone.head = prev_bone.tail
                            new_bone.tail = new_bone.head + jiggle_length * direction_world
                            new_bone.parent = prev_bone
                        chain_bones.append(new_bone_name)
                        prev_bone = new_bone
                    jiggle_bone_chains[f"Jiggle_{bone_name}_{i+1}"] = chain_bones

            bpy.ops.object.mode_set(mode='OBJECT')
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
                    for j, chain_bone_name in enumerate(jiggle_bone_chains[jiggle_bone_name]):
                        joint = new_spring.joints.add()
                        joint.node.bone_name = chain_bone_name
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
                        else:
                            joint.stiffness = stiffness_third
                            joint.angular_stiffness = angular_stiffness_third
                            joint.drag_force = drag_force_third
                            joint.radius = joint_radius_third
                        joint.max_angle = math.radians(max_angle)
                        joint.gravity_dir = Vector((0.0, 0.0, -1.0))
                        joint.gravity_power = gravity_power

            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.mode_set(mode='OBJECT')
            mesh_data = mesh.data
            jiggle_vertex_groups = []
            vertex_neighbors = [set() for _ in range(len(mesh_data.vertices))]
            for edge in mesh_data.edges:
                v0, v1 = edge.vertices
                vertex_neighbors[v0].add(v1)
                vertex_neighbors[v1].add(v0)

            hips_vg = mesh.vertex_groups.get("J_Bip_C_Hips")
            if not hips_vg:
                self.report({'WARNING'}, "Vertex group J_Bip_C_Hips not found")
                hips_vertices = set()
            else:
                hips_vertices = set()
                for v in mesh_data.vertices:
                    try:
                        weight = hips_vg.weight(v.index)
                        if weight > 0.1:
                            hips_vertices.add(v.index)
                    except RuntimeError:
                        continue

            expanded_hips_vertices = set(hips_vertices)
            for _ in range(2):
                new_selection = set(expanded_hips_vertices)
                for v_idx in expanded_hips_vertices:
                    new_selection.update(vertex_neighbors[v_idx])
                expanded_hips_vertices = new_selection

            for jiggle_bone_name, head_pos in jiggle_bone_positions.items():
                if jiggle_bone_name not in armature.data.bones:
                    self.report({'WARNING'}, f"Jiggle bone {jiggle_bone_name} not found in armature")
                    continue
                if jiggle_bone_name not in mesh.vertex_groups:
                    vg = mesh.vertex_groups.new(name=jiggle_bone_name)
                    jiggle_vertex_groups.append(jiggle_bone_name)
                else:
                    jiggle_vertex_groups.append(jiggle_bone_name)

                parent_bone = None
                for bone in selected_bones:
                    if bone in jiggle_bone_name:
                        parent_bone = bone
                        break
                if not parent_bone:
                    self.report({'WARNING'}, f"Could not determine parent bone for {jiggle_bone_name}")
                    continue

                parent_vg = mesh.vertex_groups.get(parent_bone)
                if not parent_vg:
                    self.report({'WARNING'}, f"Vertex group {parent_bone} not found for {jiggle_bone_name}")
                    continue

                lower_leg_bone = parent_bone.replace("UpperLeg", "LowerLeg")
                lower_leg_vg = mesh.vertex_groups.get(lower_leg_bone)

                bone = armature.data.bones[parent_bone]
                bone_head = armature.matrix_world @ bone.head_local
                bone_tail = armature.matrix_world @ bone.tail_local
                bone_length = (bone_tail - bone_head).length
                bone_dir = (bone_tail - bone_head).normalized()
                extended_length = bone_length * 1.2

                selected_verts = []
                weights = []
                for v in mesh_data.vertices:
                    try:
                        parent_weight = parent_vg.weight(v.index)
                        if lower_leg_vg:
                            try:
                                lower_leg_weight = lower_leg_vg.weight(v.index)
                                if lower_leg_weight > 0.1:
                                    continue
                            except RuntimeError:
                                pass
                        if v.index in expanded_hips_vertices:
                            continue
                        v_pos = mesh.matrix_world @ v.co
                        vec_to_vertex = v_pos - bone_head
                        t = vec_to_vertex.dot(bone_dir)
                        closest_point = bone_head + t * bone_dir
                        radial_dist = (v_pos - closest_point).length
                        if radial_dist < affect_radius and 0 <= t <= extended_length:
                            if t < 0:
                                dist_above_head = -t
                                weight = math.exp(-2.0 * dist_above_head / bone_length)
                            else:
                                normalized_t = t / extended_length
                                weight = (1.0 - normalized_t) ** 1.0
                            radial_weight = (1.0 - radial_dist / affect_radius) ** 1.0
                            weight *= radial_weight
                            weight *= 1.5
                            weight = max(0.0, min(1.0, weight))
                            if weight > 0.0:
                                selected_verts.append(v.index)
                                weights.append(weight)
                    except RuntimeError:
                        continue

                if selected_verts:
                    self.report({'INFO'}, f"Selected {len(selected_verts)} vertices for {jiggle_bone_name}")
                    for vert_idx, weight in zip(selected_verts, weights):
                        vg.add([vert_idx], weight, 'REPLACE')
                else:
                    self.report({'WARNING'}, f"No vertices selected for {jiggle_bone_name} in {parent_bone} group")

            if subdivision_factor > 0 and jiggle_vertex_groups:
                bpy.context.view_layer.objects.active = mesh
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_mode(type='VERT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')
                for vg_name in jiggle_vertex_groups:
                    vg = mesh.vertex_groups.get(vg_name)
                    if vg:
                        for v in mesh_data.vertices:
                            try:
                                vg.weight(v.index)
                                v.select = True
                            except RuntimeError:
                                continue
                bpy.ops.object.mode_set(mode='EDIT')
                for _ in range(subdivision_factor):
                    bpy.ops.mesh.subdivide(smoothness=0.0)
                bpy.ops.object.mode_set(mode='OBJECT')
                vertex_neighbors = [set() for _ in range(len(mesh_data.vertices))]
                for edge in mesh_data.edges:
                    v0, v1 = edge.vertices
                    vertex_neighbors[v0].add(v1)
                    vertex_neighbors[v1].add(v0)
                hips_vertices = set()
                for v in mesh_data.vertices:
                    try:
                        weight = hips_vg.weight(v.index)
                        if weight > 0.1:
                            hips_vertices.add(v.index)
                    except RuntimeError:
                        continue
                expanded_hips_vertices = set(hips_vertices)
                for _ in range(2):
                    new_selection = set(expanded_hips_vertices)
                    for v_idx in expanded_hips_vertices:
                        new_selection.update(vertex_neighbors[v_idx])
                    expanded_hips_vertices = new_selection
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
                    lower_leg_bone = parent_bone.replace("UpperLeg", "LowerLeg")
                    lower_leg_vg = mesh.vertex_groups.get(lower_leg_bone)
                    bone = armature.data.bones[parent_bone]
                    bone_head = armature.matrix_world @ bone.head_local
                    bone_tail = armature.matrix_world @ bone.tail_local
                    bone_length = (bone_tail - bone_head).length
                    bone_dir = (bone_tail - bone_head).normalized()
                    extended_length = bone_length * 1.2
                    selected_verts = []
                    weights = []
                    for v in mesh_data.vertices:
                        try:
                            parent_vg.weight(v.index)
                            if lower_leg_vg:
                                try:
                                    lower_leg_weight = lower_leg_vg.weight(v.index)
                                    if lower_leg_weight > 0.1:
                                        continue
                                except RuntimeError:
                                    pass
                            if v.index in expanded_hips_vertices:
                                continue
                            v_pos = mesh.matrix_world @ v.co
                            vec_to_vertex = v_pos - bone_head
                            t = vec_to_vertex.dot(bone_dir)
                            closest_point = bone_head + t * bone_dir
                            radial_dist = (v_pos - closest_point).length
                            if radial_dist < affect_radius and 0 <= t <= extended_length:
                                if t < 0:
                                    dist_above_head = -t
                                    weight = math.exp(-2.0 * dist_above_head / bone_length)
                                else:
                                    normalized_t = t / extended_length
                                    weight = (1.0 - normalized_t) ** 1.0
                                radial_weight = (1.0 - radial_dist / affect_radius) ** 1.0
                                weight *= radial_weight
                                weight *= 1.5
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

        # Breast Physics Section
        layout.label(text="Breast Physics", icon='MESH_CIRCLE')
        breast_box = layout.box()
        breast_box.operator("vrm.add_breast_physics", icon='MOD_PHYSICS')
        breast_tweaker_box = breast_box.box()
        breast_tweaker_box.label(text="Breast Physics Tweaker Settings:")
        breast_tweaker_box.prop(context.scene, "vrm_breast_physics_preset")
        breast_tweaker_box.operator("vrm.set_breast_physics_preset", icon='PRESET')
        breast_tweaker_box.prop(context.scene, "vrm_breast_bone_count")
        breast_tweaker_box.prop(context.scene, "vrm_breast_weight_increase")
        breast_tweaker_box.prop(context.scene, "vrm_breast_end_shrink_factor")
        breast_tweaker_box.prop(context.scene, "vrm_breast_end_weight_reduction")
        breast_tweaker_box.prop(context.scene, "vrm_breast_gravity_power")
        breast_tweaker_box.operator("vrm.breast_physics_tweaker", icon='MOD_PHYSICS')

        # Basics Section
        layout.label(text="Basics", icon='OUTLINER_OB_ARMATURE')
        basics_box = layout.box()
        basics_box.operator("vrm.add_long_hair_collider", icon='OUTLINER_OB_FORCE_FIELD')
        basics_box.operator("vrm.add_arm_hand_colliders", icon='VIEW_PAN')

        # Accurate Physics for Dresses Section
        layout.label(text="Accurate Physics for Long Dresses", icon='MESH_CYLINDER')
        dress_box = layout.box()
        dress_box.operator("vrm.add_long_dress_collision", icon='OUTLINER_OB_FORCE_FIELD')
        dress_box.prop(context.scene, "vrm_dress_params_collapsed", text="Show Parameters", icon='DOWNARROW_HLT' if not context.scene.vrm_dress_params_collapsed else 'RIGHTARROW')
        if not context.scene.vrm_dress_params_collapsed:
            collider_box = dress_box.box()
            collider_box.label(text="Collider Settings:")
            collider_box.prop(context.scene, "vrm_dress_collider_radius")
            collider_box.prop(context.scene, "vrm_upper_leg_collider_multiplier")
            skirt_box = dress_box.box()
            skirt_box.label(text="Skirt Spring Settings:")
            skirt_box.prop(context.scene, "vrm_skirt_hit_radius_first")
            skirt_box.prop(context.scene, "vrm_skirt_hit_radius_second")
            skirt_box.prop(context.scene, "vrm_skirt_hit_radius_third")
            skirt_box.prop(context.scene, "vrm_skirt_hit_radius_fourth")
            skirt_box.prop(context.scene, "vrm_skirt_gravity_power_first")
            skirt_box.prop(context.scene, "vrm_skirt_gravity_power_rest")
            skirt_box.label(text="Drag Force:")
            skirt_box.prop(context.scene, "vrm_skirt_drag_force_first")
            skirt_box.prop(context.scene, "vrm_skirt_drag_force_second")
            skirt_box.prop(context.scene, "vrm_skirt_drag_force_third")
            skirt_box.prop(context.scene, "vrm_skirt_drag_force_fourth")
            skirt_box.prop(context.scene, "vrm_skirt_drag_force_fifth")
            skirt_box.label(text="Stiffness:")
            skirt_box.prop(context.scene, "vrm_skirt_stiffness_first")
            skirt_box.prop(context.scene, "vrm_skirt_stiffness_second")
            skirt_box.prop(context.scene, "vrm_skirt_stiffness_third")
            skirt_box.prop(context.scene, "vrm_skirt_stiffness_fourth")
            skirt_box.label(text="Angular Stiffness:")
            skirt_box.prop(context.scene, "vrm_skirt_angular_stiffness_first")
            skirt_box.prop(context.scene, "vrm_skirt_angular_stiffness_second")
            skirt_box.prop(context.scene, "vrm_skirt_angular_stiffness_third")
            skirt_box.prop(context.scene, "vrm_skirt_angular_stiffness_fourth")

        topology_box = dress_box.box()
        topology_box.label(text="Topology Settings:")
        topology_box.prop(context.scene, "vrm_dress_subdivision_count")
        topology_box.prop(context.scene, "vrm_dress_subdivision_smoothness")
        topology_box.operator("vrm.improve_long_dress_topology", icon='MESH_DATA')

        # Scaling Section
        layout.label(text="Scaling", icon='MODIFIER')
        scaling_box = layout.box()
        scaling_box.prop(context.scene, "vrm_scale_factor")
        scaling_box.operator("vrm.scale_model_physics", icon='MODIFIER')

        # Jiggle Physics Section
        layout.label(text="Jiggle Physics", icon='BONE_DATA')
        jiggle_box = layout.box()
        jiggle_box.prop(context.scene, "vrm_jiggle_bone_pair")
        jiggle_box.prop(context.scene, "vrm_jiggle_affect_radius")
        jiggle_box.prop(context.scene, "vrm_jiggle_params_collapsed", text="Show Parameters", icon='DOWNARROW_HLT' if not context.scene.vrm_jiggle_params_collapsed else 'RIGHTARROW')
        if not context.scene.vrm_jiggle_params_collapsed:
            jiggle_params_box = jiggle_box.box()
            jiggle_params_box.prop(context.scene, "vrm_jiggle_bone_quantity")
            jiggle_params_box.label(text="Stiffness Settings:")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_stiffness_first")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_stiffness_second")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_stiffness_third")
            jiggle_params_box.label(text="Angular Stiffness Settings:")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_angular_stiffness_first")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_angular_stiffness_second")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_angular_stiffness_third")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_max_angle")
            jiggle_params_box.label(text="Drag Force Settings:")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_drag_force_first")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_drag_force_second")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_drag_force_third")
            jiggle_params_box.label(text="Joint Radius Settings:")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_joint_radius_first")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_joint_radius_second")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_joint_radius_third")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_gravity_power")
            jiggle_params_box.prop(context.scene, "vrm_jiggle_subdivision_factor")
        jiggle_box.operator("vrm.add_jiggle_bones", icon='BONE_DATA')

def register():
    bpy.utils.register_class(VRM_OT_Add_Breast_Physics_Colliders)
    bpy.utils.register_class(VRM_OT_Add_Long_Hair_Collider)
    bpy.utils.register_class(VRM_OT_Add_Arm_Hand_Colliders)
    bpy.utils.register_class(VRM_OT_Add_Long_Dress_Collision)
    bpy.utils.register_class(VRM_OT_Improve_Long_Dress_Topology)
    bpy.utils.register_class(VRM_OT_Add_Jiggle_Bones)
    bpy.utils.register_class(VRM_OT_Breast_Physics_Tweaker)
    bpy.utils.register_class(VRM_OT_Scale_Model_Physics)
    bpy.utils.register_class(VRM_OT_Set_Breast_Physics_Preset)
    bpy.utils.register_class(VRM_PT_Physics_Enhancer_Panel)
    bpy.types.Scene.vrm_breast_gravity_power = bpy.props.FloatProperty(
        name="Gravity Power",
        description="Gravity power for breast physics spring joints (third joint or end in 3-bone case)",
        default=0.15,
        min=0.0,
        max=10.0
    )

def unregister():
    bpy.utils.unregister_class(VRM_OT_Add_Breast_Physics_Colliders)
    bpy.utils.unregister_class(VRM_OT_Add_Long_Hair_Collider)
    bpy.utils.unregister_class(VRM_OT_Add_Arm_Hand_Colliders)
    bpy.utils.unregister_class(VRM_OT_Add_Long_Dress_Collision)
    bpy.utils.unregister_class(VRM_OT_Improve_Long_Dress_Topology)
    bpy.utils.unregister_class(VRM_OT_Add_Jiggle_Bones)
    bpy.utils.unregister_class(VRM_OT_Breast_Physics_Tweaker)
    bpy.utils.unregister_class(VRM_OT_Scale_Model_Physics)
    bpy.utils.unregister_class(VRM_OT_Set_Breast_Physics_Preset)
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
    del bpy.types.Scene.vrm_jiggle_params_collapsed
    del bpy.types.Scene.vrm_dress_subdivision_count
    del bpy.types.Scene.vrm_dress_subdivision_smoothness
    del bpy.types.Scene.vrm_dress_collider_radius
    del bpy.types.Scene.vrm_upper_leg_collider_multiplier
    del bpy.types.Scene.vrm_skirt_hit_radius_first
    del bpy.types.Scene.vrm_skirt_hit_radius_second
    del bpy.types.Scene.vrm_skirt_hit_radius_third
    del bpy.types.Scene.vrm_skirt_hit_radius_fourth
    del bpy.types.Scene.vrm_skirt_gravity_power_first
    del bpy.types.Scene.vrm_skirt_gravity_power_rest
    del bpy.types.Scene.vrm_skirt_drag_force_first
    del bpy.types.Scene.vrm_skirt_drag_force_second
    del bpy.types.Scene.vrm_skirt_drag_force_third
    del bpy.types.Scene.vrm_skirt_drag_force_fourth
    del bpy.types.Scene.vrm_skirt_drag_force_fifth
    del bpy.types.Scene.vrm_skirt_stiffness_first
    del bpy.types.Scene.vrm_skirt_stiffness_second
    del bpy.types.Scene.vrm_skirt_stiffness_third
    del bpy.types.Scene.vrm_skirt_stiffness_fourth
    del bpy.types.Scene.vrm_skirt_angular_stiffness_first
    del bpy.types.Scene.vrm_skirt_angular_stiffness_second
    del bpy.types.Scene.vrm_skirt_angular_stiffness_third
    del bpy.types.Scene.vrm_skirt_angular_stiffness_fourth
    del bpy.types.Scene.vrm_dress_params_collapsed
    del bpy.types.Scene.vrm_breast_weight_increase
    del bpy.types.Scene.vrm_breast_end_shrink_factor
    del bpy.types.Scene.vrm_breast_end_weight_reduction
    del bpy.types.Scene.vrm_breast_bone_count
    del bpy.types.Scene.vrm_breast_physics_preset
    del bpy.types.Scene.vrm_breast_gravity_power

if __name__ == "__main__":
    register()
