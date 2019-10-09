from Utility.TableInterface.View.MyTableWidget import *
from Utility.TableInterface.View.MyModelView import *
from Utility.TableInterface.View.MyModelViewFactory import *
from Utility.TableInterface.View.Button.DefaultButtonFactory import *
from Utility.TableInterface.Model.MyTableModel import *


class MyTableViewSignal(QObject):
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

        self.__model: Type[MyTableModel] = None
        self.__signal_set = MyTableViewSignal(parent)
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
        # self.__column_buttons_list: List[Optional[List[MyButtonInput]]] = [None for i in range(self.columnCount())]  # todo 없애도되나?
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

    def getSignalSet(self) -> Type[MyTableViewSignal]:
        return self.__signal_set

    def _setSignalSet(self, signal_set = Type[MyTableViewSignal]) -> None:
        self.__signal_set = signal_set

    def _model(self) -> Type[MyTableModel]:
        return self.__model

    def setModel(self, model: Type[MyTableModel]) -> None:
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
        header_item = QTableWidgetItem()  # todo 에러 발생 가능
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
            # todo proto options?
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

            if property_dict[field] is not None:  # todo: 필요한 if인가?
                self.item(row, field_column).setText(property_dict[field])

    def setRowOptionSpan(self, row_type: Option.Row, from_col: int, end_col: int) -> None:
        if from_col < end_col:
            option = self.rowOption(row_type, from_col)
            self.setRowOption(row_type, from_col, option | MyItemView.Option.SpanOwner)
            for col_iter in range(from_col + 1, end_col):
                option_iter = self.rowOption(row_type, col_iter)
                self.setRowOption(row_type, col_iter, option_iter | MyItemView.Option.Spanned)
        else:
            ErrorLogger.reportError('Correct Span?')

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
    @pyqtSlot()
    def addClicked(self):
        btn: QPushButton = self.sender()
        if btn and btn.parent():
            sender_row = self.indexAt(btn.parent().pos()).row()
            empty_dict = {}
            self.getSignalSet().InsertDataRequest.emit(sender_row + 1, empty_dict)

    @pyqtSlot(bool)
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

    @pyqtSlot()
    def deleteClicked(self):
        btn: QPushButton = self.sender()
        if btn and btn.parent():
            sender_row = self.indexAt(btn.parent().pos()).row()
            if self._model() and 0 <= sender_row < self._model().getDataCount():
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
    * insertRow
    * editItem
    """
    def insertRow(self, row: int) -> None:
        super().insertRow(row)
        self.initializeRowItems(row)

    """
    자동완성 기능: completer list를 만들어내서 자동완성함
    현재 문제점: consistent line edit로 편집할 때는 lineedit를 딱 한번만 만들고 계속 켜두기 때문에,
    만들 당시에 있던 정보만 활용가능함. 이 문제점을 해결하려면 _getCompleterList를 lineedit에 focus 될때마다 호출해야함.
    """
    # todo 자동완성기능
    def editItem(self, item: QTableWidgetItem) -> None:
        super().editItem(item)
        line_edit: ItemLineEdit = self.cellWidget(item.row(), item.column())
        completer_list = self._getCompleterList(item.row(), item.column())
        if completer_list:
            line_edit.setCompleterList(completer_list)

    def _getCompleterList(self, row: int, column: int) -> List[str]:
        completer_dict = {}
        for row_iter in range(row):
            text_iter = self.item(row_iter, column).text()
            if text_iter != '':
                if completer_dict.get(text_iter) is None:
                    completer_dict[text_iter] = 1
                else:
                    completer_dict[text_iter] += 1
        completer_list = list(completer_dict.keys())
        completer_list.sort(key=lambda string: completer_dict[string], reverse=True)
        return completer_list