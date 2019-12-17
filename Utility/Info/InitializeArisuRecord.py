import sys, os

"""
InitializeArisuRecord
프로그램 초기화 시 필수적으로 필요한 기능을 실행하고 정보를 얻어옴
* 기본 파일 경로 읽음
* 현재 작업 경로 설정 (설치된 ArisuRecord 경로를 찾아 최상위 경로로 지정함)
* 파일 경로 정보를 담고있는 FilePathConfig를 로드함
* 엑셀 모듈 관련 정보를 담고있는 ExcelModuleInformation를 로드함
** 에러시 오류창 팝업후 종료
"""

_user_first_directory = os.getcwd()
_exe_first_directory = os.path.dirname(sys.argv[0])
try:
    # 현재 작업경로 ArisuRecord 폴더 내부로 변경
    os.chdir(_exe_first_directory)
    while True:
        current_directory = os.getcwd()
        if os.path.isdir(current_directory) and current_directory.endswith('ArisuRecord'):  # todo DefaultFilePath를 사용하지 못함
            break
        os.chdir('..\\')
        if current_directory == os.getcwd():
            raise RecursionError
    print('current directory:', os.getcwd())

    # 초기 경로 UserPath에 등록
    import Utility.Info.DefaultFilePath
    Utility.Info.DefaultFilePath.DefaultFilePath.registerUserPath(_user_first_directory)

    # FilePathConfig 로딩
    import Model.Config.FilePathConfigModel
    Model.Config.FilePathConfigModel.FilePathConfigModel.instance()

    # ExcelModuleInformation 로딩
    import Utility.Module.Excel.ExcelModuleInformation
    Utility.Module.Excel.ExcelModuleInformation.ExcelModuleInformation.instance()

except Exception as e:
    from PyQt5.QtWidgets import *
    error_string = '프로그램 초기화 도중 오류가 발생해 종료되었습니다.\n'
    error_string += '기본 파일을 로드하는 동안 에러가 발생했습니다.\n'
    error_string += f'{"ArisuRecord"} 파일이나 경로가 존재하지 않습니다.\n'
    error_string += f'{"현재파일 위치":<7}: {_user_first_directory}\n'
    error_string += f'{"실행파일 위치":<7}: {_exe_first_directory}\n'
    error_string += f'{"오류":<14}: {str(e)}'

    if QApplication.instance():
        app = QApplication(sys.argv)
        main = QMainWindow()
        QMessageBox.critical(main, '위험', error_string)
        app.exec_()
    else:
        QMessageBox.critical(QApplication.activeWindow(), '위험', error_string)
    sys.exit()
