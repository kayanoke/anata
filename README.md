# anata
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
★★★                ＲＰＡ                                                  ★★★
★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
テキストに書き込んだ内容を読み取りクリックやキー入力等を行うことができます。
startsS.py → コマンドプロンプトからファイル名を指定して実行します。
              main.pyを起動し、アイコンをクリックすることでskill1.txt～skill6.txtいずれかを読み込み実行します。
main.py → 実行するとアイコンが6種表示されます。アイコンクリックするとstartsS.pyを起動します。
          再度クリックすると起動したstartsS.pyを停止します。

必要ライブラリ
pip install playsound
pip install pyautogui
pip install opencv-python
pip install pyperclip
pip install schedule


い　クリック・ダブルクリック・右クリック・マウス移動・マウスドラッグ
    name / image / accuracy / moveclickposition / stoptime /
    (click|dclick|rclick|move|drag)/★.png/accuracy=0.8/movepin=12,12/stop=1/
     1 name : 操作の名称
     2 image : 画像ファイル名
     3 accuracy : 画像の精度 0.0～1.0 無ければ accuracy=0.8
     4 moveclickposition : 画像の中心から指定分ずらして操作する。 無ければ movepin=0,0
     5 stoptime : 操作後指定秒数処理を停止。 無ければ stop=0

ろ　タイピング・キー操作
    name / string / stoptime /
    (typing|press|keydown|keyup)/hello/stop=1/
     1 name : 操作の名称
     2 string : 入力文字 全角なら全角を入れ、半角なら半角を入力？
     5 stoptime : 操作後指定秒数処理を停止。 無ければ stop=0

は　処理終了
    name / image / accuracy /
    end/★.png/accuracy=0.8/
     1 name : 操作の名称
     2 image : 画像ファイル名　指定あれば画像検索、無ければ即停止
     3 accuracy : 画像の精度 0.0～1.0 無ければ accuracy=0.8
     ※ : 処理終了しなければテキストを再度読み直して処理をする

に　一時停止
    name / stoptime /
    stop/5/
     1 name : 操作の名称
     2 stoptime : 操作後指定秒数処理を停止

ほ　アプリ起動
    name / filepath / synchronize / stoptime /
    run/C:\\appli\aplli.bat/sync=(True|False)/stop=5/
     1 name : 操作の名称
     2 filepath : ファイルパス
     3 synchronize : True=同期、False=非同期
     4 stoptime : 操作後指定秒数処理を停止 無ければ stop=0

へ　ファイルコピー・移動・削除・フォルダを開く
    name / tofilepath / fromfilepath / stoptime /
    (fmove|fcopy|fdelete|folder)/C:\\app/1.txt/C:\\app/1.txt/stop=5/
     1 name : 操作の名称
     2 tofilepath : 移動元ファイルパス
     3 fromfilepath : 移動先ファイルパス　削除・フォルダを開く場合なし
     4 stoptime : 操作後指定秒数処理を停止 無ければ stop=0
     tofilepath   : dir check & file exists & target is file only
     fromfilepath : dir check & file not exists & target is file only

と　ＩＦ条件分岐
    name / compare / jumptoT / jumptoF /
    if/1/=/1/5/7/
     1 name : 操作の名称
     2 left : 比較対象
     2 compare : 比較条件
     2 righht : 比較対象
     3 jumptoT : Trueの時のジャンプ行数
     4 jumptoF : Falseの時のジャンプ行数

ち　ＩＦ画像分岐
    name / image / jumptoT / jumptoF / accuracy / accuracy=0.8/
    ifimg/★.png/5/7/accuracy=0.8/
     1 name : 操作の名称
     2 image : 画像ファイル名　あればTrue、なければFalse
     3 jumptoT : Trueの時のジャンプ行数
     4 jumptoF : Falseの時のジャンプ行数
     5 accuracy : 画像の精度 0.0～1.0 無ければ accuracy=0.8

り　Ｆｏｒ繰り返し
    name / quantity / dobetween /
    for/1/5,10/
     1 name : 操作の名称
     2 quantity : 指定回数繰り返す
     4 dobetween : 左から右の行を繰り返す

ぬ　Ｆｏｒ画像繰り返し
    name / ( quantity | image ) / dobetween / imageoutofsight / accuracy /
    forimg/★.png/5,10/out/accuracy=0.8/
     1 name : 操作の名称
     2 image : 画像が出るまで繰り返す
     3 dobetween : 左から右の行を繰り返す
     4 imageoutofsight : out なら画像が消えるまで繰り返す
     5 accuracy : 画像の精度 0.0～1.0 無ければ accuracy=0.8

る　クリップボード
    name / text / stoptime /
    (ccopy|cpaste)/test/stop=5/
     1 name : 操作の名称
     2 text : ccopyの場合、クリップボードにコピーする
     3 stoptime : 操作後指定秒数処理を停止 無ければ stop=0
