import sys
import dataHandlers.stringProcessor as sp
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
    def create_shortcut(sourceFile:str,destinationFolder:str):
        """
        Creates a shortcut for the file sourceFile and saves it in the destinationFolder
        destinationFolder: Folder where the shortcuts should be saved
        ps1FilePath: Path to the PowerShell Script that creates the shortcuts
        sourceFile: File to make a shortcut for
        """
        #print ("original source file: ")
        # print (sourceFile)
        sourceFile = sp.process(sourceFile)

        # getting the powershell script path relative to the current file
        ps1FilePath = os.path.dirname(os.path.abspath(__file__))
        ps1FilePath = os.path.join(ps1FilePath,"createShortcutCommands.ps1")
        ps1FilePath = sp.process(ps1FilePath)

        # targetFile = sourceFile
        
        # get only the filename without the path 
        targetFile = os.path.basename(sourceFile)
        # remove the file extension
        targetFile = os.path.splitext(targetFile)[0]
        # add the .lnk extension
        targetFile = targetFile + ".lnk"
        # add the destination folder to the targetFile
        targetFile = os.path.join(destinationFolder,targetFile)

        # creating the command to execute
        p = subprocess.run([powerShellExePath,ps1FilePath,targetFile,sourceFile],stdout=sys.stdout)

        # if p.returncode == 0:
        #     print("-> Succesfully created shortcut for '" + sourceFile +"'")
        #     print("-> Destination: " + targetFile)
        # else:
        #     # print each variable of the subprocess.run([powerShellExePath,ps1FilePath,targetFile,sourceFile],stdout=sys.stdout) function
        #     print("-> PowerShell Path: " + powerShellExePath)
        #     print("-> PowerShell Script Path: " + ps1FilePath)
        #     print("-> Target File: " + targetFile)
        #     print("-> Source File: " + sourceFile)
        #     print("-> An error as has occured creating the Shortcut")
        #     exit()

