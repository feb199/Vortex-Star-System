import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from time import sleep
import keyboard
from copy import deepcopy

from utils.console import clear, bcolors
from utils.json import toJSON

class Main:
    
    def __init__(self, name, menus, spacer = "                    "):
        self.name = name
        self.status = None
        self.menus = menus
        self.spacer = spacer
        self.selected = 0
        self.navKeys = {
            "left": lambda x: x - 1,
            "right": lambda x: x + 1,
            "a": lambda x: x - 1,
            "d": lambda x: x + 1,
        }
        self.cancelKeys = [ "esc" ]
        self.proceedKeys = [ "enter" ]
        
        for menu in self.menus:
            menu.parent = self
    
    # print(f"{spacer} [{self.bind}] {self.name}", end = "")
    
    def onRender(self):
        clear()
        dashes = "--------------------------------------------"
        print(f"\n\n\n{dashes} {self.name} {dashes}")
        
        for menu in self.menus:
            displayString = menu.name
            
            foundShip = next((x for x in self.menus if x.id == menu.id), None)
            if foundShip is not None:
                if self.menus.index(foundShip) == self.selected:
                    displayString = f"{bcolors.UNDERLINE}{menu.name}{bcolors.ENDC}"
            
            print(f"{self.spacer}{displayString}", end = "")
        print("")
        
        print("\n\n\nPlease select an option by navigating using: ←, → OR A, D\nThen press the ENTER key to confirm")
        print("\nTo quit the game press: ESC")
    
    def onKeyReleased(self, *args):
        self.status = args[0]
    
    def onInput(self):
        global keyboard
        
        keyboard.unhook_all()
        
        registerKeys = deepcopy(list(self.navKeys.keys()))
        registerKeys.extend(self.cancelKeys)
        registerKeys.extend(self.proceedKeys)
        for key in registerKeys:
            keyboard.add_hotkey(key, self.onKeyReleased, args=[key], suppress=False, timeout=1, trigger_on_release=False)
        
        self.status = "reg"
        
        while self.status == "reg":
            sleep(.1)
        
        if self.status in self.navKeys.keys():
            self.selected = self.navKeys[self.status](self.selected)
            if self.selected < 0:
                self.selected = len(self.menus)-1
            elif self.selected > len(self.menus)-1:
                self.selected = 0
            
            self.onRender()
            return self.onInput()
        elif self.status in self.cancelKeys:
            keyboard.unhook_all()
            exit()
        elif self.status in self.proceedKeys:
            selectedMenu = self.menus[self.selected]
            return selectedMenu.onExecute()
    
    def onExecute(self):
        self.onRender()
        return self.onInput()

class Menu:
    
    ids = 0
    
    def __init__(self, name, child):
        self.id = Menu.ids
        Menu.ids += 1
        
        self.parent = None
        self.name = name
        self.child = child
        
        if self.child is not None:
            if self.child:
                self.child.parent = self
    
    def renderChild(self):
        clear()
        dashes = "---------------------------------------------------------"
        print(f"\n\n\n{dashes} {self.name} {dashes}")

        if self.child is not None:
            if self.child:
                self.child.onRender()
        
        return True
    
    def inputChild(self):
        if self.child is not None:
            if self.child:
                return self.child.onInput()
        
        return [False, None]

    def onExecute(self):
        self.renderChild()
        return self.inputChild()


class Item:
    
    def __init__(self, name, content = None):
        self.parent = None
        self.name = name
        self.content = content
    
    def onRender(self):
        if self.content is not None:
            print(f"{self.content}", end = "")
        else:
            print(f"{self.name}", end = "")
    
    def onExecute(self):
        self.onRender()
        return [True, "Printed"]

class TextItem(Item):
    
    ids = 0
    
    def __init__(self, content):
        super().__init__(f"text_{content}", content)
        TextItem.ids += 1
        self.id = TextItem.ids
        
        self.displayName = self.content
    
    def onRender(self):
        print(f"{self.content}", end = "")
    
    def onExecute(self):
        return [True, None, self]

def getInput(txt = None):
    sys.stdout.flush()
    if txt is None:
        print ("                                                                      ")
        print ("\033[A                             \033[A")
        userInput = input()
    else:
        print ("                                                                      ")
        print ("\033[A                             \033[A")
        userInput = input(txt)
    
    while userInput is None or not userInput:
        print ("\033[A                             \033[A")
        print ("                                                                      ")
        print ("\033[A                             \033[A")
        userInput = input()
    
    return userInput

def confirmUserInput(userInput):
    userInputConfirmed = False
        
    while not userInputConfirmed:
        print ("\033[A                             \033[A")
        userInputConfirm = input(f"Is {bcolors.WARNING}{str(userInput)}{bcolors.ENDC} correct? (yes/no): ")
        while userInputConfirm.lower() != "yes" and userInputConfirm.lower() != "no":
            print ("\033[A                             \033[A")
            userInputConfirm = input(f"Is {bcolors.WARNING}{str(userInput)}{bcolors.ENDC} correct? (yes/no): ")
        
        if userInputConfirm.lower() == "yes":
            userInputConfirmed = True
            return [True, userInput]
        elif userInputConfirm.lower() == "no":
            userInputConfirmed = True
            print ("\033[A                             \033[A")
            print ("                                                                      ")
            print ("\033[A                             \033[A")
            newUserInput = getInput("Please enter a new value: ")
            return confirmUserInput(newUserInput)
        else:
            userInputConfirmed = True
            return confirmUserInput(userInput)

class InputItem(Item):
    
    def __init__(self, fname, fcontent = None):
        super().__init__(fname, fcontent)
        self.value = f"{bcolors.GREY}{self.content}{bcolors.ENDC}"
        
        self.cancelKeys = [ "esc" ]
        self.proceedKeys = [ "enter" ]
    
    def onRender(self):
        print(f"{bcolors.BOLD}{self.name}{bcolors.ENDC}: {self.value}", end = "")
    
    def onInput(self):
        
        print(f"\n\n\nPlease select input a value\nThen press the ENTER key to confirm\n\nTo set value to default: cancel")
        
        userInput = getInput()
        
        result = confirmUserInput(userInput)
        if not result[0]: return [False, None, "ERORR"]
        
        userInput = result[1]
        
        if userInput.lower() == "cancel": return [False, None, "User Canceled"]
        
        if len(userInput) <= 0 or userInput == " ":
            if self.content is None:
                return [False, None, "Invalid Name"]
            else:
                self.value = f"{bcolors.GREY}{self.content}{bcolors.ENDC}"
        else:
            self.value = userInput
        
        # if userInput.find("\x1b[100m"):
        #     return [False, None, "Invalid Name"]
        
        return [True, self.value]
    
    def onExecute(self):
        self.onRender()
        return self.onInput()

class OptionItem(Item):
    
    def __init__(self, fname, options, optionType, spacer = "             "):
        super().__init__(fname, None)
        self.status = None
        self.selected = 0
        self.options = options
        self.type = optionType
        self.spacer = spacer
        self.navKeys = {
            "left": lambda x: x - 1,
            "right": lambda x: x + 1,
            "a": lambda x: x - 1,
            "d": lambda x: x + 1,
        }
        self.cancelKeys = [ "backspace", "space" ]
        self.returnTxt = "To return to main menu press: Backspace or Space"
        self.proceedKeys = [ "enter" ]
    
    def onRender(self):
        for option in self.options:
            displayString = option.displayName
            
            foundShip = next((x for x in self.options if x.id == option.id), None)
            if foundShip is not None:
                if self.options.index(foundShip) == self.selected:
                    displayString = f"{bcolors.UNDERLINE}{option.displayName}{bcolors.ENDC}"
            
            print(f"{self.spacer}{displayString}", end = "")
        print("")
        
        print("\n\n\nPlease select an option by navigating using: ←, → OR A, D\nThen press the ENTER key to confirm")
        print(f"\n{self.returnTxt}")
    
    def onKeyReleased(self, *args):
        self.status = args[0]
    
    def onInput(self, passThroughParent = None, passThrough = None):
        global keyboard
        
        keyboard.unhook_all()
        
        registerKeys = deepcopy(list(self.navKeys.keys()))
        registerKeys.extend(self.cancelKeys)
        registerKeys.extend(self.proceedKeys)
        for key in registerKeys:
            keyboard.add_hotkey(key, self.onKeyReleased, args=[key], suppress=False, timeout=1, trigger_on_release=False)
        
        self.status = "reg"
        
        while self.status == "reg":
            sleep(.1)
        
        if self.status in self.navKeys.keys():
            self.selected = self.navKeys[self.status](self.selected)
            if self.selected < 0:
                self.selected = len(self.options)-1
            elif self.selected > len(self.options)-1:
                self.selected = 0
            
            if passThroughParent is not None:
                passThroughParent.onRender(passThrough)
                return self.onExecute(passThroughParent, passThrough)
            else:
                self.parent.renderChild()
                return self.parent.inputChild()
        elif self.status in self.cancelKeys:
            keyboard.unhook_all()
            if passThroughParent is not None:
                return passThroughParent.onCancel(self.type)
            else:
                self.parent.parent.onRender()
                return self.parent.parent.onInput()
        elif self.status in self.proceedKeys:
            return [True, self.type, self.options[self.selected].onExecute()]
    
    def onExecute(self, passThroughParent = None, passThrough = None):
        self.onRender()
        return self.onInput(passThroughParent, passThrough)








