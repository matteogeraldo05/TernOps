#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Check if Python3 is installed, if not, install it
if ! command -v python &>/dev/null; then
    echo "Python3 is required but not installed. Installing Python3..."
    # Install Python based on the system
    # Check for Linux system
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y python3
    # Check for macOS system
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install python
    # Check for Windows system
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" ]]; then
        echo "Please install Python manually on Windows."
        exit 1
    # Check for any other system
    else
        echo "Unsupported OS for automatic Python installation. Please install Python manually."
        exit 1
    fi
fi

# Step 2: Check if pip is installed, if not, install it
if ! command -v pip &>/dev/null; then
    echo "pip is required but not installed. Installing pip..."
    python -m ensurepip --upgrade
    exit 1
fi

# Step 3: Check if pip needs to be upgraded, if so, upgrade it
current_pip_version=$(pip --version | awk '{print $2}')
latest_pip_version=$(python -m pip install --upgrade pip | tail -n 1 | awk '{print $3}')

if [[ "$current_pip_version" != "$latest_pip_version" ]]; then
    echo "Upgrading pip from version $current_pip_version to $latest_pip_version..."
    python -m pip install --upgrade pip
else
    echo "pip is already up-to-date."
fi

# Step 4: Set up the virtual environment
echo "Setting up virtual environment..."
python -m venv venv

# Step 5: Activate the virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Step 6: Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 7: Run the GUI application
echo "Running the application..."
python src/gui.py

# Step 8: Deactivate the virtual environment after running
deactivate