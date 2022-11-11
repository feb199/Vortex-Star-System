import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class bcolors:
    HEADER = '\033[95m'
    GREY = '\033[100m'
    WHITE = '\033[107m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'