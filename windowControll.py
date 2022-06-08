import subprocess
from typing import List

def _runCommand(cmd:list)->str:
    "runs command and return output"
    return subprocess.run(["wmctrl"]+cmd,stdout=subprocess.PIPE).stdout.decode("utf-8")


def __listToStr(l:list,sperator:str = " ")->str:
    "adds all items in a list together"
    total = ""
    for n,item in enumerate(l):
        total += item
        if not n >= len(l)-1:
            total += sperator
    return total

def __parsLine(str_line:str,until_name:int=8)->list:
    "splits the line in its collumns and returns as a list (the name will be returns a one item)"
    split_list = [collumn for collumn in str_line.split(" ") if collumn != '']

    pre_name = split_list[:until_name]
    name = __listToStr(split_list[until_name:])

    pre_name.append(name)
    return pre_name

def __parsTable(str_table:str)->list:
    "parses a table by splitting it into line and then parsing the lines"
    return [__parsLine(line) for line in str_table.splitlines()]

class Window:
    def __init__(self,arg_list:list):
        args_iter = iter(arg_list)
        self.id             = next(args_iter)
        self.desktop        = next(args_iter)
        self.pid            = next(args_iter)
        self.x              = next(args_iter)
        self.y              = next(args_iter)
        self.width          = next(args_iter)
        self.height         = next(args_iter)
        self.clientMaschine = next(args_iter)
        self.name           = next(args_iter)
        del(args_iter)

    def run(self,cmd:list)->str:
        "runs a command on the window"
        return _runCommand(["-i","-r",self.id] + cmd)

    def changeGeometrie(self,x:int,y:int,width:int,height:int)->None:
        "moves and resizes the window use -1 value if you dont want this axis to change"
        self.run(["-e",f"0,{x},{y},{width},{height}"])

    def move(self,x:int,y:int)->None:
        "moves the window use -1 value if you dont want this axis to change"
        self.changeGeometrie(x, y,-1,-1)

    def resize(self,width:int,height:int)->None:
        "resizes the window use -1 value if you dont want this axis to change"
        self.changeGeometrie(-1, -1, width, height)

    def moveToDesktop(self,desktop:int)->None:
        "moves the window to another desktop starting from 0 and -1 being sticky (be on the dektop at all times)"
        self.run(["-t",str(desktop)])

    def add(self,arg1:str,arg2:str = None)->None:
        """add the given propery, supported are:
        
        modal, sticky, maximized_vert, maximized_horz, shaded, skip_taskbar, 
        skip_pager, hidden, fullscreen, above, below.
        
        onyl a max of 2 properties can be changed ad once"""

        self.modify("add", arg1, arg2)

    def remove(self,arg1:str,arg2:str = None)->None:
        """remove the given propery, supported are:
        
        modal, sticky, maximized_vert, maximized_horz, shaded, skip_taskbar, 
        skip_pager, hidden, fullscreen, above, below
        
        onyl a max of 2 properties can be changed ad once"""

        self.modify("remove", arg1, arg2)

    def toggle(self,arg1:str,arg2:str = None)->None:
        """toggles the given propery, supported are:
        
        modal, sticky, maximized_vert, maximized_horz, shaded, skip_taskbar, 
        skip_pager, hidden, fullscreen, above, below.
        
        onyl a max of 2 properties can be changed ad once"""
        
        self.modify("toggle", arg1, arg2)

    def modify(self,how:str,arg1:str,arg2:str)->None:
        """changes the given propery, supported are:
        
        modal, sticky, maximized_vert, maximized_horz, shaded, skip_taskbar, 
        skip_pager, hidden, fullscreen, above, below.
        
        onyl a max of 2 properies can be changed ad once
        
        "how" can be add/remove/toggle"""
        if arg2 == None:
            self.run(["-b",f"{how},{arg1}"])
        else:
            self.run(["-b",f"{how},{arg1},{arg2}"])

def getAllWindows()->List[Window]:
    "returns all windows as window classes"
    return [Window(line) for line in __parsTable(_runCommand(["wmctrl","-l","-p","-G"]))]

def getWindow(name:str,exact_match = False) -> Window:
    """returns the first window matching to "name"

    default -> checks only if "name" is in the name of the window"""
    if exact_match:
        return [win for win in getAllWindows() if name == win.name][0]
    else:
        return [win for win in getAllWindows() if name in win.name][0]