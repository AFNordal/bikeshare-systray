@echo off
REM Get the current working directory
set "CURR_DIR=%cd%"

REM Create bikeshare-systray-launcher.bat with the current directory
echo @echo off > bikeshare-systray-launcher.bat
echo cd /d "%CURR_DIR%" >> bikeshare-systray-launcher.bat
echo python main.py >> bikeshare-systray-launcher.bat

REM Get the user's Startup folder path
for /f "tokens=2,*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Startup"') do set "STARTUP=%%b"

REM Move the launcher to the Startup folder
move /Y bikeshare-systray-launcher.bat "%STARTUP%"

start "" explorer "%STARTUP%"

echo Launcher created and moved to Startup folder.
pause