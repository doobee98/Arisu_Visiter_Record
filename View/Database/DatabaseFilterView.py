from Utility.UI.BaseUI import *
from View.Database.DatabaseFilterTableView import *


class DatabaseFilterViewSignal(QObject):
    AddNewVisitorRequest = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)


class DatabaseFilterView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__signal_set = DatabaseFilterViewSignal(self)

        # 그룹 생성
        self.group = QGroupBox()
        
        # 필터 테이블 생성
        self.table = DatabaseFilterTableView()
        
        # 라벨 생성
        self.lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize()+3),
                                      text='데이터 추가하기')

        # 버튼 생성
        self.button = BaseUI.basicQPushButton(text='추가')
        self.button.clicked.connect(self.addBtnClicked)

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(self.lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.table)
        hbox.addStretch(3)
        hbox.addWidget(self.button)
        hbox.addStretch(4)

        self.group.setLayout(hbox)
        vbox = QVBoxLayout()
        vbox.addWidget(self.group)
        self.setLayout(vbox)

    def getSignalSet(self) -> DatabaseFilterViewSignal:
        return self.__signal_set

    def addBtnClicked(self):
        self.getSignalSet().AddNewVisitorRequest.emit(self.table.getRowData())
