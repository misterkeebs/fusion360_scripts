#Author-Autodesk Inc.
#Description-Simple script display a message.

import adsk.core, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct
        rootComp = design.rootComponent
        comp = design.activeComponent

        mx = None
        for occ in comp.allOccurrences:
            if occ.component.name == 'MX Series-Cherry Key v1':
                mx = occ.component
                break

        transform = adsk.core.Matrix3D.create()
        ogTransform = occ.transform
        ui.messageBox('{}'.format(ogTransform.translation.x))
        ogTransform.translation = adsk.core.Vector3D.create(ogTransform.translation.x + 1.905, ogTransform.translation.y, ogTransform.translation.z)
        newOcc = rootComp.occurrences.addExistingComponent(mx, ogTransform)
        newOcc.transform = ogTransform

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
