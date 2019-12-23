import bpy
#from bpy.types import ( PropertyGroup , Panel , Operator ,UIList)
from bpy.types import ( PropertyGroup , Panel , Operator , UIList )
import imp
from bpy.app.handlers import persistent

from bpy.props import(
    PointerProperty,
    IntProperty,
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


try: 
    bpy.utils.unregister_class(KIAPARTICLETOOLS_Props_item)
except:
    pass


#Handler_through = False
CurrentObj = ''
CurrentProp = 0
CurrentList = 0

#---------------------------------------------------------------------------------------
#オブジェクトを選択したときにパーティクルセッティングをリストに追加
#パーティクルプロパティとリストで同期をとる
#選択をグローバルにとっておき比較
#---------------------------------------------------------------------------------------
@persistent
def kiaparticletools_handler(scene):
    #global Handler_through

    global CurrentObj
    global CurrentProp
    global CurrentList#ツールのリストインデックス


    if utils.selected() == []:
        print('aaa')
        CurrentObj = ''
        cmd.clear()
        return

    act = utils.getActiveObj()
    
    #print(CurrentObj , act.name)
    #isnotHair = False
    if act == None:
        return 

    elif cmd.check_not_ps():#パーティクルシステムがないなら先に進まない
        CurrentObj = act.name
        cmd.clear()
        return

    #選択が変更されたときだけリロード。
    if CurrentObj != act.name:
        print('selection changed')
        cmd.reload()    


    #リストを選択したときとパーティクルシステムを選択したときの処理
    props = bpy.context.scene.kiaparticletools_oa

    ps = act.particle_systems
    index_prop = ps.active_index #PSのプロパティ
    index_list = cmd.active_ps_index() #ツールのリスト

    index = None
    if CurrentList != index_list:
        ps.active_index = index = index_list
    elif CurrentProp != index_prop:
        index = index_prop
        cmd.active_index_set( index_prop )


    #インデックスに変更があった場合、いろいろアップデート
    if index != None:
        CurrentProp = CurrentList = index   

        # cmd.isBanApply = True #updateが走ってしまうのを禁止
        # props.shape = ps[index].settings.shape
        # cmd.isBanApply = False


    #表示オンオフ
    #cmd.disp()


    if act.name == CurrentObj:
        return
    else:
        CurrentObj = act.name

    #cmd.reload()



    # ui_list = bpy.context.window_manager.kiaparticletools_list
    # itemlist = ui_list.itemlist

    # cmd.clear()
    # particle_systems = act.particle_systems
    # for p in particle_systems:
    #     item = itemlist.add()
    #     item.name = p.name

        
        #bpy.data.particles[p.settings.name].shape = props.shape

    # for ob in utils.selected():
    #     item = itemlist.add()
    #     item.name = CurrentObj
        #ui_list.active_index = len(itemlist) - 1


    #props = bpy.context.scene.kiaobjectlist_props

    # #インデックスが変わったときだけ選択
    # if len(itemlist) > 0:
    #     index = ui_list.active_index
    #     if props.currentindex != index:
    #         props.currentindex = index#先に実行しておかないとdeselectでhandlerがループしてしまう
    #         bpy.ops.object.select_all(action='DESELECT')
    #         utils.selectByName(itemlist[index].name,True)




class KIAPARTICLETOOLS_Props_OA(PropertyGroup):

    # setting_name : StringProperty(name="Setting", maxlen=63, update=cmd.test)
    # allsettings : CollectionProperty(type=PropertyGroup) 

    collection_name : StringProperty(name="Collection", maxlen=63 )
    allcollections : CollectionProperty(type=PropertyGroup) 

#---------------------------------------------------------------------------------------
    #Particle Attribhte
#---------------------------------------------------------------------------------------
    
    #Hair Shape
    shape : FloatProperty(name = "shape",precision = 4, update=cmd.apply_shape)
    root_radius :  FloatProperty(name = "root_radius",precision = 4, update=cmd.apply_root_radius)
    tip_radius :  FloatProperty(name = "tip_radius",precision = 4, update=cmd.apply_tip_radius)
    radius_scale :  FloatProperty(name = "radius_scale",precision = 4, update=cmd.apply_radius_scale)

    #display
    render_step :  IntProperty(name = "render_step" , update=cmd.apply_render_step)
    display_step :  IntProperty(name = "display_step" , update=cmd.apply_display_step)
    use_hair_bspline :  BoolProperty(name = "use_hair_bspline" , update=cmd.apply_use_hair_bspline)


    edit_display_step :  IntProperty(name = "edit_display_step" , update=cmd.apply_edit_render_step)
    #bpy.context.scene.tool_settings.particle_edit.display_step = 6

#---------------------------------------------------------------------------------------
#リスト内のアイテムの見た目を指定
#---------------------------------------------------------------------------------------
class KIAPARTICLETOOLS_UL_uilist(UIList):
    

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:

            #item.nameが表示される
            #item.iconname = 'GROUP'
            layout.prop(item, "disp", text = "" , icon = item.iconname)
            layout.prop(item, "check", text = "")
            #layout.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'GROUP').mode = True
            layout.prop(item, "name", text="", emboss=False, icon_value=icon)
            #layout.prop(item, "check", text="", emboss=False, icon_value=icon)
            

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)



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


        layout.operator("kiaparticletools.create_particle_setting" , icon = 'GROUP')
        layout.operator("kiaparticletools.edit_attribute" , icon = 'GROUP')
        layout.operator("kiaparticletools.copy_particle_settings" , icon = 'GROUP')
        #layout.operator("kiaparticletools.sort_particle_sistem" , icon = 'GROUP')

        row = layout.row()
        row.operator("kiaparticletools.showhide_all" , text = "show all").mode = True
        row.operator("kiaparticletools.showhide_all" ,  text = "hide all").mode = False

        # box = layout.box()
        # box.label(text = 'Hair Shape')
        # box.prop(props, "shape" , icon='RESTRICT_VIEW_OFF')


        ui_list = context.window_manager.kiaparticletools_list
        box = layout.box()
        box.label(text = 'particle settings')

        col = box.column()
        col.template_list("KIAPARTICLETOOLS_UL_uilist", "", ui_list, "itemlist", ui_list, "active_index", rows=8)




class KIAPARTICLETOOLS_MT_edit_attribute(Operator):
    bl_idname = "kiaparticletools.edit_attribute"
    bl_label = "edit_attribute"

    def invoke(self, context, event):
        #cmd.set_collection()
        cmd.isBanApply = True
        cmd.set_attribute()
        cmd.isBanApply = False

        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        return{'FINISHED'}

    def draw(self, context):
        props = bpy.context.scene.kiaparticletools_oa
        layout = self.layout

        # box.label(text = 'effect collection')
        # row = box.row()
        # row.prop_search(props, "setting_name", props, "allsettings", icon='SCENE_DATA')

        row = layout.row()

        box = row.box()
        box.label(text = 'Hair Shape')
        box.prop(props, "shape" , icon='RESTRICT_VIEW_OFF')
        box.prop(props, "root_radius" , icon='RESTRICT_VIEW_OFF')
        box.prop(props, "tip_radius" , icon='RESTRICT_VIEW_OFF')
        box.prop(props, "radius_scale" , icon='RESTRICT_VIEW_OFF')

        box = row.box()
        box.label(text = 'Display')
        box.prop(props, "edit_display_step" , icon='RESTRICT_VIEW_OFF')
        box.prop(props, "render_step" , icon='RESTRICT_VIEW_OFF')
        box.prop(props, "display_step" , icon='RESTRICT_VIEW_OFF')
        box.prop(props, "use_hair_bspline" , icon='RESTRICT_VIEW_OFF')
        

    # root_radius :  FloatProperty(name = "root_radius",precision = 4, update=cmd.apply)
    # tip_radius :  FloatProperty(name = "tip_radius",precision = 4, update=cmd.apply)
    # radius_scale :  FloatProperty(name = "radius_scale",precision = 4, update=cmd.apply)

        box = layout.box()
        box.label(text = 'effect collection')
        row = box.row()
        row.prop_search(props, "collection_name", props, "allcollections", icon='SCENE_DATA')
        row.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'GROUP').mode = True
        row.operator("kiaparticletools.particle_effector_collection_assign" , icon = 'X').mode = False



#リスト用
class KIAPARTICLETOOLS_Props_item(PropertyGroup):
    name : StringProperty()
    check : BoolProperty()
    disp : BoolProperty( update=cmd.disp )
    iconname : StringProperty(default = 'RESTRICT_VIEW_OFF')
    idx : IntProperty()
    mod : StringProperty()

    #check : BoolProperty( update = cmd.showhide )
    #name1 : StringProperty(get=cmd.get_item, set=cmd.set_item)
    #check : StringProperty(get=cmd.get_item, set=cmd.set_item)
    

bpy.utils.register_class(KIAPARTICLETOOLS_Props_item)

class KIAPARTICLETOOLS_Props_list(PropertyGroup):
    active_index : IntProperty()
    itemlist : CollectionProperty(type=KIAPARTICLETOOLS_Props_item)#アイテムプロパティの型を収めることができるリストを生成


#---------------------------------------------------------------------------------------
#パーティクルツール
#---------------------------------------------------------------------------------------
class KIAPARTICLETOOLS_OT_particle_effector_collection_assign(Operator):
    """パーティクルのエフェクトコレクションを設定する"""
    bl_idname = "kiaparticletools.particle_effector_collection_assign"
    bl_label = ""
    mode : BoolProperty()
    def execute(self, context):
        cmd.effector_collection_assign(self.mode)
        return {'FINISHED'}

class KIAPARTICLETOOLS_OT_create_particle_setting(Operator):
    """新しい髪の毛のパーティクルセッティングを生成"""
    bl_idname = "kiaparticletools.create_particle_setting"
    bl_label = "create"
    def execute(self, context):
        cmd.create_particle_setting()
        return {'FINISHED'}

class KIAPARTICLETOOLS_OT_copy_particle_settings(Operator):
    """チェックを付けたもののパーティクルセッティングをアクティブのものと同じにする"""
    bl_idname = "kiaparticletools.copy_particle_settings"
    bl_label = "copy"
    def execute(self, context):
        cmd.copy_particle_settings()
        return {'FINISHED'}

# class KIAPARTICLETOOLS_OT_sort_particle_sistem(Operator):
#     """パーティクルシステムの名前でのソート"""
#     bl_idname = "kiaparticletools.sort_particle_sistem"
#     bl_label = "sort by name"
#     def execute(self, context):
#         cmd.sort_particle_sistem()
#         return {'FINISHED'}

class KIAPARTICLETOOLS_OT_showhide_all(Operator):
    """パーティクルシステムの表示、非表示"""
    bl_idname = "kiaparticletools.showhide_all"
    bl_label = ""
    mode : BoolProperty()
    def execute(self, context):
        cmd.showhide_all(self.mode)
        return {'FINISHED'}


classes = (
    KIAPARTICLETOOLS_Props_OA,
    KIAPARTICLETOOLS_PT_particletools,
    KIAPARTICLETOOLS_MT_edit_attribute,
    KIAPARTICLETOOLS_Props_list,

    #リスト
    KIAPARTICLETOOLS_UL_uilist,
    KIAPARTICLETOOLS_OT_particle_effector_collection_assign,

    KIAPARTICLETOOLS_OT_create_particle_setting,
    KIAPARTICLETOOLS_OT_copy_particle_settings,
    #KIAPARTICLETOOLS_OT_sort_particle_sistem,
    KIAPARTICLETOOLS_OT_showhide_all
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.kiaparticletools_oa = PointerProperty(type = KIAPARTICLETOOLS_Props_OA )
    bpy.types.WindowManager.kiaparticletools_list = PointerProperty(type = KIAPARTICLETOOLS_Props_list )
    bpy.app.handlers.depsgraph_update_pre.append(kiaparticletools_handler)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.kiaparticletools_oa
    del bpy.types.WindowManager.kiaparticletools_list
    bpy.app.handlers.depsgraph_update_pre.remove(kiaparticletools_handler)
