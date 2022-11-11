import os, sys, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def readTxtFile(txtPath):
    txtContent = []
    if txtPath.is_file():
        with open(txtPath, "r") as openfile:
            txtContent = [line.rstrip() for line in openfile]
    else:
        raise Exception(f"{bcolors.FAIL}{txtPath} file is missing{bcolors.ENDC}")

    if len(txtContent) <= 0:
        raise Exception(f"{bcolors.FAIL}{txtPath} file has no content{bcolors.ENDC}")
    
    return txtContent