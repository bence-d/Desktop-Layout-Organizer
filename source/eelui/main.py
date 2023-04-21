import eel
import sys
from dataHandlers.presetManager import PresetManager as pmgr

eel.init('web')

@eel.expose
def saysomething(name, desc):
    print("name: " + name)
    print("desc: " + desc)
    print(" ")

@eel.expose
def create_preset(name, desc):
    pmgr.create_preset(name, desc)

@eel.expose
def refresh_table():
    presetList = pmgr.get_all_entries()

    if presetList:
        for actPres in presetList:
            eel.addPresetToTable(actPres.name, actPres.description)  # This calls the Javascript function

@eel.expose
def refresh_edit_dropdown():
    presetList = pmgr.get_all_entries()

    if presetList:
        for actPres in presetList:
            eel.addPresetToEditDropdown(actPres.name, actPres.description) # This calls the Javascript function
    else:
        eel.foundNoPresets() # This calls the Javascript function, which disables the update button

@eel.expose
def delete_preset(preseToDel):
    pmgr.delete_preset(preseToDel)

@eel.expose
def loadpreset(presetToLoad):
    pmgr.load_preset(presetToLoad)

def savepreset(presetToSave):
    pmgr.save_preset(presetToSave)

eel.start('index.html', size=(800, 600), position=(0,0))