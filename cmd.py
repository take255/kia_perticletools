import bpy
import imp

from . import utils
imp.reload(utils)



# class AttrProps:
#     def __init__(self):
#         pass

#     def set_attr(self,props):
#         props.shape = ps[ps.active_index].settings.shape

isBanApply = False

ATTRIBUTE = (
'shape',
'root_radius',
'tip_radius',
'radius_scale',
'render_step',
'display_step',
'use_hair_bspline',
)

#---------------------------------------------------------------------------------------
#テンプレートを使ってアトリビュートapplyの関数生成
#---------------------------------------------------------------------------------------
template_apply = """
def apply_%s(self,context):
    apply_attr('%s')
"""
for attr in ATTRIBUTE:
    exec( template_apply % (attr , attr) )

def apply_attr( attr ):
    checked = index_checked()
    props = bpy.context.scene.kiaparticletools_oa
    particle_systems = utils.getActiveObj().particle_systems
    for i , p in enumerate(particle_systems):
        ps = p.settings
        if checked[i]:
            exec('ps.%s=props.%s' % (attr,attr))



#UPDATE
# def update_shape():
#     particle_systems = utils.getActiveObj().particle_systems
#     for p in particle_systems:
#         bpy.data.particles[p.settings.name].shape = col

#---------------------------------------------------------------------------------------
#パーティクルセッティングを変更したときパラメータをアップデート
#---------------------------------------------------------------------------------------
def test(self,context):
    act = utils.getActiveObj()
    props = bpy.context.scene.kiaparticletools_oa

    #props.setting_name
    props.collection_name = bpy.data.particles[props.setting_name].effector_weights.collection.name

#---------------------------------------------------------------------------------------
#パーティクルのパラメータアップデート
#---------------------------------------------------------------------------------------
def apply(self,context):

    checked = index_checked()

    global isBanApply
    if isBanApply:
        return
    # act = utils.getActiveObj()
    props = bpy.context.scene.kiaparticletools_oa

    particle_systems = utils.getActiveObj().particle_systems
    index = particle_systems.active_index

    for i , p in enumerate(particle_systems):
        #ps = bpy.data.particles[p.settings.name]
        ps = p.settings
        if checked[i] or index == i:
            for attr in ATTRIBUTE:
                exec('ps.%s=props.%s' % (attr,attr))
            # ps.shape = props.shape
            # ps.root_radius = props.root_radius
            # ps.tip_radius = props.tip_radius
            # ps.radius_scale = props.radius_scale


# def apply_shape(self,context):
#     checked = index_checked()
#     props = bpy.context.scene.kiaparticletools_oa
#     particle_systems = utils.getActiveObj().particle_systems
#     for i , p in enumerate(particle_systems):
#         ps = p.settings
#         if checked[i]:
#             ps.shape = props.shape






# def apply_shape(self,context):
#     apply_attr('shape')

# def apply_root_radius(self,context):
#     apply_attr('root_radius')

# def apply_tip_radius(self,context):
#     apply_attr('tip_radius')

# def apply_radius_scale(self,context):
#     apply_attr('radius_scale')

# def apply_render_step(self,context):
#     apply_attr('render_step')

# def apply_display_step(self,context):
#     apply_attr('display_step')

# def apply_use_hair_bspline(self,context):
#     apply_attr('use_hair_bspline')



def set_attribute():
    act = utils.getActiveObj()
    props = bpy.context.scene.kiaparticletools_oa

    ps = act.particle_systems
    index = ps.active_index

    for attr in ATTRIBUTE:
        exec('props.%s=ps[index].settings.%s' % (attr,attr))

    # props.shape = ps[ps.active_index].settings.shape
    # props.root_radius = ps[ps.active_index].settings.root_radius
    # props.tip_radius = ps[ps.active_index].settings.tip_radius
    # props.radius_scale = ps[ps.active_index].settings.radius_scale

    # root_radius :  FloatProperty(name = "root_radius",precision = 4, update=cmd.apply)
    # tip_radius :  FloatProperty(name = "tip_radius",precision = 4, update=cmd.apply)
    # radius_scale :  FloatProperty(name = "radius_scale",precision = 4, update=cmd.apply)


#---------------------------------------------------------------------------------------
#現在のシーンをシーンメニューにセット
#---------------------------------------------------------------------------------------
# def set_collection():
#     props = bpy.context.scene.kiaparticletools_oa
#     props.allcollections.clear()

#     for col in bpy.data.collections:
#         props.allcollections.add().name = col.name

#     #パーティクルセッティング
#     props.allsettings.clear()
#     ps = set()

#     particle_systems = utils.getActiveObj().particle_systems
#     for p in particle_systems:
#         ps.add(p.settings.name)

#     for p in ps:    
#         props.allsettings.add().name = p


#---------------------------------------------------------------------------------------
def effector_collection_assign(mode):
    if mode:
        props = bpy.context.scene.kiaparticletools_oa

        for col in bpy.data.collections:
            props.allcollections.add().name = col.name

        col = bpy.data.collections[props.collection_name]

    else:
        col = None

    particle_systems = utils.getActiveObj().particle_systems
    for p in particle_systems:
        bpy.data.particles[p.settings.name].effector_weights.collection = col

#---------------------------------------------------------------------------------------
#新しい髪の毛のパーティクルセッティングを生成
#---------------------------------------------------------------------------------------
def create_particle_setting():
    bpy.ops.object.particle_system_add()

    ob = bpy.context.object
    ps = ob.particle_systems[-1]
    s = ps.settings
    s.type = 'HAIR'
    s.count = 0
    s.hair_length = 1
    s.child_type = 'SIMPLE'
    s.display_step = 7
    s.render_step = 9

    reload()
    # for p in object.particle_systems:
    # print(p.name)
    
    #print(object.particle_systems[-1])  

    #bpy.data.particles["ParticleSettings.001"].type = 'HAIR'


#---------------------------------------------------------------------------------------
#パーティクルセッティングをコピー
#---------------------------------------------------------------------------------------
def copy_particle_settings():
    checked = index_checked()
    particle_systems = utils.getActiveObj().particle_systems
    
    active_setting = particle_systems[active_index()].settings

    for i, p in enumerate(particle_systems):
        if checked[i]:
            p.settings = active_setting
        
    
def sort_particle_sistem():
    ps = utils.getActiveObj().particle_systems
    print(dir(ps))
    #ps[0] , ps[1] = ps[1] , ps[0]
    reload()


#---------------------------------------------------------------------------------------
#リストコマンド
#---------------------------------------------------------------------------------------
def itemlist():
    ui_list = bpy.context.window_manager.kiaparticletools_list
    return ui_list.itemlist    

def active_index():
    ui_list = bpy.context.window_manager.kiaparticletools_list
    return ui_list.active_index

def active_index_set(index):
    ui_list = bpy.context.window_manager.kiaparticletools_list
    ui_list.active_index = index

def index_checked():
    # result = []
    # for node in itemlist():
    #     node.bool_val = True
    return [x.check  for x in itemlist()]

def disp():
    for x in itemlist():
        if x.check:
            x.iconname = 'RESTRICT_VIEW_OFF'


def get_item():
    pass
def showhide():
    pass
def set_item():
    pass
def clear():
    # ui_list = bpy.context.window_manager.kiaparticletools_list
    # itemlist = ui_list.itemlist    
    # itemlist.clear()
    il = itemlist()
    il.clear()

def reload():
    act = utils.getActiveObj()
    #ui_list = bpy.context.window_manager.kiaparticletools_list
    il = itemlist()
    clear()
    particle_systems = act.particle_systems
    for p in particle_systems:
        item = il.add()
        item.name = p.name
        item.iconname = 'GROUP'
