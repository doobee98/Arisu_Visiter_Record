import inspect, sys, traceback
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from Utility.MyPyqt.MyMessageBox import *
from Utility.Info.DefaultFilePath import *

"""
ErrorLogger
전역 클래스
에러 발생시 에러창을 띄우고 로그 파일을 작성함
"""


class ErrorLogger:
    __FileName = 'ErrorReport.txt'

    """
    method
    * reportError (exception 발생시 critical, 강제종료함 / exception 없을 시 warning 띄움)
    """
    @classmethod
    def reportError(cls, what: str = None, exception: Exception = None):
        try:
            caller_frame = inspect.currentframe().f_back
            error_string = cls.__createBaseErrorString(inspect.getframeinfo(caller_frame))
            if what:
                error_string += '           What: ' + what + '\n'
            error_string += '/ Traceback /\n' + traceback.format_exc() + '\n'

            cls.__debugPrint(inspect.getframeinfo(caller_frame), what)
            cls.__writeReportFile(error_string)

            if exception:
                MyMessageBox.critical(QApplication.activeWindow(), '위험', what + '\n' + str(exception))
                sys.exit()
            else:
                MyMessageBox.warning(QApplication.activeWindow(), '경고', what)
        except Exception as e:
            MyMessageBox.critical(QApplication.activeWindow(), '위험',
                                 'ErrorReport.txt 작성 중 에러가 발생했습니다.' + '\n' + str(e))

    """
    private method
    * __createBaseErrorString
    * __writeReportFile
    * __debugPrint
    """
    @classmethod
    def __createBaseErrorString(cls, error_info) -> str:
        (filepath, line_number, function_name, lines, index) = error_info
        filename = filepath.split('\\')[-1]
        result = ''
        result += 'Error Date&Time: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        result += '   CodeFileName: ' + filename + '\n'
        result += '     MethodName: ' + function_name + '\n'
        return result

    @classmethod
    def __writeReportFile(cls, error_string: str):
        error_string += '\n\n'
        directory, file_name = DefaultFilePath.Log, cls.__FileName
        file_path = (directory + '\\' + file_name) if directory != '' else file_name
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(error_string)

    @classmethod
    def __debugPrint(cls, caller, what):
        (filepath, line_number, function_name, lines, index) = caller
        filename = filepath.split('\\')[-1]
        print(filename, '/', function_name, end='')
        if what:
            print(':', what, end='')
        print()