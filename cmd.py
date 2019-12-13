import bpy
import imp

from . import utils
imp.reload(utils)


#UPDATE
# def update_strand_shape():
#     particle_systems = utils.getActiveObj().particle_systems
#     for p in particle_systems:
#         bpy.data.particles[p.settings.name].shape = col

#---------------------------------------------------------------------------------------
#パーティクルセッティングを変更したときパラメータをアップデート
#---------------------------------------------------------------------------------------
def test(self,context):
    print(11)
    act = utils.getActiveObj()
    props = bpy.context.scene.kiaparticletools_oa

    #props.setting_name
    props.collection_name = bpy.data.particles[props.setting_name].effector_weights.collection.name

#---------------------------------------------------------------------------------------
#パーティクルのパラメータアップデート
#---------------------------------------------------------------------------------------
def apply(self,context):
    act = utils.getActiveObj()
    props = bpy.context.scene.kiaparticletools_oa

    particle_systems = utils.getActiveObj().particle_systems
    for p in particle_systems:
        bpy.data.particles[p.settings.name].shape = props.strand_shape



#---------------------------------------------------------------------------------------
#現在のシーンをシーンメニューにセット
#---------------------------------------------------------------------------------------
def set_collection():
    props = bpy.context.scene.kiaparticletools_oa
    props.allcollections.clear()

    for col in bpy.data.collections:
        props.allcollections.add().name = col.name

    #パーティクルセッティング
    props.allsettings.clear()
    ps = set()

    particle_systems = utils.getActiveObj().particle_systems
    for p in particle_systems:
        ps.add(p.settings.name)

    for p in ps:    
        props.allsettings.add().name = p


#---------------------------------------------------------------------------------------
def effector_collection_assign(mode):
    if mode:
        props = bpy.context.scene.kiatools_oa

        for col in bpy.data.collections:
            props.allcollections.add().name = col.name

        col = bpy.data.collections[props.collection_name]

    else:
        col = None

    particle_systems = utils.getActiveObj().particle_systems
    for p in particle_systems:
        bpy.data.particles[p.settings.name].effector_weights.collection = col

