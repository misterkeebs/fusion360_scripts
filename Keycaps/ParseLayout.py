import re

LAYOUT = """
[["Tab","Q","W","E","R","T","Y","U","I","O","P","&larr;",{x:0.5},"7","8","9"],
[{w:1.25},"Ctrl","A","S","D","F","G","H","J","K","L",{w:1.75},"Enter",{x:0.5},"4","5","6"],
[{w:1.75},"Shift","Z","X","C","V","B","N","M","< ,",{w:1.25},"Fn1",{x:1.5},"1","2","3"],
[{y:-0.75,x:11.25},"&uarr;"],
[{y:-0.25,w:1.25},"Ctrl","Win",{w:1.25},"Alt",{w:2.25},"Space Fn2",{x:0.5,a:7,w:2.75},"",{a:4},"Alt",{x:3.5},"0","."],
[{y:-0.75,x:10.25},"&larr;","&darr;","&rarr;"]]
"""

def parse_layout():
  layout = eval(re.sub(r'([a-z]):', r'"\1":', LAYOUT))

  w = 1
  y = 1
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
        if key.get('y'):
          y += float(key.get('y'))
        continue

      if key.split():
        key = key.split()[0]

      rowDict = {
        'x': x,
        'y': y,
        'size': w,
        'name': key,
      }
      row.append(rowDict)
      x = x + w
      w = 1
    y += 1
    res.append(row)

  return res

print(parse_layout())
