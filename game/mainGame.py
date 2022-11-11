import os, sys, keyboard, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random import randint

from utils.console import clear
from utils.json import toJSON

from classes.ship import Ship
from classes.solarSystem import SolarSystem

from game.mainStory import endGameStory


def game():
    if Ship.player is None: return [ False, None, "No Player" ]
    ship = Ship.player
    
    while ship.level < 20:
        if ship.level < 4:
            SolarSystem(forceSun=True).onExecute()
        else:
            SolarSystem().onExecute()
    
    if ship.level >= 20:
        endGameStory()
    exit()
