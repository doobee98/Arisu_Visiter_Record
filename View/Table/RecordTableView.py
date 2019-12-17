from View.Table.AbstractTableView import *
from View.Table.TableItemView import *
from Model.Table.Record.RecordTableModel import *
from View.ButtonFactory import *
from Utility.Module.CompleterListModule import *

"""
RecordTableView(AbstractTableView)
RecordTableModel을 표현하기 위한 View
1. 해당 클래스에서 사용할 RowType, ItemType을 정의함
"""


class RecordTableViewSignal(AbstractTableViewSignal):
    AddButtonClicked = pyqtSignal(int)
    EditButtonToggled = pyqtSignal(int, bool)
    RemoveButtonClicked = pyqtSignal(int)
    CellFocusChanged = pyqtSignal(int, int)
    def __init__(self, parent: QWidget):
        super().__init__(parent)


class RecordTableView(AbstractTableView):
    class RowType(AbstractTableView.RowType):
        Basic = auto()
        Inserted = auto()
        Finished = auto()
        Takeover = auto()
        Overlaped = auto()

    class ItemType(AbstractTableView.ItemType):
        Basic = TableItemOption.White
        Inserted = TableItemOption.LightGray | TableItemOption.UnEditable
        Finished = TableItemOption.Gray | TableItemOption.UnEditable
        Takeover = TableItemOption.Gray | TableItemOption.UnEditable | TableItemOption.Span
        Overlaped = TableItemOption.Yellow | TableItemOption.UnEditable
        Wall = TableItemOption.Black | TableItemOption.UnFocusable | TableItemOption.UnEditable
        Unactivated = TableItemOption.Dotted | TableItemOption.UnFocusable | TableItemOption.UnEditable

    def __init__(self, parent: QWidget = None):
        ROW, COLUMN = 10, len(self.fieldModelList())
        super().__init__(ROW, COLUMN, parent)  # todo
        self._setSignalSet(RecordTableViewSignal(self))
        self.currentCellChanged.connect(lambda row, column: self.signalSet().CellFocusChanged.emit(row, column))
        self.horizontalHeader().setSectionsMovable(True)
        self.setVisibleRowCount(18)
        self.setItemPrototype(TableItemView())
        self.initializeFields()
        self.initializeCustomFields()  # initializeFields의 결과 뒤에 덮어쓰므로 반드시 뒤에서 호출
        self.myRender()
        self.fixTableWidgetSize()

    """
    initialize method
    """
    def initializeFields(self) -> None:
        RowType, ItemType = RecordTableView.RowType, RecordTableView.ItemType
        self.setHorizontalHeaderLabels(self.fieldNameList())  # todo - 이걸 initializeFields 안으로? - 옮겨봤음
        if ConfigModule.Hidden.recordFieldOrder() and set(self.fieldNameList()) == set(ConfigModule.Hidden.recordFieldOrder()):
            field_order_list = ConfigModule.Hidden.recordFieldOrder()
        else:
            field_order_list = self.fieldNameList()
            ConfigModule.Hidden.setRecordFieldOrder(field_order_list)

        for field_name_iter in self.fieldNameList():
            logical_column_iter = self.fieldColumn(field_name_iter)
            visual_column_iter = self.visualColumn(logical_column_iter)
            if visual_column_iter != field_order_list.index(field_name_iter):
                self.horizontalHeader().moveSection(visual_column_iter, field_order_list.index(field_name_iter))

        self.horizontalHeader().sectionMoved.connect(lambda: self._mySectionMoved())

        for field_model_iter in self.fieldModelList():
            field_name_iter = field_model_iter.name()
            column_iter = self.fieldColumn(field_name_iter)
            # item option setting
            if field_model_iter.recordOption(TableFieldOption.Record.DefaultUnable):
                self.setItemOption(RowType.Basic, field_name_iter, ItemType.Unactivated.value)
            else:
                self.setItemOption(RowType.Basic, field_name_iter, ItemType.Basic.value)
            self.setItemOption(RowType.Inserted, field_name_iter, ItemType.Inserted.value)
            self.setItemOption(RowType.Finished, field_name_iter, ItemType.Finished.value)
            self.setItemOption(RowType.Takeover, field_name_iter, ItemType.Takeover.value)
            self.setItemOption(RowType.Overlaped, field_name_iter, ItemType.Overlaped.value)

            # bold setting
            for row_type_iter in RowType:
                if field_model_iter.recordOption(TableFieldOption.Record.Bold):
                    item_option_iter = self.itemOption(row_type_iter, field_name_iter)
                    self.setItemOption(row_type_iter, field_name_iter, item_option_iter | TableItemOption.TextBold)

            # column setting
            if field_model_iter.recordOption(TableFieldOption.Record.Hidden):
                self.setColumnHidden(column_iter, True)
            elif field_model_iter.recordOption(TableFieldOption.Record.WidthUp):
                self.setColumnWidth(column_iter, 2 * self.columnWidth(column_iter))
            elif field_model_iter.recordOption(TableFieldOption.Record.WidthDown):
                self.resizeColumnToContents(column_iter)

    def initializeCustomFields(self) -> None:
        RowType, ItemType = RecordTableView.RowType, RecordTableView.ItemType

        left_field_title = TableFieldOption.Necessary.Button_Plus
        def leftCustomFieldRender(item: TableItemView) -> None:
            add_enable = self.rowType(item.row()) in [RowType.Inserted, RowType.Finished]
            btn_widget = ButtonFactory.createButtonWrapper(ButtonFactory.ButtonType.Add)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Add).clicked.connect(self._addButtonClicked)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Add).setEnabled(add_enable)
            item.setWidget(btn_widget)
        self.setCustomRender(left_field_title, leftCustomFieldRender)

        right_field_title = TableFieldOption.Necessary.Button_Edit_Remove
        def rightCustomFieldRender(item: TableItemView) -> None:
            edit_enable = self.rowType(item.row()) in [RowType.Inserted, RowType.Finished]
            remove_enable = self.rowType(item.row()) in RowType
            btn_widget = ButtonFactory.createButtonWrapper(ButtonFactory.ButtonType.Edit,
                                                           ButtonFactory.ButtonType.Remove)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Edit).toggled.connect(self._editButtonToggled)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Edit).setEnabled(edit_enable)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Remove).clicked.connect(self._removeButtonClicked)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Remove).setEnabled(remove_enable)
            item.setWidget(btn_widget)
        self.setCustomRender(right_field_title, rightCustomFieldRender)

        for row_type_iter in RowType:
            self.setItemOption(row_type_iter, left_field_title, ItemType.Wall.value)
            self.setItemOption(row_type_iter, right_field_title, ItemType.Wall.value)

    """
    advanced property
    * fieldModelList (override)
    * rowType (override)
    """
    def fieldModelList(self) -> List[TableFieldModel]:
        return ConfigModule.TableField.recordFieldModelList()

    def rowType(self, row: int) -> RowType:
        if self.fieldText(row, TableFieldOption.Necessary.ID) == RecordModel.IdOverlapValue:
            return RecordTableView.RowType.Overlaped
        item_model: RecordModel = self.myModel().item(row) if self.myModel() and row < self.myModel().itemCount() else None
        if item_model:
            if item_model.state() == RecordModel.State.Takeover:
                return RecordTableView.RowType.Takeover
            elif item_model.state() == RecordModel.State.Finished:
                return RecordTableView.RowType.Finished
            elif item_model.state() == RecordModel.State.Inserted:
                return RecordTableView.RowType.Inserted
            else:  # RecordModel.SearchState.Empty
                return RecordTableView.RowType.Basic
        else:
            return RecordTableView.RowType.Basic

    """
    method
    * setMyModel (override)
    * myRenderRow (override)
    * _myRenderRowTexts (override)
    * isRowWritable
    """
    def setMyModel(self, my_model: RecordTableModel) -> None:
        super().setMyModel(my_model)
        self.setRowCount(my_model.itemCount() + 10)

    def myRenderRow(self, row: int) -> None:
        super().myRenderRow(row)
        if self.rowType(row) == RecordTableView.RowType.Takeover:
            takeover_text = self.myModel().item(row).fieldData(TableFieldOption.Necessary.TAKEOVER)
            for column_iter in range(self.columnCount()):
                if self.columnSpan(row, column_iter) > 1:
                    self.item(row, column_iter).setText(takeover_text)
                    return

    # def _myRenderRowTexts(self, row: int) -> None:
    #     if self.rowType(row) != RecordTableView.RowType.Basic:
    #         super()._myRenderRowTexts(row)

    def isRowWritable(self, row: int) -> bool:  # todo 너무 금방 만듦. 다시 보기
        if self.rowType(row) in [RecordTableView.RowType.Basic, RecordTableView.RowType.Overlaped]:
            return True
        elif self.rowType(row) in [RecordTableView.RowType.Takeover]:
            return False
        else:
            button_wrapper = self.fieldItem(row, TableFieldOption.Necessary.Button_Edit_Remove).widget()
            if isinstance(button_wrapper, ButtonFactory.ButtonWrapper):
                return button_wrapper.buttonWidget(ButtonFactory.ButtonType.Edit).isChecked()
            return False

    """
    slot
    * _mySectionMoved
    """
    def _mySectionMoved(self) -> None:
        field_order_list: List[str] = [None for i in range(self.columnCount())]
        for field_name_iter in self.fieldNameList():
            field_order_list[self.visualColumn(self.fieldColumn(field_name_iter))] = field_name_iter
        ConfigModule.Hidden.setRecordFieldOrder(field_order_list)

    """
    button slot
    * addButtonClicked, editButtonToggled, removeButtonClicked
    """
    @MyPyqtSlot()
    def _addButtonClicked(self) -> None:
        btn: QPushButton = self.sender()
        if btn:
            sender_row = self.indexAt(btn.parent().pos()).row()
            self.signalSet().AddButtonClicked.emit(sender_row)

    @MyPyqtSlot(bool)
    def _editButtonToggled(self, checked: bool) -> None:
        btn: QPushButton = self.sender()
        if btn:
            sender_row = self.indexAt(btn.parent().pos()).row()
            self.signalSet().EditButtonToggled.emit(sender_row, checked)

    @MyPyqtSlot()
    def _removeButtonClicked(self) -> None:
        btn: QPushButton = self.sender()
        if btn:
            sender_row = self.indexAt(btn.parent().pos()).row()
            if ConfigModule.Application.enableAlertRemove():
                reply = MyMessageBox.question(self, '알림', f'작성된 데이터가 삭제됩니다. 삭제하시겠습니까?')
                if reply != MyMessageBox.Yes:
                    return
            self.signalSet().RemoveButtonClicked.emit(sender_row)

    """
    override
    * editItem
    """
    def editItem(self, item: TableItemView) -> None:
        super().editItem(item)
        line_edit: MyItemLineEdit = item.widget()
        completer_list = CompleterListModule.generateCompleterList(item.row(), item.column())
        if completer_list:
            line_edit.setCompleterList(completer_list)

    """
    return type override
    """
    def signalSet(self) -> RecordTableViewSignal:
        return super().signalSet()

    def myModel(self) -> RecordTableModel:
        return super().myModel()
