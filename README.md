# wmctrlpy

an easy way to use python an wmctrl to move winodws

because wmctrl is wierd you can't get the active window

get windows by name by using "getWindow"
    either matches to the excat name
    or on default it only looks for substring matching

get all windows by using getAllWindows

a Window class has these values:

    id -> hexnumber as idenifier
    desktop -> -1 for "sticky" = on all desktops, enumeration of desktops starts at 0
    pid -> decimal id for windows that support it, else it is 0
    x -> x coordinate of the window
    y -> y coordinate of the window
    width -> width if the window
    height -> height if the window
    clientMaschine -> the Computer on witch the window is (you can mostly ignore this)
    name -> the title/name of the window

and these methods:

    move(x,y)
        moves the window use -1 value if you dont want this axis to change

    resize(width,height)
        resizes the window use -1 value if you dont want this axis to change
    
    moveToDesktop(dektop)
        moves the window to another desktop starting from 0 and -1 being sticky (be on the dektop at all times)

    add(arg1:str[,arg2:str])
    remove(arg1:str[,arg2:str])
    toggle(arg1:str[,arg2:str])
        adds/removes/toogles up to one window propertie
        supported properies are

        modal, sticky, maximized_vert, maximized_horz, shaded, skip_taskbar, 
        skip_pager, hidden, fullscreen, above, below

    modify(how:str,arg1:str[,arg2:str])
        does the same thing but "how" spesifcies if you want to add/remove/toggle

note: English is not my first language, sorry for spelling - do a pull request with correction if you want