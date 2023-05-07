bl_info = {
    "name": "Custom Shape Keys Panel",
    "blender": (2, 93, 0),
    "category": "Object",
}

import bpy

class OBJECT_PT_CustomShapeKeysPanel(bpy.types.Panel):
    bl_label = "FC Shape Keys"
    bl_idname = "OBJECT_PT_custom_shape_keys"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FC Shape Keys'

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj is not None and obj.type == 'MESH' and obj.data.shape_keys is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object
        shape_key_data = obj.data.shape_keys
        shape_keys = shape_key_data.key_blocks

        # Add shape key button
        row = layout.row()
        row.operator("object.shape_key_add", text="Add Shape Key").from_mix = False

        for shape_key in shape_keys:
            if shape_key.name.startswith("FC_"):
                row = layout.row(align=True)

                # Shape key name
                row.prop(shape_key, "name", text="")
                # Shape key value slider
                row.prop(shape_key, "value", text="")
                # Shape key mute (lock) toggle
                row.prop(shape_key, "mute", text="", icon="LOCKED" if shape_key.mute else "UNLOCKED")
                # Edit mode toggle
                if obj.mode == 'EDIT' and obj.active_shape_key == shape_key:
                    row.operator("object.editmode_toggle", text="", icon="SHAPEKEY_DATA")
                else:
                    op = row.operator("object.editmode_toggle", text="", icon="EDITMODE_HLT")
                    op.index = shape_key_data.key_blocks.find(shape_key.name)

                # Remove shape key button
                op = row.operator("object.shape_key_remove", text="", icon="X")
                op.index = shape_key_data.key_blocks.find(shape_key.name)

        # Other shape key options
        if shape_key_data.use_relative:
            layout.prop(shape_key_data, "eval_time", text="Evaluation Time")
        else:
            layout.prop(shape_key_data, "slider_min", text="Range Min")
            layout.prop(shape_key_data, "slider_max", text="Range Max")

class OBJECT_OT_EditModeToggle(bpy.types.Operator):
    bl_idname = "object.editmode_toggle"
    bl_label = "Toggle Edit Mode"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        obj = context.object
        shape_key_data = obj.data.shape_keys

        if obj.mode == 'EDIT':
            bpy.ops.object.editmode_toggle()
        else:
            obj.active_shape_key_index = self.index
            bpy.ops.object.editmode_toggle()

        return {'FINISHED'}

class OBJECT_OT_ShapeKeyRemove(bpy.types.Operator):
    bl_idname = "object.shape_key_remove"
    bl_label = "Remove Shape Key"
    bl_options = {'REGISTER', 'UNDO'}

    index: bpy.props.IntProperty()

    def execute(self, context):
        obj = context.object
        shape_key_data = obj.data.shape_keys
        shape_key_data.key_blocks.remove(shape_key_data.key_blocks[self.index])

        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_PT_CustomShapeKeysPanel)
    bpy.utils.register_class(OBJECT_OT_EditModeToggle)
    bpy.utils.register_class(OBJECT_OT_ShapeKeyRemove)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ShapeKeyRemove)
    bpy.utils.unregister_class(OBJECT_OT_EditModeToggle)
    bpy.utils.unregister_class(OBJECT_PT_CustomShapeKeysPanel)

if name == "main":
    register()
