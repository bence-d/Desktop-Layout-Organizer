import sys
import stringprocessor as sp
import os
import subprocess
import win32com.client

class ShortcutUtil:
    global powerShellExePath
    powerShellExePath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

    @staticmethod
    def return_shortcut_target(shortcut_path:str):
        '''
        Returns the target of a shortcut (.lnk)\n
        :param shortcut_path: The path to the shortcut\n
        :return: The target of the shortcut\n
        '''

        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        return shortcut.Targetpath
    
    @staticmethod
    def createShortcut(sourcePath:str,destinationFolder:str,ps1FilePath:str):
        """
        Creates a shortcut for each file in the sourcePath and saves it in the destinationFolder
        destinationFolder: Folder where the shortcuts should be saved
        ps1FilePath: Path to the PowerShell Script that creates the shortcuts
        sourcePath: Folder where the files are located
        """
        sourcePath = sp.process(sourcePath)
        ps1FilePath = sp.process(ps1FilePath)

        try:
            #all entries of the targetFolder
            entries = os.listdir(sourcePath)
        except:
            print("-> File can not be found")
            exit()

        if "desktop.ini" in entries:
            ## we don't want to work with the file "desktop.ini" therefore i'm deleting it from the list
            entries.remove("desktop.ini")

        for entry in entries:

            ## Parameters being sent to the PowerShell Script to create a shortcut
            targetFile = os.path.join(sourcePath,entry)
            shortcutPath = os.path.join(destinationFolder,entry)
            
            ## DEBUG
            ## print ( " -> Printing variables used for PS execution..." )
            ## print ( "powerShellExePath: " + powerShellExePath )
            ## print ( "ps1FilePath: " + ps1FilePath )
            ## print ( "shortcutpath: " + shortcutPath )
            ## print ( "targetFile: " + targetFile)

            p = subprocess.run([powerShellExePath,ps1FilePath,shortcutPath,targetFile],stdout=sys.stdout)

            if p.returncode == 0:
                print("-> Succesfully created shortcut for '" + targetFile +"'")
            else:
                print("-> An error as has occured creating the Shortcut")
                exit()
