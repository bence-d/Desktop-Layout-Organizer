import shutil
import subprocess
import sys
import os

#alle print statements sollten am ende des projekts mittels einem alert oder einen pop-up angezeigt werden.

desktopPath = "C:\\Users\\hvb63\\OneDrive\\Desktop"
desktopPathRAW = 'C:\\Users\\hvb63\\OneDrive\\Desktop'

def createShortcut(ps1FilePath,targetFolder):
    """
    create a shortcut for every file in the "targetFolder" on the desktop\n
    "ps1FilePath" is the path of the powerShellScript (.ps1) which runs all the commands used for creating a shortcut\n
    "targetFolder" can be a folder- or a filepath where the file(s) are\n
        folderpath -> a shortcut for every file in the folder\n
        filepath -> a shortcut for the file
    """

    #absoluter pfad von der powershell exe
    powerShellExePath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

    ps1FilePath = "C:\\Users\\hvb63\\OneDrive\\Desktop\\Schule\\4bhif\\syp\\createShortcutCommands.ps1"
    try:
        #all entries of the targetFolder
        entries = os.listdir(targetFolder)
    except:
        print("File can not be found")
        exit()

    if "desktop.ini" in entries:
        #we don't want to work with the file "desktop.ini" therefore i'm deleting it from the list
        entries.remove("desktop.ini")

    for entry in entries:

        #Parameters being sent to the PowerShell Script to create a shortcut
        targetFile = "{}\\{}".format(targetFolder,entry)
        shortcutPath = "{}\\{}.lnk".format(desktopPath,entry)

        p = subprocess.run([powerShellExePath,ps1FilePath,shortcutPath,targetFile],stdout=sys.stdout)

        if p.returncode == 0:
            print("Succesfully created shortcut")
        else:
            print("An error as has occured creating the Shortcut")
            exit()

def moveFile(objectBeingMoved,targetPath):
    """
    move a file from one path to another\n
    "objectBeingMoved" -> File/Folder that is being moved to the destination\n
    "targetPath" -> the destination of the object that is being moved
    """

    shutil.move(objectBeingMoved, targetPath)

    print("Succesfully moved file") 


#testen für createshortcut
createShortcut(
    "C:\\Users\\hvb63\\Downloads\\4bhif\\syp\\createShortcutCommands.ps1",
    "C:\\Users\\hvb63\\OneDrive\\Desktop\\Schule")