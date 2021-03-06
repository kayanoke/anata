#! python3
# util.py - support skillE.py

# file path and control
import os
# determine exe or script
import sys
# init config
import configparser
# GUI automation
import pyautogui
# multi threading
import threading
# play sound file
import playsound
# date time
import datetime
# dateutil
import dateutil.relativedelta
# log
import logging
# log
import logging.config
# key & mouse bind
import pynput
# detect encoding
import chardet

# set option parameter
def setoption(textlist):
    # global value
    global paustim
    global accurcy
    global strings
    global clidura
    global dradura
    global intervl
    # initialize dafault parameter
    option = {}
    option['pause'] = paustim
    option['accuracy'] = accurcy
    option['shiftpinx'], option['shiftpiny'] = 0, 0
    option['x'], option['y'] = 0, 0
    option['xmax'], option['xmin'], option['ymax'], option['ymin'] = 0, 0, 0, 0
    option['sync'] = False
    option['start'], option['length'] = 0, 0
    option['quantity'] = 0
    option['out'] = False
    option['string'] = strings
    option['year'] = 0
    option['month'] = 0
    option['day'] = 0
    option['clickduration'] = clidura
    option['dragduration'] = dradura
    option['interval'] = intervl
    # initialize option parameter
    for text in textlist:
        datalist = text.split('=')
        if len(datalist) < 2:
            continue
        # image reconginition accuracy
        if datalist[0] == 'accuracy':
            option['accuracy'] = float(datalist[1])
            continue
        # shift x,y positon from target
        if datalist[0] == 'shiftpin':
            datalistlist = datalist[1].split(',')
            option['shiftpinx'], option['shiftpiny'] = int(datalistlist[0]), int(datalistlist[1])
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
        # string
        if datalist[0] == 'string':
            option['string'] = datalist[1]
            continue
        # year
        if datalist[0] == 'year':
            option['year'] = int(datalist[1])
            continue
        # month
        if datalist[0] == 'month':
            option['month'] = int(datalist[1])
            continue
        # day
        if datalist[0] == 'day':
            option['day'] = int(datalist[1])
            continue
        # clickduration
        if datalist[0] == 'clickduration':
            option['clickduration'] = float(datalist[1])
            continue
        # dragduration
        if datalist[0] == 'dragduration':
            option['dragduration'] = float(datalist[1])
            continue
        # interval
        if datalist[0] == 'interval':
            option['interval'] = float(datalist[1])
            continue
    # initialize dafault parameter
    option.setdefault('pause',paustim)
    option.setdefault('accuracy',accurcy)
    option.setdefault('shiftpinx',0)
    option.setdefault('shiftpiny',0)
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
    option.setdefault('string','')
    option.setdefault('year',0)
    option.setdefault('month',0)
    option.setdefault('day',0)
    option.setdefault('clickduration',clidura)
    option.setdefault('dragduration',dradura)
    option.setdefault('interval',intervl)
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
        return 'string'

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
    for i in range(len(text)):
        text[i] = text[i].replace('[sla]', '/')
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
        if idx == -1:
            result += text[data]
        else:
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

# output debug level log
def debugLog(text):
    logger.debug(text)
# output info level log
def infoLog(text):
    logger.info(text)
# output warning level log
def warningLog(text):
    logger.warning(text)
# output error level log
def errorLog(text):
    logger.error(text)
# output critical level log
def criticalLog(text):
    logger.critical(text)

# playsound internal process
def playsoundIP(name):
    global value
    global sndpath
    global soundlg
    if checkwav(name) == True:
        playsound.playsound(sndpath+name)
        infoLog(sndpath+name)

# playsound threading process
def soundasync(name):
    thread = threading.Thread(target=playsoundIP,kwargs={'name': name})
    thread.start()

# playsound threading process
def soundlog(name):
    if soundlg == True:
        soundasync(name)

# replace
def replace(text,before,after):
    before = before.replace('\\n','\n').replace('\\t','\t').replace('\\r','\r')
    after = after.replace('\\n','\n').replace('\\t','\t').replace('\\r','\r')
    return text.replace(before,after)

# get date time
def getdatetime(format,valuey,valuem,valued,string):
    date = datetime.datetime.now()
    date = date + dateutil.relativedelta.relativedelta(years=valuey,months=valuem,days=valued)
    if string.startswith('f') == True:
        date = date + dateutil.relativedelta.relativedelta(day=1)
    if string.startswith('l') == True:
        date = date + dateutil.relativedelta.relativedelta(months=1,day=1,days=-1)
    format = format.replace('YYYY','%Y')
    format = format.replace('YY','%y')
    format = format.replace('MM','hi')
    format = format.replace('M','bi')
    format = format.replace('DD','%d')
    format = format.replace('D','%#d')
    format = format.replace('HH','ji')
    format = format.replace('H','%#H')
    format = format.replace('mm','fu')
    format = format.replace('m','%#M')
    format = format.replace('SS','by')
    format = format.replace('S','%#S')
    format = format.replace('hi','%m')
    format = format.replace('bi','%#m')
    format = format.replace('ji','%H')
    format = format.replace('fu','%M')
    format = format.replace('by','%S')
    return date.strftime(format)

# untilKey bind function
def onrelease(key):
    global releaseKey
    try:
        if key.char == releaseKey:
            return False
    except AttributeError:
        if str(key) == 'Key.'+releaseKey:
            return False

# untilMouse bind function
def onclick(x, y, button, pressed):
    global releaseMouse
    if not pressed:
        if str(button) == 'Button.'+releaseMouse:
            return False

# untilKey bind function
def untilKey(key):
    global releaseKey
    releaseKey = key.lower()
    # collect events until released
    with pynput.keyboard.Listener(on_release=onrelease) as keylistener:
        keylistener.join()

# untilKey bind function
def untilMouse(key):
    global releaseMouse
    releaseMouse = key.lower()
    # collect events until released
    with pynput.mouse.Listener(on_click=onclick) as mouselistener:
        mouselistener.join()

# detect file encoding
def getencoding(file):
    with open(file,mode='rb') as f:
        b = f.read()
    enc = chardet.detect(b)
    if enc['confidence'] < 0.3:
        return 'utf-8'
    return enc['encoding']


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

# set log config
logging.config.fileConfig('configlog.ini')
logger = logging.getLogger()

# set config.ini parameter
configini = configparser.ConfigParser()
encoding = getencoding('config.ini')
configini.read('config.ini',encoding=encoding)

rootttl = configini.get('MAIN','rootTtl')
iconsiz = int(configini.get('MAIN','IconSiz'))
iconrow = int(configini.get('MAIN','IconRow'))
iconcol = int(configini.get('MAIN','IconCol'))
titlicn = configini.get('MAIN','TitlIcn')
topmost = False
if configini.get('MAIN','TopMost') == 'True':
    topmost = True
deficon = configini.get('MAIN','DefIcon')
afttime = int(configini.get('MAIN','AftTime'))
winxpos = int(configini.get('MAIN','WinXPos'))
winypos = int(configini.get('MAIN','WinYPos'))
icnpath = configini.get('SKILL','IcnPath')
sndpath = configini.get('SKILL','SndPath')
imgpath = configini.get('SKILL','ImgPath')
txtpath = configini.get('SKILL','TxtPath')
soundlg = False
if configini.get('SKILL','SoundLg') == 'True':
    soundlg = True
paustim = int(configini.get('SKILL','PausTim'))
accurcy = float(configini.get('SKILL','Accurcy'))
savfile = configini.get('SKILL','SavFile')
strings = configini.get('SKILL','Strings')
clidura = float(configini.get('SKILL','CliDura'))
dradura = float(configini.get('SKILL','DraDura'))
intervl = float(configini.get('SKILL','Intervl'))
uppcase = configini.get('SKILL','UppCase')
lowcase = configini.get('SKILL','LowCase')
getencoding('C:/Users/ebifr/OneDrive/py/anata/log.txt')
