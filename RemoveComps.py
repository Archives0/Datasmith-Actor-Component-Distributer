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
fluxData = u.EditorAssetLibrary.load_blueprint_class("/Game/FluidFlux/Environment/Readback")

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

def RemoveComps():
    global noComps
    global withComps

    soSub = u.get_engine_subsystem(u.SubobjectDataSubsystem)

    for mesh in withComps:
        rootSub = soSub.k2_gather_subobject_data_for_instance(mesh)
        subData = list()
        
        for data in rootSub:
            subData.append(data)

        soSub.delete_subobjects(subData)
        noComps.append(mesh)
    
    withComps.clear()
    print(len(buildingMeshes), "objects found")
    print(len(noComps), "without data assets")
    print(len(withComps), "with data assets")