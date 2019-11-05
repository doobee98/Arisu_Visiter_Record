cd dist
rmdir /s /q ImportExcelDB
rmdir /s /q ExportExcelRecord
rmdir /s /q Excel
rmdir /s /q ArisuRecord
rmdir /s /q exec
cd ..
pyinstaller --clean --noconsole --icon=ArisuIcon.ico ArisuRecord.py
pyinstaller ImportExcelDB.py
pyinstaller ExportExcelRecord.py
cd dist
mkdir Excel
mkdir AppData
mkdir AppData\src
mkdir AppData\log
mkdir AppData\bin
mkdir AppData\bin\config
mkdir UserData
mkdir UserData\Database
mkdir UserData\Delivery
mkdir UserData\Record
xcopy ExportExcelRecord Excel\ /e /h /k /y
copy ImportExcelDB\ImportExcelDB.exe Excel\ImportExcelDB.exe
copy ImportExcelDB\ImportExcelDB.exe.manifest Excel\ImportExcelDB.exe.manifest
ren ArisuRecord exec
rmdir /s /q ImportExcelDB
rmdir /s /q ExportExcelRecord
cd ..