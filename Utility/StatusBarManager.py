from PyQt5.QtWidgets import QStatusBar

class StatusBarManager:
    __INSTANCE = None

    def __init__(self):
        super().__init__()
        self.__status_bar: QStatusBar = None

    @classmethod
    def __instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    @classmethod
    def setStatusBar(cls, status_bar: QStatusBar) -> None:
        cls.__instance().__status_bar = status_bar
        status_bar.messageChanged.connect(cls.__myMessageChanged)

    @classmethod
    def setMessage(cls, message: str, msecs: int = 0) -> None:
        if cls.__instance().__status_bar == None:
            raise AttributeError
        cls.__instance().__status_bar.showMessage(message, msecs)

    @classmethod
    def setIdleStatus(cls) -> None:
        if cls.__instance().__status_bar == None:
            raise AttributeError
        cls.setMessage('대기중')

    @classmethod
    def __myMessageChanged(cls, text: str) -> None:
        if text == '':
            cls.setIdleStatus()
