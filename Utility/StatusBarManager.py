from PyQt5.QtWidgets import QStatusBar, QLabel
from Utility.UI.BaseUI import *

class StatusBarManager:
    __INSTANCE = None

    def __init__(self):
        super().__init__()
        self.__status_bar: QStatusBar = None
        self.__label: QLabel = None
        self.__current_message: str = None

    @classmethod
    def __instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    @classmethod
    def setStatusBar(cls, status_bar: QStatusBar) -> None:
        cls.__instance().__status_bar = status_bar
        cls.__instance().__label = BaseUI.basicQLabel()
        cls.__instance().__status_bar.addPermanentWidget(cls.__instance().__label)
        status_bar.messageChanged.connect(cls.__myMessageChanged)

    @classmethod
    def setLabelConnection(cls, is_connected: bool) -> None:
        lbl = cls.__instance().__label
        if lbl == None:
            raise AttributeError
        if is_connected:
            lbl.setText('[ 연결성공 ]')
        else:
            lbl.setText('[ 연결실패 ]')

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
    def __myMessageChanged(cls, text: str) -> None:
        if text == '':
            cls.__instance().__status_bar.showMessage('대기중')
