from dlo_library import presetmanager as pmgr

print("-> Started Tests...")

Test 1:

print("[Test 1] > Creating a preset with name")
presName = input("[Test 1] Name of new preset: ")
pmgr.create_preset(presName)

print("[Test 1] > Executed command. Check your files!")
confirm = input("Press a button to continue...")

Test 2:

print("[Test 2] > Saving preset ")
pmgr.save_preset(presName)

print("[Test 2] > Executed command. ")
userInput = input("Press a button to continue...")

Test 3:

print("[Test 3] > Loading preset ")
pmgr.load_preset(presName)

print("[Test 3] > Executed command. Check your desktop!")
userInput = input("Press a button to continue...")

Test 4:

print("[Test 4] > Delete preset ")
pmgr.delete_preset(presName)

print("[Test 4] > Executed command. Check your files!")
userInput = input("Press a button to continue...")

Test 5:

print("[Test 5] > Recreate directory tree ")
pmgr.create_directories()

print("[Test 5] > Executed command. Check your files!")
userInput = input("Press a button to continue...")