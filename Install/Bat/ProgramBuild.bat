pyinstaller --clean --noconsole --icon=Install\BuildSource\ArisuIcon.ico ArisuRecord.py
pyinstaller ConvertExcel.py

cd dist
ren ConvertExcel Excel
ren ArisuRecord exec

Bandizip.exe c -y ArisuRecord.zip Excel exec
rmdir /s /q Excel
rmdir /s /q exec
cd ..
