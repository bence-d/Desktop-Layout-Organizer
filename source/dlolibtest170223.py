import dlo_library as dlolib

presetname = input("Preset name: ")
presetdesc = input("Preset desc: ")

dlolib.presetmanager.create_preset(presetname, presetdesc);

print("> preset created")

