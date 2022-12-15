import shutil
import subprocess
import sys
import os
import stringProcessor

# alle print statements sollten am ende des projekts mittels einem alert oder einen pop-up angezeigt werden.

# Initializing Variables

ps = stringProcessor.PSStringProcessor()

# Declaring Paths

## Destination
desktopPath = input("Destination Folder: ")

## PowerShell
powerShellExePath = "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"

## PowerShell Script
ps1FilePath = input("PowerShell Script Path: ")
ps1FilePath = ps.process(ps1FilePath)

## Source (the files that the shortcuts will be made for)
sourceRAW = input("Source Path: ")
sourceFormatted = ps.process(sourceRAW)

def createShortcut(ps1FilePath,targetFolder):
    """
    create a shortcut for every file in the "targetFolder" on the desktop\n
    "ps1FilePath" is the path of the powerShellScript (.ps1) which runs all the commands used for creating a shortcut\n
    "targetFolder" can be a folder- or a filepath where the file(s) are\n
        folderpath -> a shortcut for every file in the folder\n
        filepath -> a shortcut for the file
    """

    try:
        #all entries of the targetFolder
        entries = os.listdir(sourceRAW)
    except:
        print("-> File can not be found")
        exit()

    if "desktop.ini" in entries:
        ## we don't want to work with the file "desktop.ini" therefore i'm deleting it from the list
        entries.remove("desktop.ini")

    for entry in entries:

        ## Parameters being sent to the PowerShell Script to create a shortcut
        targetFile = '{}\\{}'.format(sourceFormatted,entry)
        shortcutPath = '{}\\{}.lnk'.format(desktopPath,entry)
        
        ## DEBUG
        ## print ( " -> Printing variables used for PS execution..." )
        ## print ( "powerShellExePath: " + powerShellExePath )
        ## print ( "ps1FilePath: " + ps1FilePath )
        ## print ( "shortcutpath: " + shortcutPath )
        ## print ( "targetFile: " + targetFile)

        p = subprocess.run([powerShellExePath,ps1FilePath,shortcutPath,targetFile],stdout=sys.stdout)

        if p.returncode == 0:
            print("-> Succesfully created shortcut '" + targetFile +"'")
        else:
            print("-> An error as has occured creating the Shortcut")
            exit()

def moveFile(objectBeingMoved,targetPath):
    """
    move a file from one path to another\n
    "objectBeingMoved" -> File/Folder that is being moved to the destination\n
    "targetPath" -> the destination of the object that is being moved
    """

    shutil.move(objectBeingMoved, targetPath)

    print("-> Succesfully moved file") 


## testen für createshortcut
createShortcut(ps1FilePath, sourceRAW) 