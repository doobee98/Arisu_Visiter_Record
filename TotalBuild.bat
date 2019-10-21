cd dist
rmdir /s /q Excel
rmdir /s /q ImportExcelDB
rmdir /s /q ExportExcelRecord
cd ..
pyinstaller --clean --noconsole --onefile Arisu.py
pyinstaller ImportExcelDB.py
pyinstaller ExportExcelRecord.py
cd dist
xcopy ExportExcelRecord Excel\ /e /h /k /y
copy ImportExcelDB\ImportExcelDB.exe Excel\ImportExcelDB.exe
copy ImportExcelDB\ImportExcelDB.exe.manifest Excel\ImportExcelDB.exe.manifest
mkdir Excel\ProgramFiles
mkdir Excel\ProgramFiles\Config
cd ..