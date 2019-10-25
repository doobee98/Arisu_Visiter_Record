from Utility.Abstract.View.Table.MyTableView import *
from Model.Database.DatabaseModel import *
from Utility.Config.DatabaseFieldViewConfig import *


class DatabaseTableViewSignal(MyTableViewSignal):
    SortTableRequest = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)


class DatabaseTableView(MyTableView):
    class Option(MyTableView.Option):
        class Item(MyTableView.Option.Item):
            Fixed = MyTableView.Option.Item.Wall | MyItemView.Option.LightGray

        class Row(MyTableView.Option.Row):
            Basic = auto()

    def __init__(self, database_model: DatabaseModel):
        ROW, COL = 10, 10
        super().__init__(ROW, COL)
        self._setSignalSet(DatabaseTableViewSignal(self))
        self.setVisibleRowCount(20)
        self.setModel(database_model)

        self.setField(9, '편집')
        model_field_list = ['고유번호', '성명', '생년월일', '차량번호', '소속', '방문목적', '비고', '최초출입날짜', '최근출입날짜']
        for idx_iter, model_field_iter in enumerate(model_field_list):
            self.setModelField(idx_iter, model_field_iter)

        Config.DatabaseOption.getSignalSet().OptionChanged.connect(self.optionChanged)

        self.renderHeader()
        self.__initItemOptions()

        self.horizontalHeader().sectionDoubleClicked.connect(self.headerDoubleClicked)


    # set Database Model
    # 모델 사이즈에 맞춰서 행의 수를 조정함
    def setModel(self, model: DatabaseModel):
        self.setRowCount(model.getDataCount())
        super().setModel(model)

    def __initItemOptions(self) -> None:
        Option = DatabaseTableView.Option
        row_type = Option.Row.Basic
        # 버튼 옵션
        self.setRowButton(row_type, 9, [MyButtonInput(ButtonFactory.ButtonType.Edit, enable=True),
                                              MyButtonInput(ButtonFactory.ButtonType.Delete, enable=True)])
        # 열 옵션
        self.setRowOptionList(row_type, [Option.Item.ReadOnly | MyItemView.Option.White for i in range(self.columnCount())])
        for col_iter in range(self.columnCount()):
            if self.rowButtonList(Option.Row.Basic)[col_iter] is not None:
                self.setRowOption(row_type, col_iter, Option.Item.Wall)
            if not Config.DatabaseOption.enableFixId():
                if self.fieldColumn('고유번호') == col_iter:  # todo: 임시로 고유번호 막음
                    self.setRowOption(row_type, col_iter, Option.Item.Fixed)

    # override
    def setModelField(self, column: int, model_field: str) -> None:
        super().setModelField(column, model_field)
        header_item = QTableWidgetItem()
        header_item.setText(DatabaseFieldViewConfig.getOption(model_field, 'lined_name'))
        self.setHorizontalHeaderItem(column, header_item)

    # override
    def rowType(self, row: int) -> Option.Row:
        row_type = DatabaseTableView.Option.Row.Basic
        return row_type

    # override
    def _chooseOptions(self, row: int) -> Tuple[List[MyItemView.Option], List[Optional[List[MyButtonInput]]]]:
        row_type = self.rowType(row)
        return self.rowOptionList(row_type), self.rowButtonList(row_type)

    def render(self):
        # todo 임시, set row count 오버라이딩 필요함
        if self._model():
            self.setRowCount(self._model().getDataCount())
        super().render()

    def renderHeader(self) -> None:
        super().renderHeader()

        # 헤더 옵션값
        for field_name_iter in self.modelFieldList():
            field_column_iter = self.fieldColumn(field_name_iter)
            # 헤더 너비 설정
            if DatabaseFieldViewConfig.getOption(field_name_iter, 'fit_type') == DatabaseFieldViewConfig.Option.FitToContent:
                self.resizeColumnToContents(field_column_iter)
            elif DatabaseFieldViewConfig.getOption(field_name_iter, 'fit_type') == DatabaseFieldViewConfig.Option.FitTwice:
                default_width = self.horizontalHeader().defaultSectionSize()
                self.setColumnWidth(field_column_iter, default_width * 2)

            if DatabaseFieldViewConfig.getOption(field_name_iter, 'hide_field') == True:
                self.setColumnHidden(field_column_iter, not Config.DatabaseOption.enableShowId())

        # 편집 구역 헤더 너비 설정
        self.setColumnWidth(9, 70)

        # 전체 레이아웃 설정
        self.fixTableWidgetSize()


    """
    slot
    * headerDoubleClicked
    * optionChanged
    """
    @MyPyqtSlot(int)
    def headerDoubleClicked(self, idx: int):
        sender_col = idx
        if 0 <= sender_col < self.columnCount():
            sender_field = self.fieldList()[sender_col]
            if sender_field in self.modelFieldList():
                self.getSignalSet().SortTableRequest.emit(sender_field)

    @MyPyqtSlot()
    def optionChanged(self):
        Option = DatabaseTableView.Option
        row_type = Option.Row.Basic
        if not Config.DatabaseOption.enableFixId():
            id_column = self.fieldColumn('고유번호')
            self.setRowOption(row_type, id_column, Option.Item.Fixed)
        else:
            id_column = self.fieldColumn('고유번호')
            self.setRowOption(row_type, id_column, Option.Item.ReadOnly | MyItemView.Option.White)
        self.render()

    def editItem(self, item: QTableWidgetItem) -> None:
        super().editItem(item)
        line_edit: ItemLineEdit = self.cellWidget(item.row(), item.column())
        if DatabaseFieldViewConfig.getOption(self.fieldList()[item.column()], 'date_field') is True:
            line_edit.setDateMask()

