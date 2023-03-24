#####################################################################################
# A script for testing the 'dlo_library' file, thats part of the project.           #
# Since the automation of this process would require a virtual filesystem to be     #
# tested, the testing should be done partly with this script and manually.          #
#####################################################################################

from dlo_library import presetmanager as pmgr

# print("-> Started Tests...")

# # Test 1:

# print("[Test 1] > Creating a preset with name")
# presName = input("[Test 1] Name of new preset: ")
# pmgr.create_preset(presName)

# print("[Test 1] > Executed command. Check your files!")
# confirm = input("Press a button to continue...")

# # Test 2:

# print("[Test 2] > Saving preset ")
# pmgr.save_preset(presName)

# print("[Test 2] > Executed command. ")
# userInput = input("Press a button to continue...")

# # Test 3:

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

print("[Test 7] > Creating a preset with name")
presName = input("[Test 1] Name of new preset: ")
file_paths = pmgr.create_preset(presName, "exampledesc")

i = 1
for filepath in file_paths:
    print("> [" + str(i) +"]: " + filepath)
    i = i + 1
    pmgr.copy_file_to_repository(filepath)

confirm = input("Press a button to continue...")