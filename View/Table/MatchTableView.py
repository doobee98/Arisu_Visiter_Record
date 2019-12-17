from View.Table.AbstractTableView import *
from View.Table.TableItemView import *
from Model.Table.Database.VisitorModel import *

"""
_MatchTableTempModel(AbstractTableModel)
MatchTableView에서 임시로 사용하기 위한 테이블 모델


MatchTableView(AbstractTableView)
RecordTableView에서 Database로 검색 요청을 보내면, 그 결과를 표시하는 테이블
1. 검색 결과의 마지막 행에 Dummy Row가 존재함. 동명이인의 처리를 위한 행
"""


class MatchTableViewSignal(AbstractTableViewSignal):
    RowDoubleClicked = pyqtSignal(int)
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)


class _MatchTableTempModel(AbstractTableModel):
    # MatchTableView에서 사용하는 TableModel, VisitorModel을 아이템으로 사용함
    def __init__(self, parent: QObject = None):
        super().__init__('', parent)
        self.setBlockUpdate(True)  # no save file

    def insertItem(self, index: int, args) -> None:
        super().insertItem(index, args)

    """
    override
    * fieldNameList
    * initNull
    * _createItem
    """
    def fieldNameList(self) -> List[str]:
        return [field_model_iter.name() for field_model_iter in ConfigModule.TableField.databaseFieldModelList()
                if field_model_iter.databaseOption(TableFieldOption.Database.ShareOn) is True]

    def initNull(cls) -> '_MatchTableTempModel':
        return _MatchTableTempModel()

    def _createItem(self, field_data_dict: Dict[str, str]) -> VisitorModel:
        return VisitorModel(field_data_dict, self)


class MatchTableView(AbstractTableView):
    class RowType(AbstractTableView.RowType):
        Basic = auto()
        Dummy = auto()

    class ItemType(AbstractTableView.ItemType):
        Basic = TableItemOption.White | TableItemOption.UnEditable

    def __init__(self, parent: QObject = None):
        ROW, COLUMN = 0, len(self.fieldModelList())
        super().__init__(ROW, COLUMN, parent)
        self._setSignalSet(MatchTableViewSignal(self))
        self.setVisibleRowCount(6)
        self.cellDoubleClicked.connect(lambda row, column: self.signalSet().RowDoubleClicked.emit(row))

        # table styling
        self.verticalHeader().setHidden(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalHeader().setHighlightSections(False)

        self.initializeFields()
        self.setMyModel(_MatchTableTempModel())
        self.myRender()
        self.fixTableWidgetSize()

    """
    advanced property
    * fieldModelList (override)
    * rowType (override)
    """
    def fieldModelList(self) -> List[TableFieldModel]:
        return [field_model_iter for field_model_iter in ConfigModule.TableField.databaseFieldModelList()
                if field_model_iter.databaseOption(TableFieldOption.Database.ShareOn) is True]

    def rowType(self, row: int) -> RowType:
        if row < self.myModel().itemCount():
            return MatchTableView.RowType.Basic
        else:
            return MatchTableView.RowType.Dummy

    """
    initialize method
    * initializeFields
    """
    def initializeFields(self) -> None:
        # MatchTable을 위한 TableFieldOption이 따로 있지는 않으므로, Database의 것을 사용함
        RowType, ItemType = MatchTableView.RowType, MatchTableView.ItemType
        self.setHorizontalHeaderLabels(self.fieldNameList())
        self.setColumnHidden(self.fieldColumn('고유번호'), True)  # todo 디자인 공간이 부족해서 '고유번호' 필드를 가림
        #self.setMouseTracking(True)  # todo 대신 마우스오버되면 툴팁표시
        #self.itemEntered.connect(self._myItemEntered)  # todo: 고유번호를 툴팁으로 표시? 이걸 쓸까 말까?

        for field_model_iter in self.fieldModelList():
            field_name_iter = field_model_iter.name()
            column_iter = self.fieldColumn(field_name_iter)
            # item option setting
            self.setItemOption(RowType.Basic, field_name_iter, ItemType.Basic.value)
            self.setItemOption(RowType.Dummy, field_name_iter, ItemType.Basic.value | TableItemOption.Span)

            # bold setting
            if field_model_iter.recordOption(TableFieldOption.Record.Bold):
                item_option_iter = self.itemOption(RowType.Basic, field_name_iter)
                self.setItemOption(RowType.Basic, field_name_iter, item_option_iter | TableItemOption.TextBold)

            # column setting
            if field_model_iter.databaseOption(TableFieldOption.Database.Hidden):
                self.setColumnHidden(column_iter, True)
            elif field_model_iter.databaseOption(TableFieldOption.Database.WidthUp):
                self.setColumnWidth(column_iter, 2 * self.columnWidth(column_iter))
            elif field_model_iter.databaseOption(TableFieldOption.Database.WidthDown):
                self.resizeColumnToContents(column_iter)

    """
    method
    * setMyModel (override, overload)
    * myRenderRow (override)
    """
    @overload
    def setMyModel(self, visitor_list: List[VisitorModel]) -> None:
        pass

    @overload
    def setMyModel(self, my_model: _MatchTableTempModel) -> None:
        pass

    def setMyModel(self, args) -> None:
        if isinstance(args, _MatchTableTempModel):
            my_model = args
        elif isinstance(args, list):
            my_model = _MatchTableTempModel()
            for visitor_model_iter in args:
                my_model.addItem(visitor_model_iter.fieldDataDictionary())
        else:
            raise TypeError
        super().setMyModel(my_model)
        self.clearSpans()
        self.clearSelection()
        self.clearTexts()
        self.setRowCount(my_model.itemCount() + 1)
        self.myRender()

    def myRenderRow(self, row: int) -> None:
        super().myRenderRow(row)
        if self.rowType(row) == MatchTableView.RowType.Dummy:
            for column_iter in range(self.columnCount()):
                if self.columnSpan(row, column_iter) > 1:
                    self.item(row, column_iter).setText('(동명이인)  현재 작성 중인 행에 신규 데이터 삽입하기')
                    return

    """
    slot
    """
    @MyPyqtSlot(QTableWidgetItem)  # todo: 고유번호를 툴팁으로 표시? 이걸 쓸까 말까?
    def _myItemEntered(self, item: QTableWidgetItem) -> None:
        row = item.row()
        if self.rowType(row) == MatchTableView.RowType.Basic:
            QToolTip.hideText()
            r = self.visualItemRect(item)
            p = self.viewport().mapToGlobal(QPoint(r.center().x(), r.top()))
            QToolTip.showText(p, self.myModel().item(row).fieldData(TableFieldOption.Necessary.ID))

    """
    event
    * focusOutEvent
    * mousePressEvent
    """
    def focusOutEvent(self, e: QFocusEvent) -> None:  # todo 이벤트가 발생하지 않음
        super().focusOutEvent(e)
        self.clearSelection()

    def mousePressEvent(self, e: QMouseEvent) -> None:  # todo 마우스 프레스 이벤트를 좀 더 고민해볼것
        super().mousePressEvent(e)
        if self.indexAt(e.pos()).row() == -1:
            self.clearSelection()

    """
    return type override
    """
    def signalSet(self) -> MatchTableViewSignal:
        return super().signalSet()
