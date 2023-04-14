import os
import shutil
import subprocess
import json
import configparser

from preset import Preset
from shortcut_util import shortcututil


class PresetManager:

    global PRESETS_DIRECTORY 
    global REPOSITORY_DIRECTORY
    global PRESET_LIST_FILE_NAME
    global HOME_DIRECTORY
    global DESKTOP_PATH

    HOME_DIRECTORY = "C:\\Users\\" + os.getenv("username") 
    PRESETS_DIRECTORY = HOME_DIRECTORY + "\\AppData\\Local\\DLO\\Presets"
    REPOSITORY_DIRECTORY = PRESETS_DIRECTORY + "\\Repository"
    PRESET_LIST_FILE_NAME = PRESETS_DIRECTORY + "\\PresetList.json"
    DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')


    @staticmethod
    def create_preset(presetName:str, presetDescription:str):
        '''
        Creates a new preset with given presetName and Description\n
        presetName: Name of the preset\n
        presetDescription: Description of the preset
        '''

        PresetManager.create_directories()

        # Set the directory where the files are located
        presetsRaw = []

        # 1: Export the registry key to the registryDirectory
        subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(PRESETS_DIRECTORY, presetName)}.reg", shell=True)
        
        # 2: load the .json file that stores the presets
        if PresetManager.fileIsEmpty(PRESET_LIST_FILE_NAME) != True:
            with open(PRESET_LIST_FILE_NAME) as fp:
                presetList = json.load(fp)

            # 3: check if given preset is included in the 'presetlist.json' file
            foundPresetInList = False
            for actPreset in presetList['presets']:
                if actPreset['name'] == presetName:
                    foundPresetInList = True
                    break

            # 3 Wenn schon drin ist, Fehler zurückgeben, ansonsten Eintrag hinzufügen
            # 4: if a preset with the given name is already saved in the 'presetlist.json' file
            # return an error, otherwise add it to the file
            if not foundPresetInList:
                # Turning dictionary into a list
                for preset in presetList['presets']:
                    presetsRaw.append(Preset.to_Preset(preset))

        # Getting the files from the desktop
        file_list = [f for f in os.listdir(DESKTOP_PATH) ]
        file_paths = [os.path.join(DESKTOP_PATH, f) for f in file_list]
            
        #Adding files to the preset
        files = [] 
        for filepath in file_paths:
            #copy files to repository and then delete them from desktop

            if os.path.splitext(filepath)[1] == ".lnk":

                target_path = shortcututil.return_shortcut_target(filepath)
                files.append({"path": target_path, "name": os.path.basename(target_path)})
            else: 
                # filepath = shutil.copy(filepath,os.path.join(REPOSITORY_DIRECTORY))
                # os.remove(filepath)
                files.append({"path": filepath, "name": os.path.basename(filepath)})


        # Adding the new entry to the 'presetlist.json'
        presetsRaw.append(
            Preset(f"{presetName}",
            f"{presetDescription}",
            f"C:\\Users\\Bence\\Desktop\\{presetName}.reg",
            files)) 

        # Converting Objects into a dictionary
        presetsJSON = PresetManager.getPresetsInJsonFormat(presetsRaw)

        with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
            outfile.write(presetsJSON)

    @staticmethod
    def change_preset(presetName:str, presetNewName:str, presetNewDesc:str):
        '''
        Changes the name and description of a preset\n
        presetName: Name of the preset\n
        presetNewName: New name of the preset\n
        presetNewDesc: New description of the preset
        '''
        PresetManager.create_directories()

        # Change to the registry directory
        os.chdir(PRESETS_DIRECTORY)

        with open(PRESET_LIST_FILE_NAME) as fp:
            presetList = json.load(fp)

            for preset in presetList['presets']:
                if preset['name'] == presetName:

                    preset['name'] = presetNewName
                    preset['description'] = presetNewDesc

                    presetsRaw = []
                    for preset in presetList['presets']:
                        presetsRaw.append(Preset.to_Preset(preset))

                    presetsJSON = PresetManager.getPresetsInJsonFormat(presetsRaw)

                    with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
                        outfile.write(presetsJSON)

    @staticmethod
    def save_preset(presetName:str):
        '''
        Saves the current desktop layout as a preset\n
        presetName: Name of the preset
        '''
        PresetManager.create_directories()
        # Delete the existing preset file
        os.remove(os.path.join(PRESETS_DIRECTORY, presetName + ".reg"))
        # Export the registry key to the registry directory
        subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(PRESETS_DIRECTORY, presetName)}.reg", shell=True)

    @staticmethod
    def load_preset(presetName:str):
        '''
        Loads a preset onto the Desktop\n
        presetName: Name of the preset
        '''
        PresetManager.create_directories()
        presetFileName = os.path.join(PRESETS_DIRECTORY, presetName + ".reg")

        #delete all shortcuts from desktop
        file_list = [f for f in os.listdir(DESKTOP_PATH) ]
        file_paths = [os.path.join(DESKTOP_PATH, f) for f in file_list]
        for filepath in file_paths:
            os.remove(filepath)

        #search for entry in json and load shortcuts on to dekstop

        with open(PRESET_LIST_FILE_NAME) as fp:
            presetList = json.load(fp)

            for preset in presetList['presets']:
                if preset['name'] == presetName:

                    # Saving the preset in the config file (in order to load it on startup)
                    PresetManager.save_preset_in_config(presetName)

                    for file in preset['files']:
                        if os.path.splitext(file['path'])[1] == ".lnk":
                            shortcututil.create_shortcut(file['path'], DESKTOP_PATH)
                        else:
                            shutil.copy(file['path'], DESKTOP_PATH)

        # Exetuing registry file
        subprocess.call(['reg', 'import', presetFileName])

        # Stopping 'explorer.exe' in order to see the changes
        os.system("taskkill /im explorer.exe /F")
        
        # Starting 'explorer.exe' while not blocking the algorithm with the Input/Output stream of the CMD
        subprocess.Popen(['explorer'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    @staticmethod
    def delete_preset(presetToDelete:str):
        '''
        Deletes a preset\n
        presetToDelete: Name of the preset
        '''
        PresetManager.create_directories()

        # Change to the registry directory
        os.chdir(PRESETS_DIRECTORY)
        
        with open(PRESET_LIST_FILE_NAME) as fp:
            presetList = json.load(fp)

        for preset in presetList['presets']:
            if preset['name'] == presetToDelete:
                # Deleting given preset from list
                list.remove(presetList['presets'],preset)

                # Turning Dictionary into an object
                presetsRaw = []
                for preset in presetList['presets']:
                    presetsRaw.append(Preset.to_Preset(preset))

                presets = [obj.to_dict() for obj in presetsRaw]
                presets.sort(key=lambda obj: obj["name"])
                presetsJSON = json.dumps({"presets": presets})

                # Saving 'presetlist.json'
                with open(f"{PRESET_LIST_FILE_NAME}", "r+") as outfile:
                    outfile.truncate(0)

                with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
                    outfile.write(presetsJSON)

                # Removing registry file
                os.remove(presetToDelete + ".reg") 
                break
        return

    @staticmethod
    def get_all_entries():
        '''
        Returns a list of all presets
        '''
        PresetManager.create_directories()
        
        f = open(f"{PRESET_LIST_FILE_NAME}", "r")
        jsonlist = json.loads(f.read())

        presets = []

        for preset in jsonlist['presets']:
            presets.append(Preset.to_Preset(preset))
        
        return presets

    @staticmethod
    def create_directories():
        '''
        Creates the necessary directories if they don't exist
        '''
        
        # Check if the directories exist
        if not os.path.exists(PRESETS_DIRECTORY) and os.path.exists(REPOSITORY_DIRECTORY):
            # Create the directories
            os.makedirs(PRESETS_DIRECTORY)
            os.makedirs(REPOSITORY_DIRECTORY)

        # Check if the 'presetlist.json' File exists
        if not os.path.exists(PRESET_LIST_FILE_NAME):
            # Feeding the file an empty list
            emptyList = []

            # Converting Objects into a dictionary
            presetsJSON = json.dumps({"presets": emptyList})

            with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
                outfile.write(presetsJSON)

    @staticmethod
    def file_is_empty(filename:str):
        '''
        Checks if a file is empty by confirming that its size is 0 bytes\n
        :param filename: The file to check\n
        :return: True if the file is empty, False otherwise\n
        '''
        return os.stat(filename).st_size == 0

    @staticmethod
    def get_presets_in_json_format(presetsRaw:list):
        '''
        Returns the presets in a JSON format\n
        presetsRaw: List of Preset objects\n
        '''
        presets = [obj.to_dict() for obj in presetsRaw]
        presets.sort(key=lambda obj: obj["name"])
        presetsJSON = json.dumps({"presets": presets})
        return presetsJSON
    
    @staticmethod
    def save_preset_in_config(presetName:str):
        '''
        Saves the current presetName in the cfg file
        '''

        # Create a ConfigParser object
        config = configparser.ConfigParser()

        # Add some sections and options to the ConfigParser object
        config.add_section('Preset')
        config.set('Preset', 'presetName', presetName)

        # Write the ConfigParser object to the config file in located in the same directory as the script
        with open(os.path.join(PRESETS_DIRECTORY,'lastPreset.cfg'), 'w') as configfile:
            config.write(configfile)
            