import os, sys, keyboard
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from random import choice

from utils.console import clear
from utils.readWrite import readTxtFile
from utils.printStyle import typeWriter

from classes.menu import OptionItem
from classes.ship import Ship



class Event:
    
    def __init__(self, name, options, content = None, contentPath = None, printSpeed = 0.04):
        self.name = name
        self.content = content
        self.contentPath = contentPath
        self.options = options
        self.printSpeed = printSpeed
        
        self.displayName = f"{self.name} Event"
        
        if self.contentPath is not None:
            self.content = readTxtFile(self.contentPath)
        
        self.eventOptionsItem = None
    
    def onRender(self, speedOverride = None):
        clear()
        dashes = "--------------------------------------------"
        
        print(f"\n\n\n{dashes} {self.displayName} {dashes}")
        if speedOverride is not None:
            print(self.content)
        else:
            typeWriter(self.content, self.printSpeed)
        print(f"\n")
    
    def onInput(self, skipTo = None):
        if self.eventOptionsItem is None:
            self.eventOptionsItem = OptionItem(f"Event Options", self.options, "eventResult")
            self.eventOptionsItem.returnTxt = ""
        eventResult = self.eventOptionsItem.onExecute(self, True)
        
        if not eventResult[0]: return eventResult
        if not eventResult[2][0]: return eventResult
        
        return [True, None, eventResult]
    
    def onExecute(self, skipTo = None):
        if Ship.player is None: return [ False, None, "No Player" ]
        
        self.onRender()
        return self.onInput()
    
    def onCancel(self, type):
        return self.onExecute()

class EventOption():
    
    ids = 0
    
    def __init__(self, name, content = None, contentPath = None, printSpeed = 0.04):
        EventOption.ids += 1
        self.id = EventOption.ids
        
        self.name = name
        self.content = content
        self.contentPath = contentPath
        self.printSpeed = printSpeed
        
        self.displayName = f"{self.name}"
        
        if self.contentPath is not None:
            self.content = readTxtFile(self.contentPath)
        
        self.eventOptionsItem = None
    
    def onRender(self, displayTxt = None):
        clear()
        dashes = "--------------------------------------------"
        
        print(f"\n")
        typeWriter(self.content, self.printSpeed)
        print(f"\nPress enter to continue")
        keyboard.wait("enter")
        
        return [ True, None, "Printed" ]
    
    def onExecute(self, skipTo = None):
        if Ship.player is None: return [ False, None, "No Player" ]
        
        return self.onRender()