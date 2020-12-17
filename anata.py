#! python3
# anata.py - execute skill

# time
import time
# GUI automation
import pyautogui
# file path and control
import os
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
# webbrowser
import webbrowser
# itertools
import itertools
# util
import util

# click operation
#(click|dclick|rclick|move|drag)/★.png/accuracy=0.8/movepin=12,12/pause=1/
def clickS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    accuracy = option.get('accuracy')
    movepinx, movepiny = option.get('movepinx'), option.get('movepiny')

    # locate target position on screen
    target = util.locatescreen(textlist[1],accuracy)
    # if target is none, end
    if target is None:
        util.setLog(textlist[1]+' nai')
        time.sleep(pause)
        return
    # target center position
    x, y = pyautogui.center(target)
    # move target position
    x, y = x + movepinx, y + movepiny
    # input to screen
    # click once
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
    util.setLog(str(x)+', '+str(y)+' wo '+textlist[0])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# position click operation
#(pclick|pdclick|prclick|pmove|pdrag|zclick)/x=500/y=200/xmax=500/ymax=200/xmin=500/ymin=200/pause=1/
def pclickS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    xmax, xmin, ymax, ymin = option.get('xmax'), option.get('xmin'), option.get('ymax'), option.get('ymin')
    pause = option.get('pause')

    if textlist[0] == 'zclick':
        # random x, y
        x, y = random.randint(xmin, xmax), random.randint(ymin, ymax)
    # input to screen
    # click once
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
    util.setLog(str(x)+', '+str(y)+' wo '+textlist[0])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# typing operation
#(typing|press|keydown|keyup|hotkey)/hello/pause=1/
def typingS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

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
    # press multi keys
    if textlist[0] == 'hotkey':
        pyautogui.hotkey(textlist[1],textlist[2])

    # postprocessing
    util.setLog(textlist[1]+' wo '+textlist[0])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# pause operation
#pause/1/
def pauseS(textlist):
    # pause
    time.sleep(int(textlist[1]))

    # postprocessing
    util.setLog(textlist[1]+' byou tomaru')
    util.soundasync(textlist[0]+'.wav')

# end operation
#end/★.png/
def endS(textlist):
    # global value
    global flg
    # set option parameter
    option = util.setoption(textlist)
    accuracy = option.get('accuracy')

    # if target parameter is not there, end 
    if len(textlist) == 1:
        util.setLog('owari')
        util.soundasync(textlist[0]+'.wav')
        flg = True
        return
    if textlist[1] == '':
        util.setLog('owari')
        util.soundasync(textlist[0]+'.wav')
        flg = True
        return
    # if target locate on screen, end 
    target = util.locatescreen(textlist[1],accuracy)
    if target is None:
        util.setLog('owaranai')
        util.soundasync('isnai.wav')
        return
    flg = True

    # postprocessing
    util.setLog('owari')
    util.soundasync(textlist[0]+'.wav')

# execute application operation
#run/C:\\appli\aplli.bat/sync=(True|False)/pause=5/
def runS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    sync = option.get('sync')

    util.setLog(textlist[1] + ' wo kidou')
    util.soundasync(textlist[0]+'.wav')
    # run application
    if sync == True:
        # run with synchronize
        subprocess.run(textlist[1])
    if sync == False:
        # run with unsynchronize
        subprocess.Popen(textlist[1])

    # postprocessing
    time.sleep(pause)

# file operation
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/1.txt/pause=5/
def fileS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    # if file1 is folder, end
    if os.path.isdir(textlist[1]) == True:
        util.soundasync('isfnai.wav')
        time.sleep(pause)
        return
    # if file1 upper folder is not there, end
    if os.path.exists(os.path.dirname(textlist[1])) == False:
        util.soundasync('isfnai.wav')
        time.sleep(pause)
        return
    # if file1 is not there, end
    if os.path.exists(textlist[1]) == False:
        util.soundasync('isfnai.wav')
        time.sleep(pause)
        return
    # file move
    if textlist[0] == 'fmove':
        # if file2 upper folder is not there, end
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            util.soundasync('isfnai.wav')
            time.sleep(pause)
            return
        # if file2 is there, end
        if os.path.exists(textlist[2]) == True:
            util.soundasync('isfaru.wav')
            time.sleep(pause)
            return
        util.soundasync(textlist[0]+'.wav')
        # file move
        shutil.move(textlist[1],textlist[2])
    # file copy
    if textlist[0] == 'fcopy':
        # if file2 upper folder is not there, end
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            util.soundasync('isfnai.wav')
            time.sleep(pause)
            return
        # if file2 is there, end
        if os.path.exists(textlist[2]) == True:
            util.soundasync('isfaru.wav')
            time.sleep(pause)
            return
        util.soundasync(textlist[0]+'.wav')
        # file copy
        shutil.copy2(textlist[1],textlist[2])
    # file delete
    if textlist[0] == 'fdelete':
        util.soundasync(textlist[0]+'.wav')
        os.remove(textlist[1])

    # postprocessing
    time.sleep(pause)

# folder operation
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/1.txt/pause=5/
def folderS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    # if folder1 is file, end
    if os.path.isfile(textlist[1]) == True:
        util.soundasync('isfnai.wav')
        time.sleep(pause)
        return
    # if folder1 is not there, end
    if os.path.exists(textlist[1]) == False:
        util.soundasync('isfnai.wav')
        time.sleep(pause)
        return

    # postprocessing
    util.soundasync(textlist[0]+'.wav')
    # open explorer with folder path
    subprocess.run('explorer '+textlist[1])
    time.sleep(pause)

# conditional branch operation
#if/1/==/1/5/7/
#if/★.png/5/7/accuracy=0.8/
def ifS(textlist):
    # global value
    global skillidx
    # set option parameter
    option = util.setoption(textlist)
    accuracy = option.get('accuracy')

    target = textlist[2]
    check = checktarget(target)
    flg = False
    # locate target position on screen
    # if match, flg is True
    # equal condition
    if check == 'image':
        if target is not None:
            flg = True
        # flg is True, go to 1, else go to 2
        if flg == True:
            util.soundasync('bunkiT.wav')
            skillidx = int(textlist[3]) - 2
            util.setLog('True : go to '+int(skillidx+1))
        else:
            util.soundasync('bunkiF.wav')
            skillidx = int(textlist[4]) - 2
            util.setLog('False : go to '+int(skillidx+1))
        return
    if check == 'clip':
        target = pyperclip.paste()
    if textlist[2] == '==':
        if target == textlist[3]:
            flg = True
    # less than condition
    if textlist[2] == '<':
        if int(target) < int(textlist[3]):
            flg = True
    # less than equal condition
    if textlist[2] == '<=':
        if int(target) <= int(textlist[3]):
            flg = True
    # greater than condition
    if textlist[2] == '>':
        if int(target) > int(textlist[3]):
            flg = True
    # greater than equal condition
    if textlist[2] == '>=':
        if int(target) >= int(textlist[3]):
            flg = True
    # not equal condition
    if textlist[2] == '!=':
        if target != textlist[3]:
            flg = True
    # flg is True, go to 1, else go to 2
    if flg == True:
        util.soundasync('bunkiT.wav')
        skillidx = int(textlist[4]) - 2
        util.setLog('True : go to '+int(skillidx+1))
    else:
        util.soundasync('bunkiF.wav')
        skillidx = int(textlist[5]) - 2
        util.setLog('False : go to '+int(skillidx+1))

# repete operation
#for/quantity=5/start=5/length=10
#for/★.png/quantity=5/start=5/length=10/out=True/accuracy=0.8/
def forS(textlist):
    # global value
    global txtlist
    # set option parameter
    option = util.setoption(textlist)
    quantity, start, length = option.get('quantity'), option.get('start'), option.get('length')
    out = option.get('out')
    accuracy = option.get('accuracy')

    check = util.checktarget(textlist[1])
    if check == 'image':
        # locate target position on screen
        target = util.locatescreen(textlist[1],accuracy)
        # if target is there and out is True, go to loop
        # if target is nothing and out is False, go to loop
        if (target is None and out == True) or (target is not None and out == False):
            util.soundasync(textlist[0]+'.wav')
            util.setLog('Loop quanity : '+str(quantity)+' ,start : '+str(start)+' ,length : '+str(length))
            # loop
            for i, j in itertools.product(range(quantity-1),range(length)):
                callS(txtlist[start-1+j])
        return
    util.soundasync(textlist[0]+'.wav')
    util.setLog('Loop quanity : '+str(quantity)+' ,start : '+str(start)+' ,length : '+str(length))
    # loop
    for i, j in itertools.product(range(quantity-1),range(length)):
        callS(txtlist[start-1+j])

# clipboard operation
def clipS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    # copy to clipboard
    if textlist[0] == 'ccopy':
        pyperclip.copy(textlist[1])
    # paste with keyboard typing
    if textlist[0] == 'cpaste':
        pyautogui.hotkey('ctrl','v')

    # postprocessing
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# clipboard operation
#untill/★.png/out=True/accuracy=0.8/pause=1/
def untillS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    accuracy = option.get('accuracy')
    out = option.get('out')

    check = checktarget(textlist[1])
    while True:
        if check == 'clip':
            # locate target position on screen
            target = pyperclip.paste()
            # if target is there and out is True, go to next
            # if target is nothing and out is False, go to next
            if target != textlist[1] and out == True:
                util.setLog(textlist[1]+' out of clipboard')
                break
            if target == textlist[1] and out == False:
                util.setLog(textlist[1]+' clipboard in')
                break
        else:
            # locate target position on screen
            target = util.locatescreen(textlist[1],accuracy)
            # if target is there and out is True, go to next
            # if target is nothing and out is False, go to next
            if target is None and out == True:
                util.setLog(textlist[1]+' out of screen')
                break
            if target is not None and out == False:
                util.setLog(textlist[1]+' is displayed')
                break
        time.sleep(pause)

# scroll operation
#(scrollup|scrolldown)/5/pause=1/
def scrollS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    if textlist[0] == 'scrollup':
        pyautogui.vscroll(100*int(textlist[1]))
    if textlist[0] == 'scrolldown':
        pyautogui.vscroll(-100*int(textlist[1]))
    if textlist[0] == 'scrollleft':
        pyautogui.hscroll(-100*int(textlist[1]))
    if textlist[0] == 'scrollright':
        pyautogui.hscroll(100*int(textlist[1]))
    # postprocessing
    util.setLog(textlist[1])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# save & load text operation
#(save|load)/name/strength=★/
def saveS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    strength = option.get('strength')

    config = configparser.ConfigParser()
    config.read(savfile,encoding='utf-8')
    # save to save file
    if textlist[0] == 'save':
        #if strength is nothing, get clipboard
        if strength == 'clip':
            strength = pyperclip.paste()
            listi = strength.splitlines()
            strength = ''
            for data in listi:
                strength += data
        #if save section is nothing, get clipboard
        if config.has_section('SAVE') == False:
            config.add_section('SAVE')
        # write to save file
        config.set('SAVE',textlist[1],strength)
        with open(savfile,'w') as file:
            config.write(file)
    # load from save file
    if textlist[0] == 'load':
        # set to clipboard
        pyperclip.copy(config.get('SAVE',textlist[1]))
    # postprocessing
    util.setLog(textlist[0]+' '+textlist[1])
    util.soundasync(textlist[0]+'.wav')

#(replace|upper|lower|uppercase|lowercase|extract)/★/■
def textS(textlist):
    tmp = textlist[1]
    check = util.checktarget(tmp)
    if check == 'clip':
        tmp = pyperclip.paste()
    if textlist[0] == 'replace':
        tmp = tmp.replace(textlist[1], textlist[2])
    if textlist[0] == 'upper':
        tmp = tmp.upper()
    if textlist[0] == 'lower':
        tmp = tmp.lower()
    if textlist[0] == 'uppercase':
        tmp = util.ulcasetxt(tmp,'upper')
    if textlist[0] == 'lowercase':
        tmp = util.ulcasetxt(tmp,'lower')
    if textlist[0] == 'extract':
        tmp = util.geturl(tmp)
    pyperclip.copy(tmp)
    # postprocessing
    util.setLog(tmp)
    util.soundasync(textlist[0]+'.wav')

#jumpurl/pause=5/
def jumpurlS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    target = pyperclip.paste()
    target = util.geturl(target)
    if util.checkurl(target) == False:
        return
    # run webbrowser
    webbrowser.open(target)
    # postprocessing
    util.setLog('go to '+target)
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

#getdate/yyyymmdd/month=1/
def getdateS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    # postprocessing
    util.setLog(textlist[1])
    #util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)
    # getdate
    if txtlistlist[0] == 'getdate':
        getdateS(txtlistlist)

# analysis and call operation
def callS(txt):
    # global value
    global skillidx
    txtlistlist = util.reptxt(txt)
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
    # for
    if txtlistlist[0] == 'for':
        forS(txtlistlist)
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
    # save
    if txtlistlist[0] == 'save':
        saveS(txtlistlist)
    # load
    if txtlistlist[0] == 'load':
        saveS(txtlistlist)
    # replace
    if txtlistlist[0] == 'replace':
        textS(txtlistlist)
    # upper
    if txtlistlist[0] == 'upper':
        textS(txtlistlist)
    # lowercase
    if txtlistlist[0] == 'lower':
        textS(txtlistlist)
    # uppercase
    if txtlistlist[0] == 'uppercase':
        textS(txtlistlist)
    # lowercase
    if txtlistlist[0] == 'lowercase':
        textS(txtlistlist)
    # extract
    if txtlistlist[0] == 'extract':
        textS(txtlistlist)
    # jumpurl
    if txtlistlist[0] == 'jumpurl':
        jumpurlS(txtlistlist)
    # getdate
    if txtlistlist[0] == 'getdate':
        getdateS(txtlistlist)

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

txtpath = configini.get('SKILL','TxtPath')
savfile = configini.get('SKILL','SavFile')

# main loop flg set False
flg = False
# get command line vector
args = sys.argv

if __name__ == '__main__':
    main()
