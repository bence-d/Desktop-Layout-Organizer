%ECHO OFF

set preset=default

if exist "C:\Users\%username%\AppData\Local\DLO\" if exist "C:\Users\%username%\AppData\Local\DLO\Presets" if exist "C:\Users\%username%\AppData\Local\DLO\Repository" (
	echo "[DLO] -> Found directory tree..."
	CALL :main
	exit /B
)

mkdir C:\Users\%username%\AppData\Local\DLO\
mkdir C:\Users\%username%\AppData\Local\DLO\Presets\
mkdir C:\Users\%username%\AppData\Local\DLO\Repository\

pause

:main
cls
echo ================== DLO ==================
echo  [1]: Create New Preset
echo  [2]: Save current Preset
echo  [3]: Load current Preset
echo  [4]: Change Preset
echo  [5]: Delete Preset
echo  [6]: Exit
echo =========================================
echo  Current Preset: %preset%
echo =========================================

set /p userinput="[command]: "

if "%userinput%"=="1" (
	CALL :createpreset
) else if "%userinput%"=="2" (
	CALL :savepreset
) else if "%userinput%"=="3" (
	CALL :loadpreset
) else if "%userinput%"=="4" (
	CALL :changepreset
) else if "%userinput%"=="5" (
	CALL :deletepreset
) else if "%userinput%" == "6" (
	exit /B
) else (
	echo "[DLO] ERROR: Unknown command"
)
exit /B

:createpreset
set /p "preset=Preset name: "
reg export HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\Shell\Bags\1\Desktop "C:\Users\%username%\AppData\Local\DLO\Presets\%preset%.reg"
pause
CALL :main
exit /B

:changepreset
cd C:\Users\%username%\AppData\Local\DLO\Presets\
dir /B
set /p "preset=Preset name: "
pause
CALL :main
exit /B

:savepreset
echo "[DLO] -> Please manually refresh the desktop..."
pause
del "C:\Users\%username%\AppData\Local\DLO\Presets\%preset%.reg"
reg export HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\Shell\Bags\1\Desktop "C:\Users\%username%\AppData\Local\DLO\Presets\%preset%.reg"
CALL :main
exit /B

:loadpreset
reg import "C:\Users\%username%\AppData\Local\DLO\Presets\%preset%.reg"
taskkill /f /im explorer.exe
:: timeout /t 1
start explorer
pause
CALL :main
exit /B

:deletepreset
cd C:\Users\%username%\AppData\Local\DLO\Presets\
dir /B
set /p "userinput=Preset name: "
del "C:\Users\%username%\AppData\Local\DLO\Presets\%userinput%.reg"
CALL :main
exit /B