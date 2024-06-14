import unreal as u

allActors = list()
noComps = list()
withComps = list()
buildingMeshes = list()

metadataKey = "osm_id"

clickableComp = u.EditorAssetLibrary.load_blueprint_class("/Game/UI/AC_Clickable")
dataComp = u.EditorAssetLibrary.load_blueprint_class("/Game/UI/AC_Metadata")
uiComp = u.EditorAssetLibrary.load_blueprint_class("/Game/UI/AC_3DUI")
damageComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/AC_DamageCalculator")
# fluxData = u.EditorAssetLibrary.load_blueprint_class("/Game/FluidFlux/Environment/Readback")

def FindOSMObjects():
    global allActors
    global noComps
    global withComps
    global buildingMeshes

    allActors.clear()
    noComps.clear()
    withComps.clear()
    buildingMeshes.clear()

    allActors = u.DatasmithContentLibrary.get_all_objects_and_values_for_key(metadataKey, u.SceneComponent)

    for objects in allActors[0]:
        owner = objects.get_owner()
        buildingMeshes.append(owner.get_attached_actors()[0])

    for mesh in buildingMeshes:
        if(mesh.get_component_by_class(clickableComp)):
            withComps.append(mesh)
        else:
            noComps.append(mesh)

    print(len(buildingMeshes), "objects found")
    print(len(noComps), "without data assets")
    print(len(withComps), "with data assets")

# ## TODO Finish here

# def RemoveSubObjs(soSub, mesh):
#     subHandles = list()
#     ## Accepts actor
#     rootSub = soSub.k2_gather_subobject_data_for_instance(mesh)[0]
#     subData = soSub.k2_gather_subobject_data_for_instance(mesh)

#     subHandles.append(soSub.find_handle_for_object)

#     ## Accepts actor handle and array of handles to be deleted
#     soSub.k2_delete_subobjects_from_instance()


def RemoveComps():
    global noComps
    global withComps

    soSub = u.get_engine_subsystem(u.SubobjectDataSubsystem)

    for mesh in withComps:
        parentHandle = soSub.k2_gather_subobject_data_for_instance(mesh)[0]
        rootData = soSub.k2_gather_subobject_data_for_instance(mesh)                ## Returns array of handles for subobjs on mesh obj
        rootData.pop(1)                                                             ## Remove static mesh component from data list
        soSub.k2_delete_subbjects_from_instance(parentHandle, rootData)

        noComps.append(mesh)
    
    withComps.clear()
    print(len(buildingMeshes), "objects found")
    print(len(noComps), "without data assets")
    print(len(withComps), "with data assets")

FindOSMObjects()
RemoveComps()