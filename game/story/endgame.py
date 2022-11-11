import os, sys, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.console import clear
from utils.printStyle import typeWriter

dashes = "--------------------------------------------"

def printBanner():
    print(f"\n\n\n{dashes} Vortex Star System: End Game {dashes}")

def endgame(ship):
    printBanner()
    
    typeWriter(f"""You've arrived at your final destination which is a black hole it appears there is light at the end of it,
and you think you've finally made it but suddenly you get attacked by a swarm of aliens your ships translator activates
and the aliens say we will not let you progress any further this is our ship
and they try to take your ship but the ships weapon activates and blasts through the swarm of aliens,""", 0.04)

    typeWriter(f"""\nyou think you've won but you're wrong it turns out the alien's technology has improved and they now have shields,
you think this is the end but all your crew members join your side and you feel thankful you have them by your side.
You ask the ship to prepare its shield and power up the hyper jump the crew look confused and so do the aliens,
you turn to your crew you tell them you have a crazy idea,
while the ship is powering up you ask the crew to fire weapons or anything else they may have to help defend the ship.""", 0.04)

    typeWriter(f"""\nYour crew tries so hard to defend the ship and thankfully it pays off the ship has charged up and you are now able to hyperjump,
you tell the ship to hyperjump now and it jumps past the alien swarm and leads you further into the black hole,
you hug your crew members as you can see a way out you fly on slowly over to the light
and next thing you know you wake up and your back where you came from, you're all so happy.""", 0.04)

    typeWriter(f"""\n\n\"Congratulations you’ve finished our game, we hope you’ve enjoyed it :)\"""", 0.04)
    
    print("\n\nPress enter to exit")
    keyboard.wait("enter")
    exit()