import InitializeArisuRecord
import sys, traceback
from PyQt5.QtWidgets import QApplication
from Controller.MainController import *


if __name__ == '__main__':
    try:
        # Execute App
        app = QApplication(sys.argv)
        ExecuteLogger.printLog(str(sys.argv))  # todo 제거하기
        c = MainController()
        c.Run()
        if len(sys.argv) > 1:
            for idx in range(1, len(sys.argv)):
                c.openRecordFile(sys.argv[idx])  # todo 오늘꺼를 또 열수도 있음
        app.exec_()
    except Exception as e:
        ExecuteLogger.printLog(str(e) + 'TopLevel Quit')
        ErrorLogger.reportError('Unexpected TopLevel Quit', e)
    finally:
        ExecuteLogger.printLog('@@Finish program@@\n')
