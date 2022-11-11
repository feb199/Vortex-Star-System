import sys
import keyboard
from time import sleep

status = False

def onKeyReleased():
    global status
    status = True

def registerSkipKeybinds():
    global keyboard
    keyboard.unhook_all()
    
    global status
    status = False
    
    registerKeys = ["enter", "space"]
    for key in registerKeys:
        keyboard.add_hotkey(key, onKeyReleased, args=[], suppress=False, timeout=1, trigger_on_release=False)

def typeWriter(txt, speed = 0.1):
    registerSkipKeybinds()
    #txtArray = txt.split("\n")
    #for line in txtArray:
    for c in txt:        
        print(c, end='')
        sys.stdout.flush()
        
        if not status:
            sleep(speed) 
    print('')
    
    keyboard.unhook_all()