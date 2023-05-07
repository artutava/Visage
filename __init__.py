bl_info = {
    "name": "Visage",
    "blender": (3, 3, 0),
    "category": "Object",
}

import bpy

class OBJECT_PT_Visage_Panel(bpy.types.Panel):
    bl_label = "Visage"
    bl_idname = "OBJECT_PT_visage_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Visage"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        obj = context.object
        shape_key_data = obj.data.shape_keys

        if shape_key_data is not None:
            box = layout.box()
            col = box.column()

            for shape_key in shape_key_data.key_blocks:
                if shape_key.name.startswith("FC_"):
                    row = col.row(align=True)
                    row.prop(shape_key, "value", text=shape_key.name)
                    
                    op = row.operator("object.shape_key_remove", text="", icon="X")
                    op.all_unlocked = False
                    op.lock = False
                    op.type = 'REMOVE'
                    op.relative = False
                    op.absolute = False
                    op.index = shape_key_data.key_blocks.find(shape_key.name)

                    row = col.row(align=True)
                    row.prop(shape_key, "interpolation", text="Interpolation")
                    row.prop(shape_key, "mute", text="", icon="HIDE_OFF")

                    row = col.row(align=True)
                    row.operator("object.shape_key_add", text="Add Shape Key", icon="ADD")
                    row.operator("object.shape_key_remove", text="Remove Shape Key", icon="REMOVE")

                    row = col.row(align=True)
                    row.operator("object.shape_key_mirror", text="Mirror Shape Key", icon="ARROW_LEFTRIGHT")
                    row.operator("object.shape_key_move", text="Move Shape Key", icon="ARROW_UP_DOWN")

                    row = col.row(align=True)
                    row.operator("object.shape_key_clear", text="Clear Shape Key", icon="LOOP_BACK")
                    row.operator("object.shape_key_retime", text="Retiming Shape Key", icon="TIME")

                    row = col.row(align=True)
                    row.operator("object.shape_key_transfer", text="Transfer Shape Key", icon="COPY_ID")
                    row.operator("object.shape_key_copy", text="Copy Shape Key", icon="COPYDOWN")

def register():
    bpy.utils.register_class(OBJECT_PT_Visage_Panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_PT_Visage_Panel)

if __name__ == "__main__":
    register()
