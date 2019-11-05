from Utility.Abstract.View.Table.ItemLineEdit import *
from Utility.Manager.ShortCutManager import *


class MyTableWidgetSignal(QObject):
    Resized = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class MyTableWidget(QTableWidget):
    """
        MyTableWidget(QTableWidget)

        * Visible Row Count System: default - all row is visible
        * Focusing Cell color is not blue: QColor(30, 0, 0, 25) (whiteGray?)
        * Header Styling
        * Custom Editor: ItemLineEdit

        * fixTableWidgetSize() - fix total size to contents size
    """
    def __init__(self, rows: int = None, cols: int = None, parent: QWidget = None):
        super().__init__(rows, cols, parent)
        self.__signal_set = MyTableWidgetSignal(self)
        self.__visible_row_count = MyTableWidget.VisibleAll

        # basic header settings
        self.setCornerButtonEnabled(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)  # Cannot change cell width and height
        self.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setFrameStyle(QFrame.StyledPanel)  # header border style
        self.verticalHeader().setFrameStyle(QFrame.StyledPanel)
        self.horizontalHeader().setHidden(False)  # expose header
        self.verticalHeader().setHidden(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # disable horizontal scroll
        self.verticalHeader().setMinimumWidth(40)  # fix vertical header width (because of variable number digits)
        self.__renderHeaderFont()

        # adjust focus cell color
        palette = self.palette()
        palette.setBrush(QPalette.Highlight, QBrush(QColor(30, 0, 0, 25)))  # whiteGray?
        palette.setBrush(QPalette.HighlightedText, QBrush(Qt.black))
        self.setPalette(palette)

        # Custom Editor
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # disable Default Editor
        self.currentItemChanged.connect(self.myItemFocusChanged)
        self.itemSelectionChanged.connect(self.mySelectionChanged)

        # 전체 레이아웃 설정
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #self.installEventFilter(self)

    """
    property
    * signalSet
    * visibleRowCount
    """
    def getSignalSet(self) -> MyTableWidgetSignal:
        return self.__signal_set

    def _setSignalSet(self, signal_set: MyTableWidgetSignal) -> None:
        self.__signal_set = signal_set

    def getVisibleRowCount(self) -> int:
        return self.__visible_row_count

    VisibleAll = -1  # visible all: no limit of showing rows - show all rows
    def setVisibleRowCount(self, row_count: int) -> None:
        """
        decide visible row count.
        if table row count is over visible row count, widget will have scroll bar
        """
        self.__visible_row_count = row_count

    """
    method
    * setFocusCell
    * clearTexts
    * clearRowTexts
    * isRowAnyTexts
    * copySelectionItems, pasteSelectionItems, cutSelectionItems
    """
    def setFocusCell(self, row: int, column: int) -> None:
        """
        setCurrentCell 후 focus를 테이블에 다시 맞추어, 포커스가 셀을 벗어나지 않게 함
        """
        if self.currentRow() == row and self.currentColumn() == column:
            return
        # todo 너무 복잡해짐. 좀더 단순화할 수 없을까?
        self.clearSelection()
        if self.focusWidget():
            self.focusWidget().clearFocus()
        self.setFocus()
        self.setCurrentCell(row, column)

    def clearTexts(self) -> None:
        for row_iter in range(self.rowCount()):
            self.clearRowTexts(row_iter)

    def clearRowTexts(self, row: int) -> None:
        for col_iter in range(self.columnCount()):
            self.item(row, col_iter).setText('')

    def isRowAnyTexts(self, row: int) -> bool:
        return any([self.item(row, col_iter).text() for col_iter in range(self.columnCount())])
    
    #todo: 복사, 붙여넣기, 잘라내기 기본적인 구현은 했음, 작성된 데이터 변경시 Request 보낼 것
    def cutSelectedItems(self) -> bool:
        for item_iter in self.selectedItems():
            if not item_iter.flags() & Qt.ItemIsEditable:
                reply = MyMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?')
                if reply == MyMessageBox.Yes:
                    break
                else:
                    return False
        if self.copySelectedItems() is True:
            for item_iter in self.selectedItems():
                item_iter.setText('')
            return True
        else:
            return False

    def copySelectedItems(self) -> bool:
        selection: List[QTableWidgetItem] = self.selectedItems()
        if len(selection) == 0:
            ErrorLogger.reportError('영역 선택후 복사를 시도해 주세요.')
            return False
        selection.sort(key=lambda item: item.row())
        result_text = ''

        item_iter = selection.pop(0)
        result_text += item_iter.text()
        while selection:
            if item_iter.row() != selection[0].row():
                result_text += '\n'
            else:
                result_text += '\t'
            item_iter = selection.pop(0)
            result_text += item_iter.text()
        QApplication.clipboard().setText(result_text)
        return True
    
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
                reply = MyMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?')
                if reply == MyMessageBox.Yes:
                    break
                else:
                    return False
        for item_iter, paste_iter in zip(selection, paste_list):
            item_iter.setText(paste_iter)  # todo : 이부분에서 시그널을 보내야 함
        return True

    """
    render
    * renderHeader
    """
    def renderHeader(self) -> None:
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.__renderHeaderFont()

    def __renderHeaderFont(self) -> None:
        self.horizontalHeader().setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1))
        self.verticalHeader().setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1))

    """
    Table Resize Method
    """
    def fixTableWidgetSize(self) -> None:
        """
        테이블 크기를 행, 열 수에 맞추기
        가로: 사이즈에 딱 맞게
        세로: visible row count에 맞게
        """
        current_visible_row_count = 0
        max_visible_row_count = self.getVisibleRowCount()
        for i in range(self.rowCount()):
            if not self.isRowHidden(i):
                current_visible_row_count += 1

        # 세로 길이 조정
        h = 4  # magic number
        if self.horizontalHeader():
            if not self.horizontalHeader().isHidden():
                h += self.horizontalHeader().sizeHint().height()  # 두 줄인 경우는 sizeHint가 아니면 제대로된 값이 안나옴
        #   row의 높이가 동일하다는 가정 하에
        unit_height = self.verticalHeader().defaultSectionSize()
        h += unit_height * (self.getVisibleRowCount() if self.getVisibleRowCount() != MyTableWidget.VisibleAll
                            else current_visible_row_count)

        # 가로 길이 조정
        w = 4  # magic number
        if self.verticalHeader():
            if not self.verticalHeader().isHidden():
                w += self.verticalHeader().width()  # width를 임의로 변경했을때는 sizeHint로 변경 불가능
        for i in range(self.columnCount()):  # 숨겨지지 않은 셀값 너비
            if not self.isColumnHidden(i):
                w += self.columnWidth(i)
        if current_visible_row_count > max_visible_row_count:  # vertical scrollbar가 보일 때
            w += self.verticalScrollBar().sizeHint().width()

        self.setFixedSize(QSize(w, h))
        self.getSignalSet().Resized.emit()

    """
    Custom Editor Method: ItemLineEdit
    """
    @MyPyqtSlot(QTableWidgetItem, QTableWidgetItem)
    def myItemFocusChanged(self, current: QTableWidgetItem, previous: QTableWidgetItem) -> None:
        if previous:
            previous_widget = self.cellWidget(previous.row(), previous.column())
            if isinstance(previous_widget, ItemLineEdit) and previous_widget.autoDestroy():
                self.removeCellWidget(previous.row(), previous.column())
        # if current:
        #     # self.setCurrentItem(current)
        #     if len(self.selectedItems()) <= 1:
        #         if current.flags() & Qt.ItemIsEditable:
        #             self.editItem(current)
    
    # todo 선택 범위를 currentItemChanged로는 제대로 잡아내지 못해서, 일부를 mySelectionChanged로 옮김
    @MyPyqtSlot()
    def mySelectionChanged(self) -> None:
        if len(self.selectedItems()) == 1:
            current = self.selectedItems()[0]
            if current.flags() & Qt.ItemIsEditable:
                self.editItem(current)

    def __setItemLineEdit(self, item: QTableWidgetItem) -> None:
        """
        Set Custom Editor: ItemLineEdit
        """
        #self.setCurrentCell(item.row(), item.column())
        self.setCellWidget(item.row(), item.column(), ItemLineEdit(item, parent=self))
        le: ItemLineEdit = self.cellWidget(item.row(), item.column())
        le.setFocus()
        # ShortCutManager.addShortCut(le, Qt.CTRL + Qt.Key_X, lambda: QApplication.clipboard().setText(le.selectedText()))
        # ShortCutManager.addShortCut(le, Qt.CTRL + Qt.Key_C, lambda: QApplication.clipboard().setText(le.selectedText()))
        # ShortCutManager.addShortCut(le, Qt.CTRL + Qt.Key_V, lambda: le.setText(QApplication.clipboard().text()))

    """
    For Custom Editor Override
    """
    def editItem(self, item: QTableWidgetItem) -> None:
        self.__setItemLineEdit(item)

    def openPersistentEditor(self, item: QTableWidgetItem) -> None:
        self.editItem(item)
        le: ItemLineEdit = self.cellWidget(item.row(), item.column())
        le.setAutoDestroy(False)

    def closePersistentEditor(self, item: QTableWidgetItem) -> None:
        le: ItemLineEdit = self.cellWidget(item.row(), item.column())
        if isinstance(le, ItemLineEdit):
            self.removeCellWidget(item.row(), item.column())
            le.close()
    
    # todo 급하게 넣은 기능, 엔터치면 다음줄로 가는 것을 itemlineedit 뿐만 아니라 전체에서 적용시키기
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Return and event.spontaneous() is True:
            self.setFocusCell(self.currentRow() + 1, 1)
        super().keyPressEvent(event)

    """
    rowCount change method overriding
    """
    def rowCountChanged(self, oldCount: int, newCount: int) -> None:
        super().rowCountChanged(oldCount, newCount)
        visible_count = self.getVisibleRowCount()
        if oldCount <= visible_count < newCount or oldCount > visible_count >= newCount:
            self.fixTableWidgetSize()

    def insertRow(self, row: int) -> None:
        super().insertRow(row)
        if self.rowCount() == self.getVisibleRowCount() + 1:
            self.fixTableWidgetSize()

    def removeRow(self, row: int) -> None:
        super().removeRow(row)
        if self.rowCount() == self.getVisibleRowCount():
            self.fixTableWidgetSize()

