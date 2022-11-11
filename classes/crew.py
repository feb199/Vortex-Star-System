import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.menu import InputItem
from utils.console import clear

from random import choice

defaultCrewNames = [ "Feb199", "Alia", "Daniel", "Georgia" ]

class Person:
    
    ids = 0
    
    def __init__(self, name, id = None):
        if id is None:
            self.id = Person.ids
            Person.ids += 1
        else:
            self.id = id
        
        self.name = name

class NormalPerson(Person):
    
    def __init__(self, fname, fid = None):
        super().__init__(fname, fid)

class CaptainPerson(Person):
    
    def __init__(self, fname, fid = None):
        super().__init__(fname, fid)