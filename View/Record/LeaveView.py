from Utility.UI.BaseUI import *


class LeaveViewSignal(QObject):
    LeaveBtnClicked = pyqtSignal(str, str)

    def __init__(self, parent = None):
        super().__init__(parent)


class LeaveView(QWidget):
    DefaultIDNumBlank = ''
    DefaultNameAll = '모두'

    def __init__(self):
        super().__init__()

        # 시그널 정의
        self.__signal_set = LeaveViewSignal(self)

        # 전체 그룹 박스
        self.group = QGroupBox('나가다')
        temp_vbox = QVBoxLayout()
        self.group_content = QWidget()
        temp_vbox.addWidget(self.group_content)
        self.group.setLayout(temp_vbox)

        # 전체 그룹 박스 스타일링
        self.group.setFont(BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize() + 2))

        # 출입증 번호 그룹박스
        self.idnum_group = QGroupBox()
        self.idnum_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text='출입증 번호')
        self.idnum_line = BaseUI.basicQLineEdit(text=LeaveView.DefaultIDNumBlank)
        self.idnum_line.installFilterFunctions(Config.FilterOption.activeFunctionList('출입증번호'))

        # 출입증 번호 스타일링
        #   line
        #self.idnum_line.setFixedWidth(100)

        # 출입증 번호 레이아웃
        self.idnum_hbox = QVBoxLayout()
        self.idnum_hbox.addWidget(self.idnum_lbl)
        self.idnum_hbox.addWidget(self.idnum_line)
        self.idnum_group.setLayout(self.idnum_hbox)

        # 성명 그룹박스
        self.name_group = QGroupBox()
        self.name_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text='성명')

        self.name_line = BaseUI.basicQLineEdit(text=LeaveView.DefaultNameAll)
        self.name_line.installFilterFunctions(Config.FilterOption.activeFunctionList('성명'))

        # 성명 스타일링
        #   line
        #self.name_line.setFixedWidth(100)

        # 성명 레이아웃
        self.name_hbox = QVBoxLayout()
        self.name_hbox.addWidget(self.name_lbl)
        self.name_hbox.addWidget(self.name_line)
        self.name_group.setLayout(self.name_hbox)

        # 나가다 버튼 위젯
        self.leave_short_cut_text = 'Ctrl + D'
        self.leave_btn = BaseUI.basicQPushButton(text='나가다 (' + self.leave_short_cut_text + ')')
        self.leave_btn.clicked.connect(self.leaveBtnClicked)
        self.leave_btn.setMinimumHeight(int(self.leave_btn.sizeHint().height() * 1.5))

        # 전체 레이아웃
        QWidget.setTabOrder(self.idnum_group, self.name_group)
        QWidget.setTabOrder(self.name_group, self.leave_btn)

        self.g_layout = QGridLayout()
        self.g_layout.addWidget(self.idnum_group, 0, 0)
        self.g_layout.addWidget(self.name_group, 0, 1)
        self.g_layout.addWidget(self.leave_btn, 1, 0, 1, 2)
        self.group_content.setLayout(self.g_layout)

        vbox = QVBoxLayout()
        vbox.addWidget(self.group)
        self.setLayout(vbox)

    def __str__(self):
        return 'LeaveView'

    def getSignalSet(self) -> LeaveViewSignal:
        return self.__signal_set

    def setLineEditsDefault(self):
        self.idnum_line.setText(LeaveView.DefaultIDNumBlank)
        self.name_line.setText(LeaveView.DefaultNameAll)

    @MyPyqtSlot()
    def leaveBtnClicked(self):
        visitor_num = self.idnum_line.text()
        visitor_name = self.name_line.text()

        if visitor_num == LeaveView.DefaultIDNumBlank:
            self.idnum_line.setFocus()
        else:
            self.getSignalSet().LeaveBtnClicked.emit(visitor_num, visitor_name)

