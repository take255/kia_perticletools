import bpy
#from bpy.types import ( PropertyGroup , Panel , Operator ,UIList)
from bpy.types import ( PropertyGroup , Panel , Operator )
import imp

from bpy.props import(
    PointerProperty,
    #IntProperty,
    BoolProperty,
    StringProperty,
    CollectionProperty,
    FloatProperty,
    # EnumProperty
    )

from . import utils
from . import cmd

imp.reload(utils)
imp.reload(cmd)

bl_info = {
"name": "kia_particletools",
"author": "kisekiakeshi",
"version": (0, 1),
"blender": (2, 80, 0),
"description": "kia_particletools",
"category": "Object"}



class KIAPARTICLETOOLS_Props_OA(PropertyGroup):

    setting_name : StringProperty(name="Setting", maxlen=63, update=cmd.test)
    allsettings : CollectionProperty(type=PropertyGroup) 

    collection_name : StringProperty(name="Collection", maxlen=63 )
    allcollections : CollectionProperty(type=PropertyGroup) 

    #Hair Shape
    strand_shape : FloatProperty(name = "strand_shape",precision = 4, update=cmd.apply)


class KIAPARTICLETOOLS_PT_particletools(utils.panel):
    #bl_idname = "kiaparticletools.particletools"
    bl_label = "Particle Tools"

    def invoke(self, context, event):
        #cmd.set_collection()
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return{'FINISHED'}

    def draw(self, context):
        props = bpy.context.scene.kiaparticletools_oa
        layout = self.layout

        # box = layout.box()
        # box.label(text = 'effect collection')
        # row = box.row()
        # row.prop_search(props, "collection_name", props, "allcollections", icon='SCENE_DATA')
        # row.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'GROUP').mode = True
        # row.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'X').mode = False


        layout.operator("kiaparticletools.effector_collection" , icon = 'GROUP')

        box = layout.box()
        box.label(text = 'Hair Shape')
        box.prop(props, "strand_shape" , icon='RESTRICT_VIEW_OFF')


class KIAPARTICLETOOLS_MT_effector_collection(Operator):
    bl_idname = "kiaparticletools.effector_collection"
    bl_label = "assign effector collection"

    def invoke(self, context, event):
        cmd.set_collection()
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return{'FINISHED'}

    def draw(self, context):
        props = bpy.context.scene.kiaparticletools_oa
        layout = self.layout

        box = layout.box()
        box.label(text = 'effect collection')
        row = box.row()
        row.prop_search(props, "setting_name", props, "allsettings", icon='SCENE_DATA')


        box = layout.box()
        box.label(text = 'effect collection')
        row = box.row()
        row.prop_search(props, "collection_name", props, "allcollections", icon='SCENE_DATA')
        row.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'GROUP').mode = True
        row.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'X').mode = False



#---------------------------------------------------------------------------------------
#パーティクルツール
#---------------------------------------------------------------------------------------
class KIAPARTICLETOOLS_OT_particle_effector_collection_assign(Operator):
    """パーティクルのエフェクトコレクションを設定する"""
    bl_idname = "kiaparticletools.particle_effector_collection_assign"
    bl_label = ""
    mode : BoolProperty()
    def execute(self, context):
        particle.effector_collection_assign(self.mode)
        return {'FINISHED'}


classes = (
    KIAPARTICLETOOLS_Props_OA,
    KIAPARTICLETOOLS_PT_particletools,
    KIAPARTICLETOOLS_MT_effector_collection,
    KIAPARTICLETOOLS_OT_particle_effector_collection_assign
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.kiaparticletools_oa = PointerProperty(type=KIAPARTICLETOOLS_Props_OA)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.kiaparticletools_oa