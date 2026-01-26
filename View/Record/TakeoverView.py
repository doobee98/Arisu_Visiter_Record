from Utility.MyPyqt.MyDefaultWidgets import *

"""
TakeoverView
"""


class TakeoverViewSignal(QObject):
    TakeoverButtonClicked = pyqtSignal()
    DeliveryButtonClicked = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)


class TakeoverView(QGroupBox):
    DefaultWorker = '근무자'
    DefaultTime = '08:00'

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 시그널 정의
        self.__signal_set = TakeoverViewSignal(self)

        # 전체 위젯 스타일링
        # 타이틀만 굵고 크게, 내용물은 기본 크기 유지
        self.setTitle('인수인계')
        self.setFont(MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 2))

        # 소속 조
        team_group = QGroupBox()
        team_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text='소속 조')
        self.__team_cb = QComboBox()
        self.__team_cb.addItems(['A조', 'B조', 'C조', 'D조'])

        # 소속 조 스타일링
        #   line
        self.__team_cb.setFont(MyDefaultWidgets.basicQFont())
        self.__team_cb.setEditable(True)
        self.__team_cb.lineEdit().setAlignment(Qt.AlignCenter)
        for i in range(self.__team_cb.count()):
            self.__team_cb.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

        # 소속 조 레이아웃
        team_vbox = QVBoxLayout()
        team_vbox.addStretch(1)
        team_vbox.addWidget(team_lbl)
        team_vbox.addStretch(1)
        team_vbox.addWidget(self.__team_cb)
        team_vbox.addStretch(1)
        team_group.setLayout(team_vbox)

        # 교대자 이름
        worker_group = QGroupBox()
        worker_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text='교대자')
        self.__worker_le = MyDefaultWidgets.basicQLineEdit(text=TakeoverView.DefaultWorker)
        self.__worker_le.installFilterFunctions(ConfigModule.FieldFilter.filterFunctionList(TableFieldOption.Necessary.NAME))

        # 교대자 이름 레이아웃
        worker_vbox = QVBoxLayout()
        worker_vbox.addStretch(1)
        worker_vbox.addWidget(worker_lbl)
        worker_vbox.addStretch(1)
        worker_vbox.addWidget(self.__worker_le)
        worker_vbox.addStretch(1)
        worker_group.setLayout(worker_vbox)

        # 교대 시각
        time_group = QGroupBox()
        time_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text='교대시각')
        self.__time_le = MyDefaultWidgets.basicQLineEdit(text=TakeoverView.DefaultTime)
        self.__time_le.setTimeMask()
        # self.__time_le.editingFinished.connect(lambda: self.time_line.setText(ConfigModule.FilterOption.FilterFunction.time(self.time_line.text())))

        # 교대 시각 레이아웃
        time_vbox = QVBoxLayout()
        time_vbox.addStretch(1)
        time_vbox.addWidget(time_lbl)
        time_vbox.addStretch(1)
        time_vbox.addWidget(self.__time_le)
        time_vbox.addStretch(1)
        time_group.setLayout(time_vbox)

        # 인수인계 버튼
        take_over_btn = MyDefaultWidgets.basicQPushButton(text='인수인계')
        take_over_btn.clicked.connect(lambda: self.signalSet().TakeoverButtonClicked.emit())
        take_over_btn.setMinimumHeight(int(take_over_btn.sizeHint().height() * 1.5))

        # 전달사항 버튼
        delivery_btn = MyDefaultWidgets.basicQPushButton(text='전달사항')  # ☎📢
        delivery_btn.clicked.connect(lambda: self.signalSet().DeliveryButtonClicked.emit())

        # 버튼 레이아웃
        vbox_rightbottom = QVBoxLayout()
        vbox_rightbottom.addWidget(delivery_btn)
        vbox_rightbottom.addWidget(take_over_btn)

        # 전체 레이아웃
        QWidget.setTabOrder(team_group, worker_group)
        QWidget.setTabOrder(worker_group, time_group)
        QWidget.setTabOrder(time_group, take_over_btn)

        g_layout = QGridLayout()
        g_layout.addWidget(team_group, 0, 0)
        g_layout.addWidget(worker_group, 0, 1)
        g_layout.addWidget(time_group, 1, 0)
        g_layout.addLayout(vbox_rightbottom, 1, 1)

        self.setLayout(g_layout)

    """
    property
    * signalSet
    * teamText, timeText, workerText
    """
    def signalSet(self) -> TakeoverViewSignal:
        return self.__signal_set

    def teamText(self) -> str:
        return self.__team_cb.currentText()

    def setTeamText(self, text: str) -> None:
        self.__team_cb.setCurrentText(text)  # todo 콤보박스에서 이게 되나?

    def timeText(self) -> str:
        return self.__time_le.text()

    def setTimeText(self, text: str) -> None:
        self.__time_le.setText(text)

    def workerText(self) -> str:
        return self.__worker_le.text()

    def setWorkerText(self, text: str) -> None:
        self.__worker_le.setText(text)

    """
    method
    * setDefault
    """
    def setDefault(self):
        self.setWorkerText(TakeoverView.DefaultWorker)


