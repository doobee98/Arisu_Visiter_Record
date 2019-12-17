from Utility.MyPyqt.MyDefaultWidgets import *

"""
LeaveView
"""


class LeaveViewSignal(QObject):
    LeaveButtonClicked = pyqtSignal()

    def __init__(self, parent = None):
        super().__init__(parent)


class LeaveView(QGroupBox):
    DefaultIDNumBlank = ''
    DefaultNameAll = '모두'

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 시그널 정의
        self.__signal_set = LeaveViewSignal(self)

        # 전체 그룹 박스
        self.setTitle('나가다')
        temp_vbox = QVBoxLayout()
        group_content = QWidget()
        temp_vbox.addWidget(group_content)
        self.setLayout(temp_vbox)

        # 전체 그룹 박스 스타일링
        self.setFont(MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 2))

        # 출입증 번호 그룹박스
        idnum_group = QGroupBox()
        idnum_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text='출입증 번호')
        self.__idnum_le = MyDefaultWidgets.basicQLineEdit(text=LeaveView.DefaultIDNumBlank)
        self.__idnum_le.installFilterFunctions(ConfigModule.FieldFilter.filterFunctionList(TableFieldOption.Necessary.RECORD_ID))

        # 출입증 번호 스타일링
        #   line
        #self.idnum_line.setFixedWidth(100)

        # 출입증 번호 레이아웃
        idnum_hbox = QVBoxLayout()
        idnum_hbox.addWidget(idnum_lbl)
        idnum_hbox.addWidget(self.__idnum_le)
        idnum_group.setLayout(idnum_hbox)

        # 성명 그룹박스
        name_group = QGroupBox()
        name_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text='성명')

        self.__name_le = MyDefaultWidgets.basicQLineEdit(text=LeaveView.DefaultNameAll)
        self.__name_le.installFilterFunctions(ConfigModule.FieldFilter.filterFunctionList(TableFieldOption.Necessary.NAME))

        # 성명 스타일링
        #   line
        #self.name_line.setFixedWidth(100)

        # 성명 레이아웃
        name_hbox = QVBoxLayout()
        name_hbox.addWidget(name_lbl)
        name_hbox.addWidget(self.__name_le)
        name_group.setLayout(name_hbox)

        # 나가다 버튼 위젯
        leave_txt = '나가다 (Ctrl + D)' if ConfigModule.Application.enableShortCut() else '나가다'
        leave_btn = MyDefaultWidgets.basicQPushButton(text=leave_txt)
        leave_btn.clicked.connect(self.leaveButtonClicked)
        leave_btn.setMinimumHeight(int(leave_btn.sizeHint().height() * 1.5))

        # 전체 레이아웃
        QWidget.setTabOrder(idnum_group, name_group)
        QWidget.setTabOrder(name_group, leave_btn)

        g_layout = QGridLayout()
        g_layout.addWidget(idnum_group, 0, 0)
        g_layout.addWidget(name_group, 0, 1)
        g_layout.addWidget(leave_btn, 1, 0, 1, 2)
        group_content.setLayout(g_layout)

    """
    property
    * signalSet
    * recordIdText, nameText
    """
    def signalSet(self) -> LeaveViewSignal:
        return self.__signal_set

    def recordIdText(self) -> str:
        return self.__idnum_le.text()

    def nameText(self) -> str:
        return self.__name_le.text()

    def setRecordIdText(self, text: str) -> None:
        self.__idnum_le.setText(text)

    def setNameText(self, text: str) -> None:
        self.__name_le.setText(text)

    """
    method
    * setDefault
    """
    def setDefault(self) -> None:
        self.setRecordIdText(LeaveView.DefaultIDNumBlank)
        self.setNameText(LeaveView.DefaultNameAll)

    """
    slot
    * leaveButtonClicked
    """
    @MyPyqtSlot()
    def leaveButtonClicked(self) -> None:  # todo 시간없어서 그냥 public으로 하고 ShortCutManager에 등록함
        if self.recordIdText() == LeaveView.DefaultIDNumBlank:
            self.__idnum_le.setFocus()
        else:
            self.signalSet().LeaveButtonClicked.emit()

