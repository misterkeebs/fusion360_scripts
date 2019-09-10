import adsk.core, traceback
import re

# LAYOUT = """
# [["Esc","Q","W","E","R","T","Y","U","I","O","P","[", "]","Back\\n\\n\\n\\n\\n\\nspace"],
# [{w:1.25},"Tab\\n\\n\\n1.25","A","S","D","F","G","H","J","K","L",":\\n;","",{w:1.75},"Enter\\n\\n\\n1.75"],
# [{w:1.75},"Shift\\n\\n\\n1.75","Z","X","C","V","B","N","M","<\\n,",">\\n.","?\\n/",{c:"#66d1e8",w:1.25},"Shift\\n\\n\\n1.25","Fn"],
# [{c:"#cccccc",w:1.25},"Ctrl\\n\\n\\n1.25",{x:1,w:1.25},"Alt\\n\\n\\n1.25",{w:7},"\\n\\n\\n7",{w:1.25},"Alt\\n\\n\\n1.25",{x:1,w:1.25},"Ctrl\\n\\n\\n1.25"]]
# """
LAYOUT = """
[[{w:1.25},"Tab\\n\\n\\n1.25","A","S","D","F","G","H","J","K","L",":\\n;","",{w:1.75},"Enter\\n\\n\\n1.75"],
[{c:"#cccccc",w:1.25},"Ctrl\\n\\n\\n1.25",{x:1,w:1.25},"Alt\\n\\n\\n1.25",{w:7},"\\n\\n\\n7",{w:1.25},"Alt\\n\\n\\n1.25",{x:1,w:1.25},"Ctrl\\n\\n\\n1.25"]]
"""
INIT_X = 0
INIT_Y = 0
INIT_Z = 0

class Layout:
  def __init__(self, layout):
    self.rawLayout = layout
    self.parse()

  @classmethod
  def key_file(cls, key):
    return 'r{}_{}'.format(key['y'] + 1, int(key['size'] * 100))

  def parse(self):
    self.layout = []

    rows = eval(re.sub(r'([a-z]):', r'"\1":', LAYOUT))
    w = 1

    for (y, _row) in enumerate(rows):
      row = []
      x = 1
      for key in _row:
        if isinstance(key, dict):
          if key.get('w'):
            w = float(key.get('w'))
          if key.get('x'):
            x += float(key.get('x'))
          continue

        parts = key.split()
        if parts:
          key = parts[0]

        rowDict = {
          'x': x,
          'y': y,
          'size': w,
          'name': key,
        }
        rowDict['file'] = Layout.key_file(rowDict)
        row.append(rowDict)
        x = x + w
        w = 1

      self.layout.append(row)

def add_keycap(files, app, keyDef):
  keyFile = None
  for file in files:
    if file.name == keyDef['file']:
      keyFile = file
      break

  design = app.activeProduct
  rootComp = design.rootComponent

  transform = adsk.core.Matrix3D.create()
  transform.translation = adsk.core.Vector3D.create(INIT_X + (1.905 * (keyDef['x']-1)), INIT_Y + (1.905 * (keyDef['y']-1)), INIT_Z)
  rootComp.occurrences.addByInsert(keyFile, transform, True)

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        design = app.activeProduct
        rootComp = design.rootComponent
        comp = design.activeComponent

        keyboard = Layout(LAYOUT)

        project = app.data.activeProject
        files = project.rootFolder.dataFiles
        missing = []
        for y, row in enumerate(keyboard.layout):
            for keyDef in row:
                add_keycap(files, app, keyDef)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
