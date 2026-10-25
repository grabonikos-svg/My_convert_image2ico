@echo off
setlocal EnableExtensions
chcp 65001 >nul

set "APP_NAME=My_convert_image2ico"
set "SOURCE=%~dp0dist\main.exe"
set "INSTALL_DIR=%LOCALAPPDATA%\%APP_NAME%"
set "TARGET=%INSTALL_DIR%\%APP_NAME%.exe"

echo Εγκατάσταση %APP_NAME%...
echo.

if not exist "%SOURCE%" (
    echo Δεν βρέθηκε το εκτελέσιμο:
    echo %SOURCE%
    echo.
    echo Βεβαιώσου ότι υπάρχει ο φάκελος dist με το main.exe.
    pause
    exit /b 1
)

if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy /Y "%SOURCE%" "%TARGET%" >nul
if errorlevel 1 (
    echo Η αντιγραφή απέτυχε.
    echo Κλείσε την εφαρμογή αν είναι ανοιχτή και ξανατρέξε την εγκατάσταση.
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$shell = New-Object -ComObject WScript.Shell; $paths = @((Join-Path ([Environment]::GetFolderPath('Desktop')) ($env:APP_NAME + '.lnk')), (Join-Path ([Environment]::GetFolderPath('Programs')) ($env:APP_NAME + '.lnk'))); foreach ($path in $paths) { $shortcut = $shell.CreateShortcut($path); $shortcut.TargetPath = $env:TARGET; $shortcut.WorkingDirectory = $env:INSTALL_DIR; $shortcut.IconLocation = ($env:TARGET + ',0'); $shortcut.Description = 'Μετατροπή PNG σε εικονίδιο'; $shortcut.Save() }"
if errorlevel 1 (
    echo Η εφαρμογή αντιγράφηκε, αλλά απέτυχε η δημιουργία συντόμευσης.
    pause
    exit /b 1
)

echo Η εγκατάσταση ολοκληρώθηκε.
echo.
echo Πρόγραμμα: %TARGET%
echo Συντόμευση στην επιφάνεια εργασίας και στο μενού Έναρξη.
echo.
pause
endlocal