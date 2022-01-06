bl_info = {
    "name": "Attributes Convert Tool",
    "author": "Takeshi",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "PROPERTIES > OBJECT DATA > ATTRIBUTES TO UVS",
    "description": "Convert the Attributes in face corner to the UVs",
    "warning": "It is not a stable version.",
    "doc_url": "",
    "category": "Attributes Convert Tool",
}

import bpy


class Attributes_Bake(bpy.types.Operator):
    """Bake acitive atrritute into active uv"""
    bl_idname = "object.attributes_bake"
    bl_label = "Bake"
  
    @classmethod
    def poll(cls, context):
        return context.active_object is not None
        
           
    def execute(self, context):
        obj = context.object
        mesh_data = obj.data
        
        attri_name = mesh_data.attributes.active.name
        attri = mesh_data.attributes.get(attri_name)
        
        uv_name = mesh_data.uv_layers.active.name
        uv = mesh_data.uv_layers.get(uv_name)
        
        for i , j in attri.data.items():
            uv.data[i].uv[0] = j.vector[0]
            uv.data[i].uv[1] = j.vector[1]
            
        return {'FINISHED'}

    
class Attributes_To_UVs(bpy.types.Panel):
    """Bake the atrritutes in face corner into the UVs"""
    bl_label = "Attributes To UVs"
    bl_idname = "Attributes_To_UVs"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
        
        

    def draw(self, context):
        layout = self.layout

        obj = context.object
        mesh_data = obj.data
        
        attri_name = mesh_data.attributes.active.name  
        uv_name = mesh_data.uv_layers.active.name

        row = layout.row()
        row.label(text = 'Source Attribute: '+attri_name, icon='SNAP_VERTEX')      
        
        row = layout.row()
        row.label(text = 'Destination UV: '+uv_name, icon='GROUP_UVS')
        
        row = layout.row()
        row.operator("object.attributes_bake")
        
def menu_func(self, context):
    self.layout.operator(Attributes_Bake.bl_idname, text=Attributes_Bake.bl_label)

def register():
    bpy.utils.register_class(Attributes_To_UVs)
    bpy.utils.register_class(Attributes_Bake)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Attributes_To_UVs)
    bpy.utils.unregister_class(Attributes_Bake)
    bpy.types.VIEW3D_MT_object.remove(menu_func)

if __name__ == "__main__":
    register()
