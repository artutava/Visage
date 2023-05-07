bl_info = {
    "name": "Custom Shape Keys Panel",
    "blender": (2, 93, 0),
    "category": "Object",
}

import bpy
from bpy.props import StringProperty, IntProperty
from bpy.types import Panel, UIList, Operator

class OBJECT_UL_CustomShapeKeyList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        shape_key = item
        
        layout.prop(shape_key, "name", text="", emboss=False)
        layout.prop(shape_key, "value", text="")
        layout.prop(shape_key, "mute", text="", icon="LOCKED" if shape_key.mute else "UNLOCKED")
        icon = "PINNED" if context.object.show_only_shape_key else "UNPINNED"
        op = layout.operator("object.pin_shape_key", text="", icon=icon)
        op.index = data.key_blocks.find(shape_key.name)
        op = layout.operator("object.shape_key_remove", text="", icon="X")
        op.index = data.key_blocks.find(shape_key.name)

class OBJECT_PT_CustomShapeKeysPanel(Panel):
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



        # Custom shape key list
        box = layout.box()
        row = box.row()
        row.template_list("OBJECT_UL_CustomShapeKeyList", "", shape_key_data, "key_blocks",
                          obj, "custom_shape_key_list_index", rows=4)

        # Other shape key options
        if shape_key_data.use_relative:
            layout.prop(shape_key_data, "eval_time", text="Evaluation Time")
        else:
            layout.prop(shape_key_data, "slider_min", text="Range Min")
            layout.prop(shape_key_data, "slider_max", text="Range Max")

class OBJECT_OT_PinShapeKey(Operator):
    bl_idname = "object.pin_shape_key"
    bl_label = "Pin Shape Key"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context):
        active_object = bpy.context.active_object
        if active_object.type == 'MESH' and active_object.data.shape_keys:
            active_object.show_only_shape_key = not active_object.show_only_shape_key
        return {'FINISHED'}

class OBJECT_OT_ShapeKeyRemove(Operator):
    bl_idname = "object.shape_key_remove"
    bl_label = "Remove Shape Key"
    bl_options = {'REGISTER', 'UNDO'}

    index: IntProperty()

    def execute(self, context):
        obj = context.object
        shape_key_data = obj.data.shape_keys
        shape_key_data.key_blocks.remove(shape_key_data.key_blocks[self.index])
        return {'FINISHED'}

def register():
    bpy.utils.register_class(OBJECT_UL_CustomShapeKeyList)
    bpy.utils.register_class(OBJECT_PT_CustomShapeKeysPanel)
    bpy.utils.register_class(OBJECT_OT_PinShapeKey)
    bpy.utils.register_class(OBJECT_OT_ShapeKeyRemove)
    bpy.types.Object.custom_shape_key_list_index = IntProperty()
    bpy.types.Object.custom_shape_key_filter = StringProperty()

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_ShapeKeyRemove)
    bpy.utils.unregister_class(OBJECT_OT_PinShapeKey)
    bpy.utils.unregister_class(OBJECT_PT_CustomShapeKeysPanel)
    bpy.utils.unregister_class(OBJECT_UL_CustomShapeKeyList)
    del bpy.types.Object.custom_shape_key_list_index
    del bpy.types.Object.custom_shape_key_filter

if __name__ == "main":
    register()
