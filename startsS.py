#時間の制御
import time
#マウス操作
import pyautogui
#実行パス取得、ファイル操作
import os
#mp3再生
import playsound
#コマンドライン引数
import sys
#別プログラム起動
import subprocess
#ファイルコピー
import shutil
#マルチスレッド
import threading
#クリップボード
import pyperclip

iconPath = 'icon/'
soundPath = 'sound/'

#クリック・ダブルクリック・右クリック・マウス移動・マウスドラッグ
#(click|dclick|rclick|move|drag)/★.png/accuracy=0.8/movepin=12,12/stop=1/
def clickS(textlist):
    # パラメータ初期値設定
    conf = 0.8
    movepinx, movepiny = 0, 0
    stoptime = 0
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        # 画像判定精度
        if datalist[0] == 'accuracy':
            conf = float(datalist[1])
        # 操作座標の移動
        if datalist[0] == 'movepin':
            datalistlist = datalist[1].split(',')
            movepinx, movepiny = int(datalistlist[0]), int(datalistlist[1])
        # 一時停止
        if datalist[0] == 'stop':
            stoptime = int(datalist[1])
    # ターゲットの画像を取得
    target = pyautogui.locateOnScreen(textlist[1],confidence=conf)
    # ターゲットが画面にあるか確認
    if target is None:
        # ターゲットが無ければ終了
        setLog(textlist[1]+' is nai',False)
        #playsound.playsound(soundPath+'isnai.wav')
        time.sleep(stoptime)
        return
    # 画像の中心座標取得
    x, y = pyautogui.center(target)
    # 座標をずらす
    x, y = x + movepinx, y + movepiny
    # 座標をクリック
    if textlist[0] == 'click':
        pyautogui.click(x,y)
    # 座標をダブルクリック
    if textlist[0] == 'dclick':
        pyautogui.doubleClick(x,y)
    # 座標を右クリック
    if textlist[0] == 'rclick':
        pyautogui.rightClick(x,y)
    # 座標へポインタ移動
    if textlist[0] == 'move':
        pyautogui.moveTo(x,y)
    # 座標へドラッグ移動
    if textlist[0] == 'drag':
        pyautogui.dragTo(x,y,1,button='left')
    setLog(textlist[1]+' '+textlist[0]+' '+str(movepinx)+', '+str(movepiny)+', '+str(conf),True)
    soundasync(textlist[0]+'.wav')
    time.sleep(stoptime)
#タイピング・キー操作
#(typing|press|keydown|keyup)/hello/stop=1/
def typingS(textlist):
    # パラメータ初期値設定
    stoptime = 0
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        # 一時停止
        if datalist[0] == 'stop':
            stoptime = int(datalist[1])
    if textlist[0] == 'typing':
        pyautogui.typewrite(textlist[1])
    if textlist[0] == 'press':
        pyautogui.press(textlist[1])
    if textlist[0] == 'keydown':
        pyautogui.keyDown(textlist[1])
    if textlist[0] == 'keyup':
        pyautogui.keyUp(textlist[1])
    # 取得した文字を画面に入力
    setLog(textlist[1]+' wo typing',True)
    soundasync(textlist[0]+'.wav')
    time.sleep(stoptime)
#一時停止
def stopS(textlist):
    # 後ろの文字を取得（改行は除く）
    setLog(textlist[1]+' byou stop',True)
    soundasync(textlist[0]+'.wav')
    # 取得した数値分だけ処理を止める
    time.sleep(int(textlist[1]))
#終了
#end/★.png/
def endS(textlist):
    # グローバル変数
    global flg
    # 処理を終わる
    if len(textlist) == 1:
        soundasync(textlist[0]+'.wav')
        flg = True
        return
    if textlist[1] == '':
        soundasync(textlist[0]+'.wav')
        flg = True
        return
    conf = 0.8
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        # 画像判定精度
        if datalist[0] == 'accuracy':
            conf = float(datalist[1])
    # ターゲットの画像を取得
    if pyautogui.locateOnScreen(textlist[1],confidence=conf) is None:
        soundasync('isnai.wav')
        setLog('retry',False)
        return
    flg = True
    setLog('end',True)
    soundasync(textlist[0]+'.wav')
#アプリ起動
def runS(textlist):
    # パラメータ初期値設定
    stoptime = 0
    sync = False
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        # 一時停止
        if datalist[0] == 'stop':
            stoptime = int(datalist[1])
        if datalist[0] == 'sync':
            if datalist[1] == 'True':
                sync = True
    # 後ろの文字を取得（改行は除く）
    dataS = textlist[0]
    setLog(dataS + ' wo running',True)
    soundasync(textlist[0]+'.wav')
    # 非同期でプログラムを起動run
    if sync == True:
        subprocess.run(textlist[1])
    if sync == False:
        subprocess.Popen(textlist[1])
    time.sleep(stoptime)
#ファイルコピー・移動・削除
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/1.txt/stop=5/
def fileS(textlist):
    # パラメータ初期値設定
    stoptime = 0
    # オプションパラメータ取得
    for text in textlist:
        # 一時停止
        datalist = text.split('=')
        if datalist[0] == 'stop':
            stoptime = int(datalist[1])
    if os.path.isdir(textlist[1]) == True:
        soundasync('isfnai.wav')
        time.sleep(stoptime)
        return
    if os.path.exists(os.path.dirname(textlist[1])) == False:
        soundasync('isfnai.wav')
        time.sleep(stoptime)
        return
    if os.path.exists(textlist[1]) == False:
        soundasync('isfnai.wav')
        time.sleep(stoptime)
        return
    if textlist[0] == 'fmove':
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            soundasync('isfnai.wav')
            time.sleep(stoptime)
            return
        if os.path.exists(textlist[2]) == True:
            soundasync('isfaru.wav')
            time.sleep(stoptime)
            return
        soundasync(textlist[0]+'.wav')
        shutil.move(textlist[1],textlist[2])
    if textlist[0] == 'fcopy':
        if os.path.exists(os.path.dirname(textlist[2])) == False:
            soundasync('isfnai.wav')
            time.sleep(stoptime)
            return
        if os.path.exists(textlist[2]) == True:
            soundasync('isfaru.wav')
            time.sleep(stoptime)
            return
        soundasync(textlist[0]+'.wav')
        shutil.copy2(textlist[1],textlist[2])
    if textlist[0] == 'fdelete':
        soundasync(textlist[0]+'.wav')
        os.remove(textlist[1])
    time.sleep(stoptime)
#ファイルコピー・移動・削除
#(fmove|fcopy|fdelete)/C:\\app/1.txt/C:\\app/1.txt/stop=5/
def folderS(textlist):
    # パラメータ初期値設定
    stoptime = 0
    # オプションパラメータ取得
    for text in textlist:
        # 一時停止
        datalist = text.split('=')
        if datalist[0] == 'stop':
            stoptime = int(datalist[1])
    if os.path.isdir(textlist[1]) == False:
        soundasync('isfnai.wav')
        time.sleep(stoptime)
        return
    if os.path.exists(textlist[1]) == False:
        soundasync('isfnai.wav')
        time.sleep(stoptime)
        return
    soundasync(textlist[0]+'.wav')
    subprocess.run('explorer '+textlist[1])
    time.sleep(stoptime)
#ＩＦ条件分岐
#if/1/==/1/5/7/
def ifS(textlist):
    # グローバル変数
    global i
    if textlist[2] == '==':
        if int(textlist[1]) == int(textlist[3]):
            soundasync('bunkiT.wav')
            i = int(textlist[4]) - 1
        else:
            soundasync('bunkiF.wav')
            i = int(textlist[5]) - 1
    if textlist[2] == '<':
        if int(textlist[1]) < int(textlist[3]):
            soundasync('bunkiT.wav')
            i = int(textlist[4]) - 1
        else:
            soundasync('bunkiF.wav')
            i = int(textlist[5]) - 1
    if textlist[2] == '<=':
        if int(textlist[1]) <= int(textlist[3]):
            soundasync('bunkiT.wav')
            i = int(textlist[4]) - 1
        else:
            soundasync('bunkiF.wav')
            i = int(textlist[5]) - 1
    if textlist[2] == '>':
        if int(textlist[1]) > int(textlist[3]):
            soundasync('bunkiT.wav')
            i = int(textlist[4]) - 1
        else:
            soundasync('bunkiF.wav')
            i = int(textlist[5]) - 1
    if textlist[2] == '>=':
        if int(textlist[1]) >= int(textlist[3]):
            soundasync('bunkiT.wav')
            i = int(textlist[4]) - 1
        else:
            soundasync('bunkiF.wav')
            i = int(textlist[5]) - 1
    if textlist[2] == '!=':
        if int(textlist[1]) != int(textlist[3]):
            soundasync('bunkiT.wav')
            i = int(textlist[4]) - 1
        else:
            soundasync('bunkiF.wav')
            i = int(textlist[5]) - 1
#ＩＦ画像分岐
#ifimg/★.png/5/7/accuracy=0.8/
def ifimgS(textlist):
    # グローバル変数
    global i
    # パラメータ初期値設定
    conf = 0.8
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        # 画像判定精度
        if datalist[0] == 'accuracy':
            conf = float(datalist[1])
    # ターゲットの画像を取得
    target = pyautogui.locateOnScreen(textlist[1],confidence=conf)
    # 画像を取得して画面にあるか確認
    if target is None:
        soundasync('bunkiF.wav')
        i = int(textlist[3]) - 2
        return
    soundasync('bunkiT.wav')
    i = int(textlist[2]) - 2
#Ｆｏｒ繰り返し
#for/quantity=5/start=5/length=10
def forS(textlist):
    # グローバル変数
    global txtlist
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        if datalist[0] == 'quantity':
            quantity = int(datalist[1])
        if datalist[0] == 'start':
            start = int(datalist[1])
        if datalist[0] == 'length':
            length = int(datalist[1])
    for i in range(quantity-1):
        for j in range(length):
            dododo(txtlist[start-1+j])
#Ｆｏｒ画像繰り返し
#forimg/★.png/quantity=5/start=5/length=10/out=True/accuracy=0.8/
def forimgS(textlist):
    # グローバル変数
    global txtlist
    # パラメータ初期値設定
    conf = 0.8
    out = True
    # オプションパラメータ取得
    for text in textlist:
        datalist = text.split('=')
        if datalist[0] == 'quantity':
            quantity = int(datalist[1])
        if datalist[0] == 'start':
            start = int(datalist[1])
        if datalist[0] == 'length':
            length = int(datalist[1])
        if datalist[0] == 'out':
            out = datalist[1]
        # 画像判定精度
        if datalist[0] == 'accuracy':
            conf = datalist[1]
    while True:
        # ターゲットの画像を取得
        target = pyautogui.locateOnScreen(textlist[1],confidence=conf)
        if out == 'True':
            # 画像を取得して画面にあるか確認
            if target is None:
                for i in range(length):
                    dododo(txtlist[start-1+i])
            else:
                break
        else:
            if target is None:
                break
            else:
                for i in range(length):
                    dododo(txtlist[start-1+i])
#一時停止
def clipS(textlist):
    # パラメータ初期値設定
    stoptime = 0
    # オプションパラメータ取得
    for text in textlist:
        # 一時停止
        datalist = text.split('=')
        if datalist[0] == 'stop':
            stoptime = int(datalist[1])
    if textlist[0] == 'ccopy':
        pyperclip.copy(textlist[1])
    if textlist[0] == 'cpaste':
        pyautogui.typewrite(pyperclip.paste())
    soundasync(textlist[0]+'.wav')
    # 取得した数値分だけ処理を止める
    time.sleep(stoptime)
#テキストを読み込み各種操作を行う
def setLog(text,flg):
    print(text)

#テキストを読み込み各種操作を行う
def playsoundS(name):
    playsound.playsound(soundPath+name)
#テキストを読み込み各種操作を行う
def soundasync(name):
    t1 = threading.Thread(target=playsoundS,kwargs={'name': name})
    t1.start()

#テキストを読み込み各種操作を行う
def dododo(txt):
    # /で文字区切ってリストに格納、末尾改行は削除
    txtlistlist = txt.replace('\n', '').split('/')
    print(i,txtlistlist)
    # 最初の文字で処理を判断
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
    # stop
    if txtlistlist[0] == 'stop':
        stopS(txtlistlist)
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

#テキストを読み込み各種操作を行う
def startS(skill):
    # グローバル変数
    global i
    global txtlist
    # テキストを読み込みリストに一行ずつ格納
    with open(skill,mode='r',encoding='utf-8') as f:
        txtlist = f.readlines()
    maxidx = len(txtlist)
    i = 0
    # リストの要素で繰り返し
    while True:
        if i >= maxidx:
            break
        dododo(txtlist[i])
        i += 1

def main():
    # 永久ループ
    while True:
        if len(args) > 1:
            startS(str(args[1]))
        else:
            startS('skill1.txt')
        if flg == True:
            break

# 実行ファイルのパスを取得
# __file__は絶対パス＋ファイル名　dirnameでパス取得
if os.path.dirname(__file__) != '':
    # 処理用のデフォルトパスを実行ファイルのパスに変更
    os.chdir(os.path.dirname(__file__))

flg = False
args = sys.argv

if __name__ == '__main__':
    main()
