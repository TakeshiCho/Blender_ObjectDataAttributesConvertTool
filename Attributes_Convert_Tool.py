bl_info = {
    "name": "Attributes Convert Tool",
    "author": "Takeshi Chō",
    "version": (0, 0, 1),
    "blender": (3, 0, 0),
    "location": "PROPERTIES > OBJECT DATA > ATTRIBUTES TO UVS",
    "description": "Convert the Attributes in face corner to the UVs",
    "warning": "It is not a stable version.",
    "doc_url": "https://github.com/TakeshiCho/Blender_ObjectDataAttributesConvertTool",
    "category": "Attributes Convert Tool",
}

import bpy
from bpy.types import (Operator, Panel)


class AttributesBake(Operator):
    """Bake active attribute into active uv"""
    bl_idname = "object.attributes_bake"
    bl_label = "Bake"

    edit_channel_x: bpy.props.BoolProperty(default=True)
    edit_channel_y: bpy.props.BoolProperty(default=True)
    channel_for_x: bpy.props.IntProperty(default=0)
    channel_for_y: bpy.props.IntProperty(default=1)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = context.object
        mesh_data = obj.data

        attribute_name: str = mesh_data.attributes.active.name
        attribute = mesh_data.attributes.get(attribute_name)

        uv_name: str = mesh_data.uv_layers.active.name
        uv = mesh_data.uv_layers.get(uv_name)

        for i, attribute_item in attribute.data.items():
            if self.edit_channel_x:
                uv.data[i].uv[0] = attribute_item.vector[self.channel_for_x]
            if self.edit_channel_y:
                uv.data[i].uv[1] = attribute_item.vector[self.channel_for_y]

        return {'FINISHED'}


class AttributesToUVs(Panel):
    """Bake the attributes in face corner into the UVs"""
    bl_label = "Attributes To UVs"
    bl_idname = "Attributes_To_UVs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout
        
        obj = context.object
        mesh_data = obj.data

        if mesh_data.attributes.active and mesh_data.uv_layers.active:

            attribute_name: str = mesh_data.attributes.active.name
            attribute = mesh_data.attributes.get(attribute_name)
            uv_name = mesh_data.uv_layers.active.name

            col = layout.column(align=True)
            col.label(text='Source Attribute: ' + attribute_name, icon='SNAP_VERTEX')
            col.label(text='Destination UV: ' + uv_name, icon='GROUP_UVS')

            layout.separator()

            row = layout.row()
            subrow = row.row(align=True)
            subrow.scale_x = 1.3
            subrow.alignment = 'RIGHT'
            subrow.label(text='Edit Destination: ')
            
            subrow = row.row(align=True)
            subrow.prop(obj, "edit_channel_x")
            subrow.prop(obj, "edit_channel_y")

            isVectorAttribute = len(attribute.data.items()[1]) == 3
            
            split = layout.split()
            #if isVectorAttribute:
            
            row = layout.row()
            col = row.column(align=True)
            col.scale_x = 1.5
            col.alignment = 'RIGHT'
            if obj.edit_channel_x:
                col.label(text='Destination X:')
            if obj.edit_channel_y:
                col.label(text='Destination Y:')
            
            col = row.column(align=True)
            if obj.edit_channel_x:
                col.prop(obj, "vector_channel_x",text="")
            if obj.edit_channel_y:
                col.prop(obj, "vector_channel_y",text="")
                
            layout.separator()
            row = layout.row()
            bake_ops = row.operator("object.attributes_bake")
            bake_ops.edit_channel_x = obj.edit_channel_x
            bake_ops.edit_channel_y = obj.edit_channel_y
            bake_ops.channel_for_x = int(obj.vector_channel_x)
            bake_ops.channel_for_y = int(obj.vector_channel_y)


vector_channel = [
    ("0", "Source.X", "channel X", 0),
    ("1", "Source.Y", "channel Y", 1),
    ("2", "Source.Z", "channel Z", 2),
]

vector_2D_channel = [
    ("0", "Source.X", "channel X", 0),
    ("1", "Source.Y", "channel Y", 1),
]


def register():
    bpy.utils.register_class(AttributesToUVs)
    bpy.utils.register_class(AttributesBake)
    bpy.types.Object.edit_channel_x = bpy.props.BoolProperty(name="X", default=True)
    bpy.types.Object.edit_channel_y = bpy.props.BoolProperty(name="Y", default=True)
    bpy.types.Object.vector_channel_x = bpy.props.EnumProperty(items=vector_channel, default="0")
    bpy.types.Object.vector_channel_y = bpy.props.EnumProperty(items=vector_channel, default="1")
    bpy.types.Object.vector_2D_channel_x = bpy.props.EnumProperty(items=vector_channel, default="0")
    bpy.types.Object.vector_2D_channel_y = bpy.props.EnumProperty(items=vector_channel, default="1")


def unregister():
    del bpy.types.Object.vector_2D_channel_y
    del bpy.types.Object.vector_2D_channel_x
    del bpy.types.Object.vector_channel_y
    del bpy.types.Object.vector_channel_x
    del bpy.types.Object.edit_channel_y
    del bpy.types.Object.edit_channel_x
    bpy.utils.unregister_class(AttributesBake)
    bpy.utils.unregister_class(AttributesToUVs)


if __name__ == "__main__":
    register()
