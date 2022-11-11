import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.console import clear

from classes.ship import Ship
from game.story.backstory import backstory
from game.story.endgame import endgame


def story():
    if Ship.player is None: return [ False, None, "No Player" ]
    ship = Ship.player
    
    clear()
    backstory(ship)
    # clear()

def endGameStory():
    if Ship.player is None: return [ False, None, "No Player" ]
    ship = Ship.player
    
    clear()
    endgame(ship)