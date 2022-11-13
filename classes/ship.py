import os, sys, json, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from classes.menu import InputItem
from classes.crew import NormalPerson, CaptainPerson
from classes.system import Hull, Shield, Reactor, Weapon

from utils.console import clear, bcolors
from utils.json import toJSON

from random import choice, randint
from pathlib import Path

defaultCrew = [ NormalPerson("Feb199"), NormalPerson("Alia"), NormalPerson("Daniel"), NormalPerson("Georgia") ]
defaultSystem = [ Hull(), Shield(), Reactor(), Weapon() ]
systemTypes = {
    "hull": Hull,
    "shield": Shield,
    "reactor": Reactor,
    "weapon": Weapon
}

idsJSON = {
    "playerShip": []
}

idsPath = Path("ids.json")
if idsPath.is_file():
    with open(idsPath, "r") as openfile:
        idsJSON = json.load(openfile)
else:
    with open(idsPath, "w") as outfile:
        json.dump(idsJSON, outfile)


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

class Ship:
    
    player = None
    
    def __init__(self, name, player, shipType, displayName = False, level = 1):
        self.type = shipType
        self.player = player
        self.name = name
        self.level = level
        self.shipName = None
        self.displayName = self.name
        
        if displayName:
            self.displayName = self.shipName
        
        self.captain = None
        self.crew = []
        self.crew = defaultCrew
        self.systems = []
        self.systems = list(defaultSystem)
    
    def onRender(self):
        clear()
        dashes = "------------------------------------------------"
        print(f"\n\n\n{dashes} {self.name} {dashes}")
    
    def onInput(self):
        if self.shipName == None:
            resultShipName = InputItem("Ship Name").onExecute()
            if resultShipName[0]:
                self.shipName = resultShipName[1]
            else:
                self.shipName = self.name
            
            clear()
            self.onRender()
        
        if self.captain == None:
            resultCaptainName = InputItem("Captain Name").onExecute()
            if resultCaptainName[0]:
                isDefault = None
                for person in defaultCrew:
                    if person.name.lower() == resultCaptainName[1].lower():
                        isDefault = person
                
                if isDefault is not None:
                    self.captain = CaptainPerson(isDefault.name, isDefault.id)
                    
                    newCrew = []
                    for person in self.crew:
                        if person.id != isDefault.id:
                            newCrew.append(person)
                    
                    self.crew = newCrew
                else:
                    self.captain = CaptainPerson(resultCaptainName[1])
            else:
                captainChoice = choice(defaultCrew)
                self.captain = CaptainPerson(captainChoice.name, captainChoice.id)
                
                newCrew = []
                for person in self.crew:
                    if person.id != captainChoice.id:
                        newCrew.append(person)
                
                self.crew = newCrew
        
        self.displayName = self.shipName
        return self
    
    def onExecute(self):
        self.onRender()
        return self.onInput()

class PlayerShip(Ship):
    
    def __init__(self, fname, fshipType, fdisplayName = False, flevel = 1):
        super().__init__(fname, True, fshipType, fdisplayName, flevel)
        newID = randint(0, 100000)
        while newID in idsJSON["playerShip"]:
            newID = randint(0, 100000)
        
        self.id = newID
        
        idsJSON["playerShip"].append(self.id)
        with open("ids.json", "w") as outfile:
            json.dump(idsJSON, outfile)
        
        self.specialEvents = {}
    
    
    # self.id = newID
    
    # self.type = shipType
    # self.player = player
    # self.name = name
    # self.level = level
    # self.shipName = None
    # self.displayName = self.name
    
    # if displayName:
    #     self.displayName = self.shipName
    
    # self.captain = None
    # self.crew = []
    # self.crew = defaultCrew
    # self.systems = []
    # self.systems = list(defaultSystem)
    
    def load(self):
        with open(os.path.join(savePath, f"{self.shipName}.json"), "r") as openfile:
            shipJSON = json.load(openfile)
            
            self.id = shipJSON["id"]
            
            self.type = shipJSON["type"]
            self.player = shipJSON["player"]
            self.level = shipJSON["level"]
            
            self.specialEvents = shipJSON["specialEvents"]
            
            self.name = shipJSON["name"]
            self.shipName = shipJSON["shipName"]
            self.displayName = self.shipName
            self.captain = CaptainPerson(shipJSON["captain"]["name"], shipJSON["captain"]["id"])
            
            self.crew = []
            for person in shipJSON["crew"]:
                if person["id"] <= 3:
                    self.crew.append(defaultCrew[person["id"]])
                else:
                    self.crew.append(NormalPerson(person["name"], person["id"]))
            
            self.systems.clear()
            for system in shipJSON["systems"]:
                self.systems.append(systemTypes[system["type"]](system["name"]).load(system))
    
    def save(self):
        with open(os.path.join(savePath, f"{self.shipName}.json"), "w") as outfile:
            outfile.write(toJSON(self))

class NormalShip(PlayerShip):
    
    def __init__(self, fname, fdisplayName = False, flevel = 1):
        super().__init__(fname, "normal", fdisplayName, flevel)