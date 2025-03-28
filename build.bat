@echo off
echo Building the Python executable...
:: Create the executable
pyinstaller --onefile src\gui.py --name CelebBioApp  --icon src/images/icon.ico

echo Build complete. Executable is located in the 'dist' directory.
pause
