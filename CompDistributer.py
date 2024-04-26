import unreal as u

allActors = list()
noComps = list()
withComps = list()
buildingMeshes = list()

metadataKey = "osm_id"

clickableComp = "AC_Clickable"
dataComp = "AC_Metadata"
uiComp = "AC_3DUI"
damageComp = "AC_DamageCalculator"
fluxData = "BP_Flux_Data_Component"

def FindOSMObjects():
    global allActors
    global noComps
    global withComps
    global buildingMeshes

    buildingMeshes.clear()
    allActors = u.DatasmithContentLibrary.get_all_objects_and_values_for_key(metadataKey, u.SceneComponent)

    for sceneComps, values in allActors.items():
        for component in sceneComps:
            owner = component.get_owner()
            buildingMeshes.append(u.EditorLevelLibrary.get_attached_actors(owner)[0])

    for mesh in buildingMeshes:
        if(u.EditorLevelLibrary.actor_has_component(mesh, clickableComp)):
            withComps.append(mesh)
        else:
            noComps.append(mesh)

    print(buildingMeshes.count(), "Objects found")


def AddComps():
    global noComps
    global withComps

    for mesh in noComps:
        actor = u.EditorActorSubsystem.get_actor_reference(mesh)

        ## Check actor validity, check comp validity, then add comps.

        if(actor):
            clickComp = u.EditorLevelLibrary.add_actor_component(actor, clickableComp)
            datComp = u.EditorLevelLibrary.add_actor_component(actor, dataComp)
            uComp = u.EditorLevelLibrary.add_actor_component(actor, uiComp)
            damComp = u.EditorLevelLibrary.add_actor_component(actor, damageComp)
            fluxComp = u.EditorLevelLibrary.add_actor_component(actor, fluxData)

            if(clickComp and datComp and uComp and damComp and fluxComp):
                u.EditorLevelLibrary.attach_actor_to_actor(actor, clickComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, datComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, uComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, damComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, fluxComp)

        withComps.append(actor)

    noComps.clear()

def RemoveComps():
    global noComps
    global withComps

    for mesh in withComps:
        actor = u.EditorActorSubsystem.get_actor_reference(mesh)

        if(actor):
            clickComp = u.EditorLevelLibrary.find_actor_component_by_class(actor, clickableComp)
            datComp = u.EditorLevelLibrary.find_actor_component_by_class(actor, dataComp)
            uComp = u.EditorLevelLibrary.find_actor_component_by_class(actor, uiComp)
            damComp = u.EditorLevelLibrary.find_actor_component_by_class(actor, damageComp)
            fluxComp = u.EditorLevelLibrary.find_actor_component_by_class(actor, fluxData)

            u.EditorLevelLibrary.remove_actor_component(actor, clickComp)
            u.EditorLevelLibrary.remove_actor_component(actor, datComp)
            u.EditorLevelLibrary.remove_actor_component(actor, uComp)
            u.EditorLevelLibrary.remove_actor_component(actor, damComp)
            u.EditorLevelLibrary.remove_actor_component(actor, fluxComp)

    withComps.clear()


            