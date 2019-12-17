from Utility.MyPyqt.MyDefaultWidgets import *

"""
ScrollView
이어쓰기
"""


class ScrollViewSignal(QObject):
    ScrollButtonClicked = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)


class ScrollView(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 시그널 정의
        self.__signal_set = ScrollViewSignal(self)

        # 스크롤 라벨 생성
        scroll_txt = '이어 쓰기\n(Ctrl + Q)' if ConfigModule.Application.enableShortCut() else '이어 쓰기'
        scroll_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text=scroll_txt)

        # 스크롤 버튼 생성 및 스타일링
        scroll_btn = MyDefaultWidgets.basicQPushButton(text='▼')
        scroll_btn.clicked.connect(lambda: self.signalSet().ScrollButtonClicked.emit())

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(scroll_lbl)
        hbox.addStretch(1)
        hbox.addWidget(scroll_btn)

        self.setLayout(hbox)

    """
    property
    * signalSet
    """
    def signalSet(self) -> ScrollViewSignal:
        return self.__signal_set



