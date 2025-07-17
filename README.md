# Horizontal Vertical Wallpaper Shuffler for Windows

A Python script that automatically sets two different wallpapers — one for a horizontal (landscape) primary monitor and one for a vertical (portrait) secondary monitor — and changes them on a timer.

## Features

- Supports one horizontal + one vertical monitor setup
- Pulls images from separate folders (One for landscape wallpapers, and another for portrati)
- Combines them into a single wallpaper that spans both screens
- Applies the wallpaper in **Span mode** to  avoid tiling and flickering
- Updates automatically at a defined interval (e.g. every 30 minutes)
- Designed to run silently in the background on startup

## Folder Structure

Make sure these two folders exist and contain at least one image each
All images should be JPG or PNG format
16:9 for landscape (ideally)
9:16 for portrait (ideally)

## Requirements

Install dependencies:
'''bash
pip install --user pillow screeninfo pywin32

## Usage

Edit the config section of the script:
  Paths for each respective folder
  Shuffle interval in seconds
Run "python wallpaper_manager.py" in corresponding directory in command line

## Run on Startup (optional)
1. Rename script to wallpaper_manager.pyw
2. Open task scheduler
3. Create new task
   -Trigger at log on
   -Action: Start a program
     -Program: pythonw.exe
     -Arguments: "C:\Path\To\wallpaper_changer.pyw"
  -Enable "Run with highest privileges"

### Alternative
1. Windows Key + R to open run
2. Enter "shell:startup"
3. Enter a shortcut to the program (optimal) or the program itself
