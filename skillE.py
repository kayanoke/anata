# time
import time
# GUI automation
import pyautogui
# file path and control
import os
# play sound file
import playsound
# get command line argument vector
import sys
# subprocess 
import subprocess
# operate file
import shutil
# multi threading
import threading
# clipboard
import pyperclip
# random
import random
# init config
import configparser

# click operation
#(click|dclick|rclick|move|drag)/★.png/accuracy=0.8/movepin=12,12/pause=1/
def clickS(textlist):
    # global value
    global paustim
    global accurcy
    # initialize dafault parameter
    conf = accurcy
    movepinx, movepiny = 0, 0
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            conf = float(datalist[1])
        # move click x,y positon
        if datalist[0] == 'movepin':
            datalistlist = datalist[1].split(',')
            movepinx, movepiny = int(datalistlist[0]), int(datalistlist[1])
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    # locate target position on screen
    target = pyautogui.locateOnScreen(imgpath+textlist[1],confidence=conf)
    # if target is none, end
    if target is None:
        setLog(textlist[1]+' ga nai')
        time.sleep(pausetime)
        return
    # target center position
    x, y = pyautogui.center(target)
    # move target position
    x, y = x + movepinx, y + movepiny
    # input to screen
    # once click
    if textlist[0] == 'click':
        pyautogui.click(x,y)
    # double click
    if textlist[0] == 'dclick':
        pyautogui.doubleClick(x,y)
    # right click
    if textlist[0] == 'rclick':
        pyautogui.rightClick(x,y)
    # move to target
    if textlist[0] == 'move':
        pyautogui.moveTo(x,y)
    # drag to taget
    if textlist[0] == 'drag':
        pyautogui.dragTo(x,y,1,button='left')

    # postprocessing
    setLog(textlist[1]+' '+textlist[0]+' '+str(movepinx)+', '+str(movepiny)+', '+str(conf))
    soundasync(textlist[0]+'.wav')
    time.sleep(pausetime)

# position click operation
#(pclick|pdclick|prclick|pmove|pdrag/zclick)/x=500/y=200/xmax=500/ymax=200/xmin=500/ymin=200/pause=1/
def pclickS(textlist):
    # global value
    global paustim
    global accurcy
    # initialize dafault parameter
    conf = accurcy
    x, y = 0, 0
    xmax, xmin, ymax, ymin = 0, 0, 0, 0
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # x position
        if datalist[0] == 'x':
            x = int(datalist[1])
        # y position
        if datalist[0] == 'y':
            y = int(datalist[1])
        # random x position max
        if datalist[0] == 'xmax':
            xmax = int(datalist[1])
        # random x position min
        if datalist[0] == 'xmin':
            xmin = int(datalist[1])
        # random y position max
        if datalist[0] == 'ymax':
            ymax = int(datalist[1])
        # random y position min
        if datalist[0] == 'ymin':
            ymin = int(datalist[1])
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    if textlist[0] == 'zclick':
        # random x, y
        x, y = random.randint(xmin, xmax), random.randint(ymin, ymax)
    # input to screen
    # once click
    if textlist[0] == 'pclick' or textlist[0] == 'zclick':
        pyautogui.click(x,y)
    # double click
    if textlist[0] == 'pdclick':
        pyautogui.doubleClick(x,y)
    # right click
    if textlist[0] == 'prclick':
        pyautogui.rightClick(x,y)
    # move to target
    if textlist[0] == 'pmove':
        pyautogui.moveTo(x,y)
    # drag to taget
    if textlist[0] == 'pdrag':
        pyautogui.dragTo(x,y,1,button='left')

    # postprocessing
    setLog(textlist[0]+' '+str(x)+', '+str(y))
    soundasync(textlist[0]+'.wav')
    time.sleep(pausetime)

# typing operation
#(typing|press|keydown|keyup|hotkey)/hello/pause=1/
def typingS(textlist):
    # global value
    global paustim
    # initialize default parameter
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    textlist[1] = textlist[1].replace('[sla]', '/')
    # input to screen
    # keyboard typing
    if textlist[0] == 'typing':
        tmp = pyperclip.paste()
        pyperclip.copy(textlist[1])
        pyautogui.hotkey('ctrl','v')
        pyperclip.copy(tmp)
    # press one key
    if textlist[0] == 'press':
        pyautogui.press(textlist[1])
    # key down one key
    if textlist[0] == 'keydown':
        pyautogui.keyDown(textlist[1])
    # key up one key
    if textlist[0] == 'keyup':
        pyautogui.keyUp(textlist[1])
    if textlist[0] == 'hotkey':
        pyautogui.hotkey(textlist[1],textlist[2])

    # postprocessing
    setLog(textlist[1]+' wo nyuuryoku')
    soundasync(textlist[0]+'.wav')
    time.sleep(pausetime)

# pause operation
#pause/1/
def pauseS(textlist):
    # pause
    time.sleep(int(textlist[1]))

    # postprocessing
    setLog(textlist[1]+' byou tomaru')
    soundasync(textlist[0]+'.wav')

# end operation
#end/★.png/
def endS(textlist):
    # global value
    global flg
    global accurcy
    # initialize dafault parameter
    conf = accurcy
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            conf = float(datalist[1])
    # if target parameter is not there, end 
    if len(textlist) == 1:
        setLog('end')
        soundasync(textlist[0]+'.wav')
        flg = True
        return
    if textlist[1] == '':
        setLog('end')
        soundasync(textlist[0]+'.wav')
        flg = True
        return
    # if target locate on screen, end 
    if pyautogui.locateOnScreen(textlist[1],confidence=conf) is None:
        setLog('retry')
        soundasync('isnai.wav')
        return
    flg = True

    # postprocessing
    setLog('end')
    soundasync(textlist[0]+'.wav')

# execute application operation
#run/C:\\appli\aplli.bat/sync=(True|False)/pause=5/
def runS(textlist):
    # global value
    global paustim
    # initialize dafault parameter
    pausetime = paustim
    sync = False
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
        # synchronize
        if datalist[0] == 'sync':
            if datalist[1] == 'True':
                sync = True
    setLog(textlist[1] + ' wo kidou')
    soundasync(textlist[0]+'.wav')
    # run application
    if sync == True:
        # run with synchronize
        subprocess.run(textlist[1])
    if sync == False:
        # run with unsynchronize
        subprocess.Popen(textlist[1])

    # postprocessing
    time.sleep(pausetime)

# file operation
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/1.txt/pause=5/
def fileS(textlist):
    # global value
    global paustim
    # initialize dafault parameter
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    # if file1 is folder, end
    if os.path.isdir(textlist[1]) == True:
        soundasync('isfnai.wav')
        time.sleep(pausetime)
        return
    # if file1 upper folder is not there, end
    if os.path.exists(os.path.dirname(textlist[1])) == False:
        soundasync('isfnai.wav')
        time.sleep(pausetime)
        return
    # if file1 is not there, end
    if os.path.exists(textlist[1]) == False:
        soundasync('isfnai.wav')
        time.sleep(pausetime)
        return
    # file move
    if textlist[0] == 'fmove':
        # if file2 upper folder is not there, end
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            soundasync('isfnai.wav')
            time.sleep(pausetime)
            return
        # if file2 is there, end
        if os.path.exists(textlist[2]) == True:
            soundasync('isfaru.wav')
            time.sleep(pausetime)
            return
        soundasync(textlist[0]+'.wav')
        # file move
        shutil.move(textlist[1],textlist[2])
    # file copy
    if textlist[0] == 'fcopy':
        # if file2 upper folder is not there, end
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            soundasync('isfnai.wav')
            time.sleep(pausetime)
            return
        # if file2 is there, end
        if os.path.exists(textlist[2]) == True:
            soundasync('isfaru.wav')
            time.sleep(pausetime)
            return
        soundasync(textlist[0]+'.wav')
        # file copy
        shutil.copy2(textlist[1],textlist[2])
    # file delete
    if textlist[0] == 'fdelete':
        soundasync(textlist[0]+'.wav')
        os.remove(textlist[1])

    # postprocessing
    time.sleep(pausetime)

# folder operation
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/1.txt/pause=5/
def folderS(textlist):
    # global value
    global paustim
    # initialize dafault parameter
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    # if folder1 is file, end
    if os.path.isfile(textlist[1]) == True:
        soundasync('isfnai.wav')
        time.sleep(pausetime)
        return
    # if folder1 is not there, end
    if os.path.exists(textlist[1]) == False:
        soundasync('isfnai.wav')
        time.sleep(pausetime)
        return

    # postprocessing
    soundasync(textlist[0]+'.wav')
    # open explorer with folder path
    subprocess.run('explorer '+textlist[1])
    time.sleep(pausetime)

# conditional branch operation
#if/1/==/1/5/7/
def ifS(textlist):
    # global value
    global skillidx
    flg = False
    # if match, flg is True
    # equal condition
    if textlist[2] == '==':
        if textlist[1] == textlist[3]:
            flg = True
    # less than condition
    if textlist[2] == '<':
        if int(textlist[1]) < int(textlist[3]):
            flg = True
    # less than equal condition
    if textlist[2] == '<=':
        if int(textlist[1]) <= int(textlist[3]):
            flg = True
    # greater than condition
    if textlist[2] == '>':
        if int(textlist[1]) > int(textlist[3]):
            flg = True
    # greater than equal condition
    if textlist[2] == '>=':
        if int(textlist[1]) >= int(textlist[3]):
            flg = True
    # not equal condition
    if textlist[2] == '!=':
        if textlist[1] != textlist[3]:
            flg = True

    # flg is True, go to 1, else go to 2
    if flg == True:
        soundasync('bunkiT.wav')
        skillidx = int(textlist[4]) - 2
        setLog('True : go to '+int(skillidx+1))
    else:
        soundasync('bunkiF.wav')
        skillidx = int(textlist[5]) - 2
        setLog('False : go to '+int(skillidx+1))

# conditional branch by image operation
#ifimg/★.png/5/7/accuracy=0.8/
def ifimgS(textlist):
    # global value
    global skillidx
    global accurcy
    # initialize dafault parameter
    conf = accurcy
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            conf = float(datalist[1])
    # locate target position on screen
    target = pyautogui.locateOnScreen(imgpath+textlist[1],confidence=conf)
    # if target is there, go to 1, else go to 2
    if target is None:
        soundasync('bunkiF.wav')
        skillidx = int(textlist[3]) - 2
        setLog('False : go to '+int(skillidx+1))
    else:
        soundasync('bunkiT.wav')
        skillidx = int(textlist[2]) - 2
        setLog('True : go to '+int(skillidx+1))

# repete operation
#for/quantity=5/start=5/length=10
def forS(textlist):
    # global value
    global txtlist
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # loop quanity
        if datalist[0] == 'quantity':
            quantity = int(datalist[1])
        # start index
        if datalist[0] == 'start':
            start = int(datalist[1])
        # to index + length
        if datalist[0] == 'length':
            length = int(datalist[1])
    soundasync(textlist[0]+'.wav')
    setLog('Loop quanity : '+str(quantity)+' ,start : '+str(start)+' ,length : '+str(length))
    # loop
    for i in range(quantity-1):
        for j in range(length):
            callS(txtlist[start-1+j])

# repete by image operation
#forimg/★.png/quantity=5/start=5/length=10/out=True/accuracy=0.8/
def forimgS(textlist):
    # global value
    global txtlist
    global accurcy
    # initialize dafault parameter
    conf = accurcy
    out = False
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # loop quanity
        if datalist[0] == 'quantity':
            quantity = int(datalist[1])
        # start index
        if datalist[0] == 'start':
            start = int(datalist[1])
        # to index + length
        if datalist[0] == 'length':
            length = int(datalist[1])
        # [while image out of screen] is True
        # [while image is displayed] is False
        if datalist[0] == 'out':
            if datalist[1] == 'True':
                out = True
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            conf = datalist[1]
        # locate target position on screen
        target = pyautogui.locateOnScreen(imgpath+textlist[1],confidence=conf)
        # if target is there and out is True, go to loop
        # if target is nothing and out is False, go to loop
        if (target is None and out == True) or (target is not None and out == False):
            soundasync(textlist[0]+'.wav')
            setLog('Loop quanity : '+str(quantity)+' ,start : '+str(start)+' ,length : '+str(length))
            # loop
            for i in range(quantity-1):
                for j in range(length):
                    callS(txtlist[start-1+j])

# clipboard operation
def clipS(textlist):
    # global value
    global paustim
    # initialize dafault parameter
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    # copy to clipboard
    if textlist[0] == 'ccopy':
        pyperclip.copy(textlist[1])
    # paste with keyboard typing
    if textlist[0] == 'cpaste':
        pyautogui.hotkey('ctrl','v')

    # postprocessing
    soundasync(textlist[0]+'.wav')
    time.sleep(pausetime)

# clipboard operation
#untill/★.png/out=True/accuracy=0.8/pause=1/
def untillS(textlist):
    # global value
    global paustim
    global accurcy
    # initialize dafault parameter
    conf = accurcy
    out = False
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # [untill image out of screen] is True
        # [untill image is displayed] is False
        if datalist[0] == 'out':
            if datalist[1] == 'True':
                out = True
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            conf = datalist[1]
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    while True:
        # locate target position on screen
        target = pyautogui.locateOnScreen(imgpath+textlist[1],confidence=conf)
        # if target is there and out is True, go to next
        # if target is nothing and out is False, go to next
        if target is None and out == True:
            setLog(textlist[1]+' out of screen')
            break
        if target is not None and out == False:
            setLog(textlist[1]+' is displayed')
            break
        time.sleep(pausetime)
# scroll operation
#(scrollup|scrolldown)/5/pause=1/
def scrollS(textlist):
    # global value
    global paustim
    # initialize dafault parameter
    pausetime = paustim
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # pause
        if datalist[0] == 'pause':
            pausetime = int(datalist[1])
    if textlist[0] == 'scrollup':
        pyautogui.vscroll(100*int(textlist[1]))
    if textlist[0] == 'scrolldown':
        pyautogui.vscroll(-100*int(textlist[1]))
    if textlist[0] == 'scrollleft':
        pyautogui.hscroll(-100*int(textlist[1]))
    if textlist[0] == 'scrollright':
        pyautogui.hscroll(100*int(textlist[1]))
    # postprocessing
    setLog(textlist[1])
    soundasync(textlist[0]+'.wav')
    time.sleep(pausetime)

# output log
def setLog(text):
    print(text)

# playsound internal process
def playsoundIP(name):
    # global value
    global sndpath
    playsound.playsound(sndpath+name)

# playsound threading process
def soundasync(name):
    thread = threading.Thread(target=playsoundIP,kwargs={'name': name})
    thread.start()

# analysis and call operation
def callS(txt):
    # global value
    global skillidx
    # split '/' and delete new line code
    txtlistlist = txt.replace('\n', '').split('/')
    print(skillidx,txtlistlist)
    # analysis first text
    # click
    if txtlistlist[0] == 'click':
        clickS(txtlistlist)
    # dclick
    if txtlistlist[0] == 'dclick':
        clickS(txtlistlist)
    # rclick
    if txtlistlist[0] == 'rclick':
            clickS(txtlistlist)
    # move
    if txtlistlist[0] == 'move':
        clickS(txtlistlist)
    # drag
    if txtlistlist[0] == 'drag':
        clickS(txtlistlist)
    # zclick
    if txtlistlist[0] == 'zclick':
        pclickS(txtlistlist)
    # pclick
    if txtlistlist[0] == 'pclick':
        pclickS(txtlistlist)
    # pdclick
    if txtlistlist[0] == 'pdclick':
        pclickS(txtlistlist)
    # prclick
    if txtlistlist[0] == 'prclick':
        pclickS(txtlistlist)
    # pmove
    if txtlistlist[0] == 'pmove':
        pclickS(txtlistlist)
    # pdrag
    if txtlistlist[0] == 'pdrag':
        pclickS(txtlistlist)
    # typing
    if txtlistlist[0] == 'typing':
        typingS(txtlistlist)
    # press
    if txtlistlist[0] == 'press':
        typingS(txtlistlist)
    # keydown
    if txtlistlist[0] == 'keydown':
        typingS(txtlistlist)
    # keyup
    if txtlistlist[0] == 'keyup':
        typingS(txtlistlist)
    # hotkey
    if txtlistlist[0] == 'hotkey':
        typingS(txtlistlist)
    # pause
    if txtlistlist[0] == 'pause':
        pauseS(txtlistlist)
    # end
    if txtlistlist[0] == 'end':
        endS(txtlistlist)
    # run
    if txtlistlist[0] == 'run':
        runS(txtlistlist)
    # fmove
    if txtlistlist[0] == 'fmove':
        fileS(txtlistlist)
    # fcopy
    if txtlistlist[0] == 'fcopy':
        fileS(txtlistlist)
    # fdelete
    if txtlistlist[0] == 'fdelete':
        fileS(txtlistlist)
    # folder
    if txtlistlist[0] == 'folder':
        folderS(txtlistlist)
    # if
    if txtlistlist[0] == 'if':
        ifS(txtlistlist)
    # ifimg
    if txtlistlist[0] == 'ifimg':
        ifimgS(txtlistlist)
    # for
    if txtlistlist[0] == 'for':
        forS(txtlistlist)
    # forimg
    if txtlistlist[0] == 'forimg':
        forimgS(txtlistlist)
    # ccopy
    if txtlistlist[0] == 'ccopy':
        clipS(txtlistlist)
    # cpaste
    if txtlistlist[0] == 'cpaste':
        clipS(txtlistlist)
    # untill
    if txtlistlist[0] == 'untill':
        untillS(txtlistlist)
    # scrollup
    if txtlistlist[0] == 'scrollup':
        scrollS(txtlistlist)
    # scrolldown
    if txtlistlist[0] == 'scrolldown':
        scrollS(txtlistlist)
    # scrollleft
    if txtlistlist[0] == 'scrollleft':
        scrollS(txtlistlist)
    # scrollright
    if txtlistlist[0] == 'scrollright':
        scrollS(txtlistlist)

# start skill
def startS(skill):
    # global value
    global skillidx
    global txtlist
    # read input text and add to list one line by a time
    with open(skill,mode='r',encoding='utf-8') as f:
        txtlist = f.readlines()
    maxidx = len(txtlist)
    skillidx = 0
    # loop with skill index to max index
    while True:
        if skillidx >= maxidx:
            break
        callS(txtlist[skillidx])
        skillidx += 1

# main
def main():
    # loop while flg become True
    while True:
        # if can get args, set argv, else set skill1.txt
        if len(args) > 1:
            startS(txtpath+str(args[1]))
        else:
            startS(txtpath+'skill1.txt')
        # if flg is true, break this loop
        if flg == True:
            break

# get exceute file path
# __file__ : [absolute path + file name] and get folder path by dirname(__file__)
if os.path.dirname(__file__) != '':
    # default file path change to exec file path for process
    os.chdir(os.path.dirname(__file__))

# set config.ini parameter
configini = configparser.ConfigParser()
configini.read('config.ini',encoding='utf-8')

imgpath = configini.get('SKILL','ImgPath')
txtpath = configini.get('SKILL','TxtPath')
sndpath = configini.get('SKILL','SndPath')
paustim = int(configini.get('SKILL','PausTim'))
accurcy = float(configini.get('SKILL','Accurcy'))

# main loop flg set False
flg = False
# get command line vector
args = sys.argv

if __name__ == '__main__':
    main()
