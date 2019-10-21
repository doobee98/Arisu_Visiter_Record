from Utility.UI.BaseUI import *


class ScrollButtonViewSignal(QObject):
    ScrollBtnClicked = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)


class ScrollButtonView(QWidget):
    def __init__(self):
        super().__init__()

        # 시그널 정의
        self.__signal_set = ScrollButtonViewSignal(self)


        # 스크롤 라벨 생성
        self.scroll_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text='이어 쓰기\n(Ctrl + Q)')

        #   스크롤 버튼 생성 및 스타일링
        #self.scroll_short_cut_text = 'Ctrl + Q'
        self.scroll_btn = BaseUI.basicQPushButton(text='▼')
        #self.scroll_btn.setFixedWidth(30)
        #self.arrive_btn.setFixedWidth(int(self.arrive_btn.sizeHint().width() * 1.5))  # 임시 매직넘버값
        #self.arrive_btn.setFixedHeight(int(self.arrive_btn.sizeHint().height() * 1.5))
        self.scroll_btn.clicked.connect(self.scrollBtnClicked)

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(self.scroll_lbl)
        hbox.addStretch(1)
        hbox.addWidget(self.scroll_btn)

        self.setLayout(hbox)

    def __str__(self):
        return 'ScrollBtnView'

    def getSignalSet(self) -> ScrollButtonViewSignal:
        return self.__signal_set

    @MyPyqtSlot()
    def scrollBtnClicked(self):
        self.getSignalSet().ScrollBtnClicked.emit()


