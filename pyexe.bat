rem pyinstaller main.py
pyinstaller --onefile main.py
xcopy /y *.ini dist
xcopy /y *.ico dist
xcopy /y text dist\text\
xcopy /y image dist\image\
xcopy /y icon dist\icon\
xcopy /y sound dist\sound\
