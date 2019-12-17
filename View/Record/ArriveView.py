from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ConfigModule import *

"""
ArriveView
"""


class ArriveViewSignal(QObject):
    ArriveButtonClicked = pyqtSignal()

    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class ArriveView(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 시그널 정의
        self.__signal_set = ArriveViewSignal(self)

        # 들어오다 버튼 생성 및 스타일링
        arrive_txt = '들어오다\n(Ctrl + A)' if ConfigModule.Application.enableShortCut() else '들어오다'
        arrive_btn = MyDefaultWidgets.basicQPushButton(text=arrive_txt)
        arrive_btn.setFixedWidth(int(arrive_btn.sizeHint().width() * 1.5))  # todo 임시 매직넘버값
        arrive_btn.setFixedHeight(int(arrive_btn.sizeHint().height() * 1.5))
        arrive_btn.clicked.connect(lambda: self.signalSet().ArriveButtonClicked.emit())

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(arrive_btn)

        self.setLayout(hbox)

    """
    property
    * signalSet
    """
    def signalSet(self) -> ArriveViewSignal:
        return self.__signal_set
