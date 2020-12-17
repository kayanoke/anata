#! python3
# util.py - support skillE.py

# file path and control
import os
# init config
import configparser
# GUI automation
import pyautogui
# multi threading
import threading
# play sound file
import playsound

# set option parameter
def setoption(textlist):
    # global value
    global paustim
    global accurcy
    # initialize dafault parameter
    option = {}
    option['pause'] = paustim
    option['accuracy'] = accurcy
    option['movepinx'], option['movepiny'] = 0, 0
    option['x'], option['y'] = 0, 0
    option['xmax'], option['xmin'], option['ymax'], option['ymin'] = 0, 0, 0, 0
    option['sync'] = False
    option['start'], option['length'] = 0, 0
    option['quantity'] = 0
    option['out'] = False
    option['strength'] = ''
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            option['accuracy'] = float(datalist[1])
            continue
        # move x,y positon from target
        if datalist[0] == 'movepin':
            datalistlist = datalist[1].split(',')
            option['movepinx'], option['movepiny'] = int(datalistlist[0]), int(datalistlist[1])
            continue
        # pause
        if datalist[0] == 'pause':
            option['pause'] = int(datalist[1])
            continue
        # x position
        if datalist[0] == 'x':
            option['x'] = int(datalist[1])
            continue
        # y position
        if datalist[0] == 'y':
            option['y'] = int(datalist[1])
            continue
        # random x position max
        if datalist[0] == 'xmax':
            option['xmax'] = int(datalist[1])
            continue
        # random x position min
        if datalist[0] == 'xmin':
            option['xmin'] = int(datalist[1])
            continue
        # random y position max
        if datalist[0] == 'ymax':
            option['ymax'] = int(datalist[1])
            continue
        # random y position min
        if datalist[0] == 'ymin':
            option['ymin'] = int(datalist[1])
            continue
        # synchronize
        if datalist[0] == 'sync':
            if datalist[1] == 'True':
                option['sync'] = True
            continue
        # start index
        if datalist[0] == 'start':
            option['start'] = int(datalist[1])
            continue
        # to index + length
        if datalist[0] == 'length':
            option['length'] = int(datalist[1])
            continue
        # loop quanity
        if datalist[0] == 'quantity':
            option['quantity'] = int(datalist[1])
            continue
        # [while target out of] is True
        # [while target in] is False
        if datalist[0] == 'out':
            if datalist[1] == 'True':
                option['out'] = True
            continue
        # strength
        if datalist[0] == 'strength':
            option['strength'] = datalist[1]
            continue
    # initialize dafault parameter
    option.setdefault('pause',paustim)
    option.setdefault('accuracy',accurcy)
    option.setdefault('movepinx',0)
    option.setdefault('movepiny',0)
    option.setdefault('x',0)
    option.setdefault('y',0)
    option.setdefault('xmax',0)
    option.setdefault('xmin',0)
    option.setdefault('ymax',0)
    option.setdefault('ymin',0)
    option.setdefault('sync',False)
    option.setdefault('start',0)
    option.setdefault('length',0)
    option.setdefault('quantity',0)
    option.setdefault('out',False)
    option.setdefault('strength','')
    return option

# locate on screen
def locatescreen(png, confidence):
    # global value
    global imgpath

    if checkpng(png) == False:
        return None

    # locate target position on screen
    return pyautogui.locateOnScreen(imgpath+png,confidence=confidence)

# check target
def checktarget(target):
    if target.endswith('.png') == True:
        return 'image'
    if target == 'clip':
        return 'clip'
    result = target.splitlines()
    for data in result:
        if data.lower().startswith('http') == True:
            return 'url'
    try:
        int(target)
        return 'int'
    except ValueError:
        return 'strength'

# check exist png
def checkpng(png):
    # global value
    global imgpath

    if png.endswith('.png') == False:
        return False
    if os.path.isfile(imgpath+png) == False:
        return False

    return True

# check exist wav
def checkwav(wav):
    # global value
    global imgpath

    if wav.endswith('.wav') == False:
        return False
    if os.path.isfile(sndpath+wav) == False:
        return False
    return True

# repl txt
def reptxt(text):
    # split '/' and delete new line code
    text = text.replace('\n', '').split('/')
    for data in text:
        data = data.replace('[sla]', '/')
    return text

# repl txt
def ulcasetxt(text,case):
    # global value
    global uppcase
    global lowcase
    result = ''
    if case == 'upper':
        moto = lowcase
        saki = uppcase
    else:
        moto = uppcase
        saki = lowcase
    for data in range(len(text)):
        idx = moto.find(text[data])
        result += saki[idx]
    return result

# get one split
def geturl(text):
    result = text.splitlines()
    for data in result:
        if data.lower().startswith('http') == True:
            return data
    return ''

# check url
def checkurl(text):
    result = text.splitlines()
    for data in result:
        if data.lower().startswith('http') == True:
            return True
    return False

# output log
def setLog(text):
    print(text)

# playsound internal process
def playsoundIP(name):
    # global value
    global sndpath
    if checkwav(name) == True:
        playsound.playsound(sndpath+name)

# playsound threading process
def soundasync(name):
    thread = threading.Thread(target=playsoundIP,kwargs={'name': name})
    thread.start()

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
savfile = configini.get('SKILL','SavFile')
uppcase = configini.get('SKILL','UppCase')
lowcase = configini.get('SKILL','LowCase')
