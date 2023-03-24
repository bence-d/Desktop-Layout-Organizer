import eel
from presetManager import presetmanager as pmgr

eel.init('web')

@eel.expose
def saysomething(name, desc):
    print("name: " + name)
    print("desc: " + desc)
    print(" ")

@eel.expose
def createpreset(name, desc):
    pmgr.create_preset(name, desc)

@eel.expose
def refreshDropdown():
    presetList = pmgr.get_all_entries()

    if presetList:
        for actPres in presetList:
            # presetListNames.append(actPres.name)
            eel.add_preset_to_dropdown(actPres.name)  # This calls the Javascript function

@eel.expose
def deletepreset(preseToDel):
    pmgr.delete_preset(preseToDel)

@eel.expose
def loadpreset(presetToLoad):
    pmgr.load_preset(presetToLoad)

def savepreset(presetToSave):
    pmgr.save_preset(presetToSave)

eel.start('index.html', size=(800, 600), position=(0,0))