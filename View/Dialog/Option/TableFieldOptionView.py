from View.Dialog.Option.AbstractOptionView import *
from Utility.Module.ConfigModule import *
from Utility.MyPyqt.MyMessageBox import *

"""
TableFieldOptionView(AbstractOptionView)
다른 OptionView와 다르게, TableFieldModel 모두를 이 곳에 표현하지 않고
Field별로 하나씩 표시한다.
Field 선택은 상위 OptionDialog에서 처리한다.
"""  # todo 이쁘게 정리좀 하자


class TableFieldOptionViewSignal(QObject):
    ChangeButtonClicked = pyqtSignal()
    AddButtonClicked = pyqtSignal()
    RemoveButtonClicked = pyqtSignal()
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class TableFieldOptionView(AbstractOptionView):
    ON = 1
    OFF = 2

    def __init__(self, field_name: str, parent=None):
        Global, Record, Database = TableFieldOption.Global, TableFieldOption.Record, TableFieldOption.Database
        super().__init__(parent)
        self.__signal_set = TableFieldOptionViewSignal(self)
        self.__model: TableFieldConfigModel = ConfigModule.TableField
        self.__model.signalSet().OptionChanged.connect(self.myRender)

        self.__field_name = field_name
        self.__button_group_dict: Dict[Flag, QButtonGroup] = {}

        gbox = QGridLayout()
        gbox.addWidget(MyDefaultWidgets.basicQLabel(text='ON'), 0, 2)
        gbox.addWidget(MyDefaultWidgets.basicQLabel(text='OFF'), 0, 3)

        row_iter = 1
        # 전역 필드
        start_row = row_iter
        for idx_iter, field_flag_iter in enumerate(Global.changableOptionList()):
            field_text_iter = self.__globalPrintedText(field_flag_iter)
            # 라벨
            lbl = MyDefaultWidgets.basicQLabel(text=field_text_iter, alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 1)
            # 라디오 버튼
            btn_group = QButtonGroup()
            on_btn, off_btn = QRadioButton(), QRadioButton()
            btn_group.addButton(on_btn, TableFieldOptionView.ON)
            btn_group.addButton(off_btn, TableFieldOptionView.OFF)
            self.__button_group_dict[field_flag_iter] = btn_group
            gbox.addWidget(on_btn, row_iter, 2)
            gbox.addWidget(off_btn, row_iter, 3)
            gbox.setRowStretch(row_iter, 1)
            row_iter += 1
        end_row = row_iter
        title_lbl = MyDefaultWidgets.basicQLabel(text='전역')
        title_lbl.setStyleSheet("border: 1px solid black")
        gbox.addWidget(title_lbl, start_row, 0, end_row - start_row, 1)

        # 기록부 필드
        gbox.addWidget(QLabel(), row_iter, 0, 1, 3)
        row_iter += 1
        start_row = row_iter
        for idx_iter, field_flag_iter in enumerate(Record.changableOptionList()):
            field_text_iter = self.__recordPrintedText(field_flag_iter)
            # 라벨
            lbl = MyDefaultWidgets.basicQLabel(text=field_text_iter, alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 1)
            # 라디오 버튼
            btn_group = QButtonGroup()
            on_btn, off_btn = QRadioButton(), QRadioButton()
            btn_group.addButton(on_btn, TableFieldOptionView.ON)
            btn_group.addButton(off_btn, TableFieldOptionView.OFF)
            self.__button_group_dict[field_flag_iter] = btn_group
            gbox.addWidget(on_btn, row_iter, 2)
            gbox.addWidget(off_btn, row_iter, 3)
            gbox.setRowStretch(row_iter, 1)
            row_iter += 1
        end_row = row_iter
        title_lbl = MyDefaultWidgets.basicQLabel(text=' 기록부 ')
        title_lbl.setStyleSheet("border: 1px solid black")
        gbox.addWidget(title_lbl, start_row, 0, end_row - start_row, 1)

        # 데이터베이스 필드
        gbox.addWidget(QLabel(), row_iter, 0, 1, 3)
        row_iter += 1
        start_row = row_iter
        for idx_iter, field_flag_iter in enumerate(Database.changableOptionList()):
            field_text_iter = self.__databasePrintedText(field_flag_iter)
            # 라벨
            lbl = MyDefaultWidgets.basicQLabel(text=field_text_iter, alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 1)
            # 라디오 버튼
            btn_group = QButtonGroup()
            on_btn, off_btn = QRadioButton(), QRadioButton()
            btn_group.addButton(on_btn, TableFieldOptionView.ON)
            btn_group.addButton(off_btn, TableFieldOptionView.OFF)
            self.__button_group_dict[field_flag_iter] = btn_group
            gbox.addWidget(on_btn, row_iter, 2)
            gbox.addWidget(off_btn, row_iter, 3)
            gbox.setRowStretch(row_iter, 1)
            row_iter += 1
        end_row = row_iter
        title_lbl = MyDefaultWidgets.basicQLabel(text='DB')
        title_lbl.setStyleSheet("border: 1px solid black")
        gbox.addWidget(title_lbl, start_row, 0, end_row - start_row, 1)

        gbox.setHorizontalSpacing(40) # todo 임의값

        change_button = MyDefaultWidgets.basicQPushButton(text='이름변경')
        change_button.clicked.connect(lambda: self.signalSet().ChangeButtonClicked.emit())
        add_button = MyDefaultWidgets.basicQPushButton(text='추가')
        add_button.clicked.connect(lambda: self.signalSet().AddButtonClicked.emit())
        remove_button = MyDefaultWidgets.basicQPushButton(text='삭제')
        remove_button.clicked.connect(lambda: self.signalSet().RemoveButtonClicked.emit())
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(change_button)
        hbox.addStretch(1)
        hbox.addWidget(add_button)
        hbox.addStretch(1)
        hbox.addWidget(remove_button)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(gbox)
        vbox.addLayout(hbox)
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(vbox))
        self.myRender()

    """
    property
    * signalSet
    * fieldName
    """
    def signalSet(self) -> TableFieldOptionViewSignal:
        return self.__signal_set

    def fieldName(self) -> str:
        return self.__field_name

    def setFieldName(self, text: str) -> None:
        self.__field_name = text

    """
    advanced property
    * button
    """
    def button(self, func_enum: Flag, button_type: int) -> QRadioButton:
        return self.__button_group_dict[func_enum].button(button_type)

    """
    method
    * myRender (override)
    * applyOptionChanges (override)
    """
    def myRender(self) -> None:
        field_model = self.__model.fieldModel(self.__field_name)
        for field_flag_iter in self.__button_group_dict.keys():
            if isinstance(field_flag_iter, TableFieldOption.Global):
                enable = field_model.globalOption(field_flag_iter)
            elif isinstance(field_flag_iter, TableFieldOption.Record):
                enable = field_model.recordOption(field_flag_iter)
            else:
                enable = field_model.databaseOption(field_flag_iter)
            current_button_type = TableFieldOptionView.ON if enable else TableFieldOptionView.OFF
            self.button(field_flag_iter, current_button_type).setChecked(True)

    def applyOptionChanges(self) -> None:
        field_model = self.__model.fieldModel(self.__field_name)
        change_enum_list = []
        for field_flag_iter in self.__button_group_dict.keys():
            if isinstance(field_flag_iter, TableFieldOption.Global):
                original_enable = field_model.globalOption(field_flag_iter)
            elif isinstance(field_flag_iter, TableFieldOption.Record):
                original_enable = field_model.recordOption(field_flag_iter)
            else:
                original_enable = field_model.databaseOption(field_flag_iter)
            if original_enable != self.button(field_flag_iter, TableFieldOptionView.ON).isChecked():
                change_enum_list.append(field_flag_iter)

        if change_enum_list:
            reply = MyMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?')
            if reply == MyMessageBox.No:
                self.myRender()
                return
            self.__model.setBlockUpdate(True)
            try:
                for change_enum_iter in change_enum_list:
                    if isinstance(change_enum_iter, TableFieldOption.Global):
                        field_model.setGlobalOption(change_enum_iter, self.button(change_enum_iter, TableFieldOptionView.ON).isChecked())
                    elif isinstance(change_enum_iter, TableFieldOption.Record):
                        field_model.setRecordOption(change_enum_iter, self.button(change_enum_iter, TableFieldOptionView.ON).isChecked())
                    else:
                        field_model.setDatabaseOption(change_enum_iter, self.button(change_enum_iter, TableFieldOptionView.ON).isChecked())
                self.__model.setBlockUpdate(False)
                self.__model.update()
                sys.exit()
            except Exception as e:
                self.__model.setBlockUpdate(True)
                raise e

    """
    print text method
    * __globalPrintedText, __recordPrintedText, __databasePrintedText
    """
    def __globalPrintedText(self, field_enum: TableFieldOption.Global) -> str:
        if field_enum == TableFieldOption.Global.Share:
            return '데이터베이스와 레코드 양쪽에서 공유'
        elif field_enum == TableFieldOption.Global.IsTime:
            return '시간 정보'
        elif field_enum == TableFieldOption.Global.IsDate:
            return '날짜 정보'
        else:
            ErrorLogger.reportError('잘못된 인자입니다.\n' + str(field_enum), AttributeError)

    def __recordPrintedText(self, field_enum: TableFieldOption.Record) -> str:
        if field_enum == TableFieldOption.Record.Active:
            return '활성화'
        elif field_enum == TableFieldOption.Record.Hidden:
            return '화면에서 숨김'
        elif field_enum == TableFieldOption.Record.Group:
            return '+ 버튼으로 복사됨'
        elif field_enum == TableFieldOption.Record.ShareOn:
            return '데이터베이스에 기록됨'
        elif field_enum == TableFieldOption.Record.Bold:
            return '글씨를 두껍게'
        elif field_enum == TableFieldOption.Record.WidthUp:
            return '너비를 두 배로'
        elif field_enum == TableFieldOption.Record.WidthDown:
            return '너비를 내용에 딱 맞게'
        elif field_enum == TableFieldOption.Record.Completer:
            return '자동완성 사용'
        else:
            ErrorLogger.reportError('잘못된 인자입니다.\n' + str(field_enum), AttributeError)

    def __databasePrintedText(self, field_enum: TableFieldOption.Database) -> str:
        if field_enum == TableFieldOption.Database.Active:
            return '활성화'
        elif field_enum == TableFieldOption.Database.Hidden:
            return '화면에서 숨김'
        elif field_enum == TableFieldOption.Database.ShareOn:
            return '기록부에 입력됨'
        elif field_enum == TableFieldOption.Database.Bold:
            return '글씨를 두껍게'
        elif field_enum == TableFieldOption.Database.WidthUp:
            return '너비를 두 배로'
        elif field_enum == TableFieldOption.Database.WidthDown:
            return '너비를 내용에 딱 맞게'
        else:
            ErrorLogger.reportError('잘못된 인자입니다.\n' + str(field_enum), AttributeError)





