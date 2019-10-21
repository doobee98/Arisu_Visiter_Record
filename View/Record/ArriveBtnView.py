from Utility.UI.BaseUI import *


class ArriveBtnViewSignal(QObject):
    ArriveBtnClicked = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)

class ArriveBtnView(QWidget):
    def __init__(self):
        super().__init__()

        # 시그널 정의
        self.__signal_set = ArriveBtnViewSignal(self)

        #   들어오다 버튼 생성 및 스타일링
        self.arrive_short_cut_text = 'Ctrl + A'
        self.arrive_btn = BaseUI.basicQPushButton(text='들어오다\n(' + self.arrive_short_cut_text + ')')
        self.arrive_btn.setFixedWidth(int(self.arrive_btn.sizeHint().width() * 1.5))  # 임시 매직넘버값
        self.arrive_btn.setFixedHeight(int(self.arrive_btn.sizeHint().height() * 1.5))
        self.arrive_btn.clicked.connect(self.arriveBtnClicked)

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(self.arrive_btn)

        self.setLayout(hbox)

    def __str__(self):
        return 'ArriveBtnView'

    def getSignalSet(self) -> ArriveBtnViewSignal:
        return self.__signal_set

    @MyPyqtSlot()
    def arriveBtnClicked(self):
        self.getSignalSet().ArriveBtnClicked.emit()


