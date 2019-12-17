from Utility.MyPyqt.MyTableWidget import *
from View.Table.TableItemView import *
from Model.Table.Abstract.AbstractTableModel import *

"""
AbstractTableView(MyTableWidget)
AbstractTableModel을 표현하기 위한 View
1. RowType에 따라 Item View Set이 정해진다.  (Ex: Inserted -> [Wall, Inserted, Inserted, Unable, Wall])
2. Model이 변하면 View도 변하도록 connection을 생성함.
"""

class AbstractTableViewSignal(MyTableWidgetSignal):
    Paste = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)


class AbstractTableView(MyTableWidget):
    class RowType(Enum):
        pass

    class ItemType(Enum):
        pass

    def __init__(self, rows: int, columns: int, parent: QWidget = None):
        self.__my_model: AbstractTableModel = None
        self.__item_option_dictionary: Dict[Tuple[AbstractTableView.RowType, str], TableItemOption] = {}
        self.__custom_field_render_dictionary: Dict[str, Callable[[TableItemView], None]] = {}
        self.__highlight_row_list: List[int] = []

        super().__init__(rows, columns, parent)
        self._setSignalSet(AbstractTableViewSignal(self))
        self.setItemPrototype(TableItemView()) # todo setItemProtoType 바꿔야 하는데

    """
    property
    * myModel
    * _itemOptionDictionary
    * _customFieldRenderDictionary
    * highlightRowList
    """
    def myModel(self) -> AbstractTableModel:
        return self.__my_model

    def setMyModel(self, my_model: AbstractTableModel) -> None:
        self.__my_model = my_model
        self._connectMyModel(my_model)

    def _itemOptionDictionary(self) -> Dict[Tuple[RowType, str], TableItemOption]:
        return self.__item_option_dictionary

    def _customFieldRenderDictionary(self) -> Dict[str, Callable]:
        return self.__custom_field_render_dictionary

    def highLightRowList(self) -> List[int]:
        return self.__highlight_row_list

    def setHighLightRowList(self, highlight_row_list: List[int]) -> None:
        self.__highlight_row_list = highlight_row_list

    """
    advanced property
    * rowType
    * fieldModelList, fieldNameList
    * fieldColumn, fieldModel, fieldTitle, fieldText, fieldItem
    * customFieldList
    * customFieldRender
    * itemOption
    """
    def rowType(self, row: int) -> RowType:
        raise NotImplementedError

    def fieldModelList(self) -> List[TableFieldModel]:
        raise NotImplementedError

    def fieldNameList(self) -> List[str]:
        return [field_model_iter.name() for field_model_iter in self.fieldModelList()]

    def fieldColumn(self, field_name: str) -> int:
        for column_iter in range(self.columnCount()):
            if field_name == self.fieldTitle(column_iter):
                return column_iter
        raise AttributeError

    def fieldModel(self, column: int) -> Optional[TableFieldModel]:
        for field_model_iter in self.fieldModelList():
            if field_model_iter.name() == self.fieldTitle(column):
                return field_model_iter
        return None

    def fieldTitle(self, column: int) -> str:
        return self.horizontalHeaderItem(column).text()
    
    def fieldText(self, row: int, field_name: str) -> str:
        return self.fieldItem(row, field_name).text()

    def fieldItem(self, row: int, field_name: str) -> TableItemView:
        return self.item(row, self.fieldColumn(field_name))

    def customRenderFieldList(self) -> List[str]:
        return list(self._customFieldRenderDictionary().keys())

    def customRender(self, field_name: str) -> Callable[[TableItemView], None]:
        return self._customFieldRenderDictionary()[field_name]

    def setCustomRender(self, field_name: str, render_func: Callable[[TableItemView], None]) -> None:
        self.__custom_field_render_dictionary[field_name] = render_func

    def itemOption(self, row_type: RowType, field_name: str) -> TableItemOption:
        return self._itemOptionDictionary()[(row_type, field_name)]

    def setItemOption(self, row_type: RowType, field_name: str, item_option: TableItemOption) -> None:
        self.__item_option_dictionary[(row_type, field_name)] = item_option

    """
    method
    * _connectMyModel
    * rowTextDictionary
    * setRowTexts, clearRowTexts, clearTexts
    * myRender, myRenderRow
    """
    def _connectMyModel(self, my_model: AbstractTableModel) -> None:
        my_model.signalSet().ItemChanged.connect(self._itemModelChanged)
        my_model.signalSet().ItemInserted.connect(self._itemModelInserted)
        my_model.signalSet().ItemRemoved.connect(self._itemModelRemoved)
        
    def rowTextDictionary(self, row: int) -> Dict[str, str]:
        return {field_name_iter: self.fieldText(row, field_name_iter) for field_name_iter in self.myModel().fieldNameList()}
        # todo myModel의 fieldNameList를 쓰는게 최선일까
        
    def setRowTexts(self, row: int, field_text_dictionary: Dict[str, str]) -> None:
        if self.myModel() and row < self.myModel().itemCount():
            dic = {field_name_iter: data_iter for field_name_iter, data_iter in field_text_dictionary.items()
                   if field_name_iter in self.myModel().fieldNameList()}
            self.myModel().item(row).setFieldDatum(dic)
        else:
            for field_name_iter, text_iter in field_text_dictionary.items():
                self.item(row, self.fieldColumn(field_name_iter)).setText(text_iter)

    def clearRowTexts(self, row: int) -> None:
        for column_iter in range(self.columnCount()):
            self.item(row, column_iter).setText('')
        # if self.myModel():
        #     row_text_dictionary = {field_name_iter: AbstractTableItemModel.DefaultValue for field_name_iter in self.myModel().fieldNameList()}
        #     self.setRowTexts(row, row_text_dictionary)
    
    def clearTexts(self) -> None:
        for row_iter in range(self.rowCount()):
            self.clearRowTexts(row_iter)

    def myRender(self) -> None:
        self.clearSpans()
        self.clearTexts()
        for row_iter in range(self.rowCount()):
            self.myRenderRow(row_iter)

    def myRenderRow(self, row: int) -> None:
        # custom Rendering 먼저 함
        for custom_field_name_iter in self.customRenderFieldList():
            self.customRender(custom_field_name_iter)(self.item(row, self.fieldColumn(custom_field_name_iter)))

        # item_model의 텍스트를 표시하고, 색상등의 옵션 설정을 렌더링
        item_model = self.myModel().item(row) if self.myModel() and row < self.myModel().itemCount() else None
        span_horizon_list = []
        for column_iter in range(self.columnCount()):
            field_title_iter = self.fieldTitle(column_iter)
            item_option_iter = self.itemOption(self.rowType(row), field_title_iter)

            # span rendering prepare
            if item_option_iter & TableItemOption.Span:
                span_horizon_list.append(column_iter)

            # item option rendering
            self.item(row, column_iter).setMyFlags(item_option_iter)
            self.item(row, column_iter).myRender()

            # data rendering
            field_title_iter = self.fieldTitle(column_iter)
            if item_model and field_title_iter in item_model.fieldNameList():
                self.item(row, column_iter).setText(item_model.fieldData(field_title_iter))

            # highlight rendering
            if row in self.highLightRowList():
                self.item(row, column_iter).setBackground(QColor(0x99ffff))

        # span rendering
        if span_horizon_list:
            span_horizon_list.sort()
            min, max = span_horizon_list[0], span_horizon_list[-1]
            self.setSpan(row, span_horizon_list[0], 1, max - min + 1)  # todo 일단 등차라고 가정하고 했음

    """
    slot
    * _itemModelChanged, _itemModelInserted, _itemModelRemoved
    """
    @MyPyqtSlot(int)
    def _itemModelChanged(self, index: int) -> None:
        self.myRenderRow(index)

    @MyPyqtSlot(int)
    def _itemModelInserted(self, index: int) -> None:
        self.insertRow(index)
        self.myRenderRow(index)

    @MyPyqtSlot(int)
    def _itemModelRemoved(self, index: int) -> None:
        self.removeRow(index)

    """
    override
    * editItem
    * cutSelectedItems, pasteSelectedItems
    """
    def editItem(self, item: TableItemView) -> None:
        super().editItem(item)
        line_edit: MyItemLineEdit = item.widget()
        field_model = self.fieldModel(item.column())
        line_edit.installFilterFunctions(ConfigModule.FieldFilter.filterFunctionList(field_model.name()))
        if field_model.globalOption(TableFieldOption.Global.IsDate):
            line_edit.setDateMask()
        elif field_model.globalOption(TableFieldOption.Global.IsTime):
            line_edit.setTimeMask()

    def cutSelectedItems(self) -> bool:
        selection: List[TableItemView] = self.selectedItems()
        if any([self.fieldModel(item_iter.column()).globalOption(TableFieldOption.Global.Uneditable) for item_iter in selection]):
            MyMessageBox.warning(self, '경고', '변경할 수 없는 항목이 포함되어 있습니다.')
            return False
        if any([not item_iter.flags() & Qt.ItemIsEditable for item_iter in selection]):
            reply = MyMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?')
            if not reply == MyMessageBox.Yes:
                return False
        if self.copySelectedItems() is True:
            row_text_dict: Dict[int, Dict[str, str]] = {}
            for item_iter in selection:
                row_iter, column_iter = item_iter.row(), item_iter.column()
                if row_text_dict.get(row_iter) is None:
                    row_text_dict[row_iter] = {}
                row_text_dict[row_iter][self.fieldTitle(column_iter)] = AbstractTableItemModel.DefaultValue
            self.signalSet().Paste.emit(row_text_dict)
            return True
        else:
            return False

    def pasteSelectedItems(self) -> bool:
        selection: List[TableItemView] = self.selectedItems()
        if len(selection) == 0:
            ErrorLogger.reportError('영역 선택후 붙여넣기를 시도해 주세요.')
            return False
        if not QApplication.clipboard().text():
            ErrorLogger.reportError('클립보드에 복사된 텍스트가 없습니다.')
            return False
        text_list = QApplication.clipboard().text().split('\n')
        paste_list: List[str] = []
        paste_row_count = len(text_list)
        while text_list:
            paste_list += text_list.pop(0).split('\t')
        paste_column_count = len(paste_list) // paste_row_count

        start_row, start_column = selection[0].row(), selection[0].column()
        if start_row + paste_row_count > self.rowCount() or start_column + paste_column_count > self.columnCount():
            ErrorLogger.reportError('붙여넣기하려는 영역의 크기가 복사된 영역의 크기보다 큽니다.')
            return False

        selection = []
        row_iter, col_iter = 0, 0
        while row_iter < paste_row_count:
            if self.isRowHidden(start_row + row_iter):
                paste_row_count += 1
            else:
                while col_iter < paste_column_count:
                    if self.isColumnHidden(start_column + col_iter):
                        paste_column_count += 1
                    else:
                        selection.append(self.item(start_row + row_iter, start_column + col_iter))
                    col_iter += 1
            row_iter += 1
            col_iter = 0

        if any([self.fieldModel(item_iter.column()).globalOption(TableFieldOption.Global.Uneditable) for item_iter in selection]):
            MyMessageBox.warning(self, '경고', '변경할 수 없는 항목이 포함되어 있습니다.')
            return False
        if any([not item_iter.flags() & Qt.ItemIsEditable for item_iter in selection]):
            reply = MyMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?')
            if not reply == MyMessageBox.Yes:
                return False

        row_iter, row_text_dict = None, {}
        for item_iter, paste_iter in zip(selection, paste_list):
            if row_iter != item_iter.row():
                row_iter = item_iter.row()
                row_text_dict[row_iter] = {}
            row_text_dict[row_iter][self.fieldTitle(item_iter.column())] = paste_iter
        self.signalSet().Paste.emit(row_text_dict)
        return True

    """
    return type override
    """
    def signalSet(self) -> AbstractTableViewSignal:
        return super().signalSet()

    def item(self, row: int, column: int) -> TableItemView:
        return super().item(row, column)




