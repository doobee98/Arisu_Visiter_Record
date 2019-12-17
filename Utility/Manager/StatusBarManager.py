from PyQt5.QtWidgets import QStatusBar, QLabel
from Utility.MyPyqt.MyDefaultWidgets import *

"""
StatusBarManager
전역 클래스
MainView(QMainWindow)의 상태바를 관리한다.
"""


class StatusBarManager:
    __INSTANCE = None
    @classmethod
    def __instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    def __init__(self):
        super().__init__()
        self.__status_bar: QStatusBar = None
        self.__label: QLabel = None
        self.__current_message: str = None

    """
    property
    * statusBar  (initialize를 겸함)
    """
    @classmethod
    def setStatusBar(cls, status_bar: QStatusBar) -> None:
        cls.__instance().__status_bar = status_bar
        cls.__instance().__label = MyDefaultWidgets.basicQLabel()
        cls.__instance().__status_bar.addPermanentWidget(cls.__instance().__label)
        status_bar.messageChanged.connect(cls.__myMessageChanged)

    """
    method
    * setMessage, setIdleStatus
    * setLabelConnection
    """
    @classmethod
    def setMessage(cls, message: str, msecs: int = 0) -> None:
        if cls.__instance().__status_bar == None:
            raise AttributeError
        if cls.__instance().__status_bar.currentMessage() != message:
            cls.__instance().__status_bar.showMessage(message, msecs)
            ExecuteLogger.printLog('Status: ' + message)

    @classmethod
    def setIdleStatus(cls) -> None:
        cls.setMessage('대기중')

    @classmethod
    def setLabelConnection(cls, is_connected: bool) -> None:
        lbl = cls.__instance().__label
        if lbl == None:
            raise AttributeError
        if is_connected:
            lbl.setText('[ 연결성공 ]')
        else:
            lbl.setText('[ 연결실패 ]')

    """
    slot
    * __myMessageChanged
    """
    @classmethod
    def __myMessageChanged(cls, text: str) -> None:
        if text == '':
            cls.__instance().__status_bar.showMessage('대기중')  # todo setMessage로 바꿔도 될까?
