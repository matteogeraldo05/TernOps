@echo off
echo Building the Python executable...

:: Ensure pyinstaller is installed
where pyinstaller >nul 2>nul
if errorlevel 1 (
    echo pyinstaller not found. Installing...
    pip install pyinstaller
)

:: Create the executable
pyinstaller --onefile src\gui.py --name CelebBioApp  --icon src/images/icon.ico

echo Build complete. Executable is located in the 'dist' directory.
pause
