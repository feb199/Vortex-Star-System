import sys
import subprocess
import pkg_resources

required = {'keyboard'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


import os, sys, json, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.console import bcolors

from menu.mainMenu import menu

from pathlib import Path



defaultSavePath = Path("saves")
defaultSettings = {
    "savePath": os.path.abspath(defaultSavePath)
}
settings = {
    "savePath": os.path.abspath(defaultSavePath)
}

ifError = False

settingsPath = Path("settings.json")
if settingsPath.is_file():
    with open(settingsPath, "r") as openfile:
        try:
            settings = json.load(openfile)
        except:
            ifError = True
            print(f"\n\n{bcolors.WARNING}WARNING: Settings Path: '{settingsPath}' corrupted\nFalling back to default settings{bcolors.ENDC}")
            settings = defaultSettings
    
    if "savePath" not in settings:
        settings = defaultSettings
        with open(settingsPath, "w") as outfile:
            json.dump(defaultSettings, outfile)
else:
    with open(settingsPath, "w") as outfile:
        json.dump(defaultSettings, outfile)


savePath = Path(settings["savePath"])
if not savePath.is_dir():
    ifError = True
    print(f"\n\n{bcolors.WARNING}WARNING: Save Path: '{savePath}' dosent exist\nFalling back to default save path: '{os.path.abspath(defaultSavePath)}'{bcolors.ENDC}")
    savePath = defaultSavePath
    if not savePath.is_dir():
        os.mkdir(savePath)


if ifError:
    print("\nPress Enter to continue")
    keyboard.wait("enter")



def main():
    menu()

if __name__ == "__main__":
    # print(f"Test")
    # print(f"{bcolors.GREY}Test{bcolors.ENDC}")
    main()
    keyboard.wait("enter")

