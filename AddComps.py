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

    print(len(buildingMeshes), "Objects found")


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

            clickComp = u.new_object

            if(clickComp and datComp and uComp and damComp and fluxComp):
                u.EditorLevelLibrary.attach_actor_to_actor(actor, clickComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, datComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, uComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, damComp)
                u.EditorLevelLibrary.attach_actor_to_actor(actor, fluxComp)

        withComps.append(actor)

    noComps.clear()

FindOSMObjects()