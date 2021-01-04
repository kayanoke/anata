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
# regex
import re
# log
import logging

#logging.basicConfig(filename='logger.log',level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')
#logging.debug('anata.py start')

# click operation by image recognition
#(click|dclick|rclick|move|drag)/★.png/accuracy=0.8/shiftpin=12,12/pause=1/
def clickS(textlist):
    #logging.basicConfig(filename='logger.log',level=logging.DEBUG,format=' %(asctime)s - %(levelname)s - %(message)s')
    #logging.debug('clickS start')
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    accuracy = option.get('accuracy')
    shiftpinx, shiftpiny = option.get('shiftpinx'), option.get('shiftpiny')
    clickduration = option.get('clickduration')
    dragduration = option.get('dragduration')

    # locate target position on screen
    target = util.locatescreen(textlist[1],accuracy)
    # if target is none, end
    if target is None:
        util.setLog(textlist[1]+' nai')
        time.sleep(pause)
        return
    # target center position
    x, y = pyautogui.center(target)
    # shift target position
    x, y = x + shiftpinx, y + shiftpiny
    # output to screen
    # click once
    if textlist[0] == 'click':
        pyautogui.click(x,y,duration=clickduration)
    # double click
    if textlist[0] == 'dclick':
        pyautogui.doubleClick(x,y,duration=clickduration)
    # right click
    if textlist[0] == 'rclick':
        pyautogui.rightClick(x,y,duration=clickduration)
    # move to target
    if textlist[0] == 'move':
        pyautogui.moveTo(x,y,duration=clickduration)
    # drag to taget
    if textlist[0] == 'drag':
        pyautogui.dragTo(x,y,duration=dragduration,button='left')

    # postprocessing
    util.setLog(str(x)+', '+str(y)+' wo '+textlist[0])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)
    #logging.debug('clickS end')

# click operation click by position
#(clickp|dclickp|rclickp|movep|dragp|clickz)/x=500/y=200/xmax=500/ymax=200/xmin=500/ymin=200/pause=1/
def clickpS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    xmax, xmin, ymax, ymin = option.get('xmax'), option.get('xmin'), option.get('ymax'), option.get('ymin')
    pause = option.get('pause')
    clickduration = option.get('clickduration')
    dragduration = option.get('dragduration')

    if textlist[0] == 'clickz':
        # random x, y
        x, y = random.randint(xmin, xmax), random.randint(ymin, ymax)
        pyautogui.click(x,y,duration=clickduration)
    # output to screen
    # click once
    if textlist[0] == 'clickp':
        pyautogui.click(x,y,duration=clickduration)
    # double click
    if textlist[0] == 'dclickp':
        pyautogui.doubleClick(x,y,duration=clickduration)
    # right click
    if textlist[0] == 'rclickp':
        pyautogui.rightClick(x,y,duration=clickduration)
    # move to target
    if textlist[0] == 'movep':
        pyautogui.moveTo(x,y,duration=clickduration)
    # drag to taget
    if textlist[0] == 'dragp':
        pyautogui.dragTo(x,y,1,button='left',duration=dragduration)

    # postprocessing
    util.setLog(str(x)+', '+str(y)+' wo '+textlist[0])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# key operation
#(typing|press|keydown|keyup|hotkey)/hello(/v)/pause=1/
def typingS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    interval = option.get('interval')

    # output to screen
    # keyboard typing
    if textlist[0] == 'typing':
        tmp = pyperclip.paste()
        print(tmp,pyperclip.paste(),textlist[1])
        pyperclip.copy(textlist[1])
        pyautogui.hotkey('ctrl','v')
        time.sleep(1)
        pyperclip.copy(tmp)
        #pyautogui.typewrite(textlist[1],interval=interval)
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
    # press triplekey keys
    if textlist[0] == 'triplekey':
        pyautogui.keyDown(textlist[1])
        pyautogui.keyDown(textlist[2])
        pyautogui.press(textlist[3])
        pyautogui.keyUp(textlist[1])
        pyautogui.keyUp(textlist[2])

    # postprocessing
    util.setLog(textlist[1]+' wo '+textlist[0])
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# pause operation
#pause/5/
def pauseS(textlist):
    # pause
    time.sleep(int(textlist[1]))

    # postprocessing
    util.setLog(textlist[1]+' byou tomaru')
    util.soundasync(textlist[0]+'.wav')

# end operation
#end/★.png/accuracy=0.8/
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

# launch app operation
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
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/2.txt/pause=5/
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
#(folder)/C:\\app/1.txt/pause=5/
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

    check = util.checktarget(textlist[1])
    flg = False
    # locate target position on screen
    # if match, flg is True
    if check == 'image':
        target = util.locatescreen(textlist[1],accuracy)
        if target is not None:
            flg = True
        # flg is True, go to 1, else go to 2
        if flg == True:
            util.soundasync('bunkiT.wav')
            skillidx = int(textlist[2]) - 2
            util.setLog('True : go to '+int(skillidx+1))
        else:
            util.soundasync('bunkiF.wav')
            skillidx = int(textlist[3]) - 2
            util.setLog('False : go to '+int(skillidx+1))
        return
    # target is not image
    target = textlist[1]
    if check == 'clip':
        target = pyperclip.paste()
    # equal condition
    if textlist[2] == '==' or textlist[2] == '=':
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
    if textlist[2] == '!=' or textlist[2] == '<>':
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
def forS(textlist):
    # global value
    global txtlist
    # set option parameter
    option = util.setoption(textlist)
    quantity, start, length = option.get('quantity'), option.get('start'), option.get('length')
    util.soundasync(textlist[0]+'.wav')
    util.setLog('Loop quanity : '+str(quantity)+' ,start : '+str(start)+' ,length : '+str(length))
    # loop
    for i, j in itertools.product(range(quantity-1),range(length)):
        callS(txtlist[start-1+j])

# clipboard operation
#(copy|paste)/★/pause=5/
def clipS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    # copy to clipboard
    if textlist[0] == 'copy':
        pyperclip.copy(textlist[1])
    # paste with keyboard typing
    if textlist[0] == 'paste':
        pyautogui.hotkey('ctrl','v')

    # postprocessing
    util.soundasync(textlist[0]+'.wav')
    time.sleep(pause)

# wait untill match operation
#untill/(★.png|string)/out=True/accuracy=0.8/pause=1/
def untillS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    accuracy = option.get('accuracy')
    out = option.get('out')

    check = util.checktarget(textlist[1])
    while True:
        if check == 'image':
            # target is image
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
        else:
            # target is string
            target = pyperclip.paste()
            # if target is there and out is True, go to next
            # if target is nothing and out is False, go to next
            if target != textlist[1] and out == True:
                util.setLog(textlist[1]+' out of clipboard')
                break
            if target == textlist[1] and out == False:
                util.setLog(textlist[1]+' clipboard in')
                break
            # regex search
            if re.search(textlist[1], target) is None and out == True:
                util.setLog(textlist[1]+' search out')
                break
            if re.search(textlist[1], target) is not None and out == False:
                util.setLog(textlist[1]+' search in')
                break
        time.sleep(pause)

# scroll operation
#(scrollup|scrolldown|scrollleft|scrollright)/5/pause=1/
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
#(save|load)/name/string=★/
def saveS(textlist):
    # global value
    global savfile
    # set option parameter
    option = util.setoption(textlist)
    string = option.get('string')

    config = configparser.ConfigParser()
    config.read(savfile,encoding='utf-8')
    # save to save file
    if textlist[0] == 'save':
        #if string is nothing or clip, get clipboard
        if string == 'clip' or string == '':
            cliplist = pyperclip.paste().splitlines()
            string = ''
            for data in cliplist:
                string += data
        #if save section is nothing, get clipboard
        if config.has_section('SAVE') == False:
            config.add_section('SAVE')
        # write to save file
        config.set('SAVE',textlist[1],string)
        with open(savfile,'w') as file:
            config.write(file)
    # load from save file
    if textlist[0] == 'load':
        # set to clipboard
        pyperclip.copy(config.get('SAVE',textlist[1]))
    # postprocessing
    util.setLog(textlist[0]+' '+textlist[1])
    util.soundasync(textlist[0]+'.wav')

# clioboard exchange operation
#(replace|upper|lower|uppercase|lowercase|extract)/★/■/
def textS(textlist):
    tmp = textlist[1]
    # set option parameter
    option = util.setoption(textlist)
    string = option.get('string')
    check = util.checktarget(tmp)
    #if string is nothing or clip, get clipboard
    if check == 'clip' or string == '':
        tmp = pyperclip.paste()
        print(tmp)
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
    util.setLog('clip : '+tmp)
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

#date copy operation
#date/YYYYMMDD/year=1/month=1/day=1/string=firstday/
def dateS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    year = option.get('year')
    month = option.get('month')
    day = option.get('day')
    string = option.get('string')

    text = util.getdatetime(textlist[1],year,month,day,string)
    pyperclip.copy(text)

    # postprocessing
    util.setLog(text+' copy')
    util.soundasync(textlist[0]+'.wav')

# unill and click operation
def meikaS(textlist):
    # set option parameter
    #meika/1.png/0~3/a~~~
    foruntill = []
    forclick = []
    i = 0
    for text in textlist:
        if i == 0:
            foruntill.append('untill')
            forclick.append('dummy')
        elif i == 2:
            forclick[0] = text
        else:
            foruntill.append(text)
            forclick.append(text)
        i += 1
    untillS(foruntill)
    clickS(forclick)

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
    # clickz
    if txtlistlist[0] == 'clickz':
        clickpS(txtlistlist)
    # clickp
    if txtlistlist[0] == 'clickp':
        clickpS(txtlistlist)
    # dclickp
    if txtlistlist[0] == 'dclickp':
        clickpS(txtlistlist)
    # rclickp
    if txtlistlist[0] == 'rclickp':
        clickpS(txtlistlist)
    # movep
    if txtlistlist[0] == 'movep':
        clickpS(txtlistlist)
    # dragp
    if txtlistlist[0] == 'dragp':
        clickpS(txtlistlist)
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
    # triplekey
    if txtlistlist[0] == 'triplekey':
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
    # copy
    if txtlistlist[0] == 'copy':
        clipS(txtlistlist)
    # paste
    if txtlistlist[0] == 'paste':
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
    # date
    if txtlistlist[0] == 'date':
        dateS(txtlistlist)
    # meika
    if txtlistlist[0] == 'meika':
        meikaS(txtlistlist)

# start skill
def startS(skill):
    #logging.debug('startS start')
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
    #logging.debug('startS end')

# multi
def multi(name='skill1.txt'):
    # global value
    global txtpath
    global flg
    # loop while flg become True
    while True:
        # if can get args, set argv, else set skill1.txt
        startS(txtpath+name)
        # if flg is true, break this loop
        if flg == True:
            break

# init
def init():
    #logging.debug('init start')
    # global value
    global savfile
    global txtpath
    global flg
    # main loop flg set False
    flg = False
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

    # set config.ini parameter
    configini = configparser.ConfigParser()
    configini.read('config.ini',encoding='utf-8')
    txtpath = configini.get('SKILL','TxtPath')
    savfile = configini.get('SKILL','SavFile')
    #logging.debug('init end')

# main
def main():
    #logging.debug('main start')
    # global value
    global flg
    global txtpath

    # get command line vector
    args = sys.argv

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
    #logging.debug('main end')

init()
if __name__ == '__main__':
    main()

#logging.debug('anata.py end')
