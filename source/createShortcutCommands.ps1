#PowerShell Script used for creating a Shortcut

#targetfile  $args[1]
#shortcutPath $args[0]
if ((Test-Path $args[1]) -eq "True") {

    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($args[0])
    $Shortcut.TargetPath = $args[1]
    $Shortcut.Save()
}
else {
    exit 1
}

#$? returns True when last operation succeeded
#return $?
