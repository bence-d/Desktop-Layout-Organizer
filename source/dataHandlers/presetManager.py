import os
import shutil
import subprocess
import json
import configparser
import pythoncom

from dataHandlers.preset import Preset
from dataHandlers.shortcut_util import ShortcutUtil


class PresetManager:

    global PRESETS_DIRECTORY 
    global REPOSITORY_DIRECTORY
    global PRESET_LIST_FILE_NAME
    global HOME_DIRECTORY
    global DESKTOP_PATH
    global DEVELOPER_MODE

    HOME_DIRECTORY = "C:\\Users\\" + os.getenv("username") 
    PRESETS_DIRECTORY = HOME_DIRECTORY + "\\AppData\\Local\\DLO\\Presets"
    REPOSITORY_DIRECTORY = PRESETS_DIRECTORY + "\\Repository"
    PRESET_LIST_FILE_NAME = PRESETS_DIRECTORY + "\\PresetList.json"
    DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
    DEVELOPER_MODE = False


    @staticmethod
    def create_preset(presetName:str, presetDescription:str):
        pythoncom.CoInitialize()
        # Developer mode
        if (DEVELOPER_MODE):
            DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop\\DLODEV')
        else:
            DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')

        '''
        Creates a new preset with given presetName and Description\n
        presetName: Name of the preset\n
        presetDescription: Description of the preset
        '''

        PresetManager.create_directories()

        # Set the directory where the files are located
        presetsRaw = []
 
        # 1: load the .json file that stores the presets
        if PresetManager.file_is_empty(PRESET_LIST_FILE_NAME) != True:
            with open(PRESET_LIST_FILE_NAME) as fp:
                presetList = json.load(fp)

            # 2: check if given preset is included in the 'presetlist.json' file
            for actPreset in presetList['presets']:
                if actPreset['name'] == presetName:
                    # 3: return an error if a preset with the given name is already saved in the 'presetlist.json' file
                    return "ERROR: A preset with the given name already exists!"
            
            # 4: turning dictionary into a list
            for preset in presetList['presets']:
                presetsRaw.append(Preset.to_Preset(preset))

        # 5: Export the registry key to the registryDirectory
        subprocess.call(f'reg export HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\Shell\Bags\\1\Desktop "{os.path.join(PRESETS_DIRECTORY, presetName)}.reg"', shell=True)

        # Getting the files from the desktop
        file_list = [f for f in os.listdir(DESKTOP_PATH) ]
        file_paths = [os.path.join(DESKTOP_PATH, f) for f in file_list]

        # Adding the new entry to the 'presetlist.json'
        presetId = PresetManager.get_next_available_id()

        presetToAdd = Preset(
            f"{presetId}",
            f"{presetName}",
            f"{presetDescription}",
            f"C:\\Users\\Bence\\Desktop\\{presetName}.reg",
            []) # files to be added under the control of the user later of via the interface -> that's why it returns file_paths
        presetsRaw.append(presetToAdd) 

        # Converting Objects into a dictionary
        presetsJSON = PresetManager.get_presets_in_json_format(presetsRaw)

        with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
            outfile.write(presetsJSON)

        # Returning the paths of the files that are on the desktop, so the frontend can create shortcuts for them one by one
        return [presetToAdd.to_Dict(), file_paths]
        #return "response from the presetmanager "

    @staticmethod
    def change_preset(presetID:int, presetNewName:str, presetNewDesc:str, presetNewFiles:list):
        '''
        Changes the name and description of a preset\n
        presetID: ID of the preset\n
        presetNewName: New name of the preset\n
        presetNewDesc: New description of the preset
        '''

        print("recieved files:")
        print(presetNewFiles)
        print("preset data:")
        print(presetID)
        print(presetNewName)
        print(presetNewDesc)

        pythoncom.CoInitialize()
        PresetManager.create_directories()

        # Developer mode
        if (DEVELOPER_MODE):
            DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop\\DLODEV')
        else:
            DESKTOP_PATH = os.path.join(os.path.expanduser('~'), 'Desktop')
            
        # Change to the registry directory
        os.chdir(PRESETS_DIRECTORY)

        with open(PRESET_LIST_FILE_NAME) as fp:
            presetList = json.load(fp)

            for preset in presetList['presets']:
                #print("comparing " + str(preset['id']) + "[type " + str(type(preset['id'])) + "]" + " with " + str(presetID) + "[type " + str(type(presetID)) + "]")
                if preset['id'] == str(presetID):
                    # print("found preset in presetlist")

                    preset['name'] = presetNewName
                    preset['description'] = presetNewDesc

                    presetsRaw = []
                    for actPresetToAddToList in presetList['presets']:
                        presetsRaw.append(Preset.to_Preset(actPresetToAddToList))

                    #Adding files to the preset
                    files = [] 
                    for filepath in presetNewFiles:
                        #copy files to repository and then delete them from desktop

                        #print("for filepath: ")
                        # print (filepath)
                        #print("os path splitext: ")
                        #print (os.path.splitext(filepath)[1])
                        # print the extension of the file save in filepath

                        if os.path.splitext(filepath)[1] == ".lnk":
                            target_path = ShortcutUtil.return_shortcut_target(filepath)
                            # adding file to the presetlist...
                            files.append({"path": target_path, "name": os.path.basename(target_path)})
                        else: 
                            # copying file into repostiory

                            # check filepath['path'] exists
                            if os.path.exists(filepath):
                                newFilePath = shutil.copy(filepath,os.path.join(REPOSITORY_DIRECTORY))

                                # deleting file from desktop
                                os.remove(filepath)
                                # creating shortcut on desktop
                                ShortcutUtil.create_shortcut(newFilePath, DESKTOP_PATH)
                                # adding file to the presetlist
                                files.append({"path": filepath, "name": os.path.basename(filepath)})

                    preset['files'] = files

                    # search for preset.id in presetsRaw
                    for actPreset in presetsRaw:
                        if actPreset.id == str(presetID):
                            #print("found preset in presetsraw")
                            actPreset.name = presetNewName
                            actPreset.description = presetNewDesc
                            actPreset.files = files
                            #print("newfiles: ")
                            print(actPreset.files)

                    presetsJSON = PresetManager.get_presets_in_json_format(presetsRaw)
                    with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
                        outfile.write(presetsJSON)
                    return preset
                
        print("preset not found in presetlist")
        return "ERROR: No preset found with id'" + str(presetID) + "'"

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
        pythoncom.CoInitialize()
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
                        if os.path.splitext(file['name'])[1] == ".lnk":
                            ShortcutUtil.create_shortcut(file, DESKTOP_PATH)
                        else:
                            shutil.copy(file['path'], DESKTOP_PATH)

        # Exetuing registry file
        subprocess.call(['reg', 'import', presetFileName])

        # Stopping 'explorer.exe' in order to see the changes
        os.system("taskkill /im explorer.exe /F")
        
        # Starting 'explorer.exe' while not blocking the algorithm with the Input/Output stream of the CMD
        subprocess.Popen(['explorer'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    @staticmethod
    def delete_preset(presetID:int):
        '''
        Deletes a preset\n
        presetToDelete: Name of the preset
        '''
        PresetManager.create_directories()

        # Change to the registry directory
        os.chdir(PRESETS_DIRECTORY)
        
        with open(PRESET_LIST_FILE_NAME) as fp:
            presetList = json.load(fp)

        presetToDelete = Preset("", "", "", "", [])

        for preset in presetList['presets']:
            if preset['id'] == str(presetID):
                # Deleting given preset from list
                list.remove(presetList['presets'],preset)

                presetToDelete = preset

                # Turning Dictionary into an object
                presetsRaw = []
                for preset in presetList['presets']:
                    presetsRaw.append(Preset.to_Preset(preset))

                presets = [obj.to_Dict() for obj in presetsRaw]
                presets.sort(key=lambda obj: obj["name"])
                presetsJSON = json.dumps({"presets": presets})

                # Saving 'presetlist.json'
                with open(f"{PRESET_LIST_FILE_NAME}", "r+") as outfile:
                    outfile.truncate(0)

                with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
                    outfile.write(presetsJSON)

                # Removing registry file
                os.remove(preset['name'] + ".reg") 
                return presetToDelete
        
        return "ERROR: No preset found with id'" + str(presetID) + "'"
    
    @staticmethod
    def update_preset(presetID: int, presetName:str, presetDescription:str):
        '''
        Updates a preset\n
        presetName: New Name of the preset
        presetDescription: New description of the preset
        '''
        PresetManager.create_directories()

        # Change to the registry directory
        os.chdir(PRESETS_DIRECTORY)
        
        with open(PRESET_LIST_FILE_NAME) as fp:
            presetList = json.load(fp)

        for preset in presetList['presets']:
            if preset['id'] == presetID:
                # make a copy of the old registry file
                shutil.copy(preset.name + ".reg", presetName + ".reg")
                os.remove(preset.name + ".reg")

                # replacing old preset attributes with the new ones+
                preset['name'] = presetName	
                preset['description'] = presetDescription

                # Turning Dictionary into an object
                presetsRaw = []
                for preset in presetList['presets']:
                    presetsRaw.append(Preset.to_Preset(preset))

                presets = [obj.to_Dict() for obj in presetsRaw]
                presets.sort(key=lambda obj: obj["name"])
                presetsJSON = json.dumps({"presets": presets})

                # Saving 'presetlist.json'
                with open(f"{PRESET_LIST_FILE_NAME}", "r+") as outfile:
                    outfile.truncate(0)

                with open(f"{PRESET_LIST_FILE_NAME}", "w") as outfile:
                    outfile.write(presetsJSON)
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
        if not os.path.exists(PRESETS_DIRECTORY) or not os.path.exists(REPOSITORY_DIRECTORY):
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
        presets = [obj.to_Dict() for obj in presetsRaw]
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
   
    @staticmethod
    def preset_exists(presetName:str):
        '''
        Checks if a preset already exists\n
        presetName: Name of the preset
        '''
        presets = PresetManager.get_all_entries()
        for preset in presets:
            if preset.name == presetName:
                return True
        return False

    @staticmethod     
    def import_preset(source_file:str, destination_file:str, preset_name:str):
        '''
        Imports a preset from a source file to a destination file\n
        :param source_file: The source file to import the preset from\n
        :param destination_file: The destination file to import the preset to\n
        :param preset_name: The name of the preset to import\n
        :return: True if the preset was imported successfully, False otherwise\n
        '''
        # Load the source file
        with open(source_file, 'r') as source:
            source_data = json.load(source)

        # Load the destination file, if it exists
        try:
            with open(destination_file, 'r') as destination:
                destination_data = json.load(destination)
        except FileNotFoundError:
            # If the destination file doesn't exist, create an empty dictionary
            destination_data = {"presets": []}

        # Check if the preset already exists in the destination file
        for preset in destination_data['presets']:
            if preset['name'] == preset_name:
                print("The preset already exists in the destination file. Import aborted.")
                return False

        # Find the specific preset object in the source file
        found_preset = None
        for preset in source_data['presets']:
            if preset['name'] == preset_name:
                found_preset = preset
                break

        if found_preset is None:
            print("The specified preset was not found in the source file.")
            return False

        # Copy the preset object to the destination file
        destination_data['presets'].append(found_preset)

        # Save the updated destination file
        with open(destination_file, 'w') as destination:
            json.dump(destination_data, destination, indent=4)

        print("The preset was successfully imported.")
        return True
                
        @staticmethod
        def get_next_available_id():
            '''
            Returns the next available id
            '''
            highest_id = -1

            presets = PresetManager.get_all_entries()
            for preset in presets:
                if int(preset.id) > int(highest_id):
                    highest_id = preset.id
            
            highest_id = int(highest_id) + 1

            return str(highest_id)

    @staticmethod
    def export_preset(source_file:str, destination_file:str, preset_name:str):
        '''
        Exports a preset from a source file to a destination file\n
        :param source_file: The source file to export the preset from\n
        :param destination_file: The destination file to export the preset to\n
        :param preset_name: The name of the preset to export\n
        :return: True if the preset was exported successfully, False otherwise\n
        '''

        #import_preset and export_preset are the same function, the only difference is the order of the parameters
        PresetManager.import_preset(destination_file,source_file,preset_name)

    @staticmethod
    def get_next_available_id():
        highest_id = -1

        presets = PresetManager.get_all_entries()
        for preset in presets:
            if int(preset.id) > int(highest_id):
                highest_id = preset.id

        highest_id = int(highest_id) + 1

        return str(highest_id)
