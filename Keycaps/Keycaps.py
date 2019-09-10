#Author-Autodesk Inc.
#Description-Simple script display a message.

import adsk.core, traceback
import re

LAYOUT = """
[["Esc","Q","W","E","R","T","Y","U","I","O","P","[", "]","Back\\n\\n\\n\\n\\n\\nspace"],
[{w:1.25},"Tab\\n\\n\\n1.25","A","S","D","F","G","H","J","K","L",":\\n;","",{w:1.75},"Enter\\n\\n\\n1.75"],
[{w:1.75},"Shift\\n\\n\\n1.75","Z","X","C","V","B","N","M","<\\n,",">\\n.","?\\n/",{c:"#66d1e8",w:1.25},"Shift\\n\\n\\n1.25","Fn"],
[{c:"#cccccc",w:1.25},"Ctrl\\n\\n\\n1.25",{x:1,w:1.25},"Alt\\n\\n\\n1.25",{w:7},"\\n\\n\\n7",{w:1.25},"Alt\\n\\n\\n1.25",{x:1,w:1.25},"Ctrl\\n\\n\\n1.25"]]
"""

def parse_layout():
  layout = eval(re.sub(r'([a-z]):', r'"\1":', LAYOUT))

  w = 1
  res = []
  for _row in layout:
    row = []
    x = 1
    for key in _row:
      if isinstance(key, dict):
        if key.get('w'):
          w = float(key.get('w'))
        if key.get('x'):
          x += float(key.get('x'))
        continue

      if key.split():
        key = key.split()[0]

      row.append([x, w, key])
      x = x + w
      w = 1
    res.append(row)

  return res

def add_switch(rootComp, occ, mx, xPos, yPos):
  transform = adsk.core.Matrix3D.create()
  ogTransform = occ.transform
  ogTransform.translation = adsk.core.Vector3D.create(ogTransform.translation.x + (1.905 * xPos), ogTransform.translation.y + (1.905 * yPos), ogTransform.translation.z)
  newOcc = rootComp.occurrences.addExistingComponent(mx, ogTransform)
  newOcc.transform = ogTransform

def add_keycap(files, app, occ, row, size, x, y):
  fileName = 'r{}_{}'.format(row, size)
  keyFile = None
  for file in files:
    if file.name == fileName:
      keyFile = file
      break

  design = app.activeProduct
  rootComp = design.rootComponent

  transform = adsk.core.Matrix3D.create()
  ogTransform = occ.transform
  ogTransform.translation = adsk.core.Vector3D.create(ogTransform.translation.x + (1.905 * (x-1)), ogTransform.translation.y + (1.905 * (y-1)), ogTransform.translation.z)
  if keyFile is not None:
    rootComp.occurrences.addByInsert(keyFile, ogTransform, True)
    return None

  return keyFile

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct
        rootComp = design.rootComponent
        comp = design.activeComponent

        mx = None
        occ = None
        for occ in comp.allOccurrences:
          if occ.component.name == 'MX Series-Cherry Key v1':
            mx = occ.component
            break

        rows = parse_layout()
        project = app.data.activeProject
        files = project.rootFolder.dataFiles
        missing = []
        for y, row in enumerate(rows):
            for keyDef in row:
                px, size, key = keyDef
                x = px - 1 + ((size-1)/2)
                # ui.messageBox('Size: {}'.format(size))
                ret = add_keycap(files, app, occ, y+2, size*100, x, -(y-1))
                if ret is not None:
                  missing.append(ret)
        ui.messageBox('Missing: {}'.format(', '.join(missing)))

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
