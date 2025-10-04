@echo off
echo Building Advanced File Sorter...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Install PyInstaller if not already installed
echo Installing/updating PyInstaller...
pip install pyinstaller

REM Run the build script
echo.
echo Starting build process...
python build_exe.py

echo.
echo Build process completed!
echo Check the 'dist' folder for your executable.
pause
