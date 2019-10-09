from Utility.UI.BaseUI import *
from Utility.ItemLineEdit import *


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
        self.verticalHeader().setMinimumWidth(50)  # fix vertical header width (because of variable number digits)
        self.__renderHeaderFont()

        # adjust focus cell color
        palette = self.palette()
        palette.setBrush(QPalette.Highlight, QBrush(QColor(30, 0, 0, 25)))  # whiteGray?
        palette.setBrush(QPalette.HighlightedText, QBrush(Qt.black))
        self.setPalette(palette)

        # Custom Editor
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # disable Default Editor
        self.currentItemChanged.connect(self.myItemFocusChanged)

        # 전체 레이아웃 설정
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    VisibleAll = -1  # visible all: no limit of showing rows - show all rows
    def setVisibleRowCount(self, row_count: int) -> None:
        """
        decide visible row count.
        if table row count is over visible row count, widget will have scroll bar
        """
        self.__visible_row_count = row_count

    def setFocusCell(self, row: int, column: int) -> None:
        """
        setCurrentCell 후 focus를 테이블에 다시 맞추어, 포커스가 셀을 벗어나지 않게 함
        """
        # todo 너무 복잡해짐. 좀더 단순화할 수 없을까?
        self.clearSelection()
        if self.focusWidget():
            self.focusWidget().clearFocus()
        self.setFocus()
        self.setCurrentCell(row, column)

    """
    method
    * clearTexts
    * clearRowTexts
    * isRowAnyTexts
    """
    def clearTexts(self) -> None:
        for row_iter in range(self.rowCount()):
            self.clearRowTexts(row_iter)

    def clearRowTexts(self, row: int) -> None:
        for col_iter in range(self.columnCount()):
            self.item(row, col_iter).setText('')

    def isRowAnyTexts(self, row: int) -> bool:
        return any([self.item(row, col_iter).text() for col_iter in range(self.columnCount())])

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
        max_visible_row_count = self.__visible_row_count
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
        h += unit_height * (self.__visible_row_count if self.__visible_row_count != MyTableWidget.VisibleAll
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

    """
    Custom Editor Method: ItemLineEdit
    """
    @pyqtSlot(QTableWidgetItem, QTableWidgetItem)
    def myItemFocusChanged(self, current: QTableWidgetItem, previous: QTableWidgetItem) -> None:
        if previous:
            previous_widget = self.cellWidget(previous.row(), previous.column())
            if isinstance(previous_widget, ItemLineEdit) and previous_widget.autoDestroy():
                self.removeCellWidget(previous.row(), previous.column())
        if current:
            # self.setCurrentItem(current)
            if len(self.selectedItems()) <= 1:
                if current.flags() & Qt.ItemIsEditable:
                    self.editItem(current)

    def __setItemLineEdit(self, item: QTableWidgetItem) -> None:
        """
        Set Custom Editor: ItemLineEdit
        """
        #self.setCurrentCell(item.row(), item.column())
        self.setCellWidget(item.row(), item.column(), ItemLineEdit(item, parent=self))
        self.cellWidget(item.row(), item.column()).setFocus()

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

