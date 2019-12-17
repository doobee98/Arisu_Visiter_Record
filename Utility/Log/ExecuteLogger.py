import inspect, sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from Utility.MyPyqt.MyMessageBox import *
from Utility.Info.DefaultFilePath import *
from Utility.Log.ErrorLogger import *

"""
ExecuteLogger
전역 클래스
실행 로그를 로그파일에 기록함
"""


class ExecuteLogger:
    __FileName = 'Log.txt'

    """
    method
    * printLog
    """
    @classmethod
    def printLog(cls, text: str):
        try:
            directory, file_name = DefaultFilePath.Log, cls.__FileName
            file_path = (directory + '\\' + file_name) if directory != '' else file_name
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + text + '\n')
        except Exception as e:
            ErrorLogger.reportError('Log.txt 작성 중 에러가 발생했습니다.\n', e)
