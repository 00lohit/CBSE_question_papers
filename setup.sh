#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment based on the operating system
if [[ "$OSTYPE" == "darwin"* || "$OSTYPE" == "linux-gnu" ]]; then
    source venv/bin/activate
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    .\venv\Scripts\activate
else
    echo "Unsupported operating system"
    exit 1
fi

# Install requirements
pip install -r requirements.txt

# Display a message to the user to remind them to deactivate after use
echo "Activating the virtual environment. Run 'deactivate' to exit."
