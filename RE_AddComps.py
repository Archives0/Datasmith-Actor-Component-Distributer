import unreal as u

allActors = list()
noComps = list()
withComps = list()
buildingMeshes = list()

metadataKey = "osm_id"
tagName = "Building"

clickableComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/Components/AC_Interactable")
dataComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/Components/AC_Metadata")
damageComp = u.EditorAssetLibrary.load_blueprint_class("/Game/Blueprints/Components/AC_Damage")
fluxComp = u.EditorAssetLibrary.load_blueprint_class("/Game/FluidFlux/Environment/Readback/BP_FluxDataComponent")

def AddTag(actor):
    if(u.Name(tagName) not in actor.tags):
        aTags = actor.tags
        aTags.append(u.Name(tagName))
        actor.tags = aTags

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

    for objects in allActors[0]:                                        ## All actors, without metadata value.
        owner = objects.get_owner()
        buildingMeshes.append(owner.get_attached_actors()[0])           ## Fill list with only meshes attached to actors.

    for mesh in buildingMeshes:
        AddTag(mesh)

        if(mesh.get_component_by_class(clickableComp)):                 ## If clickable component is present.
            withComps.append(mesh)
        else:
            noComps.append(mesh)

    print(len(buildingMeshes), "objects found")
    print(len(noComps), "without data assets")
    print(len(withComps), "with data assets")


def AddComps():
    global noComps
    global withComps

    numTasks = len(noComps)
    counter = 1
    soSub = u.get_engine_subsystem(u.SubobjectDataSubsystem)

    with u.ScopedEditorTransaction("Added actor components") as trans:
        with u.ScopedSlowTask(numTasks, "Adding actor components...") as slowTask:
            slowTask.make_dialog(True)

            for mesh in noComps:                                                ## Add components if mesh does not have base clickable component
                if slowTask.should_cancel():
                    print("Task cancelled")
                    break

                slowTask.enter_progress_frame(1, "Adding actor components..." + str(counter) + " / " + str(numTasks))

                rootSub = soSub.k2_gather_subobject_data_for_instance(mesh)[0]

                clickSub = soSub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=rootSub, new_class=clickableComp))
                dataSub = soSub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=rootSub, new_class=dataComp))
                damSub = soSub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=rootSub, new_class=damageComp))
                soSub.add_new_subobject(u.AddNewSubobjectParams(parent_handle=rootSub, new_class=fluxComp))

                withComps.append(mesh)
                counter += 1

        noComps.clear()
    
    print(len(buildingMeshes), "objects found")
    print(len(noComps), "without data assets")
    print(len(withComps), "with data assets")

FindOSMObjects()
AddComps()