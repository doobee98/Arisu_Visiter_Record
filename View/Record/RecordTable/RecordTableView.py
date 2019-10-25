from Utility.Abstract.View.Table.MyTableView import *
from Utility.Config.RecordFieldViewConfig import *
from Model.Record.RecordTableModel import *
from Utility.CompleterListModule import *


class RecordTableViewSignal(MyTableViewSignal):
    FindDatabaseRequest = pyqtSignal(dict)
    ChangeDataGroupRequest = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)


class RecordTableView(MyTableView):
    class Option(MyTableView.Option):
        class Item(MyTableView.Option.Item):
            Inserted = MyTableView.Option.Item.ReadOnly
            Finished = Inserted | MyItemView.Option.Gray

        class Row(MyTableView.Option.Row):
            Basic = auto()
            NotInserted = auto()
            Inserted = auto()
            Finished = auto()
            Takeover = auto()

    def __init__(self, model: RecordTableModel):
        ROW, COL = 10, 16
        super().__init__(ROW, COL)
        self._setSignalSet(RecordTableViewSignal(self))
        self.setVisibleRowCount(15)
        self.setModel(model)

        self.setField(0, '그룹\n추가')
        self.setField(15, '편집')
        model_field_list = ['출입증번호', '성명', '생년월일', '차량번호', '소속', '방문목적', '반출입물품명', '반입/반출량',
                            '비고', '들어오다시간', '들어오다근무자', '나가다시간', '나가다근무자', '고유번호']
        for idx_iter, model_field_iter in enumerate(model_field_list):
            self.setModelField(idx_iter + 1, model_field_iter)

        Config.RecordOption.getSignalSet().OptionChanged.connect(self.optionChanged)

        self.__initItemOptions()
        self.fixTableWidgetSize()

    def __initItemOptions(self) -> None:
        Option = RecordTableView.Option
        # 버튼 옵션
        for row_type_iter in Option.Row:
            if row_type_iter == Option.Row.Basic:
                add_enable, edit_enable, delete_enable, eraser_enable = False, False, True, True  # todo delete-true?
            elif row_type_iter == Option.Row.NotInserted:
                add_enable, edit_enable, delete_enable, eraser_enable = False, False, True, True
            elif row_type_iter == Option.Row.Inserted:
                add_enable, edit_enable, delete_enable, eraser_enable = True, True, True, True
            elif row_type_iter == Option.Row.Finished:
                add_enable, edit_enable, delete_enable, eraser_enable = True, True, True, True
            else:  # Takeover
                add_enable, edit_enable, delete_enable, eraser_enable = False, True, True, False
            self.setRowButton(row_type_iter, 0, [MyButtonInput(ButtonFactory.ButtonType.Add, enable=add_enable)])
            self.setRowButton(row_type_iter, 15, [MyButtonInput(ButtonFactory.ButtonType.Edit, enable=edit_enable),
                                                  MyButtonInput(ButtonFactory.ButtonType.Delete, enable=delete_enable)])
        # 열 옵션
        self.setRowOptionList(Option.Row.Basic, [Option.Item.Basic for i in range(self.columnCount())])
        self.setRowOptionList(Option.Row.NotInserted, [Option.Item.Basic for i in range(self.columnCount())])
        self.setRowOptionList(Option.Row.Inserted, [Option.Item.Inserted for i in range(self.columnCount())])
        self.setRowOptionList(Option.Row.Finished, [Option.Item.Finished for i in range(self.columnCount())])
        self.setRowOptionList(Option.Row.Takeover, [Option.Item.Finished for i in range(self.columnCount())])
        for row_type_iter in Option.Row:
            for col_iter in range(self.columnCount()):
                if col_iter == 1:
                    current_option = self.rowOptionList(row_type_iter)[col_iter]
                    self.setRowOption(row_type_iter, col_iter, current_option | MyItemView.Option.BoldStyle)
                if self.rowButton(Option.Row.Basic, col_iter) is not None:
                    self.setRowOption(row_type_iter, col_iter, Option.Item.Wall)
                if not Config.RecordOption.enableFixId():
                    if self.fieldColumn('고유번호') == col_iter:  # todo: 임시로 고유번호 막음
                        current_option = self.rowOptionList(row_type_iter)[col_iter]
                        self.setRowOption(row_type_iter, col_iter, current_option | MyItemView.Option.Unable)
        self.setRowOptionSpan(Option.Row.Takeover, 1, 15)

    # override
    def setModel(self, model: MyTableModel) -> None:
        super().setModel(model)
        if model:
            self.setRowCount(model.getDataCount() + 10)

    def setModelField(self, column: int, model_field: str) -> None:
        super().setModelField(column, model_field)
        header_item = QTableWidgetItem()
        header_item.setText(str(RecordFieldViewConfig.getOption(model_field, 'lined_name')))
        self.setHorizontalHeaderItem(column, header_item)

    def renderHeader(self) -> None:
        super().renderHeader()
        # 헤더 옵션값
        for field_name_iter in self.modelFieldList():
            field_column_iter = self.fieldColumn(field_name_iter)
            # 헤더 너비 설정
            if RecordFieldViewConfig.getOption(field_name_iter, 'fit_type') == RecordFieldViewConfig.Option.FitToContent:
                self.resizeColumnToContents(field_column_iter)
            elif RecordFieldViewConfig.getOption(field_name_iter, 'fit_type') == RecordFieldViewConfig.Option.FitTwice:
                default_width = self.horizontalHeader().defaultSectionSize()
                self.setColumnWidth(field_column_iter, default_width * 2)

            # 필드 기본 비활성화 여부 결정
            if RecordFieldViewConfig.getOption(field_name_iter, 'base_unactivated') == True:
                self.setRowOption(RecordTableView.Option.Row.Basic, field_column_iter,
                                  RecordTableView.Option.Item.Dotted)
                self.setRowOption(RecordTableView.Option.Row.NotInserted, field_column_iter,
                                  RecordTableView.Option.Item.Dotted)

            if RecordFieldViewConfig.getOption(field_name_iter, 'hide_field') == True:
                # todo 임시로 show enable로 처리함
                self.setColumnHidden(field_column_iter, not Config.RecordOption.enableShowId())
            else:
                self.setColumnHidden(field_column_iter, False)

            if RecordFieldViewConfig.getOption(field_name_iter, 'search_field') == True:
                header_item = self.horizontalHeaderItem(field_column_iter)
                header_item.setForeground(Qt.red)  # 색깔을 뭐로 할까?

                header_font = header_item.font()
                header_font.setBold(True)
                header_item.setFont(header_font)
        # todo 임시 헤더 길이
        # 출입자번호 탭 너비 설정
        self.setColumnWidth(1, 70)

        # 버튼 구역 헤더 너비 설정
        self.setColumnWidth(0, 40)
        self.setColumnWidth(15, 70)

        # todo: interactive section width
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # self.horizontalHeader().sectionResized.connect(self.fixTableWidgetSize)

        self.fixTableWidgetSize()


    # override
    def renderRow(self, row: int) -> None:
        super().renderRow(row)
        if self.rowType(row) == RecordTableView.Option.Row.Takeover:
            take_over_string = self._model().getData(row).getProperty('인수인계')
            self.item(row, 1).setText(take_over_string)

    def rowType(self, row: int) -> Option.Row:
        """
        row에 있는 데이터의 상태를 보고 row type을 판단하여 반환한다.
        """
        table_model = self._model()
        row_type = RecordTableView.Option.Row.Basic

        if row < table_model.getDataCount():
            model_state = table_model.getData(row).getState()
            if table_model.getData(row).isTakeoverRecord():
                row_type = RecordTableView.Option.Row.Takeover
            elif model_state == RecordModel.State.Generated:
                row_type = RecordTableView.Option.Row.NotInserted
            elif model_state == RecordModel.State.Inserted:
                row_type = RecordTableView.Option.Row.Inserted
            elif model_state == RecordModel.State.Finished:
                row_type = RecordTableView.Option.Row.Finished
        else:
            row_type = RecordTableView.Option.Row.Basic

        return row_type

    # override
    def _chooseOptions(self, row: int) -> Tuple[List[MyItemView.Option], List[Optional[List[MyButtonInput]]]]:
        """
        row type에 따른 option을 반환하고, 세부적인 조정이 필요하다면 조정하여 반환한다.
        """
        row_type = self.rowType(row)
        row_option_list, row_button_list = self.rowOptionList(row_type), self.rowButtonList(row_type)
        return row_option_list, row_button_list

    # override
    def addClicked(self):
        btn: QPushButton = self.sender()
        if btn and btn.parent():
            sender_row = self.indexAt(btn.parent().pos()).row()
            sender_row_dict = self.getRowTexts(sender_row)

            group_property_dict = {}
            for field_name in RecordFieldViewConfig.FieldsDictionary.keys():
                if RecordFieldViewConfig.getOption(field_name, 'group_field') is True \
                        and RecordFieldViewConfig.getOption(field_name, 'base_unactivated') is not True:
                    group_property_dict[field_name] = sender_row_dict[field_name]
            self.getSignalSet().InsertDataRequest.emit(sender_row + 1, group_property_dict)

    def myItemFocusChanged(self, current: QTableWidgetItem, previous: QTableWidgetItem) -> None:
        if current:
            self.findRowDatabase(self.currentRow())
        super().myItemFocusChanged(current, previous)

    def findRowDatabase(self, row: int) -> None:
        search_property_dict = {}
        for field_name_iter in self.modelFieldList():
            field_column_iter = self.fieldColumn(field_name_iter)
            if RecordFieldViewConfig.getOption(field_name_iter, 'search_field'):
                if self.item(row, field_column_iter).text():  # 빈 텍스트가 아니라면
                    search_property_dict[field_name_iter] = self.item(row, field_column_iter).text()
        self.getSignalSet().FindDatabaseRequest.emit(search_property_dict)

    def isRowAnyTexts(self, row: int) -> bool:
        if self.item(row, self.fieldColumn('고유번호')).text() == RecordModel.IdDefaultString:
            for col_iter in range(self.columnCount()):
                if col_iter == self.fieldColumn('고유번호'):
                    continue
                else:
                    if self.item(row, col_iter).text() != RecordModel.DefaultString:
                        return True
            return False
        else:
            return super().isRowAnyTexts(row)

    def isRowWritable(self, row: int) -> bool:
        if self.rowType(row) in [RecordTableView.Option.Row.Basic, RecordTableView.Option.Row.NotInserted]:
            return True
        elif self.rowType(row) == RecordTableView.Option.Row.Takeover:
            return False
        else:
            if self.cellWidget(row, 15).layout().itemAt(0).widget().isChecked() is True:  # todo 버튼찾기 단순화
                return True
            else:
                return False

    def getRecordDate(self) -> str:
        if self._model():
            return self._model().getRecordDate()
        else:
            return None

    def setFocusNextRow(self):
        if self._model():
            self.setFocusCell(self._model().getDataCount(), 1)
    
    @MyPyqtSlot()
    def optionChanged(self) -> None:
        Option = RecordTableView.Option
        if not Config.RecordOption.enableFixId():
            id_column = self.fieldColumn('고유번호')
            for row_type_iter in Option.Row:
                current_option = self.rowOption(row_type_iter, id_column)
                self.setRowOption(row_type_iter, id_column, current_option | MyItemView.Option.Unable)
        else:
            id_column = self.fieldColumn('고유번호')
            self.setRowOption(Option.Row.Basic, id_column, Option.Item.Basic)
            self.setRowOption(Option.Row.NotInserted, id_column, Option.Item.Basic)
            self.setRowOption(Option.Row.Inserted, id_column, Option.Item.Inserted)
            self.setRowOption(Option.Row.Finished, id_column, Option.Item.Finished)
            self.setRowOption(Option.Row.Takeover, id_column, Option.Item.Finished | MyItemView.Option.Spanned)
            # todo: 임시로 spanned 넣음. 초기화하는 메소드를 추가할 것
        self.render()

    def editItem(self, item: QTableWidgetItem) -> None:
        super().editItem(item)
        line_edit: ItemLineEdit = self.cellWidget(item.row(), item.column())
        field = self.fieldList()[item.column()]
        line_edit.installFilterFunctions(Config.FilterOption.activeFunctionList(field))
        completer_list = CompleterListModule.getCompleterList(item.row(), item.column())
        if completer_list:
            line_edit.setCompleterList(completer_list)
        if RecordFieldViewConfig.getOption(self.fieldList()[item.column()], 'time_field') is True:
            line_edit.setTimeMask()

    def openPersistentEditor(self, item: QTableWidgetItem) -> None:
        # todo 버그때문에 잠금
        super().openPersistentEditor(item)
        le: ItemLineEdit = self.cellWidget(item.row(), item.column())
        le.setCompleterList([])

    """
    자동완성 기능: completer list를 만들어내서 자동완성함
    현재 문제점: consistent line edit로 편집할 때는 lineedit를 딱 한번만 만들고 계속 켜두기 때문에,
    만들 당시에 있던 정보만 활용가능함. 이 문제점을 해결하려면 _getCompleterList를 lineedit에 focus 될때마다 호출해야함.
    """
