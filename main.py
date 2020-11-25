#時間の制御
import time
#マウス操作
import pyautogui
#スケジュール
import schedule
#実行パス取得
import os
#別プログラム起動
import subprocess
#mp3再生
import playsound
#別ファイル
import startsS
#GUI
import tkinter
#画像
from PIL import ImageTk
from PIL import Image

iconPath = 'icon/'
soundPath = 'sound/'

# 画像をクリックしたときの処理
def event_function(event):
    global on_off_list
    global canvas
    global proclist
    xx = event.x // 64 
    # on_off_listを1にして赤枠をつける。すでに一なら0にして赤枠を消す。
    if on_off_list[xx] == 0:
        on_off_list[xx] = 1
        canvas.create_rectangle(2+xx*64,2,-1+(xx+1)*64, 63,width=2,outline='red',tags='tangle'+str(xx))
        playsound.playsound(soundPath+'start.wav')
        proclist[xx] = subprocess.Popen(['python','startsS.py','skill'+str(xx+1)+'.txt'])
    else:
        # すでに押しているスキルの場合
        on_off_list[xx] = 0
        canvas.delete('tangle'+str(xx))
        # プロセスを終わる
        proclist[xx].terminate()
        # 動いていたらNone、終わったら返り値、動いてなかったらエラーを返す。
        #subprocess.Popen.poll(proclist[1])
# 実行ファイルのパスを取得
# __file__は絶対パス＋ファイル名　dirnameでパス取得
if os.path.dirname(__file__) != '':
    # 処理用のデフォルトパスを実行ファイルのパスに変更
    os.chdir(os.path.dirname(__file__))

# ウィンドウ（フレーム）の作成
root = tkinter.Tk()
# ウィンドウの名前を設定
root.title("yourSkill")

# リストの初期化
on_off_list = [0, 0, 0, 0, 0, 0]
img_im_list = []
# 画像表示用のキャンバス作成
canvas = tkinter.Canvas(bg="black", width=384, height=64)
canvas.place(x=0, y=0) # 左上の座標を指定

# 6回繰り返す。
for i in range(6):
    img_im_list.append(Image.open(iconPath+str(i + 1) + '.png')) 
    img_im_list[i] = ImageTk.PhotoImage(img_im_list[i])
    canvas.create_image(64*i, 0, image=img_im_list[i], anchor=tkinter.NW)

# キャンバスにボタンイベントを追加
canvas.bind('<Button-1>', event_function)

# スキル用のプロセスリストを初期化
proclist = [0,0,0,0,0,0]

# メニューバー
check = tkinter.IntVar()
check.set(1)
menubar = tkinter.Menu(root)
root.configure(menu = menubar)
games = tkinter.Menu(menubar, tearoff = False)
create = tkinter.Menu(menubar, tearoff = False)
checks = tkinter.Menu(menubar, tearoff = False)
menubar.add_cascade(label="Files", underline = 0, menu=games)
menubar.add_cascade(label="Create", underline = 0, menu=create)
menubar.add_cascade(label="Check", underline = 0, menu=checks)
games.add_command(label = 'Save', command=startsS.startS)
create.add_command(label = 'Click', command=startsS.startS)
create.add_command(label = 'DClick', command=startsS.startS)
create.add_command(label = 'Move', command=startsS.startS)
create.add_command(label = 'Click&Drug', command=startsS.startS)
create.add_command(label = 'Typing', command=startsS.startS)
create.add_command(label = 'Key', command=startsS.startS)
checks.add_radiobutton(label = 'Check 1', variable = check, value = 1)
checks.add_radiobutton(label = 'Check 2', variable = check, value = 2)
checks.add_radiobutton(label = 'Check 3', variable = check, value = 3)
checks.add_radiobutton(label = 'Check 4', variable = check, value = 4)
checks.add_radiobutton(label = 'Check 5', variable = check, value = 5)
checks.add_radiobutton(label = 'Check 6', variable = check, value = 6)

# ウィンドウの大きさ、位置を設定
root.geometry('384x64+1530+900')

root.resizable(width=False, height=False)
root.mainloop()
