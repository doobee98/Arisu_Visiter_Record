from Utility.Abstract.View.MyLineEdit import *
from Utility.UI.BaseUI import *



class ItemLineEdit(MyLineEdit):
    """
    ItemLineEdit
    기존에 사용되는 QTableWidgetItem에서의 LineEdit의 단점을 보완하기위해 만들어진 클래스
    * QCompleter 지원
    * 기존의 LineEdit과 같이 자동 삭제, 생성 지원 and 부모 클래스에서의 Persistent Editor 역시 지원함
    * 기존의 LineEdit와 같이 TableWidgetItem과의 text 동기화 지원
    * 기본 Font와 Alignment를 BaseUI와 맞춤
    * TableWidget에서의 Tab, Shift+Tab(BackTab), Right, Left, Enter 키의 작동 재정의 (엑셀과 비슷하게)
    """
    def __init__(self, item: QTableWidgetItem, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.__auto_destroy = True
        self.__item = item
        self.setFont(BaseUI.basicQFont())
        self.setText(self.__item.text())

        completer = QCompleter()
        completer.popup().setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()-1))
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # 대소문자 무시
        completer.setMaxVisibleItems(5)  # todo 임시값
        self.setCompleter(completer)

        table = self.__item.tableWidget()
        table.itemChanged.connect(self.myItemChanged)
        self.textChanged.connect(self.myTextChanged)

    def setCompleterList(self, completer_list: List[str]):
        list_model = QStringListModel(completer_list)
        self.completer().setModel(list_model)
        self.completer().popup().setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        # 너비 자동 조정
        popup = self.completer().popup()
        content_width = popup.sizeHintForColumn(0) + 2 * popup.frameWidth()
        popup.setFixedWidth(content_width)


    def focusInEvent(self, a0: QFocusEvent) -> None:
        super().focusInEvent(a0)
        row, col = self.__item.row(), self.__item.column()
        self.__item.tableWidget().setCurrentCell(row, col)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """
        Right: 텍스트의 가장 오른쪽 끝에서 Right 키를 눌렀을 때, Tab 키와 같은 행동
        Left: 텍스트의 가장 왼쪽 끝에서 Left 키를 눌렀을 때, BackTab 키와 같은 행동
        Enter: (외부) Enter키를 눌렀을 때, 다음 줄의 작성 가능한 셀로 focus를 이동
               (내부) Completer가 켜진 상태에서 Tab 키 등의 다른 메소드를 활용할 시 오류가 발생하기에,
                      내부적으로 Enter 키를 거쳐서 Completer를 종료하고 나서 다른 키를 처리하게 함
        """
        if event.key() == Qt.Key_Right:
            if self.cursorPosition() == len(self.text()):  # 텍스트 커서가 오른쪽 끝이면
                return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)
                QApplication.postEvent(self, return_event)
                QApplication.postEvent(self, tab_event)
                return
        elif event.key() == Qt.Key_Left:
            if self.cursorPosition() == 0:
                return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                back_tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)
                QApplication.postEvent(self, return_event)
                QApplication.postEvent(self, back_tab_event)
                return
        elif event.key() in [Qt.Key_Return, Qt.Key_Enter] and event.spontaneous() is True:
            # 외부에서 직접 엔터키를 눌렀을 때 -> next Row로 이동시키는 내부 Alt+Enter 이벤트를 발생시킴
            # 내부에서 들어온 return 처리일때 -> Enter 처리만 함
            next_row_event = QKeyEvent(QEvent.KeyPress, Qt.ALT + Qt.Key_Enter, Qt.NoModifier)
            QApplication.postEvent(self, next_row_event)
        elif event.key() == Qt.ALT + Qt.Key_Enter and event.spontaneous() is False:
            # 외부에서 엔터키를 눌렀을 때 발생시키는 next row 전용 이벤트
            self.__item.tableWidget().setFocusCell(self.__item.row() + 1, 1)
        super().keyPressEvent(event)

    def event(self, event: QEvent) -> bool:
        """
        Tab & BackTab
        외부에서 탭키나 백탭키를 입력하였을 때는, 리턴 이벤트를 거치고 오도록 함
        내부에서 발생한 탭키나 백탭키는 원래 처리(이전이나 다음 행)으로 제대로 가도록 함
        (무한루프를 방지하기 위해 spontaneous를 기준으로 처리 방식을 다르게 함)
        """
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Tab and event.spontaneous() is True:
                return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)
                QApplication.postEvent(self, return_event)
                QApplication.postEvent(self, tab_event)
                return True
            elif event.key() == Qt.Key_Backtab and event.spontaneous() is True:  # todo 백탭의 지원 여부??
                return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                back_tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)
                QApplication.postEvent(self, return_event)
                QApplication.postEvent(self, back_tab_event)
                return True
        return super().event(event)

    def autoDestroy(self) -> bool:
        return self.__auto_destroy

    def setAutoDestroy(self, enable: bool):
        self.__auto_destroy = enable

    @MyPyqtSlot(str)
    def myTextChanged(self, s: str):
        cursor_pos = self.cursorPosition()
        self.blockSignals(True)
        self.__item.setText(s)
        self.blockSignals(False)
        self.setCursorPosition(cursor_pos)

    @MyPyqtSlot(QTableWidgetItem)
    def myItemChanged(self, item: QTableWidgetItem):
        if item == self.__item:
            self.blockSignals(True)
            self.setText(item.text())
            self.blockSignals(False)

        
