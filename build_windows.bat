@echo off
REM Build script for Windows

echo Building Kart Racing Game for Windows...

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Create the executable using the spec file
pyinstaller KartRacing.spec

echo Build complete! Executable created in dist/ folder
echo Run with: dist\KartRacing.exe
pause