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
#パーティクルのパラメータアップデート
#---------------------------------------------------------------------------------------
def apply(self,context):
    act = utils.getActiveObj()
    props = bpy.context.scene.kiaparticletools_oa

    particle_systems = utils.getActiveObj().particle_systems
    for p in particle_systems:
        bpy.data.particles[p.settings.name].shape = props.strand_shape


#現在のシーンをシーンメニューにセット
def set_collection():
    props = bpy.context.scene.kiaparticletools_oa
    props.allcollections.clear()

    for col in bpy.data.collections:
        props.allcollections.add().name = col.name

    #パーティクルセッティング
    props.allsettings.clear()

    particle_systems = utils.getActiveObj().particle_systems
    for p in particle_systems:
        props.allsettings.add().name = p.settings.name

#        bpy.data.particles[p.settings.name].effector_weights.collection = col

    #row.prop_search(props, "setting_name", props, "allsettings", icon='SCENE_DATA')



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

