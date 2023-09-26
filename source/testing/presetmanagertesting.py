#####################################################################################
# A script for testing the 'dlo_library' file, thats part of the project.           #
# Since the automation of this process would require a virtual filesystem to be     #
# tested, the testing should be done partly with this script and manually.          #
#####################################################################################

# 1) Get relative path to this file
import os
import sys

pathToDataHandlers = os.path.dirname(os.path.realpath(__file__))

# 2) Go to the parent folder 
pathToDataHandlers = os.path.abspath(os.path.join(pathToDataHandlers, os.pardir))

# 3) Add the folder containing 'dataHandlers' to the system path
sys.path.append(pathToDataHandlers)

# 4) Import the dataHandlers
from dataHandlers.presetManager import PresetManager as pmgr

# from source import presetManager as pmgr

print(" > Started Tests...")

# print("[Test 1] > Importing a preset")
# source_file = "C:\\Users\\bence\\Desktop\\presetToImport.json"
# destination_file = "C:\\Users\\bence\\AppData\\Local\\DLO\\Presets\\PresetList.json"
# preset_name = "test0012409"
# print("[Test 1] > ", source_file, destination_file, preset_name)
# pmgr.import_preset(source_file, destination_file, preset_name)
# print(" > importing done...")

print("[Test 2] > Exporting a preset")
preset_name = "gaming2"
pmgr.export_preset(preset_name)
print(" > exporting done...")

# Test 1:

# pmgr.load_preset("imp3")

# print("[Test 1] > Creating a preset with name")
# presName = input("[Test 1] Name of new preset: ")
# description = "sample description"
# result = pmgr.create_preset(presName, description)
# print(result)
# print("[Test 1] > Executed command. Check your files!")

#pmgr.change_preset(result[0]['id'], result[0]['name'], result[0]['description'], result[1])


# # Test 2:

# print("[Test 2] > Saving preset ")
# pmgr.save_preset(presName)

# print("[Test 2] > Executed command. ")
# userInput = input("Press a button to continue...")

# Test 3:

# presName = "testpreset"
# print("[Test 3] > Loading preset ")
# pmgr.load_preset(presName)
# print("[Test 3] > Executed command. Check your desktop!")
# userInput = input("Press a button to continue...")

# # Test 4:

# print("[Test 4] > Delete preset ")
# pmgr.delete_preset(presName)

# print("[Test 4] > Executed command. Check your files!")
# userInput = input("Press a button to continue...")

# # Test 5:

# print("[Test 5] > Recreate directory tree ")
# pmgr.create_directories()

# print("[Test 5] > Executed command. Check your files!")
# userInput = input("Press a button to continue...")

# Test 6:

# print("[Test 6] > Get a list of members in 'presetlist.json' ")
# listOfEntries = pmgr.get_all_entries()
# emptyList = []

# if type(listOfEntries) == type(emptyList):
#     print("[Test 6] > Presets found:")
#     for actPres in listOfEntries:
#         print("[Test 6] > " + actPres.name)
#     print("[Test 6] > Test Passed. (Method returns a list with entries.)")
# else:
#     print("[Test 6] > Test Failed. (Method returns a variable with an unexpected datatype: " + type(listOfEntries) + ".")

# userInput = input("Press a button to continue...")

# Test 7:

# print("[Test 7] > Creating a preset with name")
# presName = input("[Test 1] Name of new preset: ")
# file_paths = pmgr.create_preset(presName, "exampledesc")

#i = 1
#for filepath in file_paths:
#    print("> [" + str(i) +"]: " + filepath)
#    i = i + 1
#    pmgr.copy_file_to_repository(filepath)