#!/bin/bash
# Build script for Linux

echo "Building Kart Racing Game for Linux..."

# Install PyInstaller if not already installed
pip install pyinstaller

# Create the executable
pyinstaller --onefile --windowed --name="KartRacing" main.py

echo "Build complete! Executable created in dist/ folder"
echo "Run with: ./dist/KartRacing"