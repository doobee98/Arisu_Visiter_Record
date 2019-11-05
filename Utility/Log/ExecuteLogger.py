import inspect, sys
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from Utility.Abstract.View.MyMessageBox import *
from Utility.File.BasicFileTable import *


# 에러 로거에서 에러가 발생할 경우를 처리하여야함
# try except
class ExecuteLogger:
    __FileName = 'Log.txt'

    @classmethod
    def printLog(cls, text: str):
        try:
            directory, file_name = BasicFileTable.Log, cls.__FileName
            file_path = (directory + '\\' + file_name) if directory != '' else file_name
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + text + '\n')
        except Exception as e:
            MyMessageBox.critical(QApplication.activeWindow(), '위험',
                                 'ExecuteLogger - 처리할 수 없는 에러입니다.' + '\n' + str(e))
