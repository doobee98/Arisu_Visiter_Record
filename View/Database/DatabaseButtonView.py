from Utility.UI.BaseUI import *


class DatabaseButtonViewSignal(QObject):
    AddNewVisitorRequest = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class DatabaseButtonView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__signal_set = DatabaseButtonViewSignal(self)

        self.add_btn = BaseUI.basicQPushButton(text='추가')
        self.add_btn.clicked.connect(self.addBtnClicked)

        vbox = QVBoxLayout()
        vbox.addWidget(self.add_btn)

        self.setLayout(vbox)

    def getSignalSet(self) -> DatabaseButtonViewSignal:
        return self.__signal_set

    def addBtnClicked(self):
        self.getSignalSet().AddNewVisitorRequest.emit()
