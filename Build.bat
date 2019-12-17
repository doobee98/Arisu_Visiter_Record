::  Build.bat - 전체 빌드 생성

del /q "dist\ArisuRecord_64bit.zip"
call Install\Bat\DataDirectoryBuild.bat   rem ArisuRecordData.zip
call Install\Bat\ProgramBuild.bat    rem ArisuRecord.zip
call Install\Bat\InstallBuild.bat    rem setup.exe

cd dist
Bandizip.exe c -y ArisuRecord_64bit.zip ArisuRecord.zip ArisuRecordData.zip setup.exe
del /q "ArisuRecord.zip"
del /q "ArisuRecordData.zip"
del /q "setup.exe"
cd ..


::  DataDirectoryBuild.bat - AppData와 UserData 폴더를 생성
::  하단 주석문 내용은 Utility.Info.DefaultFilePath의 내용 일부를 참조함
:: AppData     | log  <실행시 생기는 로그(ErrorReport, ExecuteLog)를 저장>
::             | bin       | config  <실행시 필요한 설정 파일을 암호화하여 저장>
::             | src  <실행시 필요한 데이터 소스 파일들을 저장>
:: UserData    | Record  <기록부 파일을 암호화하여 저장>
::             | Database  <데이터베이스 파일을 암호화하여 저장>
::             | Delivery  <전달사항 파일을 암호화하여 저장>
::  Install\BuildSource 폴더 내부에서 필요한 소스를 참조함


::  ProgramBuild.bat - ArisuRecord 폴더를 생성하여 실행 파일에 필요한 데이터를 구축함
::  하단 주석문 내용은 Utility.Info.DefaultFilePath의 내용 일부를 참조함
::  Excel  <엑셀 파일과 연동하기위한 라이브러리 및 실행파일>
::  exec  <프로그램 실행을 위한 라이브러리 및 실행파일>


::  InstallBuild.bat - setup.exe 생성