from Utility.UI.BaseUI import *


class TakeOverViewSignal(QObject):
    TakeOverBtnClicked = pyqtSignal(str, str, str)
    DeliveryBtnClicked = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)


class TakeOverView(QWidget):
    DefaultWorker = '근무자'
    DefaultTime = '08:00'

    def __init__(self):
        super().__init__()

        # 시그널 정의
        self.__signal_set = TakeOverViewSignal()

        # 전체 그룹 박스
        self.group = QGroupBox('인수인계')

        # 전체 그룹 박스 스타일링
        # 타이틀만 굵고 크게, 내용물은 기본 크기 유지
        self.group.setFont(BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize() + 2))
        #self.group_content.setFont(BaseUI.basicQFont())


        # 소속 조
        self.team_group = QGroupBox()
        self.team_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text='소속 조')
        self.team_cb = QComboBox()
        self.team_cb.addItems(['A조', 'B조', 'C조', 'D조'])

        # 소속 조 스타일링
        #   line
        self.team_cb.setFont(BaseUI.basicQFont())
        self.team_cb.setEditable(True)
        self.team_cb.lineEdit().setReadOnly(True)
        self.team_cb.lineEdit().setAlignment(Qt.AlignCenter)
        for i in range(self.team_cb.count()):
            self.team_cb.setItemData(i, Qt.AlignCenter, Qt.TextAlignmentRole)

        # 소속 조 레이아웃
        self.team_vbox = QVBoxLayout()
        self.team_vbox.addStretch(1)
        self.team_vbox.addWidget(self.team_lbl)
        self.team_vbox.addStretch(1)
        self.team_vbox.addWidget(self.team_cb)
        self.team_vbox.addStretch(1)
        self.team_group.setLayout(self.team_vbox)

        # 교대자 이름
        self.worker_group = QGroupBox()
        # self.worker_lbl = QLabel('교대자')
        self.worker_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text='교대자')
        self.worker_line = BaseUI.basicQLineEdit(text=TakeOverView.DefaultWorker)
        #self.worker_line.setFixedWidth(100)

        # 교대자 이름 레이아웃
        self.worker_vbox = QVBoxLayout()
        self.worker_vbox.addStretch(1)
        self.worker_vbox.addWidget(self.worker_lbl)
        self.worker_vbox.addStretch(1)
        self.worker_vbox.addWidget(self.worker_line)
        self.worker_vbox.addStretch(1)
        self.worker_group.setLayout(self.worker_vbox)

        # 교대 시각
        self.time_group = QGroupBox()
        self.time_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text='교대시각')
        self.time_line = BaseUI.basicQLineEdit(text=TakeOverView.DefaultTime)
        #self.time_line.setFixedWidth(100)

        # 교대 시각 레이아웃
        self.time_vbox = QVBoxLayout()
        self.time_vbox.addStretch(1)
        self.time_vbox.addWidget(self.time_lbl)
        self.time_vbox.addStretch(1)
        self.time_vbox.addWidget(self.time_line)
        self.time_vbox.addStretch(1)
        self.time_group.setLayout(self.time_vbox)

        # 인수인계 버튼
        self.take_over_btn = BaseUI.basicQPushButton(text='인수인계')
        self.take_over_btn.clicked.connect(self.takeOverBtnClicked)
        self.take_over_btn.setMinimumHeight(int(self.take_over_btn.sizeHint().height() * 1.5))

        # 전달사항 버튼
        self.delivery_btn = BaseUI.basicQPushButton(text='전달사항')  # ☎📢
        self.delivery_btn.clicked.connect(self.deliveryBtnClicked)

        # 버튼 레이아웃
        vbox_rightbottom = QVBoxLayout()
        vbox_rightbottom.addWidget(self.delivery_btn)
        vbox_rightbottom.addWidget(self.take_over_btn)

        # 전체 레이아웃
        QWidget.setTabOrder(self.team_group, self.worker_group)
        QWidget.setTabOrder(self.worker_group, self.time_group)
        QWidget.setTabOrder(self.time_group, self.take_over_btn)

        self.g_layout = QGridLayout()
        self.g_layout.addWidget(self.team_group, 0, 0)
        self.g_layout.addWidget(self.worker_group, 0, 1)
        self.g_layout.addWidget(self.time_group, 1, 0)
        self.g_layout.addLayout(vbox_rightbottom, 1, 1)

        self.group.setLayout(self.g_layout)

        vbox = QVBoxLayout()
        vbox.addWidget(self.group)
        self.setLayout(vbox)

    def __str__(self):
        return 'TakeOverView'

    def getSignalSet(self) -> TakeOverViewSignal:
        return self.__signal_set

    def setLineEditsDefault(self):
        # self.time_line.setText(TakeOverView.DefaultTime)
        self.worker_line.setText(TakeOverView.DefaultWorker)

    def setCurrentVisitorNumber(self, visitor_num: int) -> None:
        self.remain_number = visitor_num
        self.remain_lbl.setText(f'잔여인원: {self.remain_number}명')

    @pyqtSlot()
    def takeOverBtnClicked(self):
        take_over_team = self.team_cb.currentText()
        take_over_time = self.time_line.text()
        take_over_worker = self.worker_line.text()

        self.getSignalSet().TakeOverBtnClicked.emit(take_over_time, take_over_team, take_over_worker)

    @pyqtSlot()
    def deliveryBtnClicked(self):
        self.getSignalSet().DeliveryBtnClicked.emit()
