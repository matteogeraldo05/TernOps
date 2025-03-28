#!/bin/bash
echo "Building the Python executable..."

# Ensure pyinstaller is installed
if ! command -v pyinstaller &> /dev/null
then
    echo "pyinstaller not found. Installing..."
    pip install pyinstaller
fi

# Create the executable
pyinstaller --onefile src/gui.py --name CelebBioApp --icon src/images/icon.ico

echo "Build complete. Executable is located in the 'dist' directory."
