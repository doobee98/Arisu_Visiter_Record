import inspect, sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMessageBox
from Utility.File.FilePathConfig import *


# 에러 로거에서 에러가 발생할 경우를 처리하여야함
# try except
class ExecuteLogger:
    __FileName = 'Log'

    @classmethod
    def printLog(cls, text: str):
        try:
            directory, file_name = FilePathConfig.getLogPath(cls.__FileName)
            file_path = (directory + '\\' + file_name) if directory != '' else file_name
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + text + '\n')
        except Exception as e:
            QMessageBox.critical(QApplication.activeWindow(), '위험',
                                 'ExecuteLogger - 처리할 수 없는 에러입니다.' + '\n' + str(e))
