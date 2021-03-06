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

# click operation by image recognition
#(click|dclick|rclick|move|drag)/★.png/accuracy=0.8/shiftpin=12,12/pause=1/
def clickS(textlist):
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
        util.infoLog(textlist[1]+' nai')
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
    util.infoLog(str(x)+', '+str(y)+' wo '+textlist[0])
    util.soundlog(textlist[0]+'.wav')
    time.sleep(pause)

# click operation click by position
#(clickp|dclickp|rclickp|movep|dragp|clickz)/x=500/y=200/xmax=500/ymax=200/xmin=500/ymin=200/pause=1/
def clickpS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    x, y = option.get('x'), option.get('y')
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
        pyautogui.dragTo(x,y,button='left',duration=dragduration)

    # postprocessing
    util.infoLog(str(x)+', '+str(y)+' wo '+textlist[0])
    util.soundlog(textlist[0]+'.wav')
    time.sleep(pause)

# key operation
#(typing|press|keydown|keyup|hotkey|triplekey)/hello(/v)/pause=1/
def typingS(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    interval = option.get('interval')

    # output to screen
    # keyboard typing
    if textlist[0] == 'typing':
        tmp = pyperclip.paste()
        pyperclip.copy(textlist[1])
        pyautogui.hotkey('ctrl','v')
        time.sleep(1)
        pyperclip.copy(tmp)
    # keyboard typing2
    if textlist[0] == 'typing2':
        pyautogui.typewrite(textlist[1],interval=interval)
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
    util.infoLog(textlist[1]+' wo '+textlist[0])
    util.soundlog(textlist[0]+'.wav')
    time.sleep(pause)

# pause operation
#pause/5/
def pause(textlist):
    # pause
    time.sleep(int(textlist[1]))

    # postprocessing
    util.infoLog(textlist[1]+' byou tomaru')
    util.soundlog(textlist[0]+'.wav')

# end operation
#end/★.png/accuracy=0.8/
def end(textlist):
    # global value
    global flg
    # set option parameter
    option = util.setoption(textlist)
    accuracy = option.get('accuracy')
    out = option.get('out')

    # if target parameter is not there, end 
    if len(textlist) == 1:
        util.infoLog('owari')
        util.soundlog(textlist[0]+'.wav')
        flg = True
        return
    if textlist[1] == '':
        util.infoLog('owari')
        util.soundlog(textlist[0]+'.wav')
        flg = True
        return
    # if target locate on screen, end 
    target = util.locatescreen(textlist[1],accuracy)
    if target is None and out == False:
        util.infoLog('owaranai')
        util.soundlog('isnai.wav')
        return
    if target is not None and out == True:
        util.infoLog('owaranai')
        util.soundlog('isnai.wav')
        return
    flg = True

    # postprocessing
    util.infoLog('owari')
    util.soundlog(textlist[0]+'.wav')

# launch app operation
#run/C:\\appli\aplli.bat/sync=(True|False)/pause=5/
def run(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    sync = option.get('sync')

    util.infoLog(textlist[1] + ' wo kidou')
    util.soundlog(textlist[0]+'.wav')
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
        util.soundlog('isfnai.wav')
        time.sleep(pause)
        return
    # if file1 upper folder is not there, end
    if os.path.exists(os.path.dirname(textlist[1])) == False:
        util.soundlog('isfnai.wav')
        time.sleep(pause)
        return
    # if file1 is not there, end
    if os.path.exists(textlist[1]) == False:
        util.soundlog('isfnai.wav')
        time.sleep(pause)
        return
    # file move
    if textlist[0] == 'fmove':
        # if file2 upper folder is not there, end
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            util.soundlog('isfnai.wav')
            time.sleep(pause)
            return
        # if file2 is there, end
        if os.path.exists(textlist[2]) == True:
            util.soundlog('isfaru.wav')
            time.sleep(pause)
            return
        util.soundlog(textlist[0]+'.wav')
        # file move
        shutil.move(textlist[1],textlist[2])
    # file copy
    if textlist[0] == 'fcopy':
        # if file2 upper folder is not there, end
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            util.soundlog('isfnai.wav')
            time.sleep(pause)
            return
        # if file2 is there, end
        if os.path.exists(textlist[2]) == True:
            util.soundlog('isfaru.wav')
            time.sleep(pause)
            return
        util.soundlog(textlist[0]+'.wav')
        # file copy
        shutil.copy2(textlist[1],textlist[2])
    # file delete
    if textlist[0] == 'fdelete':
        util.soundlog(textlist[0]+'.wav')
        os.remove(textlist[1])

    # postprocessing
    time.sleep(pause)

# folder operation
#(folder)/C:\\app/1.txt/pause=5/
def folder(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    # if folder1 is file, end
    if os.path.isfile(textlist[1]) == True:
        util.soundlog('isfnai.wav')
        time.sleep(pause)
        return
    # if folder1 is not there, end
    if os.path.exists(textlist[1]) == False:
        util.soundlog('isfnai.wav')
        time.sleep(pause)
        return

    # postprocessing
    util.soundlog(textlist[0]+'.wav')
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
            util.soundlog('bunkiT.wav')
            skillidx = int(textlist[2]) - 2
            util.infoLog('True : go to '+str(skillidx+1))
        else:
            util.soundlog('bunkiF.wav')
            skillidx = int(textlist[3]) - 2
            util.infoLog('False : go to '+str(skillidx+1))
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
        util.soundlog('bunkiT.wav')
        skillidx = int(textlist[4]) - 2
        util.infoLog('True : go to '+str(skillidx+1))
    else:
        util.soundlog('bunkiF.wav')
        skillidx = int(textlist[5]) - 2
        util.infoLog('False : go to '+str(skillidx+1))

# repete operation
#for/quantity=5/start=5/length=10
def forS(textlist):
    # global value
    global txtlist
    # set option parameter
    option = util.setoption(textlist)
    quantity, start, length = option.get('quantity'), option.get('start'), option.get('length')
    util.soundlog(textlist[0]+'.wav')
    util.infoLog('Loop quanity : '+str(quantity)+' ,start : '+str(start)+' ,length : '+str(length))
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
    util.soundlog(textlist[0]+'.wav')
    time.sleep(pause)

# wait until match operation
#until/(★.png|string)/out=True/accuracy=0.8/pause=1/
def until(textlist):
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
                util.infoLog(textlist[1]+' out of screen')
                break
            if target is not None and out == False:
                util.infoLog(textlist[1]+' is displayed')
                break
        else:
            # target is string
            target = pyperclip.paste()
            # if target is there and out is True, go to next
            # if target is nothing and out is False, go to next
            if target != textlist[1] and out == True:
                util.infoLog(textlist[1]+' out of clipboard')
                break
            if target == textlist[1] and out == False:
                util.infoLog(textlist[1]+' clipboard in')
                break
            # regex search
            if re.search(textlist[1], target) is None and out == True:
                util.infoLog(textlist[1]+' search out')
                break
            if re.search(textlist[1], target) is not None and out == False:
                util.infoLog(textlist[1]+' search in')
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
    util.infoLog(textlist[1])
    util.soundlog(textlist[0]+'.wav')
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
        with open(savfile,'w',encoding='utf-8') as file:
            config.write(file)
    # load from save file
    if textlist[0] == 'load':
        # set to clipboard
        pyperclip.copy(config.get('SAVE',textlist[1]))
    # postprocessing
    util.infoLog(textlist[0]+' '+textlist[1])
    util.soundlog(textlist[0]+'.wav')

# clioboard exchange operation
#(replace|upper|lower|uppercase|lowercase|extract)/★/■/
def textS(textlist):
    tmp = textlist[1]
    # set option parameter
    option = util.setoption(textlist)
    string = option.get('string')
    #if string is nothing or clip, get clipboard
    if string == 'clip' or string == '':
        tmp = pyperclip.paste()
    if textlist[0] == 'replace':
        tmp = util.replace(tmp,textlist[1], textlist[2])
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
    util.infoLog('clip : '+tmp)
    util.soundlog(textlist[0]+'.wav')

#jumpurl/pause=5/
def jumpurl(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')

    target = pyperclip.paste()
    target = util.geturl(target)
    if util.checkurl(target) == False:
        util.infoLog('url janai '+target)
        util.soundlog(textlist[0]+'.wav')
        return
    # run webbrowser
    webbrowser.open(target)
    # postprocessing
    util.infoLog('go to '+target)
    util.soundlog(textlist[0]+'.wav')
    time.sleep(pause)

#date copy operation
#date/YYYYMMDD/year=1/month=1/day=1/string=firstday/
def date(textlist):
    # set option parameter
    option = util.setoption(textlist)
    year = option.get('year')
    month = option.get('month')
    day = option.get('day')
    string = option.get('string')

    text = util.getdatetime(textlist[1],year,month,day,string)
    pyperclip.copy(text)

    # postprocessing
    util.infoLog(text+' copy')
    util.soundlog(textlist[0]+'.wav')

# launch app operation
#sound/★.wav/sync=False/pause=5/
def sound(textlist):
    # set option parameter
    option = util.setoption(textlist)
    pause = option.get('pause')
    sync = option.get('sync')

    util.infoLog(textlist[1] + ' wo nagasu')
    # play sound
    if sync == True:
        # play sound with synchronize
        util.playsoundIP(textlist[1])
    if sync == False:
        # play sound with unsynchronize
        util.soundasync(textlist[1])

    # postprocessing
    time.sleep(pause)

# until and click operation
#meika/1.png/0~3/a~~~
def meika(textlist):
    # set option parameter
    foruntil = []
    forclick = []
    i = 0
    for text in textlist:
        if i == 0:
            foruntil.append('until')
            forclick.append('dummy')
        elif i == 2:
            forclick[0] = text
        else:
            foruntil.append(text)
            forclick.append(text)
        i += 1
    until(foruntil)
    clickS(forclick)

#date copy operation
#untilKey/Enter/
def untilkey(textlist):

    util.untilKey(textlist[1])

    # postprocessing
    util.infoLog('let''s go next')
    #util.soundlog(textlist[0]+'.wav')

#date copy operation
#untilKey/Enter/
def untilmouse(textlist):

    util.untilMouse(textlist[1])

    # postprocessing
    util.infoLog('let''s go next')
    #util.soundlog(textlist[0]+'.wav')

# analysis and call operation
def callS(txt):
    # global value
    global skillidx
    txtlistlist = util.reptxt(txt)
    util.infoLog(txtlistlist)
    clickList = ['click','dclick','rclick','move','drag']
    clickpList = ['clickz','clickp','dclickp','rclickp','movep','dragp']
    typingList = ['typing','typing2','press','keydown','keyup','hotkey','triplekey']
    fileList = ['fmove','fcopy','fdelete']
    clipList = ['copy','paste']
    scrollList = ['scrollup','scrolldown','scrollleft','scrollright']
    saveList = ['save','load']
    textList = ['replace','upper','lower','uppercase','lowercase','extract']
    # analysis first text
    # click
    if txtlistlist[0] in clickList:
        clickS(txtlistlist)
    # clickz
    elif txtlistlist[0] in clickpList:
        clickpS(txtlistlist)
    # hotkey
    elif txtlistlist[0] in typingList:
        typingS(txtlistlist)
    # fmove
    elif txtlistlist[0] in fileList:
        fileS(txtlistlist)
    # if
    elif txtlistlist[0] == 'if':
        ifS(txtlistlist)
    # for
    elif txtlistlist[0] == 'for':
        forS(txtlistlist)
    # copy
    elif txtlistlist[0] in clipList:
        clipS(txtlistlist)
    # scrollup
    elif txtlistlist[0] in scrollList:
        scrollS(txtlistlist)
    # save
    elif txtlistlist[0] in saveList:
        saveS(txtlistlist)
    # replace
    elif txtlistlist[0] in textList:
        textS(txtlistlist)
    else:
        try:
            eval(txtlistlist[0].replace('__','')+'(txtlistlist)')
        except NameError:
            pass

# start skill
def startS(skill):
    # global value
    global skillidx
    global txtlist
    global flg
    # read input text and add to list one line by a time
    encoding = util.getencoding(skill)
    with open(skill,mode='r',encoding=encoding) as f:
        txtlist = f.readlines()
    maxidx = len(txtlist)
    skillidx = 0
    # loop with skill index to max index
    while True:
        if skillidx >= maxidx:
            break
        # if flg is true, break this loop
        if flg == True:
            break
        callS(txtlist[skillidx])
        skillidx += 1

# multi
def multi(name):
    # global value
    global txtpath
    global flg
    # loop while flg become True
    while True:
        startS(txtpath+name)
        # if flg is true, break this loop
        if flg == True:
            break

# init
def init():
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
    encoding = util.getencoding('config.ini')
    configini.read('config.ini',encoding=encoding)
    txtpath = configini.get('SKILL','TxtPath')
    savfile = configini.get('SKILL','SavFile')

# main
def main():
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

init()

if __name__ == '__main__':
    main()
