bl_info = {
    "name": "VRM Physics Enhancer",
    "blender": (3, 0, 0),
    "category": "3D View",
    "author": "Meringue Rouge",
    "version": (1, 0),
    "location": "View3D > Sidebar > VRM Physics Enhancer",
    "description": "Adds physics colliders for breasts, long hair, and arms/hands to VRM models",
    "warning": "",
    "doc_url": "",
}

import bpy

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


def register():
    bpy.utils.register_class(VRM_OT_Add_Breast_Physics_Colliders)
    bpy.utils.register_class(VRM_OT_Add_Long_Hair_Collider)
    bpy.utils.register_class(VRM_OT_Add_Arm_Hand_Colliders)
    bpy.utils.register_class(VRM_PT_Physics_Enhancer_Panel)


if __name__ == "__main__":
    register()
