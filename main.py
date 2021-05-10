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

# skill icon class
class SkillIcon():

    # initialize
    def __init__(self, widget, skilltext, tooltip):
        # tkinter widget
        self.widget = widget
        # process
        self.proc = 0
        # onoff
        self.onoff = 0
        # skill text file name
        self.skill = skilltext
        # skill tooltip
        self.tooltip = tooltip
        self.id = None
        self.tw = None
        # bind eventfunction to click event
        self.widget.bind('<Button-1>',self.click)
        # bind eventfunction to canvas enter & leave event
        self.widget.bind('<Enter>',self.enter)
        self.widget.bind('<Leave>',self.leave)

    # icon click event
    def click(self, event):
        # global value
        global iconsiz
        global sndpath
        global afttime
        # if onofflist is 0, onofflist set 1 and create red rectangle
        # else, onofflist set 0 and delete red rectangle
        if self.onoff == 0:
            self.onoff = 1
            lowrx = -1 + iconsiz
            lowry = -1 + iconsiz
            # create red rectangle
            self.widget.create_rectangle(1,1,lowrx,lowry,width=2,outline='red',tags='tangle')
            #playsound.playsound(sndpath+'start.wav')
            # exec skill unsynchronize
            self.proc = multiprocessing.Process(target=anata.multi,args=(self.skill,))
            self.proc.start()
            # after function
            self.widget.after(afttime,self.repeat)
        else:
            self.onoff = 0
            # delete red rectangle
            self.widget.delete('tangle')
            # kill process
            self.proc.terminate()

    # after function
    def repeat(self):
        # global value
        global afttime
        # check subprocess
        if self.proc.is_alive() == False:
            self.onoff = 0
            # delete red rectangle
            self.widget.delete('tangle')
            return
        # continue after function
        if self.onoff == 1:
            self.widget.after(afttime,self.repeat)

    # click icon function
    def enter(self, event):
        self.schedule()
    
    # leave from icon function
    def leave(self, event):
        self.unschedule()
        self.id = self.widget.after(1000,self.deltooltip)
    
    def schedule(self):
        if self.tw:
            return
        self.unschedule()
        self.id = self.widget.after(1500,self.disptooltip)
    
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    
    # display tool tip
    def disptooltip(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
        x, y = self.widget.winfo_pointerxy()
        self.tw = tkinter.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.geometry(f'+{x+10}+{y+10}')
        self.tw.attributes('-topmost',True)
        label = tkinter.Label(self.tw,text=self.tooltip,background="lightyellow",relief="solid",borderwidth=1,justify="left")
        label.pack(ipadx=10)

    # delete tool tip
    def deltooltip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

# closing event
def onclosing():
    global root
    global canvaslist
    # kill all multiprocess
    try:
        for canvas in canvaslist:
            if type(canvas.proc) is not int:
                canvas.proc.terminate()
    finally:
        # exit root
        root.destroy()

def main():
    # global value
    global iconsiz
    global sndpath
    global root
    global afttime
    global canvaslist
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
    txtpath = util.txtpath
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
    imglist = []
    canvaslist = []
    # create image canvas
    # put widget x,y position
    # loop with iconnnum
    for j, i in itertools.product(range(iconcol),range(iconrow)):
        canvas = tkinter.Canvas(bg="black",width=iconsiz,height=iconsiz)
        canvaswidth = i * iconsiz
        canvasheight = j * iconsiz
        canvas.place(x=canvaswidth,y=canvasheight)
        idx = i + (j*iconrow)
        icnimg = icnpath+str(idx+1)+'.png'
        # image is there?
        if os.path.isfile(icnimg) == False:
            icnimg = icnpath + deficon
        img = Image.open(icnimg)
        img = img.resize((iconsiz,iconsiz))
        imglist.append(img)
        imglist[idx] = ImageTk.PhotoImage(imglist[idx])
        # create image
        canvas.create_image(0,0,image=imglist[idx],anchor=tkinter.NW)
        try:
            with open(txtpath+'skill'+str(idx+1)+'.txt', mode='r', encoding='utf-8') as f:
                readdata = f.readlines()[0].replace('\n', '')
        except FileNotFoundError:
            pass
        canvaslist.append(SkillIcon(canvas,'skill'+str(idx+1)+'.txt',readdata))
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

