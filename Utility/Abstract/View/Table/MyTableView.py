from Utility.Abstract.View.Table.MyModelViewFactory import *
from Utility.Abstract.View.Button.DefaultButtonFactory import *
from Utility.Abstract.Model.MyTableModel import *
from Utility.Abstract.View.Table.MyTableWidget import *


class MyTableViewSignal(MyTableWidgetSignal):
    """
    MyTableViewSignal
    AppendDataRequest(property_dict): 새로운 데이터를 추가시켜 달라는 요청
    InsertDataRequest(index, property_dict): 해당 index에 새로운 데이터를 삽입시켜 달라는 요청
    ChangeDataRequest(index, property_dict): 해당 index 데이터를 인자를 참조하여 변경해달라는 요청
    DeleteDataRequest(index): 해당 index 데이터를 삭제해 달라는 요청
    """
    AppendDataRequest = pyqtSignal(dict)
    InsertDataRequest = pyqtSignal(int, dict)
    ChangeDataRequest = pyqtSignal(int, dict)
    DeleteDataRequest = pyqtSignal(int)
    ChangeDataGroupRequest = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)


class MyTableView(MyTableWidget):
    class Option:
        class Item:
            Basic = MyItemView.Option.Default
            ReadOnly = MyItemView.Option.Default | MyItemView.Option.LightGray | MyItemView.Option.Uneditable
            Wall = MyItemView.Option.Default | MyItemView.Option.Black | MyItemView.Option.Unable
            Dotted = MyItemView.Option.Default | MyItemView.Option.Dotted | MyItemView.Option.Unable

        class Row(Enum):
            pass

        class Highlight(Enum):
            Cyan = MyItemView.Option.LightBlue
            Red = MyItemView.Option.Red

    def __init__(self, rows: int, cols: int, parent=None):
        super().__init__(rows, cols, parent)

        self.__model: MyTableModel = None
        self._setSignalSet(MyTableViewSignal(parent))
        self.__button_factory = DefaultButtonFactory(self)
        self.__row_view_factory = MyModelViewFactory(self)
        self.__item_view_factory = MyItemViewFactory(self)
        self.buttonFactory().addButtonSlot(ButtonFactory.ButtonType.Add, self.addClicked)
        self.buttonFactory().addButtonSlot(ButtonFactory.ButtonType.Edit, self.editToggled)
        self.buttonFactory().addButtonSlot(ButtonFactory.ButtonType.Delete, self.deleteClicked)

        self.__field_list = ['' for i in range(self.columnCount())]
        self.__model_field_list = []
        self.__row_options_dict: Dict[MyTableView.Option.Row, List[MyItemView.Option]] = {}
        self.__row_buttons_dict: Dict[MyTableView.Option.Row, List[Optional[List[MyButtonInput]]]] = {}
        self.__highlight_cell_dict: Dict[Tuple[int, int], MyTableView.Option.Highlight] = {}
        """
        row_options: row_option에 따른 default item style 관리
        row_buttons: row_option에 따른 default item button widget 관리
        """

        Config.TotalOption.getSignalSet().OptionChanged.connect(self.render)

        self.initializeItems()
        self.fixTableWidgetSize()

    """
    property
    * signalSet
    * model
    * buttonFactory
    * rowViewFactory
    * itemViewFactory
    * rowOptions
    * rowButtons
    * fieldList
    * modelFieldList
    * highlightDictionary
    """

    def getSignalSet(self) -> MyTableViewSignal:
        return super().getSignalSet()

    def _model(self) -> MyTableModel:
        return self.__model

    def setModel(self, model: MyTableModel) -> None:
        self.__model = model

    def buttonFactory(self) -> ButtonFactory:
        return self.__button_factory

    def rowViewFactory(self) -> MyModelViewFactory:
        return self.__row_view_factory

    def itemViewFactory(self) -> MyItemViewFactory:
        return self.__item_view_factory

    def rowOptionList(self, row_type: Option.Row) -> List[MyItemView.Option]:
        if self.__row_options_dict.get(row_type):
            return self.__row_options_dict.get(row_type).copy()
        else:
            return None

    def rowOption(self, row_type: Option.Row, column: int) -> MyItemView.Option:
        return self.rowOptionList(row_type)[column]

    def setRowOptionList(self, row_type: Option.Row, option_list: List[MyItemView.Option]):
        # todo list length 체크: column count와 같아야함
        self.__row_options_dict[row_type] = option_list

    def setRowOption(self, row_type: Option.Row, column: int, option: MyItemView.Option):
        self.__row_options_dict[row_type][column] = option

    def rowButtonList(self, row_type: Option.Row) -> List[Optional[List[MyButtonInput]]]:
        if self.__row_buttons_dict.get(row_type):
            return self.__row_buttons_dict[row_type].copy()
        else:
            return None

    def rowButton(self, row_type: Option.Row, column: int) -> Optional[List[MyButtonInput]]:
        if self.rowButtonList(row_type)[column]:
            return self.rowButtonList(row_type)[column].copy()
        else:
            return None

    def setRowButtonList(self, row_type: Option.Row, button_list: List[Optional[List[MyButtonInput]]]) -> None:
        self.__row_buttons_dict[row_type] = button_list

    def __setDefaultRowButtonList(self, row_type: Option.Row) -> None:
        self.setRowButtonList(row_type, [None for i in range(self.columnCount())])

    def setRowButton(self, row_type: Option.Row, column: int, button: List[MyButtonInput]) -> None:
        if self.__row_buttons_dict.get(row_type) is None:
            self.__setDefaultRowButtonList(row_type)
        self.__row_buttons_dict[row_type][column] = button

    def fieldList(self) -> List[str]:
        return self.__field_list.copy()

    def setFieldList(self, field_list: List[str]) -> None:
        self.__field_list = field_list

    def setField(self, column: int, field: str) -> None:
        self.__field_list[column] = field
        header_item = QTableWidgetItem()
        header_item.setText(field)
        self.setHorizontalHeaderItem(column, header_item)

    def modelFieldList(self) -> List[str]:
        return self.__model_field_list.copy()

    def setModelField(self, column: int, model_field: str) -> None:
        self.__model_field_list.append(model_field)
        self.setField(column, model_field)

    def setModelFieldList(self, model_field_list: List[str]) -> None:
        self.__model_field_list = model_field_list

    def __highlightDictionary(self) -> Dict[Tuple[int, int], Option.Highlight]:
        return self.__highlight_cell_dict

    def highlightColor(self, row: int, column: int) -> Option.Highlight:
        pos = tuple([row, column])
        return self.__highlight_cell_dict.get(pos)

    def setHighlight(self, row: int, column: int, color: Option.Highlight) -> None:
        pos = tuple([row, column])
        self.__highlight_cell_dict[pos] = color  # todo change color state?

    def unhighlight(self, row: int, column: int) -> None:
        if self.highlightColor(row, column):
            pos = tuple([row, column])
            del self.__highlight_cell_dict[pos]
        else:
            pass  # todo: 에러처리 필요?

    """
    method
    * fieldColumn(field)
    * initializeItems
    * getRowTexts
    * setRowTexts
    * setSpanOption
    * highlightRow
    * clearHighlight
    """

    def fieldColumn(self, field: str) -> int:
        return self.fieldList().index(field)

    def initializeItems(self):
        for row_iter in range(self.rowCount()):
            self.initializeRowItems(row_iter)

    def initializeRowItems(self, row: int) -> None:
        """
        qtablewidget은 기본적으로 item setting이 안되어있기에 
        qtablewidgetitem을 초기화해줌
        """
        for col_iter in range(self.columnCount()):
            proto_item = QTableWidgetItem()
            proto_item.setFont(BaseUI.basicQFont())
            self.setItem(row, col_iter, proto_item)

    def getRowTexts(self, row: int) -> Dict[str, str]:
        property_dict = {}
        for field in self.modelFieldList():
            field_column = self.fieldColumn(field)
            property_dict[field] = self.item(row, field_column).text()
        return property_dict

    def setRowTexts(self, row: int, property_dict: Dict[str, str]) -> None:
        for field in property_dict.keys():
            field_column = self.fieldColumn(field)

            if property_dict[field] is not None:  # todo: 필요한 if인가?, 현재는 덮어쓰는 방식임
                self.item(row, field_column).setText(str(property_dict[field]))

    def setRowOptionSpan(self, row_type: Option.Row, from_col: int, end_col: int) -> None:
        if from_col < end_col:
            option = self.rowOption(row_type, from_col)
            self.setRowOption(row_type, from_col, option | MyItemView.Option.SpanOwner)
            for col_iter in range(from_col + 1, end_col):
                option_iter = self.rowOption(row_type, col_iter)
                self.setRowOption(row_type, col_iter, option_iter | MyItemView.Option.Spanned)
        else:
            ErrorLogger.reportError('셀 병합 코드에서 에러가 발생했습니다.', EOFError)

    def highlightRow(self, row: int) -> None:
        for col_iter in range(self.columnCount()):
            item_iter = self.item(row, col_iter)
            if item_iter.flags() & Qt.ItemIsEnabled:
                self.setHighlight(row, col_iter, MyTableView.Option.Highlight.Cyan)

    def clearHighlight(self) -> None:
        self.__highlight_cell_dict.clear()

    """
    buttonSlot
    * addClicked
    * editToggled
    * deleteClicked
    """
    @MyPyqtSlot()
    def addClicked(self):
        btn: QPushButton = self.sender()
        if btn and btn.parent():
            sender_row = self.indexAt(btn.parent().pos()).row()
            empty_dict = {}
            self.getSignalSet().InsertDataRequest.emit(sender_row + 1, empty_dict)

    @MyPyqtSlot(bool)
    def editToggled(self, checked: bool):
        btn: QPushButton = self.sender()
        if btn and btn.parent():
            sender_row = self.indexAt(btn.parent().pos()).row()

            # edit 상태로 전환할때
            if checked is True:
                for field_iter in self.modelFieldList():
                    col_iter = self.fieldColumn(field_iter)
                    item_iter = self.item(sender_row, col_iter)
                    if not self.isColumnHidden(col_iter):  # 임시
                        if item_iter.flags() & Qt.ItemIsEnabled:
                            self.openPersistentEditor(item_iter)
                # for col_iter in range(self.columnCount()):
                #     item_iter = self.item(sender_row, col_iter)
                #     if not self.isColumnHidden(col_iter):  # 임시
                #         if item_iter.flags() & Qt.ItemIsEnabled:
                #             self.openPersistentEditor(item_iter)
                self.cellWidget(sender_row, 1).setFocus()

            # edit 상태를 끝낼때
            else:
                for col_iter in range(self.columnCount()):
                    # 열려있는 ItemLineEdit를 모두 종료합니다.
                    if isinstance(self.cellWidget(sender_row, col_iter), ItemLineEdit):
                        self.closePersistentEditor(self.item(sender_row, col_iter))
                self.setFocusCell(sender_row, 1)

                changed_property_dict = self.getRowTexts(sender_row)
                self.getSignalSet().ChangeDataRequest.emit(sender_row, changed_property_dict)

    @MyPyqtSlot()
    def deleteClicked(self):
        btn: QPushButton = self.sender()
        if btn and btn.parent():
            sender_row = self.indexAt(btn.parent().pos()).row()
            if self._model() and 0 <= sender_row < self._model().getDataCount():
                if Config.TotalOption.isDeleteCheck():
                    reply = QMessageBox.question(self, '알림', f'작성된 데이터가 삭제됩니다. 삭제하시겠습니까?',
                                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                    if reply == QMessageBox.No:
                        return
                self.getSignalSet().DeleteDataRequest.emit(sender_row)
            else:
                self.clearRowTexts(sender_row)  # todo 필요없는 기능일수도 있음
                self.setFocusCell(sender_row, 1)


    """
    rendering
    * render
    * renderRow
    * chooseOption
    """

    def render(self) -> None:
        #self.clearTexts()  # todo 이대로? 렌더 규칙 세우기
        self.clearSpans()
        self.renderHeader()
        current_x, current_y = (self.currentRow(), self.currentColumn()) if self.currentItem() else (None, None)
        for row_iter in range(self.rowCount()):
            self.renderRow(row_iter)
        if current_x is not None and current_y is not None:
            self.setFocusCell(current_x, current_y)

    def renderRow(self, row: int) -> None:
        table_model = self._model()
        if table_model:
            model_iter = table_model.getData(row) if row < table_model.getDataCount() else None
            item_list = [self.item(row, col_iter) for col_iter in range(self.columnCount())]
            options_list, buttons_list = self._chooseOptions(row)
            for col_iter in range(self.columnCount()):
                if self.highlightColor(row, col_iter):
                    options_list[col_iter] |= self.highlightColor(row, col_iter).value
            self.rowViewFactory().optionView(options_list, buttons_list).render(item_list, model_iter)

    def rowType(self, row: int) -> Option.Row:
        raise NotImplementedError

    def _chooseOptions(self, row: int) -> Tuple[List[MyItemView.Option], List[Optional[List[MyButtonInput]]]]:
        raise NotImplementedError

    """
    override
    * setRowCount
    * insertRow
    * cutSelectedItems, pasteSelectedItems
    """
    def setRowCount(self, rows: int) -> None:
        super().setRowCount(rows)
        self.initializeItems()

    def insertRow(self, row: int) -> None:
        super().insertRow(row)
        self.initializeRowItems(row)

    def cutSelectedItems(self) -> bool:
        for item_iter in self.selectedItems():
            if not item_iter.flags() & Qt.ItemIsEditable:
                reply = QMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    break
                else:
                    return False
        if self.copySelectedItems() is True:
            row_text_dict: Dict[int, Dict[str, str]] = {}

            for cut_item_iter in self.selectedItems():
                row, col = cut_item_iter.row(), cut_item_iter.column()
                if row_text_dict.get(row) is None:
                    row_text_dict[row] = {}
                row_text_dict[row][self.fieldList()[col]] = ''

            self.getSignalSet().ChangeDataGroupRequest.emit(row_text_dict)
            return True
        else:
            return False

    def pasteSelectedItems(self) -> bool:
        selection: List[QTableWidgetItem] = self.selectedItems()
        if len(selection) == 0:
            ErrorLogger.reportError('영역 선택후 붙여넣기를 시도해 주세요.')
            return False
        clipboard_text = QApplication.clipboard().text()
        if not clipboard_text:
            ErrorLogger.reportError('클립보드에 복사된 텍스트가 없습니다.')
            return False
        text_list = clipboard_text.split('\n')
        paste_list: List[str] = []
        paste_row_count = len(text_list)
        while text_list:
            text_list_row = text_list.pop(0).split('\t')
            paste_list += text_list_row
        paste_column_count = len(paste_list) // paste_row_count

        if len(selection) == 0:
            return False
        else:
            row, col = selection[0].row(), selection[0].column()
            selection.clear()
            if row + paste_row_count > self.rowCount() or col + paste_column_count > self.columnCount():
                ErrorLogger.reportError('붙여넣기하려는 영역의 크기가 복사된 영역의 크기보다 큽니다.')
                return False
            for row_iter in range(paste_row_count):
                for col_iter in range(paste_column_count):
                    selection.append(self.item(row + row_iter, col + col_iter))
        for item_iter in selection:
            if not item_iter.flags() & Qt.ItemIsEditable:
                reply = QMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?',
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    break
                else:
                    return False
        row_iter = None
        row_text_dict: Dict[int, Dict[str, str]] = {}

        for item_iter, paste_iter in zip(selection, paste_list):
            if row_iter != item_iter.row():
                row_iter = item_iter.row()
                row_text_dict[row_iter] = {}
            row_text_dict[row_iter][self.fieldList()[item_iter.column()]] = paste_iter
        self.getSignalSet().ChangeDataGroupRequest.emit(row_text_dict)
        return True
