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

import unittest
import json
from os.path import join
import shutil
import xlsxwriter

class TestShortcutUtilMethods(unittest.TestCase):

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

    def test_a_txt(self):
        # [1] > create shtest1.txt on the desktop
        filename = "shtest1.txt"
        filepath = os.path.join(DESKTOP_PATH, filename)
        file = open(filepath,'w')   # Trying to create a new file or open one
        file.close()

        # [2] > try to copy shtest1.txt to the repository
        newFilePath = shutil.copy(filepath,os.path.join(REPOSITORY_DIRECTORY))

        # [3] > check if the file exists in the repository
        self.assertTrue(os.path.exists(newFilePath))

        # [4] > delete the file from the repository and from the desktop
        os.remove(newFilePath)
        os.remove(filepath)

    def test_a_folder(self):
        # [1] > create shtestfolder1 on the desktop
        foldername = "shtestfolder1"
        folderpath = os.path.join(DESKTOP_PATH, foldername)
        os.mkdir(folderpath)

        # [2] > try to copy shtestfolder1 to the repository
        newFolderPath = shutil.copytree(folderpath,os.path.join(REPOSITORY_DIRECTORY,foldername))

        # [3] > check if the folder exists in the repository
        self.assertTrue(os.path.exists(newFolderPath))

        # [4] > delete the folder from the repository and from the desktop
        shutil.rmtree(newFolderPath)
        shutil.rmtree(folderpath)

    def test_a_file_with_special_name(self):
        # [1] > create a file with special characters in the name
        filename = "shtest1!@#$%^&()_+{}`-=[];',.txt" # on Windows the following characters are not allowed: \/:*?"<>|
        filepath = os.path.join(DESKTOP_PATH, filename)
        file = open(filepath,'w')
        file.close()

        # [2] > try to copy the file to the repository
        newFilePath = shutil.copy(filepath,os.path.join(REPOSITORY_DIRECTORY))

        # [3] > check if the file exists in the repository
        self.assertTrue(os.path.exists(newFilePath))

        # [4] > delete the file from the repository and from the desktop
        os.remove(newFilePath)
        os.remove(filepath)

    def test_a_folder_with_special_name(self):
        # [1] > create a folder with special characters in the name
        foldername = "shtestfolder1!@#$%^&()_+{}`-=[];',."
        folderpath = os.path.join(DESKTOP_PATH, foldername)
        os.mkdir(folderpath)

        # [2] > try to copy the folder to the repository
        newFolderPath = shutil.copytree(folderpath,os.path.join(REPOSITORY_DIRECTORY,foldername))

        # [3] > check if the folder exists in the repository
        self.assertTrue(os.path.exists(newFolderPath))

        # [4] > delete the folder from the repository and from the desktop
        shutil.rmtree(newFolderPath)
        shutil.rmtree(folderpath)

    def test_an_occupied_txt(self):
        # [1] > create shtest1.txt on the desktop
        filename = "shtest1.xlsx"
        filepath = os.path.join(DESKTOP_PATH, filename)
        # file = open(filepath,'w')   # Trying to create a new file or open one
        # file.close()
        workbook = xlsxwriter.Workbook(filepath)
        worksheet = workbook.add_worksheet()
        workbook.close()

        # [1] Let the user open a file and then continue when ready

        print(f"[SHUTILTEST] > Please open {filename} and then press any button to continue")
        randomUserInput = input()

        newFilePath = shutil.copy(filepath,os.path.join(REPOSITORY_DIRECTORY))

        # [3] > check if the file exists in the repository
        self.assertTrue(os.path.exists(newFilePath))

        os.remove(newFilePath)
        
        success = False
        while success == False:
            try:
                # [4] > delete the file from the repository and from the desktop
                os.remove(filepath)
                success = True
            except PermissionError as e:
                if e.args[0] == 13:
                    print(f"[SHUTILTEST] > Please close {filename} and then press any button to continue")
                    randomUserInput = input()

if __name__ == '__main__':
    unittest.main()
else:
    print("__name__=" + __name__)