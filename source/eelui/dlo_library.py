import os
import shutil
import subprocess
import json
import win32com.client # pip install pywin32

class Preset:
    def __init__(self, name, description, registryLocation, files):
        self.name = name
        self.description = description
        self.registryLocation = registryLocation
        self.files = files

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def to_dict(self):
        return {"name": self.name, "description": self.description, "registryLocation": self.registryLocation, "files": self.files}
    
    def to_Preset(dict):
        """dict as a parameter
         \n returns a Preset object with the name,description and registryLocation values
        """
        return Preset(dict['name'],dict['description'],dict['registryLocation'],dict['files'])

class presetmanager:

    global presetsDirectory
    global repositoryDirectory
    global presetListFilename
    global homeDirectory
    homeDirectory = "C:\\Users\\" + os.getenv("username") 
    presetsDirectory = homeDirectory + "\\AppData\\Local\\DLO\\Presets"
    repositoryDirectory = homeDirectory + "\\AppData\\Local\\DLO\\Presets\\Repository"
    presetListFilename = homeDirectory + "\\AppData\\Local\\DLO\\Presets\\PresetList.json"

    @staticmethod
    def create_preset(presetName, presetDescription):
        '''
        Creates a new preset with given presetName and Description\n
        presetName: Name of the preset\n
        presetDescription: Description of the preset
        '''

        presetmanager.create_directories()

        # Set the directory where the files are located
        desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop') # Getting the desktop path
        presetsRaw = []

        # 1: Export the registry key to the registryDirectory
        subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(presetsDirectory, presetName)}.reg", shell=True)
        
        # 2: load the .json file that stores the presets
        if presetmanager.fileIsEmpty(presetListFilename) != True:
            with open(presetListFilename) as fp:
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
        file_list = [f for f in os.listdir(desktop_path) ]
        file_paths = [os.path.join(desktop_path, f) for f in file_list]
            
        #Adding files to the preset
        files = [] 
        for filepath in file_paths:
            #copy files to repository and then delete them from desktop

            if os.path.splitext(filepath)[1] == ".lnk":

                target_path = return_shortcut_target(filepath)
                files.append({"path": target_path, "name": os.path.basename(target_path)})
            else: 
                
                filepath = shutil.copy(filepath,os.path.join(repositoryDirectory))
                os.remove(filepath)
                files.append({"path": filepath, "name": os.path.basename(filepath)})


        # Adding the new entry to the 'presetlist.json'
        presetsRaw.append(
            Preset(f"{presetName}",
            f"{presetDescription}",
            f"C:\\Users\\Bence\\Desktop\\{presetName}.reg",
            files)) 

        # Converting Objects into a dictionary
        presetsJSON = getPresetsInJsonFormat(presetsRaw)

        with open(f"{presetListFilename}", "w") as outfile:
            outfile.write(presetsJSON)

    @staticmethod
    def change_preset(presetName, presetNewName, presetNewDesc):
        presetmanager.create_directories()

        # Change to the registry directory
        os.chdir(presetsDirectory)

        with open(presetListFilename) as fp:
            presetList = json.load(fp)

            for preset in presetList['presets']:
                if preset['name'] == presetName:

                    preset['name'] = presetNewName
                    preset['description'] = presetNewDesc

                    presetsRaw = []
                    for preset in presetList['presets']:
                        presetsRaw.append(Preset.to_Preset(preset))

                    presetsJSON = getPresetsInJsonFormat(presetsRaw)

                    with open(f"{presetListFilename}", "w") as outfile:
                        outfile.write(presetsJSON)

    @staticmethod
    def save_preset(presetName):
        presetmanager.create_directories()
        # Delete the existing preset file
        os.remove(os.path.join(presetsDirectory, presetName + ".reg"))
        # Export the registry key to the registry directory
        subprocess.call(f"reg export HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\Shell\\Bags\\1\\Desktop {os.path.join(presetsDirectory, presetName)}.reg", shell=True)

    @staticmethod
    def load_preset(presetName):
        presetmanager.create_directories()
        # Getting name of registry file
        presetFileName = os.path.join(presetsDirectory, presetName + ".reg")

        # Exetuing registry file
        subprocess.call(['reg', 'import', presetFileName])

        # Stopping 'explorer.exe' in order to see the changes
        os.system("taskkill /im explorer.exe /F")
        
        # Starting 'explorer.exe' while not blocking the algorithm with the Input/Output stream of the CMD
        subprocess.Popen(['explorer'], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

    @staticmethod
    def delete_preset(presetToDelete):
        presetmanager.create_directories()

        # Change to the registry directory
        os.chdir(presetsDirectory)
        
        with open(presetListFilename) as fp:
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
                with open(f"{presetListFilename}", "r+") as outfile:
                    outfile.truncate(0)

                with open(f"{presetListFilename}", "w") as outfile:
                    outfile.write(presetsJSON)

                # Removing registry file
                os.remove(presetToDelete + ".reg") 
                break
        return

    @staticmethod
    def get_all_entries():
        presetmanager.create_directories()
        
        f = open(f"{presetListFilename}", "r")
        jsonlist = json.loads(f.read())

        presets = []

        for preset in jsonlist['presets']:
            presets.append(Preset.to_Preset(preset))
        
        return presets

    @staticmethod
    def create_directories():
        
        # Check if the directories exist
        if not os.path.exists(presetsDirectory) and os.path.exists(repositoryDirectory):
            # Create the directories
            os.makedirs(presetsDirectory)
            os.makedirs(repositoryDirectory)

        # Check if the 'presetlist.json' File exists
        if not os.path.exists(presetListFilename):
            # Feeding the file an empty list
            emptyList = []

            # Converting Objects into a dictionary
            presetsJSON = json.dumps({"presets": emptyList})

            with open(f"{presetListFilename}", "w") as outfile:
                outfile.write(presetsJSON)
  
    @staticmethod
    def fileIsEmpty(filename):
        '''
        Checks if a file is empty by confirming that its size is 0 bytes\n
        :param filename: The file to check\n
        :return: True if the file is empty, False otherwise\n
        '''
        return os.stat(filename).st_size == 0
    
@staticmethod
def return_shortcut_target(shortcut_path):
    '''
    Returns the target of a shortcut (.lnk)\n
    :param shortcut_path: The path to the shortcut\n
    :return: The target of the shortcut\n
    '''

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    return shortcut.Targetpath

@staticmethod
def getPresetsInJsonFormat(presetsRaw):
    presets = [obj.to_dict() for obj in presetsRaw]
    presets.sort(key=lambda obj: obj["name"])
    presetsJSON = json.dumps({"presets": presets})
    return presetsJSON