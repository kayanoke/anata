# time
import time
# GUI automation
import pyautogui
# file path and control
import os
# subprocess
import subprocess
# play sound file
import playsound
# skill exec
import skillE
# GUI
import tkinter
# image
from PIL import ImageTk
from PIL import Image
# init config
import configparser

# reference folder path
iconPath = 'icon/'
soundPath = 'sound/'
imagePath = 'image/'
# set initialize parameter
iconsize = 64
iconnum = 6

# icon click event
def eventfunction(event):
    # global value
    global onofflist
    global canvas
    global proclist
    global iconsize
    xx = event.x // iconsize
    # if onofflist is 0, onofflist set 1 and create red rectangle
    # else, onofflist set 0 and delete red rectangle
    if onofflist[xx] == 0:
        onofflist[xx] = 1
        canvas.create_rectangle(2+xx*iconsize,2,-1+(xx+1)*iconsize,iconsize-1,width=2,outline='red',tags='tangle'+str(xx))
        playsound.playsound(soundPath+'start.wav')
        proclist[xx] = subprocess.Popen(['python','skillE.py','skill'+str(xx+1)+'.txt'])
    else:
        onofflist[xx] = 0
        # delete red rectangle
        canvas.delete('tangle'+str(xx))
        # kill process
        proclist[xx].terminate()

# get exceute file path
# __file__ : [absolute path + file name] and get folder path by dirname(__file__)
if os.path.dirname(__file__) != '':
    # default file path change to exec file path for process
    os.chdir(os.path.dirname(__file__))

config_ini = configparser.ConfigParser()
config_ini.read('config.ini',encoding='utf-8')

clock1 = config_ini.get('SKILL1','Clock')

# create window
root = tkinter.Tk()
# set title
root.title("yourSkill")

imgwidth = iconsize * iconnum
# initialize list
onofflist = []
imgimlist = []
proclist = []
# create image canvas
canvas = tkinter.Canvas(bg="black",width=imgwidth,height=iconsize)
# put widget x,y position
canvas.place(x=0,y=0)

# loop with iconnnum
for i in range(iconnum):
    onofflist.append(0)
    img = Image.open(iconPath+str(i+1)+'.png')
    img = img.resize((iconsize, iconsize))
    imgimlist.append(img) 
    imgimlist[i] = ImageTk.PhotoImage(imgimlist[i])
    canvas.create_image(iconsize*i,0,image=imgimlist[i],anchor=tkinter.NW)
    proclist.append(0)

# bind eventfunction to click event
canvas.bind('<Button-1>', eventfunction)

# menu
check = tkinter.IntVar()
check.set(1)
menubar = tkinter.Menu(root)
root.configure(menu=menubar)
games = tkinter.Menu(menubar,tearoff=False)
create = tkinter.Menu(menubar,tearoff=False)
checks = tkinter.Menu(menubar,tearoff=False)
menubar.add_cascade(label="Files",underline=0,menu=games)
menubar.add_cascade(label="Create",underline=0,menu=create)
menubar.add_cascade(label="Check",underline=0,menu=checks)
games.add_command(label='Save',command=skillE.startS)
create.add_command(label='Click',command=skillE.startS)
create.add_command(label='DClick',command=skillE.startS)
create.add_command(label='Move',command=skillE.startS)
create.add_command(label='Click&Drug',command=skillE.startS)
create.add_command(label='Typing',command=skillE.startS)
create.add_command(label='Key',command=skillE.startS)
checks.add_radiobutton(label='Check 1',variable=check,value=1)
checks.add_radiobutton(label='Check 2',variable=check,value=2)
checks.add_radiobutton(label='Check 3',variable=check,value=3)
checks.add_radiobutton(label='Check 4',variable=check,value=4)
checks.add_radiobutton(label='Check 5',variable=check,value=5)
checks.add_radiobutton(label='Check 6',variable=check,value=6)

screenwidth, screenheight = pyautogui.size()
windowxposition = screenwidth - imgwidth - 15
windowyposition = screenheight - iconsize - 115
windowheight = iconnum + 58
# set window size and position
root.geometry(str(imgwidth)+'x'+str(windowheight)+'+'+str(windowxposition)+'+'+str(windowyposition))

root.resizable(width=False, height=False)
root.mainloop()
