import os
import random
import time
import ctypes
from PIL import Image
from screeninfo import get_monitors
import win32api
import win32con

# ENTER CONFIG DETAILS HERE
LANDSCAPE_FOLDER = r"C:\Users\
PORTRAIT_FOLDER = r"C:\Users\
#in seconds, 30 minute intervals (Adjustable)
SHUFFLE_INTERVAL = 1800

#Find monitors
def get_monitors_sorted():
    monitors = get_monitors()
    return sorted(monitors, key=lambda m: m.x)
# Get image files from respective folders
def get_images(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
#Combine landscape and portrait image into one spanning wallpaper
def create_combined_wallpaper(landscape_path, portrait_path, monitors):
    # Determine virtual desktop bounds
    min_x = min(m.x for m in monitors)
    min_y = min(m.y for m in monitors)
    max_x = max(m.x + m.width for m in monitors)
    max_y = max(m.y + m.height for m in monitors)

    total_width = max_x - min_x
    total_height = max_y - min_y

    combined = Image.new("RGB", (total_width, total_height), color=(0, 0, 0))

    image_paths = [landscape_path, portrait_path]

    for i, monitor in enumerate(monitors):
        img = Image.open(image_paths[i])
        img_ratio = img.width / img.height
        mon_ratio = monitor.width / monitor.height

        if img_ratio > mon_ratio:
            new_height = monitor.height
            new_width = int(img_ratio * new_height)
        else:
            new_width = monitor.width
            new_height = int(new_width / img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Calculate paste position
        paste_x = monitor.x - min_x + (monitor.width - new_width) // 2
        paste_y = monitor.y - min_y + (monitor.height - new_height) // 2

        combined.paste(img, (paste_x, paste_y))

    output_path = os.path.join(os.getenv('TEMP'), "dual_wallpaper.bmp")
    combined.save(output_path, "BMP")
    return output_path


#Set wallpaper with system api (win32api)
def set_wallpaper(path):
    import win32api, win32con, pythoncom
    from win32com.shell import shell, shellcon

    #Use span mode to avoid tiling
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                r"Control Panel\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "22")  
    win32api.RegCloseKey(key)

    # Set wallpaper
    pythoncom.CoInitialize()
    iad = pythoncom.CoCreateInstance(
        shell.CLSID_ActiveDesktop,
        None,
        pythoncom.CLSCTX_INPROC_SERVER,
        shell.IID_IActiveDesktop
    )
    iad.SetWallpaper(path, 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)


#Main loop with error checking
def main():
    landscape_images = get_images(LANDSCAPE_FOLDER)
    portrait_images = get_images(PORTRAIT_FOLDER)
    #If folder empty or set incorrectly
    if not landscape_images or not portrait_images:
        print("Error: One or both wallpaper folders are empty.")
        return
    #If less than two monitors
    monitors = get_monitors_sorted()
    if len(monitors) < 2:
        print("Error: At least two monitors required.")
        return
    #Can get rid of print statements if unwanted
    print("Starting wallpaper shuffle...")
    while True:
        landscape = random.choice(landscape_images)
        portrait = random.choice(portrait_images)
        combined_path = create_combined_wallpaper(landscape, portrait, monitors)
        set_wallpaper(combined_path)
        print(f"Wallpaper updated at {time.strftime('%H:%M:%S')}")
        time.sleep(SHUFFLE_INTERVAL)

if __name__ == "__main__":
    main()
