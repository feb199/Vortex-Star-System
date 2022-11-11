import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.menu import InputItem
from utils.console import clear

from random import choice

defaultHP = {
    "front": 500,
    "back": 100,
    "left": 300,
    "right": 300
}

class System:
    
    def __init__(self, name, systemType):
        self.name = name
        self.type = systemType

class Hull(System):
    
    def __init__(self, fname = "Normal", hp = defaultHP):
        super().__init__(fname, "hull")
        self.destroyed = False
        self.frontHP = hp["front"]
        self.backHP = hp["back"]
        self.leftHP = hp["left"]
        self.rightHP = hp["right"]
    
    def load(self, inputJSON):
        self.destroyed = inputJSON["destroyed"]
        self.frontHP = inputJSON["frontHP"]
        self.backHP = inputJSON["backHP"]
        self.leftHP = inputJSON["leftHP"]
        self.rightHP = inputJSON["rightHP"]
        return self

class Shield(System):
    
    def __init__(self, fname = "Normal", maxHp = 100, maxEnergy = 1000):
        super().__init__(fname, "shield")
        self.active = False
        self.destroyed = False
        self.hp = maxHp
        self.maxHP = maxHp
        self.maxEnergy = maxEnergy
        self.energy = 0
    
    def load(self, inputJSON):
        self.destroyed = inputJSON["destroyed"]
        self.hp = inputJSON["hp"]
        self.maxHP = inputJSON["maxHP"]
        self.maxEnergy = inputJSON["maxEnergy"]
        return self

class Reactor(System):
    
    def __init__(self, fname = "Normal", maxHp = 100, maxEnergy = 5000):
        super().__init__(fname, "reactor")
        self.active = False
        self.destroyed = False
        self.hp = maxHp
        self.maxHP = maxHp
        self.maxEnergy = maxEnergy
        self.energyOutput = 0
    
    def load(self, inputJSON):
        self.destroyed = inputJSON["destroyed"]
        self.hp = inputJSON["hp"]
        self.maxHP = inputJSON["maxHP"]
        self.maxEnergy = inputJSON["maxEnergy"]
        return self



class Weapon(System):
    def __init__(self, fname = None, maxHp = 100, damage = None, rate = 50):
        super().__init__(fname, "weapon")
        self.active = False
        self.destroyed = False
        self.hp = maxHp
        self.maxHP = maxHp
        self.damage = damage
        self.rate = rate
        self.currentRate = 0
    
    def load(self, inputJSON):
        self.destroyed = inputJSON["destroyed"]
        self.hp = inputJSON["hp"]
        self.maxHP = inputJSON["maxHP"]
        self.damage = inputJSON["damage"]
        self.rate = inputJSON["rate"]
        return self