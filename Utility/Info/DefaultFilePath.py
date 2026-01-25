import sys, os

"""
DefaultFilePath
프로그램 설치시 디폴트 설치 경로를 테이블화 시킴.

ArisuRecordData | AppData     | log  <실행시 생기는 로그(ErrorReport, ExecuteLog)를 저장>
                              | bin       | config  <실행시 필요한 설정 파일을 암호화하여 저장>
                              | src  <실행시 필요한 데이터 소스 파일들을 저장>
                | UserData    | Record  <기록부 파일을 암호화하여 저장>
                              | Database  <데이터베이스 파일을 암호화하여 저장>
                              | Delivery  <전달사항 파일을 암호화하여 저장>
"""
#todo 해당 경로가 없으면 그냥 create하도록 해버리면 어떨까?


class DefaultFilePath:
    MainFile = 'ArisuRecord'

    USER = None                                         # InitializeArisuRecord에서 cls.registerUserPath로 등록 후 사용
    ExcelExportEXE = None                               # InitializeArisuRecord에서 cls.initializeExcelExportExePath로 초기화 후 사용
    DATA = os.path.expanduser("~\\ArisuRecordData")
    SOURCE = os.path.join(DATA, 'AppData\\src')

    Database = os.path.join(DATA, 'UserData\\Database')
    Record = os.path.join(DATA, 'UserData\\Record')
    Delivery = os.path.join(DATA, 'UserData\\Delivery')
    Log = os.path.join(DATA, 'AppData\\log')
    Config = os.path.join(DATA, 'AppData\\bin\\config')

    ExcelExport = os.path.expanduser("~\\Desktop")
    ExcelRecordSample = os.path.join(SOURCE, 'ReportSample.xlsx')
    ExcelDatabaseSample = os.path.join(SOURCE, 'DatabaseSample.xlsx')
    Icon = os.path.join(SOURCE, 'ArisuIcon.ico')

    @classmethod
    def registerUserPath(cls, user: str) -> None:
        cls.USER = user

    @classmethod
    def initializeExcelExportExePath(cls) -> None:
        _excel_exe_first_directory = os.path.dirname(sys.argv[0])

        # 현재 작업경로 ArisuRecord 폴더 내부로 변경
        os.chdir(_excel_exe_first_directory)
        while True:
            current_directory = os.getcwd()
            if os.path.isdir(current_directory) and current_directory.endswith('ArisuRecord'):  # todo DefaultFilePath를 사용하지 못함
                break
            os.chdir('..\\')
            if current_directory == os.getcwd():
                raise RecursionError

        cls.ExcelExportEXE = os.path.join(current_directory, 'Excel\\ConvertExcel.exe')
