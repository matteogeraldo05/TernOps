#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Step 1: Check if Python3 is installed
if ! command -v python &>/dev/null; then
    echo "Python3 is required but not installed. Please install Python3."
    exit 1
fi

# Step 2: Check if pip is installed
if ! command -v pip &>/dev/null; then
    echo "pip is required but not installed. Please install pip."
    exit 1
fi

# Step 3: Set up the virtual environment
echo "Setting up virtual environment..."
python -m venv venv

# Step 4: Activate the virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Step 5: Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Step 6: Run the GUI application
echo "Running the application..."
python src/gui.py

# Step 7: Deactivate the virtual environment after running
deactivate