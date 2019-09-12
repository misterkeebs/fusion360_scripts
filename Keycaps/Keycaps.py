# import adsk.core, traceback
import adsk.core, traceback
import re

# LAYOUT = """
# [["Esc","Q","W","E","R","T","Y","U","I","O","P","[", "]","Back\\n\\n\\n\\n\\n\\nspace"],
# [{w:1.25},"Tab\\n\\n\\n1.25","A","S","D","F","G","H","J","K","L",":\\n;","",{w:1.75},"Enter\\n\\n\\n1.75"],
# [{w:1.75},"Shift\\n\\n\\n1.75","Z","X","C","V","B","N","M","<\\n,",">\\n.","?\\n/",{c:"#66d1e8",w:1.25},"Shift\\n\\n\\n1.25","Fn"],
# [{c:"#cccccc",w:1.25},"Ctrl\\n\\n\\n1.25",{x:1,w:1.25},"Alt\\n\\n\\n1.25",{w:7},"\\n\\n\\n7",{w:1.25},"Alt\\n\\n\\n1.25",{x:1,w:1.25},"Ctrl\\n\\n\\n1.25"]]
# """
LAYOUT = """
[["Esc","Q","W","E","R","T","Y","U","I","O","P","[", "]","Back\\n\\n\\n\\n\\n\\nspace"],
[{w:1.25},"Tab\\n\\n\\n1.25","A","S","D","F","G","H","J","K","L",":\\n;","",{w:1.75},"Enter\\n\\n\\n1.75"]]
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

def find_file(files, file):
  for _file in files:
    if _file.name == file:
      return _file
  return None

def find_match(files, row, size):
  match_name = 'r{}_{}'.format(row, size)
  return find_file(files, match_name)

def find_key(files, file):
  perfect_match = find_file(files, file)
  if perfect_match:
    return perfect_match

  size = file.split('_')[1]
  row = int(file.split('_')[0][1])
  if row >= 1:
    for i in range(row, 5):
      match = find_match(files, i, size)
      if match:
        return match

  if row <= 4:
    for i in range(1, row+1):
      match = find_match(files, i, size)
      if match:
        return match

def add_keycap(files, app, keyDef):
  keyFile = find_key(files, keyDef['file'])
  if not keyFile:
    return

  design = app.activeProduct
  rootComp = design.rootComponent

  transform = adsk.core.Matrix3D.create()
  transform.translation = adsk.core.Vector3D.create(INIT_X + (1.905 * (keyDef['x']-1)), INIT_Y + (1.905 * (keyDef['y']-1)), INIT_Z)
  try:
    rootComp.occurrences.addByInsert(keyFile, transform, True)
  except:
    app.userInterface.messageBox('Could not add file: {}'.format(keyDef['file']))

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

        ui.messageBox('Done')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

# files = [
#   {'name': 'r1_125'},
#   {'name': 'r2_125'},
#   {'name': 'r3_125'},
# ]
# # print find_key(files, 'r4_125')
# print add_keycap(files, None, {'file': 'r3_125'})
