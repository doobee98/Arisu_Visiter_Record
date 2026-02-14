pyinstaller --clean --noconsole --icon=Install\BuildSource\ArisuIcon.ico --name ArisuRecord index.py
pyinstaller ConvertExcel.py

cd dist
ren ConvertExcel Excel
ren ArisuRecord exec

python ..\zip.py ArisuRecord.zip Excel exec
rmdir /s /q Excel
rmdir /s /q exec
cd ..
