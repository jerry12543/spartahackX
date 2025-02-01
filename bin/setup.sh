#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Create a virtual environment named '.venv'
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip to the latest version
pip install --upgrade pip

# Install dependencies from requirements.txt
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
    echo "Dependencies installed successfully."
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Deactivate the virtual environment
deactivate

echo "Virtual environment setup complete."