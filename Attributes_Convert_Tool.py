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

    edit_uv_channel_x: bpy.props.BoolProperty(default=True)
    edit_uv_channel_y: bpy.props.BoolProperty(default=True)
    channel_for_x: bpy.props.IntProperty(default=0)
    channel_for_y: bpy.props.IntProperty(default=1)

    @classmethod
    def poll(cls, context):
        any_edit_channel: bool = context.object.edit_uv_channel_x or context.object.edit_uv_channel_y
        return context.active_object is not None and any_edit_channel

    def execute(self, context):
        obj = context.object
        mesh_data = obj.data

        attribute_name: str = mesh_data.attributes.active.name
        attribute = mesh_data.attributes.get(attribute_name)

        uv_name: str = mesh_data.uv_layers.active.name
        uv = mesh_data.uv_layers.get(uv_name)

        for i, attribute_item in attribute.data.items():
            if self.edit_uv_channel_x:
                uv.data[i].uv[0] = attribute_item.vector[self.channel_for_x]
            if self.edit_uv_channel_y:
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
            col.label(text='Source Attribute: ' + attribute_name, icon='OUTLINER_DATA_MESH')
            col.label(text='Destination UV: ' + uv_name, icon='GROUP_UVS')

            layout.separator()

            row_edit_channel = layout.row(align=True)          
            subrow = row_edit_channel.row(align=True)
            subrow.scale_x = 2
            subrow.label(text='Edit Destination: ',icon = 'MODIFIER_ON')
            
            subrow = row_edit_channel.row(align=True)
            subrow.alignment = 'RIGHT'
            subrow.scale_x = 1
            subrow.prop(obj, "edit_uv_channel_x")
            subrow.prop(obj, "edit_uv_channel_y")

            isVectorAttribute = len(attribute.data.items()[1]) == 3
            #if isVectorAttribute:
            draw_dest_scr_channel_options(obj, layout, "vector")
                            
            layout.separator()
            row = layout.row()
            bake_ops = row.operator("object.attributes_bake")
            bake_ops.edit_uv_channel_x = obj.edit_uv_channel_x
            bake_ops.edit_uv_channel_y = obj.edit_uv_channel_y
            bake_ops.channel_for_x = int(obj.uv_x_to_attribute_vector)
            bake_ops.channel_for_y = int(obj.uv_y_to_attribute_vector)
            
    
def draw_dest_scr_channel_options(obj, layout, var_type: str):
    row_dest_scr_select = layout.row(align=True)
    
    col = row_dest_scr_select.column(align=True)            
    if obj.edit_uv_channel_x:
        col.label(text='Destination.X:', icon='GROUP_UVS')
    if obj.edit_uv_channel_y:
        col.label(text='Destination.Y:', icon='GROUP_UVS')
        
    col = row_dest_scr_select.column(align=True)
    col.scale_x = 1.25
    if obj.edit_uv_channel_x:
        col.prop(obj, "uv_x_to_attribute_"+var_type, text="", icon='OUTLINER_DATA_MESH')
    if obj.edit_uv_channel_y:
        col.prop(obj, "uv_y_to_attribute_"+var_type, text="", icon='OUTLINER_DATA_MESH')


vector_channel = [
    ("0", "Source.X", "Source Channel X", 0),
    ("1", "Source.Y", "Source Channel Y", 1),
    ("2", "Source.Z", "Source Channel Z", 2),
]

vector_2D_channel = [
    ("0", "Source.X", "Source Channel X", 0),
    ("1", "Source.Y", "Source Channel Y", 1),
]


def register():
    bpy.utils.register_class(AttributesToUVs)
    bpy.utils.register_class(AttributesBake)
    bpy.types.Object.edit_uv_channel_x = bpy.props.BoolProperty(name="X", default=True)
    bpy.types.Object.edit_uv_channel_y = bpy.props.BoolProperty(name="Y", default=True)
    bpy.types.Object.uv_x_to_attribute_vector = bpy.props.EnumProperty(items=vector_channel, name='Source Channel',default="0")
    bpy.types.Object.uv_y_to_attribute_vector = bpy.props.EnumProperty(items=vector_channel, name='Source Channel', default="1")
    bpy.types.Object.uv_x_to_attribute_vector_2D = bpy.props.EnumProperty(items=vector_channel, name='Source Channel', default="0")
    bpy.types.Object.uv_y_to_attribute_vector_2D = bpy.props.EnumProperty(items=vector_channel, name='Source Channel', default="1")


def unregister():
    del bpy.types.Object.uv_y_to_attribute_vector_2D
    del bpy.types.Object.uv_x_to_attribute_vector_2D
    del bpy.types.Object.uv_y_to_attribute_vector
    del bpy.types.Object.uv_x_to_attribute_vector
    del bpy.types.Object.edit_uv_channel_y
    del bpy.types.Object.edit_uv_channel_x
    bpy.utils.unregister_class(AttributesBake)
    bpy.utils.unregister_class(AttributesToUVs)


if __name__ == "__main__":
    register()