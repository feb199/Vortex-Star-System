import sys
import subprocess
import pkg_resources

required = {'keyboard'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)


import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import keyboard

from utils.console import bcolors

from menu.mainMenu import menu


def main():
    menu()


if __name__ == "__main__":
    # print(f"Test")
    # print(f"{bcolors.GREY}Test{bcolors.ENDC}")
    main()
    keyboard.wait("enter")

