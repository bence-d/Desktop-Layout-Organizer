import os
import subprocess
import sys
import json

# Set the preset to default
preset = "default"

# Set the directory where the files are located
registryDirectory = "C:\\Users\\" + os.getenv("username") + "\\AppData\\Local\\DLO"
presetListFilename = "C:\\Users\\" + os.getenv("username") + "\\AppData\\Local\\DLO\\Presets\\PresetList.json"

def main():
    while True:
        # Clear the screen
        subprocess.call("cls", shell=True)
        print("================== DLO ==================")
        print(" [1]: Create New Preset")
        print(" [2]: Save current Preset")
        print(" [3]: Load current Preset")
        print(" [4]: Change Preset")
        print(" [5]: Delete Preset")
        print(" [6]: Exit")
        print("=========================================")
        print(" Current Preset:", presetName)
        print("=========================================")

        # Get the user's input
        user_input = input("[command]: ")

        if user_input == "1":
            create_preset()
        elif user_input == "2":
            save_preset()
        elif user_input == "3":
            load_preset()
        elif user_input == "4":
            change_preset()
        elif user_input == "5":
            delete_preset()
        elif user_input == "6":
            sys.exit()
        else:
            print("[DLO] ERROR: Unknown command")

def create_preset():
    global presetName
    presetName = input("Preset name: ")
    # Export the registry key to the registryDirectory
    subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(registryDirectory, 'Presets', preset)}.reg", shell=True)
    
    # 1 JSON File laden

    f = open(f"{presetListFilename}", "r")
    presetList = json.loads(f.read())

    # 2 Schauen, ob der Eintrag schon drin ist

    foundPresetInList = False
    for actPreset in presetList['presets']:
        if actPreset['name'] == presetName:
            foundPresetInList = True
            break

    # 3 Wenn schon drin ist, Fehler zurückgeben, ansonsten Eintrag hinzufügen

    if foundPresetInList:
        print("[DLO]: A preset with that name already exists.")
    else: 
        print("[DLO]: Adding entry... es sollte da erscheinen ")
    
    input("Press enter to continue...")
    main()

def change_preset():
    global presetName
    # Change to the registry directory
    os.chdir(os.path.join(registryDirectory, "Presets"))
    # List the files in the registry directory
    print(os.listdir())
    presetName = input("Preset name: ")
    input("Press enter to continue...")
    main()

def save_preset():
    print("[DLO] -> Please manually refresh the desktop...")
    input("Press enter to continue...")
    # Delete the existing preset file
    os.remove(os.path.join(registryDirectory, "Presets", presetName + ".reg"))
    # Export the registry key to the registry directory
    subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(registryDirectory, 'Presets', preset)}.reg", shell=True)


def load_preset():
    global presetName
    presetFileName = os.path.join(registryDirectory, "Presets", presetName + ".reg")
    subprocess.call(['reg', 'import', presetFileName])
    os.system("taskkill /im explorer.exe /F")
    subprocess.Popen(['explorer'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
    return

def delete_preset():
    global presetName
    # Change to the registry directory
    os.chdir(os.path.join(registryDirectory, "Presets"))
    # List the files in the registry directory
    print(os.listdir())
    presetToDelete = input("Preset name: ")
    os.remove(presetToDelete + ".reg")
    input("Press enter to continue...")
    return

# Check if the directories exist
if os.path.exists(registryDirectory) and os.path.exists(os.path.join(registryDirectory, "Presets")) and os.path.exists(os.path.join(registryDirectory, "Repository")):
    # Call the main function
    main()
else:
    # Create the directories
    os.makedirs(os.path.join(registryDirectory, "Presets"))
    os.makedirs(os.path.join(registryDirectory, "Repository"))