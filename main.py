#! python3
# main.py - anata gui

# GUI automation
import pyautogui
# file path and control
import os
# determine exe or script
import sys
# play sound file
#import playsound
# GUI
import tkinter
# image
from PIL import ImageTk
from PIL import Image
# itertools
import itertools
# multiprocess
import multiprocessing
#anata.py
import anata
#util.py
import util

# closing event
def onclosing():
    global proclist
    global root
    # kill all multiprocess
    try:
        for proc in proclist:
            if type(proc) is not int:
                proc.terminate()
    finally:
        # exit root
        root.destroy()

# icon click event
def eventfunction(event):
    # global value
    global onofflist
    global canvas
    global proclist
    global iconsiz
    global iconcol
    global iconrow
    global sndpath
    global root
    global afttime
    xx = event.x // iconsiz
    yy = event.y // iconsiz
    number = xx + yy * iconrow
    # if onofflist is 0, onofflist set 1 and create red rectangle
    # else, onofflist set 0 and delete red rectangle
    if onofflist[number] == 0:
        onofflist[number] = 1
        uplx = 2 + xx * iconsiz
        uply = 2 + yy * iconsiz
        lowrx = -1 + (xx+1) * iconsiz
        lowry = -1 + (yy+1) * iconsiz
        # create red rectangle
        canvas.create_rectangle(uplx,uply,lowrx,lowry,width=2,outline='red',tags='tangle'+str(number))
        #playsound.playsound(sndpath+'start.wav')
        # exec skill unsynchronize
        proclist[number] = multiprocessing.Process(target=anata.multi,args=('skill'+str(number+1)+'.txt',))
        proclist[number].start()
        # after function
        root.after(afttime,repeat,number)
    else:
        onofflist[number] = 0
        # delete red rectangle
        canvas.delete('tangle'+str(number))
        # kill process
        proclist[number].terminate()

# after function
def repeat(number):
    # global value
    global onofflist
    global canvas
    global proclist
    global root
    global afttime
    # check subprocess
    if proclist[number].is_alive() == False:
        onofflist[number] = 0
        # delete red rectangle
        canvas.delete('tangle'+str(number))
        return
    # continue after function
    if onofflist[number] == 1:
        root.after(afttime,repeat,number)

def main():
    # global value
    global onofflist
    global canvas
    global proclist
    global iconsiz
    global iconcol
    global iconrow
    global sndpath
    global root
    global afttime
    global winxpos
    global winypos
    # determine if application is a script file or frozen exe
    if getattr(sys, 'frozen', False):
        applicationpath = os.path.dirname(sys.executable)
    else:
        applicationpath = os.path.dirname(__file__)
    # get exceute file path
    # __file__ : [absolute path + file name] and get folder path by dirname(__file__)
    if os.path.dirname(applicationpath) != '':
        # default file path change to exec file path for process
        os.chdir(applicationpath)

    # get config parameter
    rootttl = util.rootttl
    iconsiz = util.iconsiz
    iconrow = util.iconrow
    iconcol = util.iconcol
    titlicn = util.titlicn
    deficon = util.deficon
    topmost = util.topmost
    afttime = util.afttime
    winxpos = util.winxpos
    winypos = util.winypos
    icnpath = util.icnpath
    sndpath = util.sndpath

    # create window
    root = tkinter.Tk()
    # set title
    root.title(rootttl)
    # set screen front
    root.attributes('-topmost',topmost)
    # set title icon
    root.iconbitmap(default=titlicn)

    imgwidth = iconsiz * iconrow
    imgheight = iconsiz * iconcol
    # initialize list
    onofflist = []
    imglist = []
    proclist = []
    # create image canvas
    canvas = tkinter.Canvas(bg="black",width=imgwidth,height=imgheight)
    # put widget x,y position
    canvas.place(x=0,y=0)
    # loop with iconnnum
    for j, i in itertools.product(range(iconcol),range(iconrow)):
        idx = i + (j*iconrow)
        onofflist.append(0)
        icnimg = icnpath+str(idx+1)+'.png'
        # image is there?
        if os.path.isfile(icnimg) == False:
            icnimg = icnpath + deficon
        img = Image.open(icnimg)
        img = img.resize((iconsiz, iconsiz))
        imglist.append(img)
        imglist[idx] = ImageTk.PhotoImage(imglist[idx])
        # create image
        canvas.create_image(iconsiz*i,iconsiz*j,image=imglist[idx],anchor=tkinter.NW)
        proclist.append(0)

    # bind eventfunction to click event
    canvas.bind('<Button-1>', eventfunction)
    # bind window close event
    root.protocol("WM_DELETE_WINDOW",onclosing)

    screenwidth, screenheight = pyautogui.size()
    windowxposition = screenwidth - imgwidth - winxpos
    windowyposition = screenheight - imgheight - winypos
    windowheight = imgheight

    # set window size and position
    root.geometry(str(imgwidth)+'x'+str(windowheight)+'+'+str(windowxposition)+'+'+str(windowyposition))
    # window size fixed
    root.resizable(width=False,height=False)
    root.mainloop()

if __name__ == '__main__':
    # it is for exe with multiprocessing
    multiprocessing.freeze_support()
    main()

