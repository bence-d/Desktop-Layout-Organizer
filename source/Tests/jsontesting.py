import json
import os
import sys
sys.path.append('source') 
from preset_class import Preset

currObj = ""

presetsRaw =  [
    Preset("Preset1", "Description of Preset1", "C:\\Users\\Bence\\Desktop\\preset1.reg",[]), 
    Preset("Preset2", "Description of Preset2", "C:\\Users\\Bence\\Desktop\\preset2.reg",[]),
    Preset("Preset3", "Description of Preset3", "C:\\Users\\Bence\\Desktop\\preset3.reg",[])
]

# build a list of dicts from your objects:
presets = [obj.to_dict() for obj in presetsRaw]

presets.sort(key=lambda obj: obj["name"])

presetsJSON = json.dumps({"presets": presets})
print("\n-> jsdata: " + presetsJSON)


### HOW TO WRITE FILE ###

# Set the directory where the files are located
filename = "C:\\Users\\" + os.getenv("username") + "\\AppData\\Local\\DLO\\Presets\\presetlist.json"

print("\n-> writing to... " + filename)

# Writing to the given filename
with open(f"{filename}", "w") as outfile:
   outfile.write(presetsJSON)


### HOW TO READ FILE ###

f = open(f"{filename}", "r")
fileRead = json.loads(f.read())

print("\n-> printing file output...")
for a in fileRead['presets']:
    print(a['name'])

### WORKING WITH OBJECTS ###

currObj = fileRead['presets'][1]
print("\n-> currObj: " + currObj['name'])

### TO_PRESET TEST ###
p1 = Preset.to_Preset(fileRead['presets'][0])

print(p1.name)