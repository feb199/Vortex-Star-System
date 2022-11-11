import os, sys, json, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pathlib import Path

from utils.console import bcolors

from classes.menu import Main, Menu, OptionItem
from classes.ship import NormalShip, Ship

from game.mainGame import game as mainGame
from game.mainStory import story as mainStory


shipTypes = {
    "normal": NormalShip
}

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


saveNames = []

savePath = Path(settings["savePath"])
if savePath.is_dir():
    saveNames = [f for f in os.listdir(savePath) if os.path.isfile(os.path.join(savePath, f))]
else:
    ifError = True
    print(f"\n\n{bcolors.WARNING}WARNING: Save Path: '{savePath}' dosent exist\nFalling back to default save path: '{os.path.abspath(defaultSavePath)}'{bcolors.ENDC}")
    savePath = defaultSavePath
    if savePath.is_dir():
        saveNames = [f for f in os.listdir(savePath) if os.path.isfile(os.path.join(savePath, f))]
    else:
        os.mkdir(savePath)


if ifError:
    print("\nPress Enter to continue")
    keyboard.wait("enter")


def startup():
    saves = []
    
    for saveName in saveNames:
        savePath = os.path.join(settings["savePath"], saveName)
        savePath = Path(savePath)
        
        if savePath.is_file():
            saveShipJSON = None
            with open(savePath, "r") as openfile:
                saveShipJSON = json.load(openfile)
            
            if saveShipJSON is not None:
                saveShip = shipTypes[saveShipJSON["type"]](saveShipJSON["name"], True)
                if saveShip is not None and saveShip:
                    saveShip.shipName = saveShipJSON["shipName"]
                    saveShip.load()
                    saves.append(saveShip)
    
    main = Main("Vortex Star System: Main Menu", [
        Menu("New",
            OptionItem("Ship Selection", [
                NormalShip("Organism Space Ship")
            ], "new")
        ),
        Menu("Load",  OptionItem("Select Save", saves, "load"))
    ], "                                      ")
    
    return main

def menu():
    main = startup()

    mainMenu(main)

def mainMenu(main, repeat = False, incorrect = ""):
    result = main.onExecute()
    
    if result[0]:
        if result[1] == "new":
            ship = result[2]
            ship.save()
            Ship.player = ship
            mainStory()
            mainGame()
        elif result[1] == "load":
            ship = result[2]
            ship.load()
            Ship.player = ship
            mainGame()



if __name__ == "__main__":
    menu()