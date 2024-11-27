import unreal as u

allActors = list()
noComps = list()
withComps = list()
buildingMeshes = list()

metadataKey = "osm_id"

clickableComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/Components/AC_Interactable")
dataComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/Components/AC_Metadata")
# damageComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/AC_DamageCalculator")
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

def RemoveComps():
    global noComps
    global withComps

    soSub = u.get_engine_subsystem(u.SubobjectDataSubsystem)
    numTasks = len(withComps)
    counter = 1

    with u.ScopedEditorTransaction("Removed actor components") as trans:
        with u.ScopedSlowTask(numTasks, "Removing actor components...") as slowTask:
            slowTask.make_dialog(True)

            for mesh in withComps:
                if slowTask.should_cancel():
                    print("Task canceled")
                    break

                slowTask.enter_progress_frame(1, "Removing actor components..." + str(counter) + " / " + str(numTasks))

                parentHandle = soSub.k2_gather_subobject_data_for_instance(mesh)[0]
                rootData = soSub.k2_gather_subobject_data_for_instance(mesh)                ## Returns array of handles for subobjs on mesh obj
                rootData.pop(1)                                                             ## Remove static mesh component from data list
                soSub.k2_delete_subobjects_from_instance(parentHandle, rootData)

                noComps.append(mesh)
                counter += 1
            
            withComps.clear()
        print(len(buildingMeshes), "objects found")
        print(len(noComps), "without data assets")
        print(len(withComps), "with data assets")

FindOSMObjects()
RemoveComps()