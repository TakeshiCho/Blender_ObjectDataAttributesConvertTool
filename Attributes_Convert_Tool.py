bl_info = {
    "name": "Attributes Convert Tool",
    "author": "Takeshi Chō",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "PROPERTIES > OBJECT DATA > ATTRIBUTES TO UVS",
    "description": "Convert the Attributes in face corner to the UVs",
    "warning": "It is not a stable version.",
    "doc_url": "https://github.com/TakeshiCho/Blender_ObjectDataAttributesConvertTool",
    "category": "Attributes Convert Tool",
}

import bpy
from bpy.types import (Operator,Panel,Menu)


class AttributesBake(Operator):
    """Bake active attribute into active uv"""
    bl_idname = "object.attributes_bake"
    bl_label = "Bake"
    
    channel_x: bpy.props.IntProperty(default=0)
    channel_y: bpy.props.IntProperty(default=1)
  
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
        
        for i , attribute_item in attribute.data.items():
            uv.data[i].uv[0] = attribute_item.vector[self.channel_x]
            uv.data[i].uv[1] = attribute_item.vector[self.channel_y]
            
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
            uv_name = mesh_data.uv_layers.active.name
        
            row = layout.row()
            row.label(text = 'Source Attribute: '+attribute_name, icon='SNAP_VERTEX')      
            
            row = layout.row()
            row.label(text = 'Destination UV: '+uv_name, icon='GROUP_UVS')
            
            row = layout.row()
            row.prop(obj,"channel_x")
            row.label(text = 'Bake Into UV Channel X')
            
            row = layout.row()
            row.prop(obj,"channel_y")
            row.label(text = 'Bake Into UV Channel Y')
            
            row = layout.row()
            bake_ops = row.operator("object.attributes_bake")
            bake_ops.channel_x = obj.channel_x
            bake_ops.channel_y = obj.channel_y
            

def register():
    bpy.utils.register_class(AttributesToUVs)
    bpy.utils.register_class(AttributesBake)
    bpy.types.Object.channel_x = bpy.props.IntProperty(name='Source Channel',default=0,min=0,max=2)
    bpy.types.Object.channel_y = bpy.props.IntProperty(name='Source Channel',default=0,min=0,max=2)

def unregister():
    bpy.utils.unregister_class(AttributesToUVs)
    bpy.utils.unregister_class(AttributesBake)
    del bpy.types.Object.channel_x
    del bpy.types.Object.channel_y
if __name__ == "__main__":
    register()
