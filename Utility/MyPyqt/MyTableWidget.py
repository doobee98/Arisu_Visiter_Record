from Utility.MyPyqt.MyItemLineEdit import *
from Utility.MyPyqt.MyMessageBox import *
#from Utility.Manager.ShortCutManager import *
from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ConfigModule import *


"""
MyTableWidget(QTableWidget)
1. 크기 규격 설정: 보이는 행의 수를 설정해서 테이블 뷰의 크기를 일정하게 정함.
2. 포커스 cell item의 색상을 파랑색에서 whiteGray로 바꿈
3. 헤더 스타일링
4. custom TextLineEditor: MyItemLineEdit
5. item Prototype 세팅
6. fixTableWidgetSize: 테이블 위젯의 크기를 자동으로 조절함
"""


class MyTableWidgetSignal(QObject):
    Resized = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class MyTableWidget(QTableWidget):
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
        self.horizontalHeader().setStyleSheet('::section{background-color:rgb(245, 245, 245)}')  # todo 헤더 색상 포인트 주었음
        self.verticalHeader().setStyleSheet('::section{background-color:rgb(245, 245, 245)}')
        # self.cornerWidget().setStyleSheet('QTableCornerButton::section{backgroud-color: rgb(0, 0, 0)}') todo 코너 버튼 색상 넣고싶음
        self.__myRenderHeaderFont()

        # focus cell color change: blue -> custom whiteGray
        color_white_gray = QColor(30, 0, 0, 25)
        palette = self.palette()
        palette.setBrush(QPalette.Highlight, QBrush(color_white_gray))
        palette.setBrush(QPalette.HighlightedText, QBrush(Qt.black))
        self.setPalette(palette)

        # Custom Editor
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # disable Default Editor
        self.currentItemChanged.connect(self._myItemFocusChanged)
        self.itemSelectionChanged.connect(self._mySelectionChanged)

        # setting prototype
        self.setItemPrototype(QTableWidgetItem())

    """
    property
    * signalSet
    * visibleRowCount
    """
    def signalSet(self) -> MyTableWidgetSignal:
        return self.__signal_set

    def _setSignalSet(self, signal_set: MyTableWidgetSignal) -> None:
        self.__signal_set = signal_set

    VisibleAll = -1
    def visibleRowCount(self) -> int:
        return self.__visible_row_count

    def setVisibleRowCount(self, row_count: int) -> None:
        self.__visible_row_count = row_count

    """
    method
    * myRenderHeader, __myRenderHeaderFont
    * setFocusCell
    * copySelectionItems, pasteSelectionItems, cutSelectionItems
    """
    def myRenderHeader(self) -> None:
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.__myRenderHeaderFont()

    def __myRenderHeaderFont(self) -> None:
        self.horizontalHeader().setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 2))
        self.verticalHeader().setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 2))

    def setFocusCell(self, row: int, column: int) -> None:
        """
        셀 이동시 CustomEditor로 옮겨진 Focus를 바로잡음
        이 함수가 아닌 setCurrentCell 이용시 Focus가 돌아오지 않음
        """
        if self.currentRow() == row and self.currentColumn() == column:
            return
        self.clearSelection()
        if self.focusWidget():
            self.focusWidget().clearFocus()
        self.setFocus()
        self.setCurrentCell(row, column)

    def cutSelectedItems(self) -> bool:
        selection: List[QTableWidgetItem] = self.selectedItems()
        if any([not item_iter.flags() & Qt.ItemIsEditable for item_iter in selection]):
            reply = MyMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?')
            if not reply == MyMessageBox.Yes:
                return False
        if self.copySelectedItems() is True:
            for item_iter in selection:
                item_iter.setText('')  # todo 이거 모델에다가 적용해야함
            return True
        else:
            return False

    def copySelectedItems(self) -> bool:
        selection: List[QTableWidgetItem] = self.selectedItems()
        if len(selection) == 0:
            ErrorLogger.reportError('영역 선택후 복사를 시도해 주세요.')
            return False
        selection.sort(key=lambda item: item.row())

        result_text = selection[0].text()
        for index in range(1, len(selection)):
            result_text += '\n' if selection[index - 1].row() != selection[index].row() else '\t'
            result_text += selection[index].text()
        QApplication.clipboard().setText(result_text)
        return True

    # todo 간소화 필요함
    def pasteSelectedItems(self) -> bool:
        selection: List[QTableWidgetItem] = self.selectedItems()
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

        if any([not item_iter.flags() & Qt.ItemIsEditable for item_iter in selection]):
            reply = MyMessageBox.question(self, '알림', f'작성된 데이터 내용이 변경됩니다. 편집하시겠습니까?')
            if not reply == MyMessageBox.Yes:
                return False
        for item_iter, paste_iter in zip(selection, paste_list):
            item_iter.setText(paste_iter)
        return True

    """
    Resize Method
    * fixTableWidgetSize
    """
    def fixTableWidgetSize(self) -> None:
        """
        테이블 크기를 행, 열 수에 맞추기
        가로: 사이즈에 딱 맞게
        세로: visible row count에 맞게
        """
        current_visible_row_count = 0
        max_visible_row_count = self.visibleRowCount()
        for i in range(self.rowCount()):
            if not self.isRowHidden(i):
                current_visible_row_count += 1

        # 세로 길이 조정
        h = 4  # magic number
        if not self.horizontalHeader().isHidden():
            h += self.horizontalHeader().sizeHint().height()  # 두 줄인 경우는 sizeHint가 아니면 제대로된 값이 안나옴
        #   row의 높이가 동일하다는 가정 하에
        unit_height = self.verticalHeader().defaultSectionSize()
        h += unit_height * (self.visibleRowCount() if self.visibleRowCount() != MyTableWidget.VisibleAll
                            else current_visible_row_count)
        # 가로 길이 조정
        w = 4  # magic number
        if not self.verticalHeader().isHidden():
            w += self.verticalHeader().width()  # width를 임의로 변경했을때는 sizeHint로 변경 불가능
        for i in range(self.columnCount()):  # 숨겨지지 않은 셀값 너비
            if not self.isColumnHidden(i):
                w += self.columnWidth(i)
        if current_visible_row_count > max_visible_row_count:  # vertical scrollbar가 보일 때
            w += self.verticalScrollBar().sizeHint().width()
        # Resize
        self.setFixedSize(QSize(w, h))
        self.signalSet().Resized.emit()

    """
    Custom Editor method
    * __setItemLineEdit
    * closeEditItem 
    * editItem (override)
    * openPersistentEditor, closePersistentEditor (override)
    * keyPressEvent (override)
    """
    def __setItemLineEdit(self, item: QTableWidgetItem) -> None:
        """
        Set Custom Editor: MyItemLineEdit
        """
        # self.setCurrentCell(item.row(), item.column())
        self.setCellWidget(item.row(), item.column(), MyItemLineEdit(item, parent=self))
        le: MyItemLineEdit = self.cellWidget(item.row(), item.column())
        le.setFocus()
        # ShortCutManager.addShortCut(le, Qt.CTRL + Qt.Key_X, lambda: QApplication.clipboard().setText(le.selectedText()))
        # ShortCutManager.addShortCut(le, Qt.CTRL + Qt.Key_C, lambda: QApplication.clipboard().setText(le.selectedText()))
        # ShortCutManager.addShortCut(le, Qt.CTRL + Qt.Key_V, lambda: le.setText(QApplication.clipboard().text()))

    def editItem(self, item: QTableWidgetItem) -> None:
        self.__setItemLineEdit(item)

    def closeEditItem(self, item: QTableWidgetItem) -> None:
        le: MyItemLineEdit = self.cellWidget(item.row(), item.column())
        if isinstance(le, MyItemLineEdit):
            self.removeCellWidget(item.row(), item.column())
            le.close()

    def openPersistentEditor(self, item: QTableWidgetItem) -> None:
        self.editItem(item)
        le: MyItemLineEdit = self.cellWidget(item.row(), item.column())
        le.setAutoDestroy(False)

    def closePersistentEditor(self, item: QTableWidgetItem) -> None:
        self.closeEditItem(item)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        # 엔터치면 테이블 다음줄로 이동함
        if event.key() == Qt.Key_Return and event.spontaneous() is True:
            self.setFocusCell(self.currentRow() + 1, 1)
        super().keyPressEvent(event)

    """
    Custom Editor Slot
    * _myItemFocusChanged, _mySelectionChanged  (selection의 변화는 itemFocusChanged로 잡지 못해서 함수 두 개로 관리함)
    """
    @MyPyqtSlot(QTableWidgetItem, QTableWidgetItem)
    def _myItemFocusChanged(self, current: QTableWidgetItem, previous: QTableWidgetItem) -> None:
        if previous:
            previous_widget = self.cellWidget(previous.row(), previous.column())
            if isinstance(previous_widget, MyItemLineEdit) and previous_widget.autoDestroy():
                self.removeCellWidget(previous.row(), previous.column())

    @MyPyqtSlot()
    def _mySelectionChanged(self) -> None:
        if len(self.selectedItems()) == 1:
            current = self.selectedItems()[0]
            if current.flags() & Qt.ItemIsEditable:
                self.editItem(current)

    """
    override
    * setItemPrototype
    * setRowCount, setColumnCount
    * insertRow, removeRow
    * insertColumn, removeColumn
    """
    def setItemPrototype(self, item: QTableWidgetItem) -> None:
        super().setItemPrototype(item)
        for row_iter in range(self.rowCount()):
            for column_iter in range(self.columnCount()):
                self.setItem(row_iter, column_iter, item.clone())

    def setRowCount(self, rows: int) -> None:
        original_row_count, new_row_count = self.rowCount(), rows
        super().setRowCount(rows)
        if original_row_count != new_row_count:
            for row_iter in range(self.rowCount()):
                for column_iter in range(self.columnCount()):
                    self.setItem(row_iter, column_iter, self.itemPrototype().clone())
            visible_count = self.visibleRowCount()
            if original_row_count <= visible_count < new_row_count or original_row_count > visible_count >= new_row_count:
                self.fixTableWidgetSize()

    def setColumnCount(self, columns: int) -> None:
        original_column_count, new_column_count = self.columnCount(), columns
        super().setColumnCount(columns)
        if original_column_count != new_column_count:
            for row_iter in range(self.rowCount()):
                for column_iter in range(self.columnCount()):
                    self.setItem(row_iter, column_iter, self.itemPrototype().clone())
            self.fixTableWidgetSize()

    def insertRow(self, row: int) -> None:
        super().insertRow(row)
        for column_iter in range(self.columnCount()):
            self.setItem(row, column_iter, self.itemPrototype().clone())
        if self.rowCount() == self.visibleRowCount() + 1:
            self.fixTableWidgetSize()

    def removeRow(self, row: int) -> None:
        super().removeRow(row)
        if self.rowCount() == self.visibleRowCount():
            self.fixTableWidgetSize()

    def insertColumn(self, column: int) -> None:
        super().insertColumn(column)
        for row_iter in range(self.rowCount()):
            self.setItem(row_iter, column, self.itemPrototype().clone())
        self.fixTableWidgetSize()

    def removeColumn(self, column: int) -> None:
        super().removeColumn(column)
        self.fixTableWidgetSize()


