from View.Table.AbstractTableView import *
from View.Table.TableItemView import *
from Model.Table.Database.DatabaseTableModel import *
from View.ButtonFactory import *

"""
DatabaseTableView(AbstractTableView)
DatabaseTableModel을 표현하기 위한 View
1. 해당 클래스에서 사용할 RowType, ItemType을 정의함
"""


class DatabaseTableViewSignal(AbstractTableViewSignal):
    EditButtonToggled = pyqtSignal(int, bool)
    RemoveButtonClicked = pyqtSignal(int)
    FieldHeaderDoubleClicked = pyqtSignal(str)
    def __init__(self, parent: QWidget):
        super().__init__(parent)


class DatabaseTableView(AbstractTableView):
    class RowType(AbstractTableView.RowType):
        Basic = auto()

    class ItemType(AbstractTableView.ItemType):
        Basic = TableItemOption.White | TableItemOption.UnEditable
        Uneditable = TableItemOption.LightGray | TableItemOption.UnEditable | TableItemOption.UnFocusable
        Wall = TableItemOption.Black | TableItemOption.UnFocusable | TableItemOption.UnEditable

    def __init__(self, parent: QWidget = None):
        ROW, COLUMN = 0, len(self.fieldModelList())
        super().__init__(ROW, COLUMN, parent)  # todo
        self._setSignalSet(DatabaseTableViewSignal(self))
        self.setVisibleRowCount(22)
        self.horizontalHeader().setSectionsMovable(True)

        self.setItemPrototype(TableItemView())

        self.initializeFields()
        self.initializeCustomFields()  # initializeFields의 결과 뒤에 덮어쓰므로 반드시 뒤에서 호출
        self.myRender()
        self.fixTableWidgetSize()

    """
    initialize method
    """
    def initializeFields(self) -> None:
        RowType, ItemType = DatabaseTableView.RowType, DatabaseTableView.ItemType
        self.setHorizontalHeaderLabels(self.fieldNameList())  # todo - 이걸 initializeFields 안으로? - 옮겨봤음
        if ConfigModule.Hidden.databaseFieldOrder() and set(self.fieldNameList()) == set(ConfigModule.Hidden.databaseFieldOrder()):
            field_order_list = ConfigModule.Hidden.databaseFieldOrder()
        else:
            field_order_list = self.fieldNameList()
            ConfigModule.Hidden.setDatabaseFieldOrder(field_order_list)

        for field_name_iter in self.fieldNameList():
            logical_column_iter = self.fieldColumn(field_name_iter)
            visual_column_iter = self.visualColumn(logical_column_iter)
            if visual_column_iter != field_order_list.index(field_name_iter):
                self.horizontalHeader().moveSection(visual_column_iter, field_order_list.index(field_name_iter))

        self.horizontalHeader().sectionDoubleClicked.connect(lambda index: self.signalSet().FieldHeaderDoubleClicked.emit(self.fieldTitle(index)))
        self.horizontalHeader().sectionMoved.connect(lambda: self._mySectionMoved())

        for field_model_iter in self.fieldModelList():
            field_name_iter = field_model_iter.name()
            column_iter = self.fieldColumn(field_name_iter)
            # item option setting
            if field_model_iter.globalOption(TableFieldOption.Global.Uneditable):
                self.setItemOption(RowType.Basic, field_name_iter, ItemType.Uneditable.value)
            else:
                self.setItemOption(RowType.Basic, field_name_iter, ItemType.Basic.value)

            # bold setting
            for row_type_iter in RowType:
                if field_model_iter.databaseOption(TableFieldOption.Database.Bold):
                    item_option_iter = self.itemOption(row_type_iter, field_name_iter)
                    self.setItemOption(row_type_iter, field_name_iter, item_option_iter | TableItemOption.TextBold)

            # column setting
            if field_model_iter.databaseOption(TableFieldOption.Database.Hidden):
                self.setColumnHidden(column_iter, True)
            elif field_model_iter.databaseOption(TableFieldOption.Database.WidthUp):
                self.setColumnWidth(column_iter, 2 * self.columnWidth(column_iter))
            elif field_model_iter.databaseOption(TableFieldOption.Database.WidthDown):
                self.resizeColumnToContents(column_iter)

    def initializeCustomFields(self) -> None:
        RowType, ItemType = DatabaseTableView.RowType, DatabaseTableView.ItemType

        unable_field_title_list = [field_model_iter.name() for field_model_iter in self.fieldModelList()
                                   if field_model_iter.globalOption(TableFieldOption.Global.Uneditable)]
        for field_title_iter in unable_field_title_list:
            self.setCustomRender(field_title_iter, lambda item: item.setForeground(Qt.black))

        right_field_title = TableFieldOption.Necessary.Button_Edit_Remove
        def rightCustomFieldRender(item: TableItemView) -> None:
            btn_widget = ButtonFactory.createButtonWrapper(ButtonFactory.ButtonType.Edit,
                                                           ButtonFactory.ButtonType.Remove)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Edit).toggled.connect(self._editButtonToggled)
            btn_widget.buttonWidget(ButtonFactory.ButtonType.Remove).clicked.connect(self._removeButtonClicked)
            item.setWidget(btn_widget)
        self.setCustomRender(right_field_title, rightCustomFieldRender)

        for row_type_iter in RowType:
            self.setItemOption(row_type_iter, right_field_title, ItemType.Wall.value)

    """
    advanced property
    * fieldModelList (override)
    * rowType
    """
    def fieldModelList(self) -> List[TableFieldModel]:
        return ConfigModule.TableField.databaseFieldModelList()

    def rowType(self, row: int) -> RowType:
        return DatabaseTableView.RowType.Basic

    """
    method
    * setMyModel (override)
    """
    def setMyModel(self, my_model: DatabaseTableModel) -> None:
        super().setMyModel(my_model)
        self.setRowCount(my_model.itemCount())
        my_model.signalSet().SortInfoChanged.connect(lambda: self.myRender())

    """
    button method and slot
    * addButtonClicked, editButtonToggled, removeButtonClicked
    """
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
    slot
    * _mySectionMoved
    """
    def _mySectionMoved(self) -> None:
        field_order_list: List[str] = [None for i in range(self.columnCount())]
        for field_name_iter in self.fieldNameList():
            field_order_list[self.visualColumn(self.fieldColumn(field_name_iter))] = field_name_iter
        ConfigModule.Hidden.setDatabaseFieldOrder(field_order_list)

    """
    return type override
    """
    def signalSet(self) -> DatabaseTableViewSignal:
        return super().signalSet()

    def myModel(self) -> DatabaseTableModel:
        return super().myModel()
