import sys, traceback
from PyQt5.QtWidgets import QApplication
from Controller.MainController import *


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        c = MainController()
        c.Run()

        app.exec_()
    except Exception as e:
        ExecuteLogger.printLog(str(e) + 'TopLevel Quit')
        ErrorLogger.reportError('Unexpected TopLevel Quit', e)
    finally:
        ExecuteLogger.printLog('@@Finish program@@\n')
