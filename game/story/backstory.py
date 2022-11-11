import os, sys, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.console import clear
from utils.printStyle import typeWriter

dashes = "--------------------------------------------"

def printBanner():
    print(f"\n\n\n{dashes} Vortex Star System: Backstory {dashes}")

def backstory(ship):
    printBanner()
    
    typeWriter(f"""{ship.shipName.capitalize()} Organism Spaceship was badly damaged and needed to get repaired,
the warp hole system in the Organism Spaceship that was used to travel between galaxies was destroyed,
so they have to go to the centre of the galaxy to the black hole,
to build a structure to travel back to their home galaxy.""", 0.04)
    
    print("\nPress enter to continue")
    keyboard.wait("enter")
    
    clear()
    printBanner()
    
    # Part 1
    typeWriter(f"""In an unknown galaxy the {ship.shipName.capitalize()} has encountered an accident which has damaged the ship,
Captain {ship.captain.name.capitalize()} has successfully landed the ship in a strange galaxy with unknown planets.""", 0.035)
    
    # Part 2
    typeWriter(f"""\nAll of the crew members including the captain are very confused on where they have landed,
but all they know is the ship is very damaged and they need to repair it as soon as possible.""", 0.035)
    
    # Part 3
    typeWriter(f"""\nAs the crew looks around the surroundings they see some nuts, bolts and parts of scrap metal
that they think could work to repair parts of the ship that could help them travel further through the system.""", 0.035)
    
    # Part 4
    typeWriter(f"""\nAs the crew are preparing the ship for parts they hear a faint “Help” coming from the distance,
they all decide that one crew member should have a look around and see if they can find someone that begged for help.""", 0.035)
    
    # Part 5
    typeWriter(f"""\nAfter an hour the crew member comes back with a tall man who is very beaten up,
the crew take him in and bandages his wounds and gives him some food and drink,
the man thanks the team and asks if he could join them.""", 0.035)
    
    # Part 6
    typeWriter(f"""\nThe crew finally fixed the ship enough to travel to the nearest solar system.""", 0.035)
    
    print("\n\nPress enter to continue")
    keyboard.wait("enter")