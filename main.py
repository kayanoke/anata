#! python3
# main.py - anata gui

# GUI automation
import pyautogui
# file path and control
import os
# subprocess
import subprocess
# play sound file
import playsound
# GUI
import tkinter
# image
from PIL import ImageTk
from PIL import Image
# init config
import configparser
# itertools
import itertools

# icon click event
def eventfunction(event):
    # global value
    global onofflist
    global canvas
    global proclist
    global iconsiz
    global iconcol
    xx = event.x // iconsiz
    yy = event.y // iconsiz
    # if onofflist is 0, onofflist set 1 and create red rectangle
    # else, onofflist set 0 and delete red rectangle
    if onofflist[xx+yy] == 0:
        onofflist[xx+yy] = 1
        uplx = 2+xx*iconsiz
        uply = 2+yy*iconsiz
        lowrx = -1+(xx+1)*iconsiz
        lowry = -1+(yy+1)*iconsiz
        canvas.create_rectangle(uplx,uply,lowrx,lowry,width=2,outline='red',tags='tangle'+str(xx+yy))
        playsound.playsound(sndpath+'start.wav')
        proclist[xx+yy] = subprocess.Popen(['python','skillE.py','skill'+str(xx+yy+1)+'.txt'])
    else:
        onofflist[xx+yy] = 0
        # delete red rectangle
        canvas.delete('tangle'+str(xx+yy))
        # kill process
        proclist[xx+yy].terminate()

# get exceute file path
# __file__ : [absolute path + file name] and get folder path by dirname(__file__)
if os.path.dirname(__file__) != '':
    # default file path change to exec file path for process
    os.chdir(os.path.dirname(__file__))

# set config.ini parameter
configini = configparser.ConfigParser()
configini.read('config.ini',encoding='utf-8')

iconsiz = int(configini.get('MAIN','IconSiz'))
iconnum = int(configini.get('MAIN','IconNum'))
iconrow = int(configini.get('MAIN','IconRow'))
iconcol = int(configini.get('MAIN','IconCol'))
icnpath = configini.get('SKILL','IcnPath')
sndpath = configini.get('SKILL','SndPath')


# create window
root = tkinter.Tk()
# set title
root.title("anata")

imgwidth = iconsiz * iconrow
imgheight = iconsiz * iconcol
# initialize list
onofflist = []
imgimlist = []
proclist = []
# create image canvas
canvas = tkinter.Canvas(bg="black",width=imgwidth,height=imgheight)
# put widget x,y position
canvas.place(x=0,y=0)
# loop with iconnnum
for j, i in itertools.product(range(iconcol),range(iconrow)):
    idx = i + (j*iconrow)
    onofflist.append(0)
    img = Image.open(icnpath+str(idx+1)+'.png')
    img = img.resize((iconsiz, iconsiz))
    imgimlist.append(img)
    imgimlist[idx] = ImageTk.PhotoImage(imgimlist[idx])
    canvas.create_image(iconsiz*i,iconsiz*j,image=imgimlist[idx],anchor=tkinter.NW)
    proclist.append(0)

# bind eventfunction to click event
canvas.bind('<Button-1>', eventfunction)

# menu
#check = tkinter.IntVar()
#check.set(1)
#menubar = tkinter.Menu(root)
#root.configure(menu=menubar)
#ames = tkinter.Menu(menubar,tearoff=False)
#create = tkinter.Menu(menubar,tearoff=False)
#checks = tkinter.Menu(menubar,tearoff=False)
#menubar.add_cascade(label="Files",underline=0,menu=games)
#menubar.add_cascade(label="Create",underline=0,menu=create)
#menubar.add_cascade(label="Check",underline=0,menu=checks)
#games.add_command(label='Save',command=skillE.startS)
#create.add_command(label='Click',command=skillE.startS)
#create.add_command(label='DClick',command=skillE.startS)
#create.add_command(label='Move',command=skillE.startS)
#create.add_command(label='Click&Drug',command=skillE.startS)
#create.add_command(label='Typing',command=skillE.startS)
#create.add_command(label='Key',command=skillE.startS)
#checks.add_radiobutton(label='Check 1',variable=check,value=1)
#checks.add_radiobutton(label='Check 2',variable=check,value=2)
#checks.add_radiobutton(label='Check 3',variable=check,value=3)
#checks.add_radiobutton(label='Check 4',variable=check,value=4)
#checks.add_radiobutton(label='Check 5',variable=check,value=5)
#checks.add_radiobutton(label='Check 6',variable=check,value=6)

screenwidth, screenheight = pyautogui.size()
windowxposition = screenwidth - imgwidth - 15 - 800
windowyposition = screenheight - imgheight - 115 - 800
windowheight = imgheight
# set window size and position
root.geometry(str(imgwidth)+'x'+str(windowheight)+'+'+str(windowxposition)+'+'+str(windowyposition))

root.resizable(width=False, height=False)
root.mainloop()
