import os, sys, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random import randint, choice
from pathlib import Path
from time import sleep

from utils.console import clear, bcolors
from utils.readWrite import readTxtFile

from classes.ship import Ship
from classes.menu import OptionItem, TextItem

from game.mainStory import desertPlanetEvent, metalPlanetEvent, greenPlanetEvent, oceanPlanetEvent, icyPlanetEvent


defaultPlanetNames = readTxtFile(Path("planetNames.txt"))
planetNames = list(defaultPlanetNames)

defaultStarNames = readTxtFile(Path("starNames.txt"))
starNames = list(defaultStarNames)

defaultMoonNames = readTxtFile(Path("moonNames.txt"))
moonNames = list(defaultMoonNames)


planetTypes = []


class SolarSystem:
    
    def __init__(self, numSuns = None, numPlanets = None, forceSun = False):
        self.forceSun = forceSun
        
        self.numSuns = numSuns
        if self.numSuns is None:
            chance = randint(0, 6)
            if forceSun:
                chance = 0
            
            if chance == 1:
                self.numSuns = 0
            else:
                chance2 = randint(0, 4)
                if chance2 == 1:
                    chance3 = randint(0, 4)
                    if chance3 == 1:
                        self.numSuns = 3
                    else:
                        self.numSuns = 2
                else:
                    self.numSuns = 1
        
        if self.forceSun and self.numSuns == 0:
            self.numSuns = 1
        
        
        self.numPlanets = numPlanets
        if self.numPlanets is None:
            self.numPlanets = randint(2, 5)
        
        
        self.planets = []
        if self.numPlanets > 0:
            for i in range(self.numPlanets):
                self.planets.append(choice(planetTypes)(self))
        
        self.suns = []
        if self.numSuns > 0:
            for i in range(self.numSuns):
                self.suns.append(Sun(self))
        
        self.structures = []
        if self.numSuns <= 0:
            self.structures.append(Wormhole(self))
        
        self.exploreOptions = []
        self.exploreOptionsItem = None
        self.placeOptionsItems = {}
    
    def onRenderArt(self, isPlace = False):
        if isPlace:
            print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█████████████████████████████████████████▀▀▀▀▀██████████████████████████████████
███████████████████████████████████████▀░░░░░░░▀████████████████████████████████
██████████████████████████████████████▌░░░░░░░░░████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
████████████████████████████████████████▄▄░░,▄▄█████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
        else:
            print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█▀▀▒▒▒▒▀▀▀██████████████████████████████████████████████████████████████████████
▒▒▒▒▒▒▒▒▒▒▒▒▀███████████████████████████████████████████████████████████████████
▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████████████████████████████████████████████████████████
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀█████████████████████████▀▀▀▀▀████████▀░▒▒▒░░▀██████████████████
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████▀████▀▀████▀░░░░░░░▀████░▒▒▒▒▒▒▒▒▒░██████████▒╢╢╢▒██
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███░░██▒▒██▒▒▒██▒▒▒▒██▌░░░░░░░░░████░▒▒▒▒▒▒▒▒▒▒▐██░░░░██╢╢╢╢╢╢▒█
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████▄████▄▄████░░░░░░░░░████░░░▒▒▒▒▒▒▒▄███▄░░▄███▒╢╢╢▒██
▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐████████████████████████▄▄░░,▄▄███████▄░▒▒▒▒░▄██████████████████
▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████████████████████████████████████████████████████████
▒▒▒▒▒▒▒▒▒▒▒▒▄███████████████████████████████████████████████████████████████████
▒▒▒▒▒▒▒▒▒▄██████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self, displayTxt = None):
        clear()
        dashes = "--------------------------------------------"
        
        if displayTxt is None:
            self.onRenderArt()
            print(f"\n\n\n{dashes} Level {Ship.player.level} System {dashes}")
        else:
            self.onRenderArt(True)
            print(f"\n\n\n{dashes} {displayTxt} {dashes}")
    
    def onInput(self, skipTo = None):
        options = {
            "Planets": self.planets,
            "Structures": self.structures,
            "Suns": self.suns
        }
        if skipTo is not None and skipTo in options:            
            if skipTo not in self.placeOptionsItems and len(options[skipTo]) > 0:
                placeOptionsItem = OptionItem(f"Explore {skipTo}", options[skipTo], "placeResult")
                placeOptionsItem.returnTxt = "To return to explore options press: Backspace or Space"
                self.placeOptionsItems[skipTo] = placeOptionsItem
            placeResult = self.placeOptionsItems[skipTo].onExecute(self, skipTo)
            
            print(placeResult)
            
            return [True, None, placeResult]
        else:
            if len(self.exploreOptions) <= 0:
                if self.numPlanets > 0:
                    self.exploreOptions.append(TextItem([*options.keys()][0]))
                
                if len(self.structures) > 0:
                    self.exploreOptions.append(TextItem([*options.keys()][1]))
                
                if self.numSuns > 0:
                    self.exploreOptions.append(TextItem([*options.keys()][2]))
            
            if self.exploreOptionsItem is None:
                self.exploreOptionsItem = OptionItem("Explore Options", self.exploreOptions, "exploreOption")
                self.exploreOptionsItem.cancelKeys = [ "esc" ]
                self.exploreOptionsItem.returnTxt = "To quit the game press: ESC"
            exploreResult = self.exploreOptionsItem.onExecute(self)
            
            # Planets[True, 'exploreOption', [True, None, 'Printed']]
            if not exploreResult[0]: return exploreResult
            if not exploreResult[2][0]: return exploreResult
            
            exploreOption = exploreResult[2][2]
            
            if exploreOption.content in options:
                clear()
                self.onRender(exploreOption.content)
                
                if exploreOption.content not in self.placeOptionsItems:
                    placeOptionsItem = OptionItem(f"Explore {exploreOption.content}", options[exploreOption.content], "placeResult")
                    placeOptionsItem.returnTxt = "To return to explore options press: Backspace or Space"
                    self.placeOptionsItems[exploreOption.content] = placeOptionsItem
                placeResult = self.placeOptionsItems[exploreOption.content].onExecute(self, exploreOption.content)
                
                print(placeResult)
                
                return [True, None, placeResult]
            else:
                raise Exception(f"{bcolors.FAIL}'{exploreOption.content}' Some how not in 'options'{bcolors.ENDC}")
    
    def onExecute(self, skipTo = None):
        if Ship.player is None: return [ False, None, "No Player" ]
        
        self.onRender(skipTo)
        return self.onInput(skipTo)
    
    def onCancel(self, type):
        if type == "exploreOption":
            exit()
        elif type == "placeResult":
            return self.onExecute()

# Base Classes
class Planet:
    
    ids = 0
    
    def __init__(self, planetType, parent, numMoons = None, forceMoon = False):
        global planetNames
        
        Planet.ids += 1
        self.id = Planet.ids
        
        self.parent = parent
        
        self.type = planetType
        self.forceMoon = forceMoon
        
        self.numMoons = numMoons
        if self.numMoons is None:
            chance = randint(0, 2)
            if forceMoon:
                chance = 1
            
            if chance == 1:
                chance2 = randint(0, 3)
                if chance2 == 1:
                    chance3 = randint(0, 3)
                    if chance3 == 1:
                        self.numMoons = 3
                    else:
                        self.numMoons = 2
                else:
                    self.numMoons = 1
            else:
                self.numMoons = 0
        
        if self.forceMoon and self.numMoons == 0:
            self.numMoons = 1
        
        
        self.name = choice(planetNames)
        if len(starNames) <= 1:
            planetNames = list(defaultPlanetNames)
        else:
            planetNames.remove(self.name)
        
        self.displayName = f"{self.type} {self.name} Planet"
        
        self.moons = []
        if self.numMoons > 0:
            for i in range(self.numMoons):
                self.moons.append(Moon(self))
        
        self.moonsOptionsItem = None
    
    def onRenderArt(self):
        print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█████████████████████████████████████████▀▀▀▀▀██████████████████████████████████
███████████████████████████████████████▀░░░░░░░▀████████████████████████████████
██████████████████████████████████████▌░░░░░░░░░████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
████████████████████████████████████████▄▄░░,▄▄█████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self, displayTxt = None):
        clear()
        dashes = "--------------------------------------------"
        
        self.onRenderArt()
        print(f"\n\n\n{dashes} {self.displayName} Planet {dashes}")
    
    def onInput(self):
        if self.numMoons > 0:
            if self.moonsOptionsItem is None:
                self.moonsOptionsItem = OptionItem(f"Explore Moons", self.moons, "structureResult")
                self.moonsOptionsItem.returnTxt = "To return to explore options press: Backspace or Space"
            moonResult = self.moonsOptionsItem.onExecute(self)
            
            return [True, None, moonResult]
        return self.onCancel()
    
    def onSpecialEvent(self):
        pass
    
    def onExecute(self, passThrough = None, passThroughTxt = None):
        self.onSpecialEvent()
        self.onRender()
        return self.onInput()
    
    def onCancel(self, type = None):
        return self.parent.onExecute("Planets")

class Sun:
    
    ids = 0
    
    def __init__(self, parent):
        global starNames
        
        Sun.ids += 1
        self.id = Sun.ids
        
        self.parent = parent
        
        self.name = choice(starNames)
        if len(starNames) <= 1:
            starNames = list(defaultStarNames)
        else:
            starNames.remove(self.name)
        
        self.displayName = f"{self.name} Sun"
        
        self.structures = [ DysonSphere(self) ]
        self.structureOptionsItem = None
    
    def onRenderArt(self):
        print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█████████████████████████████████████████▀▀▀▀▀██████████████████████████████████
███████████████████████████████████████▀░░░░░░░▀████████████████████████████████
██████████████████████████████████████▌░░░░░░░░░████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
████████████████████████████████████████▄▄░░,▄▄█████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self, displayTxt = None):
        clear()
        dashes = "--------------------------------------------"
        
        self.onRenderArt()
        print(f"\n\n\n{dashes} {self.displayName} Sun {dashes}")
    
    def onInput(self):
        if self.structureOptionsItem is None:
            self.structureOptionsItem = OptionItem(f"Explore Structures", self.structures, "structureResult")
            self.structureOptionsItem.returnTxt = "To return to explore options press: Backspace or Space"
        structureResult = self.structureOptionsItem.onExecute(self, "Structures")
        
        if not structureResult[0]: return structureResult
        
        return [True, None, structureResult]
    
    def onExecute(self):
        self.onRender()
        return self.onInput()
    
    def onCancel(self, type = None):
        return self.parent.onExecute("Suns")

class Moon:
    
    ids = 0
    
    def __init__(self, parent):
        global moonNames
        
        Moon.ids += 1
        self.id = Moon.ids
        
        self.parent = parent
        
        self.name = choice(moonNames)
        if len(moonNames) <= 1:
            moonNames = list(defaultMoonNames)
        else:
            moonNames.remove(self.name)
        
        self.displayName = f"{self.name} Moon"
    
    def onRenderArt(self):
        print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█████████████████████████████████████████▀▀▀▀▀██████████████████████████████████
███████████████████████████████████████▀░░░░░░░▀████████████████████████████████
██████████████████████████████████████▌░░░░░░░░░████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
████████████████████████████████████████▄▄░░,▄▄█████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self, displayTxt = None):
        clear()
        dashes = "--------------------------------------------"
        
        self.onRenderArt()
        print(f"\n\n\n{dashes} {self.displayName} Moon {dashes}")
    
    def onInput(self):
        return self.onCancel()
    
    def onExecute(self):
        self.onRender()
        return self.onInput()

    def onCancel(self, type = None):
        return self.parent.onExecute()

class Structure:
    
    ids = 0
    
    def __init__(self, name, structureType, damaged = False, parent = None):
        Structure.ids += 1
        self.id = Structure.ids
        
        self.name = name
        self.type = structureType
        self.damaged = damaged
        
        self.parent = parent
        
        self.displayName = f"{self.name} {self.type}"
        if self.damaged:
            self.displayName = f"Damaged {self.name} {self.type}"
    
    def onRenderArt(self):
        print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
███████████████████████████████████████▀▀▀▀▀▀▀▀▀████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
███████████████████████████████████████░░░░░░░░░████████████████████████████████
███████████████████████████████████████▄▄▄▄▄▄▄▄▄████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self, displayTxt = None):
        clear()
        dashes = "--------------------------------------------"
        
        self.onRenderArt()
        print(f"\n\n\n{dashes} {self.displayName} Structure {dashes}")
    
    def onInput(self):
        return [ True, None, self ]
    
    def onExecute(self):
        self.onRender()
        return self.onInput()
    
    def onCancel(self, type = None):
        return self.parent.onExecute("Structures")




# Specific Classes
class IcyPlanet(Planet):
    
    def __init__(self, fparent, fnumMoons = None, fforceMoon = False):
        super().__init__("Icy", fparent,fnumMoons, fforceMoon)
    
    def onSpecialEvent(self):
        if self.type not in Ship.player.specialEvents:
            icyPlanetEvent().onExecute()
            Ship.player.specialEvents[self.type] = True
            Ship.player.save()
planetTypes.append(IcyPlanet)

class OceanPlanet(Planet):
    
    def __init__(self, fparent,fnumMoons = None, fforceMoon = False):
        super().__init__("Ocean", fparent,fnumMoons, fforceMoon)
    
    def onSpecialEvent(self):
        if self.type not in Ship.player.specialEvents:
            oceanPlanetEvent().onExecute()
            Ship.player.specialEvents[self.type] = True
            Ship.player.save()
planetTypes.append(OceanPlanet)

class GreenPlanet(Planet):
    
    def __init__(self, fparent,fnumMoons = None, fforceMoon = False):
        super().__init__("Green", fparent,fnumMoons, fforceMoon)
    
    def onSpecialEvent(self):
        if self.type not in Ship.player.specialEvents:
            greenPlanetEvent().onExecute()
            Ship.player.specialEvents[self.type] = True
            Ship.player.save()
planetTypes.append(GreenPlanet)

class MetalPlanet(Planet):
    
    def __init__(self, fparent,fnumMoons = None, fforceMoon = False):
        super().__init__("Metal", fparent,fnumMoons, fforceMoon)
    
    def onSpecialEvent(self):
        if self.type not in Ship.player.specialEvents:
            metalPlanetEvent().onExecute()
            Ship.player.specialEvents[self.type] = True
            Ship.player.save()
planetTypes.append(MetalPlanet)

class DesertPlanet(Planet):
    
    def __init__(self, fparent,fnumMoons = None, fforceMoon = False):
        super().__init__("Desert", fparent,fnumMoons, fforceMoon)
    
    def onSpecialEvent(self):
        if self.type not in Ship.player.specialEvents:
            desertPlanetEvent().onExecute()
            Ship.player.specialEvents[self.type] = True
            Ship.player.save()
planetTypes.append(DesertPlanet)



class Wormhole(Structure):
    
    names = []
    
    def __init__(self, fparent = None):
        genName = f"F{randint(137, 999)}"
        while genName in Wormhole.names:
            genName = f"F{randint(137, 999)}"
        
        super().__init__(genName, "Wormhole", False, fparent)
        
        self.structures = [ DysonSphere(self) ]
        self.structureOptionsItem = None
    
    def onRenderArt(self):
        print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
█████████████████████████████████████████▀▀▀▀▀██████████████████████████████████
███████████████████████████████████████▀       ▀████████████████████████████████
██████████████████████████████████████▌         ████████████████████████████████
███████████████████████████████████████         ████████████████████████████████
████████████████████████████████████████▄▄   ▄▄█████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self):
        clear()
        dashes = "--------------------------------------------"
        
        self.onRenderArt()
        print(f"\n\n\n{dashes} {self.displayName} {dashes}")
    
    def onInput(self):
        if self.structureOptionsItem is None:
            self.structureOptionsItem = OptionItem(f"Explore Structures", self.structures, "structureResult")
            self.structureOptionsItem.returnTxt = "To return to explore options press: Backspace or Space"
        structureResult = self.structureOptionsItem.onExecute(self, "Structures")
        
        if not structureResult[0]: return structureResult
        if not structureResult[2][0]: return structureResult
        
        structureOption = structureResult[2][2]
        
        print(structureOption)
        return [True, None, structureOption]
    
    def onExecute(self):
        self.onRender()
        return self.onInput()
    
    def onCancel(self, type):
        return self.parent.onExecute()

class DysonSphere(Structure):
    
    names = []
    
    def __init__(self, fparent):
        damaged = False
        
        chance = randint(0, 5)
        if chance != 1:
            damaged = True
        
        super().__init__(fparent.name, "Dyson Sphere", damaged, fparent)
        
    
    def onRenderArt(self):
        print(f"""
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████▀▀▀▀████████████████████████████████████
██████████████████████████████████████▀      ▀██████████████████████████████████
████████████████████████████████████▀          ▀████████████████████████████████
████████████████████████████████████            ████████████████████████████████
████████████████████████████████████            ████████████████████████████████
████████████████████████████████████▄          ▄████████████████████████████████
██████████████████████████████████████▄      ▄██████████████████████████████████
████████████████████████████████████████▄▄▄▄████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████
████████████████████████████████████████████████████████████████████████████████""")
    
    def onRender(self):
        clear()
        dashes = "--------------------------------------------"
        
        self.onRenderArt()
        print(f"\n\n\n{dashes} {self.displayName} {dashes}")
    
    def onInput(self):
        if self.damaged:
            print("Repairing damage.")
            sleep(0.5)
            print ("\033[A                             \033[A")
            print("Repairing damage..")
            sleep(0.5)
            print ("\033[A                             \033[A")
            print("Repairing damage...")
            sleep(0.5)
            print ("\033[A                             \033[A")
            print("Repairing damage....")
            sleep(0.5)
            print ("\033[A                             \033[A")
            print("Repaired")
            
            self.damaged = False
        
        print("Teleporting through Dyson Sphere\n\nPress enter to continue")
        keyboard.wait("enter")
        
        Ship.player.level += 1
        Ship.player.save()
        return [ True, None, self ]
    
    def onExecute(self):
        self.onRender()
        return self.onInput()