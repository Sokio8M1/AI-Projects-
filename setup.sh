# For those viewing this script...This is a sh script used to setup the voice assistant project in os like macOS , linux.

#!/bin/bash
echo "=============================="
echo "   Voice Assistant Setup"
echo "=============================="

# Step 1: Handle reset
if [ "$1" == "reset" ]; then
    echo "Reset mode: deleting old virtual environment..."
    rm -rf venv
fi

# Step 2: Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Step 3: Activate virtual environment
source venv/bin/activate

# Step 4: Upgrade pip
python3 -m pip install --upgrade pip

# Step 5: Install from requirements2.txt
if [ -f "requirements2.txt" ]; then
    echo "Installing dependencies from requirements2.txt..."
    pip install -r requirements2.txt
else
    echo "requirements2.txt not found! Please create it in this folder."
    exit 1
fi

# Step 6: Run assistant
echo "Starting your assistant..."
python3 assistant.py
