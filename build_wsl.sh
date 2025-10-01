#!/bin/bash
# Build script for Linux using WSL from Windows

echo "Building Kart Racing Game for Linux using WSL..."

# Update package manager and install Python dependencies
sudo apt update
sudo apt install python3-pip python3-dev -y

# Install required Python packages
pip3 install pygame pyinstaller

# Build the executable
pyinstaller --onefile --windowed --name="KartRacing-Linux" main.py

echo "Build complete! Linux executable created in dist/ folder"
echo "The executable will work on Linux systems"