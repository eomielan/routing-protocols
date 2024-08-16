#!/bin/bash

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Virtual environment is activated."
    
    # Install package from requirements.txt
    if [[ -f "requirements.txt" ]]; then
        echo "Installing packages from requirements.txt..."
        pip install -r requirements.txt
        echo "Packages installed successfully."
    else
        echo "requirements.txt not found."
    fi
else
    echo "Virtual environment is not activated."
fi
