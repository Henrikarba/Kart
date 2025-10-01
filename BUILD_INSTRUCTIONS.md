# Kart Racing Game Build Instructions

## Prerequisites

- Python 3.7 or higher
- pygame library
- pyinstaller library

## Building for Windows (.exe)

### Method 1: Using the batch script (Recommended)

1. Double-click `build_windows.bat`
2. Wait for the build to complete
3. Find your executable in `dist/KartRacing.exe`

### Method 2: Manual command line

```cmd
pip install pyinstaller
pyinstaller KartRacing.spec
```

## Building for Linux

### Method 1: Using the shell script (Recommended)

1. Make the script executable: `chmod +x build_linux.sh`
2. Run the script: `./build_linux.sh`
3. Find your executable in `dist/KartRacing`

### Method 2: Manual command line

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="KartRacing" main.py
```

## Building for macOS

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="KartRacing" main.py
```

## Distribution

### Windows

- The executable `KartRacing.exe` is standalone and can be run on any Windows machine
- No Python installation required on target machine
- The file will be quite large (50-100MB) as it includes Python and pygame

### Linux

- The executable `KartRacing` will only run on Linux systems with similar architecture
- No Python installation required on target machine
- May need to make executable: `chmod +x KartRacing`

### Notes

- The first run may be slower as PyInstaller unpacks the application
- Antivirus software might flag the executable - this is normal for PyInstaller builds
- For smaller file sizes, consider using `--onedir` instead of `--onefile` but this creates a folder with multiple files

## Troubleshooting

### Common Issues:

1. **Import errors**: Make sure all modules are listed in the spec file
2. **Missing pygame**: Ensure pygame is installed in the same Python environment
3. **Permission errors**: Run command prompt/terminal as administrator if needed
4. **Large file size**: This is normal - PyInstaller bundles Python and all dependencies

### Testing the Build:

After building, test the executable on a clean machine without Python to ensure it works standalone.
