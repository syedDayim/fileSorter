#!/usr/bin/env python3
"""
Build script for creating executable file
Run this script to build the executable: python build_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main build function"""
    print("🚀 Building Advanced File Sorter Executable")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✅ PyInstaller version: {PyInstaller.__version__}")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        if not run_command("pip install pyinstaller", "Installing PyInstaller"):
            return False
    
    # Clean previous builds
    if os.path.exists("dist"):
        print("🧹 Cleaning previous builds...")
        shutil.rmtree("dist")
    
    if os.path.exists("build"):
        print("🧹 Cleaning build directory...")
        shutil.rmtree("build")
    
    # Create the executable
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window (GUI app)
        "--name=AdvancedFileSorter",
        "--icon=icon.ico",  # Add icon if you have one
        "--add-data=file_sorter_settings.json;.",  # Include settings file
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.messagebox",
        "--hidden-import=tkinter.scrolledtext",
        "fileSorter.py"
    ]
    
    # Remove icon parameter if no icon file exists
    if not os.path.exists("icon.ico"):
        pyinstaller_cmd.remove("--icon=icon.ico")
    
    # Remove settings file parameter if it doesn't exist
    if not os.path.exists("file_sorter_settings.json"):
        pyinstaller_cmd.remove("--add-data=file_sorter_settings.json;.")
    
    command = " ".join(pyinstaller_cmd)
    
    if not run_command(command, "Building executable"):
        return False
    
    # Check if executable was created
    exe_path = Path("dist/AdvancedFileSorter.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Executable created successfully!")
        print(f"📁 Location: {exe_path.absolute()}")
        print(f"📊 Size: {size_mb:.1f} MB")
        
        # Create a simple README for the release
        readme_content = """# Advanced File Sorter - Executable

## How to Use
1. Download `AdvancedFileSorter.exe`
2. Double-click to run
3. Select a directory to sort
4. Click "Preview Files" to see what will be sorted
5. Click "Sort Files" to organize your files

## Features
- Automatically sorts files into categories (Documents, Images, Videos, Music, etc.)
- Preview mode to see what will be moved
- Undo functionality
- Customizable file type mappings
- Smart duplicate handling

## System Requirements
- Windows 10/11
- No additional software required

## Developer
Created by Syed Dayim
- Email: dayim1277@gmail.com
- GitHub: github.com/syedDayim
"""
        
        with open("dist/README.txt", "w") as f:
            f.write(readme_content)
        
        print("📝 Created README.txt in dist folder")
        print("\n🎉 Build completed successfully!")
        print("📦 Your executable is ready in the 'dist' folder")
        
    else:
        print("❌ Executable was not created")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
