import json
import os

currObj = ""

## OBJECT CLASS ###

class Preset:
    def __init__(self, name, description, registryLocation):
        self.name = name
        self.description = description
        self.registryLocation = registryLocation

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_dict(self):
        return {"name": self.name, "description": self.description, "registryLocation": self.registryLocation}
    
    def to_Preset(dict):
        """dict as a parameter
         \n returns a Preset object with the name,description and registryLocation values
        """
        return Preset(dict['name'],dict['description'],dict['registryLocation'])

### HOW TO SAVE OBJECT ###

presetsRaw =  [
    Preset("Preset1", "Description of Preset1", "C:\\Users\\Bence\\Desktop\\preset1.reg"), 
    Preset("Preset2", "Description of Preset2", "C:\\Users\\Bence\\Desktop\\preset2.reg"),
    Preset("Preset3", "Description of Preset3", "C:\\Users\\Bence\\Desktop\\preset3.reg")
]

### HOW TO SERIALIZE OBJECT ###

# build a list of dicts from your objects:
presets = [obj.to_dict() for obj in presetsRaw]

# sort it based on number:
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