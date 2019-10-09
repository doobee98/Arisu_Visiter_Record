from Utility.Config.ConfigModule import *
from Utility.UI.BaseUI import *

from typing import List
from Utility.CommandManager import *


class ItemLineEdit(QLineEdit):
    def __init__(self, item: QTableWidgetItem, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.__auto_destroy = True
        self.__item = item

        self.setText(self.__item.text())
        self.selectAll()
        self.setAlignment(Qt.AlignCenter)
        self.setFont(BaseUI.basicQFont())  # TODO FONTSIZE

        completer = QCompleter()
        completer.popup().setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()-1))  # TODO FONTSIZE
        completer.setMaxVisibleItems(5)  # todo 임시값
        self.setCompleter(completer)

        table = self.__item.tableWidget()
        table.itemChanged.connect(self.myItemChanged)
        self.textChanged.connect(self.myTextChanged)

    def setCompleterList(self, completer_list: List[str]):
        list_model = QStringListModel(completer_list)
        self.completer().setModel(list_model)

    def focusInEvent(self, a0: QFocusEvent) -> None:
        super().focusInEvent(a0)
        row, col = self.__item.row(), self.__item.column()
        self.__item.tableWidget().setCurrentCell(row, col)

    # def finishEdit(self):
    #     self.clearCompleter()
    #     QApplication.postEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Right:
            if self.cursorPosition() == len(self.text()):  # 텍스트 커서가 오른쪽 끝이면
                return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)
                QApplication.postEvent(self, return_event)
                QApplication.postEvent(self, tab_event)
                event.setAccepted(True)
                #return
        elif event.key() == Qt.Key_Left:  # left arrow key -> back tab key
            if self.cursorPosition() == 0:  # 텍스트 커서가 왼쪽 끝이면
                return_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Return, Qt.NoModifier)
                back_tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)
                QApplication.postEvent(self, return_event)
                QApplication.postEvent(self, back_tab_event)
                event.setAccepted(True)
                #return
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # 외부에서 직접 엔터키를 눌렀을 때 -> next Row로 이동
            # 내부에서 들어온 return 처리일때 -> 처리만 제대로 하고 패스
            if event.spontaneous() is True:
                # todo: command로 할 수 없나?
                self.__item.tableWidget().setFocusCell(self.__item.row() + 1, 1)
                #CommandManager.postCommand(View.Table.FocusCellCommand(self.__item.tableWidget(), self.__item.row() + 1, 1))
        super().keyPressEvent(event)

    def event(self, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            # 외부에서 탭키나 백탭키를 입력하였을 때는, 리턴을 하고 오도록 함
            # 내부에서 발생한 탭키나 백탭키는 원래 처리(이전이나 다음 행)으로 제대로 가도록 함
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

    # def event(self, event: QEvent) -> bool:
    #     if event.type() == QEvent.KeyPress:
    #         print(QKeySequence(event.key()).toString())
    #         if event.key() == Qt.Key_Tab or event.key() == Qt.Key_Backtab:
    #             self.clearCompleter()
    #             #return False
    #         # if event.key() == Qt.Key_Right:
    #         #     if self.cursorPosition() == len(self.text()): # 텍스트 커서가 오른쪽 끝이면
    #         #         tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)  # 탭키 효과로 넘어가게
    #         #         QApplication.postEvent(self, tab_event)
    #         #         # self.event(tab_event)
    #         #         return True  # 원래 효과 무시
    #         # elif event.key() == Qt.Key_Left:  # left arrow key -> back tab key
    #         #     if self.cursorPosition() == 0:  # 텍스트 커서가 왼쪽 끝이면
    #         #         shift_tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)  # 백탭키 효과로 이전칸으로
    #         #         QApplication.postEvent(self, shift_tab_event)
    #         #         # self.event(shift_tab_event)
    #         #         return True  # 원래 효과 무시
    #         # elif event.key() == Qt.Key_Return:
    #         #     tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)  # 탭키 효과로 넘어가게
    #         #     QApplication.postEvent(self, tab_event)
    #         #     # self.event(tab_event)
    #         #     return True  # 원래 효과 무시
    #         # elif event.key() == Qt.Key_Tab:
    #         #     self.clearCompleter()
    #         #     table = self.__item.tableWidget()
    #         #     next_row, next_column = self.__item.row(), self.__item.column() + 1
    #         #     next_column %= table.columnCount()
    #         #     #table.setFocusCell(next_row, next_column)
    #         #     return True  # 원래 효과 무시
    #         # elif event.key() == Qt.Key_Backtab:
    #         #     self.clearCompleter()
    #         #     table = self.__item.tableWidget()
    #         #     before_row, before_column = self.__item.row(), self.__item.column() - 1
    #         #     before_column = (before_column + table.columnCount()) % table.columnCount()
    #         #     table.setCurrentCell(before_row, before_column)
    #         #     return True  # 원래 효과 무시
    #
    #     return QLineEdit.event(self, event)

    def autoDestroy(self) -> bool:
        return self.__auto_destroy

    def setAutoDestroy(self, enable: bool):
        self.__auto_destroy = enable

    @pyqtSlot(str)
    def myTextChanged(self, s: str):
        self.blockSignals(True)
        self.__item.setText(s)
        self.blockSignals(False)

    @pyqtSlot(QTableWidgetItem)
    def myItemChanged(self, item: QTableWidgetItem):
        if item == self.__item:
            self.blockSignals(True)
            self.setText(item.text())
            self.blockSignals(False)
