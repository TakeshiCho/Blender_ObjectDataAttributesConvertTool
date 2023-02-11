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


class DATA_OT_AttributesBake(Operator):
    """Bake active attribute into active uv"""
    bl_idname = "object.attributes_bake"
    bl_label = "Bake"

    is_edit_uv_x: bpy.props.BoolProperty(default=True)
    is_edit_uv_y: bpy.props.BoolProperty(default=True)
    channel_for_x: bpy.props.IntProperty(default=0)
    channel_for_y: bpy.props.IntProperty(default=1)
    attribute_type: bpy.props.StringProperty(default="vector")

    @classmethod
    def poll(cls, context):
        obj = context.object
        mesh_data = obj.data
        attribute_name: str = mesh_data.attributes.active.name
        attribute = mesh_data.attributes.get(attribute_name)
        is_corner_domain = attribute.domain == 'CORNER'
    
        any_edit_channel: bool = context.object.data.attributeSettings.is_edit_uv_x or context.object.data.attributeSettings.is_edit_uv_y
        return context.active_object is not None and any_edit_channel and is_corner_domain

    def execute(self, context):
        obj = context.object
        mesh_data = obj.data

        attribute_name: str = mesh_data.attributes.active.name
        attribute = mesh_data.attributes.get(attribute_name)

        uv_name: str = mesh_data.uv_layers.active.name
        uv = mesh_data.uv_layers.get(uv_name)

        if self.attribute_type == "vector" or self.attribute_type == "vector2D":
            for i, attribute_item in attribute.data.items():
                if self.is_edit_uv_x:
                    uv.data[i].uv[0] = attribute_item.vector[self.channel_for_x]
                if self.is_edit_uv_y:
                    uv.data[i].uv[1] = attribute_item.vector[self.channel_for_y]
                    
        elif self.attribute_type == "color":
            for i, attribute_item in attribute.data.items():
                if self.is_edit_uv_x:
                    uv.data[i].uv[0] = attribute_item.color[self.channel_for_x]
                if self.is_edit_uv_y:
                    uv.data[i].uv[1] = attribute_item.color[self.channel_for_y]        

        return {'FINISHED'}


class DATA_PT_AttributesToUVs(Panel):
    """Bake the attributes in face corner into the UVs"""
    bl_label = "Attributes To UVs"
    bl_idname = "Attributes_To_UVs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        obj = context.object
        mesh_data = obj.data
        is_mesh: bool = type(mesh_data).__name__ == 'Mesh'
        return context.active_object is not None and is_mesh

    def draw(self, context):
        layout = self.layout
        obj = context.object
        mesh_data = obj.data

        if mesh_data.attributes.active and mesh_data.uv_layers.active:

            attribute_name: str = mesh_data.attributes.active.name
            uv_name = mesh_data.uv_layers.active.name

            col = layout.column(align=True)
            col.label(text='Source Attribute: ' + attribute_name, icon='OUTLINER_DATA_MESH')
            col.label(text='Destination UV: ' + uv_name, icon='GROUP_UVS')

            layout.separator()

            row_edit_channel = layout.row(align=True)
            subrow = row_edit_channel.row(align=True)
            subrow.scale_x = 2
            subrow.label(text='Edit UV Channels: ', icon='MODIFIER_ON')

            subrow = row_edit_channel.row(align=True)
            subrow.alignment = 'RIGHT'
            subrow.scale_x = 1
            
            settings = mesh_data.attributeSettings

            subrow.prop(settings, "is_edit_uv_x")
            subrow.prop(settings, "is_edit_uv_y")

            attribute = mesh_data.attributes.get(attribute_name)
            
            if type(attribute).__name__ == "Float2Attribute":
                draw_options_and_butten(settings, layout, "vector2D")
            elif type(attribute).__name__ == "FloatVectorAttribute":
                draw_options_and_butten(settings, layout, "vector")
            elif type(attribute).__name__ == "FloatColorAttribute":
                draw_options_and_butten(settings, layout, "color")
            elif type(attribute).__name__ == "ByteColorAttribute":
                draw_options_and_butten(settings, layout, "color")

            draw_errow(attribute, layout)


def draw_options_and_butten(settings, layout, var_type: str):
    draw_dest_scr_channel_options(settings, layout, var_type)
    layout.separator()
    draw_bake_butten(settings, layout, var_type)


def draw_dest_scr_channel_options(settings, layout, var_type: str):
    row_dest_scr_select = layout.row(align=True)

    col = row_dest_scr_select.column(align=True)
    if settings.is_edit_uv_x:
        col.label(text='UV.X:', icon='GROUP_UVS')
    if settings.is_edit_uv_y:
        col.label(text='UV.Y:', icon='GROUP_UVS')

    col = row_dest_scr_select.column(align=True)
    col.scale_x = 1.25
    if settings.is_edit_uv_x:
        col.prop(settings, f"uv_x_of_{var_type}", text="Attribute.", icon='OUTLINER_DATA_MESH')
    if settings.is_edit_uv_y:
        col.prop(settings, f"uv_y_of_{var_type}", text="Attribute.", icon='OUTLINER_DATA_MESH')


def draw_bake_butten(settings, layout, var_type: str):
    row = layout.row()
    bake_ops = row.operator("object.attributes_bake")
    bake_ops.is_edit_uv_x = settings.is_edit_uv_x
    bake_ops.is_edit_uv_y = settings.is_edit_uv_y
    if var_type == "vector2D":
        bake_ops.channel_for_x = int(settings.uv_x_of_vector2D)
        bake_ops.channel_for_y = int(settings.uv_y_of_vector2D)
    elif var_type == "vector":
        bake_ops.channel_for_x = int(settings.uv_x_of_vector)
        bake_ops.channel_for_y = int(settings.uv_y_of_vector)
    elif var_type == "color":
        bake_ops.channel_for_x = int(settings.uv_x_of_color)
        bake_ops.channel_for_y = int(settings.uv_y_of_color)
    bake_ops.attribute_type = var_type
    

def draw_errow(attribute, layout):
    if type(attribute).__name__ != "Float2Attribute" and type(attribute).__name__ != "FloatVectorAttribute" and type(attribute).__name__ != "FloatColorAttribute" and type(attribute).__name__ != "ByteColorAttribute":
        layout.separator()
        row = layout.row(align=True)
        row.label(text='Error: Selected attribute is must a Vector, 2D Vector or Color!',icon='ERROR')
    elif attribute.domain != 'CORNER':
        layout.separator()
        row = layout.row(align=True)
        row.label(text='Error: Selected attribute is must in Face Corner',icon='ERROR')


vector_2D_channel = [
    ("0", "X", "Source Channel X", 0),
    ("1", "Y", "Source Channel Y", 1),
]

vector_channel = [
    ("0", "X", "Source Channel X", 0),
    ("1", "Y", "Source Channel Y", 1),
    ("2", "Z", "Source Channel Z", 2),
]

color_channel = [
    ("0", "R", "Source Channel Red", 0),
    ("1", "G", "Source Channel Green", 1),
    ("2", "B", "Source Channel Blue", 2),
    ("3", "Alpha", "Source Channel Alpha", 3),
]


class AttributesToUVsSettings(bpy.types.PropertyGroup):
    is_edit_uv_x: bpy.props.BoolProperty(name="X", default=True)
    is_edit_uv_y: bpy.props.BoolProperty(name="Y", default=True)
    uv_x_of_vector2D: bpy.props.EnumProperty(items=vector_2D_channel, name='Source Channel', default="0")
    uv_y_of_vector2D: bpy.props.EnumProperty(items=vector_2D_channel, name='Source Channel', default="1")
    uv_x_of_vector: bpy.props.EnumProperty(items=vector_channel, name='Source Channel',default="0")
    uv_y_of_vector: bpy.props.EnumProperty(items=vector_channel, name='Source Channel', default="1")
    uv_x_of_color: bpy.props.EnumProperty(items=color_channel, name='Source Channel', default="0")
    uv_y_of_color: bpy.props.EnumProperty(items=color_channel, name='Source Channel', default="1")


def register():
    bpy.utils.register_class(DATA_PT_AttributesToUVs)
    bpy.utils.register_class(DATA_OT_AttributesBake)
    bpy.utils.register_class(AttributesToUVsSettings)
    bpy.types.Mesh.attributeSettings = bpy.props.PointerProperty(type=AttributesToUVsSettings)


def unregister():
    del bpy.types.Mesh.attributeSettings
    bpy.utils.unregister_class(AttributesToUVsSettings)
    bpy.utils.unregister_class(DATA_OT_AttributesBake)
    bpy.utils.unregister_class(DATA_PT_AttributesToUVs)


if __name__ == "__main__":
    register()
