import os
import subprocess
import sys

# Set the preset to default
preset = "default"

# Set the directory where the files are located
directory = "C:\\Users\\" + os.getenv("username") + "\\AppData\\Local\\DLO"

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
        print(" Current Preset:", preset)
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
    global preset
    preset = input("Preset name: ")
    # Export the registry key to the Presets directory
    subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(directory, 'Presets', preset)}.reg", shell=True)
    input("Press enter to continue...")
    main()

def change_preset():
    global preset
    # Change to the Presets directory
    os.chdir(os.path.join(directory, "Presets"))
    # List the files in the directory
    print(os.listdir())
    preset = input("Preset name: ")
    input("Press enter to continue...")
    main()

def save_preset():
    print("[DLO] -> Please manually refresh the desktop...")
    input("Press enter to continue...")
    # Delete the existing preset file
    os.remove(os.path.join(directory, "Presets", preset + ".reg"))
    # Export the registry key to the Presets directory
    subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(directory, 'Presets', preset)}.reg", shell=True)

def load_preset():
    return

def delete_preset():
    return

# Check if the directories exist
if os.path.exists(directory) and os.path.exists(os.path.join(directory, "Presets")) and os.path.exists(os.path.join(directory, "Repository")):
    # Call the main function
    main()
else:
    # Create the directories
    os.makedirs(os.path.join(directory, "Presets"))
    os.makedirs(os.path.join(directory, "Repository"))