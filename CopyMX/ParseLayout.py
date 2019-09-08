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
    for key in _row:
      if isinstance(key, dict):
        w = float(key['w'])
        continue

      if key.split():
        key = key.split()[0]

      row.append([w, key])
      w = 1
    res.append(row)

  return res

print(parse_layout())
