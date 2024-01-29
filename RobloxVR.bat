@echo off
set "steamappsDir=C:\Program Files (x86)\Steam\steamapps"

:menu
cls       
echo Fuck roblox oppening SteamVR                                                                                    

echo Options:
echo 1 - Rename SteamVR folder to "SteamVR1"
echo 2 - Restore folder name.
echo 3 - Quit

set /p option="Enter your choice: "

if "%option%"=="1" (
    echo Renaming SteamVR folder to "SteamVR1"...
    rename "%steamappsDir%\common\SteamVR" "SteamVR1"
    echo Folder renamed to "SteamVR1" successfully.
    pause
    goto menu
)

if "%option%"=="2" (
    echo Restoring folder name...
    rename "%steamappsDir%\common\SteamVR1" "SteamVR"
    echo Folder name restored successfully.
    pause
    goto menu
)

if "%option%"=="3" (
    exit /b
)

echo Invalid option. Please choose a valid option.
pause
goto menu