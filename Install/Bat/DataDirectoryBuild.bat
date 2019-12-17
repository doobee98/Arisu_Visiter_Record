cd dist
mkdir AppData
mkdir AppData\log
mkdir AppData\bin
mkdir AppData\bin\config
mkdir AppData\src
mkdir UserData
mkdir UserData\Record
mkdir UserData\Database
mkdir UserData\Delivery

xcopy ..\Install\BuildSource AppData\src\ /e /h /k /y

Bandizip.exe c -y ArisuRecordData.zip AppData UserData
rmdir /s /q AppData
rmdir /s /q UserData
cd ..

