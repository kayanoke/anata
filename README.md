# RPA script with only text and image file
# ★★★★★★★★★
# ★★★anata★★★
# ★★★★★★★★★
require pyautogui opencv pyperclip library 
検索
## Please donate from this link. Donations will motivate me. Of the donated money, 300 yen will be used for my sweets memories.

## https://paypal.me/familytec

## how to use
    0. please you write operation command to skill.txt in text folder. and collect image file in image folder.
    1. exec main.py by start.bat ($ python main.py)
    2. click icon to start skill. icon will display red frame
    3. if you want to exit, click the icon. icon will delete red frame

## config parameter
    ### [MAIN]
    RootTtl : main gui title
    IconSiz : main gui icon size
    IconRow : main gui icon rows
    IconCol : main gui icon columns
    TitlIcn : main gui title icon
    TopMost : True -> main gui display top
    DefIcon : main gui default icon image
    AftTime : main gui redrawing cycle
    WinXPos : main gui x position　from the right
    WinYPos : main gui u position　from the down
    # [SKILL]
    IcnPath : icon file path
    SndPath : sound file path
    ImgPath : image file path
    TxtPath : text file path
    PausTim : default pause time
    Accurcy : default image recognize accuracy
    SavFile : save operation file
    Strings : default string text
    CliDura : default click duration
    DraDura : default drag duration
    Intervl : default typing interbal
    UppCase : upper case strings
    LowCase : lower case strings
    ### [SKILL1]
    not used

## い　click operation by image recognition
    name / image / accuracy / shiftposition / pause /
    (click|dclick|rclick|move|drag)/★.png/accuracy=0.8/shiftpin=12,12/pause=1/
     1. name : operation name -> click:click/dclick:double click/rclick:right click/move:move cursol/drag:drag cursol
     2. image : image recognition file(png)
     3. accuracy : image recognition accuracy 0.0～1.0 default:accuracy=0.8
     4. shiftposition : shift target position default:shiftpin=0,0
     5. pause : pause for seconds default:pause=0

## ろ　click operation click by position
    name / x position / y position / pause /
    (clickp|dclickp|rclickp|movep|dragp|clickz)/x=500/y=200/xmax=500/ymax=200/xmin=500/ymin=200/pause=1/
     1. name : operation name -> clickp:click/dclickp:double click/rclickp:right click/movep:move cursol/dragp:drag cursol/clickz:random click
     2. x position : target x position
     3. y position : target y position
     4. xmax, ymax, xmin, ymin : range for random click
     5. pause : pause for seconds default:pause=0

## は　key operation
    name / string / string2 / pause /
    (typing|press|keydown|keyup|hotkey)/★(/★)/pause=1/
     1. name : operation name -> typing:keyboard typing/press:press key/keydown:hold down key/keyup:hold up key/hotkey:press 2 keys
     2. string : output string
     3. string2 : 2nd string for hotkey
     4. pause : pause for seconds default:pause=0

## に　end operation
    name / image / accuracy /
    end/★.png/accuracy=0.8/
     1. name : operation name -> end:close operation
     2. image : image recognition file(png) if no image is specified, immediately end if image recognition fails, restart operation from the beginning
     3. accuracy : image recognition accuracy 0.0～1.0 default:accuracy=0.8

## ほ　pause operation
    name / pause /
    pause/5/
     1. name : operation name -> pause:pause operation
     2. pause : pause for seconds

## へ　launch app operation
    name / filepath / synchronize / pause /
    run/C:\\appli\aplli.bat/sync=(True|False)/pause=5/
     1. name : operation name -> run:launch app
     2. filepath : application file path
     3. synchronize : True=synchronize,False=unsynchronize
     4. pause : pause for seconds default:pause=0

## と　file operation
    name / fromfilepath / tofilepath / pause /
    (fmove|fcopy|fdelete|folder)/C:\\app/1.txt/C:\\app/2.txt/pause=5/
     1. name : operation name -> fmove:move file/fcopy:copy file/fdelete:delete file/folder:open folder
     2. fromfilepath : target file path dir check & file exists & target is file only
     3. tofilepath : target to move file path for file move and copy dir check & file not exists & target is file only
     4. pause : pause for seconds default:pause=0

## ち　conditional branch operation
    name / left / compare / right /jumptoT / jumptoF /
    if/1/=/1/5/7/
     1. name : operation name -> if:conditional branch
     2. left : left condition 'clip' load clipboard
     3. compare : compare sign
     4. right : right condition
     5. jumptoT : jump number with True
     6. jumptoF : jump number with False

## り　conditional branch operation by image recognition
    name / image / jumptoT / jumptoF / accuracy /
    if/★.png/5/7/accuracy=0.8/
     1. name : operation name -> if:conditional branch
     2. image : image recognition file(png)
     3. jumptoT : jump number with image recognition success
     4. jumptoF : jump number with image recognition fails
     5. accuracy : image recognition accuracy 0.0～1.0 default:accuracy=0.8

## ぬ　repeate operation
    name / quantity / start / length /
    for/quantity=5/start=5/length=10/
     1. name : operation name -> for:repeate
     2. quantity : repeate quantity
     3. start : start number
     4. length : 1 repeate operation length

## る　clipboard operation
    name / string / pause /
    (ccopy|cpaste)/test/pause=5/
     1. name : operation name -> ccopy:string is copied to clipboard/cpaste:paste from clipboard
     2. string : copy string for ccopy
     3. pause : pause for seconds default:pause=0

## を　wait until match operation
    name / image / targetout / accuracy / pause /
    name / string / targetout / accuracy / pause /
    until/(★.png|string)/out=True/accuracy=0.8/pause=1/
     1. name : operation name -> until:wait until match
     2. image : image recognition file(png)
     3. string : match to clipboard text and enable to regex
     4. targetout : True:target out, False:target in
     5. accuracy : image recognition accuracy 0.0～1.0 default:accuracy=0.8
     6. pause : pause for seconds default:pause=0

## わ　scroll operation
    name / amount / pause /
    (scrollup|scrolldown|scrollleft|scrollright)/5/pause=1/
     1. name : operation name -> scrollup:scroll up/scrolldown:scroll down/scrollleft:scroll left/scrollright:scroll right
     2. amount : scroll amount
     3. pause : pause for seconds default:pause=0

## か　save & load text operation
    name / save name / string /
    (save|load)/name1/string=★/
     1. name : operation name -> save:save string with save name/load:get save name string
     2. save name : save name
     3. string : save string

## よ　clioboard exchange operation
    name / string1 / string2 /
    (replace|upper|lower|uppercase|lowercase|extract)/★/■/
     1. name : operation name -> replace:string1 replace string2/upper:upper/lower:lower/uppercase:uppercase/lowercase:lowercase/extract:extract url
     2. string1 : replace TO
     3. string2 : replace FROM

## た　jump to clipboard url operation
    name / pause /
    jumpurl/pause=5/
     1. name : operation name -> jumpurl:jump to url
     2. pause : pause for seconds default:pause=0

## れ　extract date to clipboard operation
    name / pause /
    jumpurl/pause=5/
     1. name : operation name -> jumpurl:jump to url
     2. pause : pause for seconds default:pause=0

## そ　date copy operation
    name / format / add year / add month / add date / string
    getdate/YYYYMMDD/year=1/month=1/date=1/string=firstday/
     1. name : operation name -> getdate:copy to date
     2. format : YYYY,YY,MM,M,DD,D,HH,H,mm,m,ss,s can set
     3. add year : add year
     4. add month : add month
     5. add date : add date
     6. string : firstday:first day lastday:last day

つねならむうゐのおくやまけふこえてあさきゆめみしゑひもせす

pyautogui
https://github.com/asweigart/pyautogui

pyperclip
https://github.com/asweigart/pyperclip

opencv-python
https://github.com/skvark/opencv-python
