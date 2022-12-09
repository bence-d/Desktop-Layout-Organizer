$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("C:\Users\hvb63\OneDrive\Desktop\Schule.lnk")
$Shortcut.TargetPath = "C:\Users\hvb63\OneDrive\Desktop\Schule"
$Shortcut.Save()