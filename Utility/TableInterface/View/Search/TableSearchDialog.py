from Utility.TableInterface.View.MyTableView import *
from Utility.ShowingView import *
from Utility.UI.BaseUI import *


class TableSearchDialogSignal(QObject):
    SearchTableRequest = pyqtSignal(dict)
    BeforeSearchRequest = pyqtSignal()
    NextSearchRequest = pyqtSignal()
    FinishSearchRequest = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

# todo: 계속 검색 버튼 만들기.
class TableSearchDialog(QDialog, ShowingView):
    class State(Enum):
        Write = auto()
        Searching = auto()

    def __init__(self, table_view_model: Type[MyTableView]):
        super().__init__()
        self.__table_view = table_view_model
        self.__signal_set = TableSearchDialogSignal(self)
        self.__state = None

        self.__search_line_edit_dict: Dict[str, QLineEdit] = {}
        self.__search_grid_layout = QGridLayout()
        for row_iter, field_iter in enumerate(self.searchFieldList()):
            lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text=field_iter, alignment=Qt.AlignLeft)
            le = BaseUI.basicQLineEdit(alignment=Qt.AlignLeft)
            le.installEventFilter(self)
            self.__search_grid_layout.addWidget(lbl, row_iter, 0)
            self.__search_grid_layout.addWidget(le, row_iter, 1)
            self.__search_line_edit_dict[field_iter] = le

        self.__search_button = BaseUI.basicQPushButton(text='\n검색\n')
        self.__search_button.clicked.connect(self.searchButtonClicked)
        self.__before_button = BaseUI.basicQPushButton(text='이전')
        self.__before_button.clicked.connect(self.beforeButtonClicked)
        self.__next_button = BaseUI.basicQPushButton(text='계속')
        self.__next_button.clicked.connect(self.nextButtonClicked)
        self.__rewrite_button = BaseUI.basicQPushButton(text='\n다시 입력\n')
        self.__rewrite_button.clicked.connect(self.rewriteButtonClicked)
        vbox_button = QVBoxLayout()
        vbox_button.addWidget(self.__before_button)
        vbox_button.addWidget(self.__next_button)
        hbox = QHBoxLayout()
        hbox.addWidget(self.__search_button)
        hbox.addLayout(vbox_button)
        hbox.addWidget(self.__rewrite_button)

        vbox = QVBoxLayout()
        vbox.addLayout(self.__search_grid_layout)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setState(TableSearchDialog.State.Write)
        self.setWindowTitle('검색')

    def getSignalSet(self) -> TableSearchDialogSignal:
        return self.__signal_set

    def __tableView(self) -> Type[MyTableView]:
        return self.__table_view

    def activeView(self) -> Type['ShowingView']:
        return self

    def state(self) -> State:
        return self.__state

    def setState(self, state: State) -> None:
        self.__state = state

        if state == TableSearchDialog.State.Write:
            le_enable, search_enable, before_enable, next_enable, rewrite_enable = True, True, False, False, False
        else:
            le_enable, search_enable, before_enable, next_enable, rewrite_enable = False, False, True, True, True

        for le_iter in self.__search_line_edit_dict.values():
            le_iter.setEnabled(le_enable)
        self.searchButton().setEnabled(search_enable)
        self.beforeButton().setEnabled(before_enable)
        self.nextButton().setEnabled(next_enable)
        self.rewriteButton().setEnabled(rewrite_enable)

    def searchFieldList(self) -> List[str]:
        return self.__tableView().modelFieldList()

    def searchLineEdit(self, field: str) -> QLineEdit:
        return self.__search_line_edit_dict.get(field)

    def searchGridLayout(self) -> QGridLayout:
        return self.__search_grid_layout

    def searchButton(self) -> QPushButton:
        return self.__search_button

    def beforeButton(self) -> QPushButton:
        return self.__before_button

    def nextButton(self) -> QPushButton:
        return self.__next_button

    def rewriteButton(self) -> QPushButton:
        return self.__rewrite_button

    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        if self.state() == TableSearchDialog.State.Searching:
            self.searchButtonClicked()

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.state() == TableSearchDialog.State.Searching:
            self.getSignalSet().FinishSearchRequest.emit()
        super().closeEvent(a0)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)

    @pyqtSlot()
    def searchButtonClicked(self) -> None:
        search_dict = {}
        for field_iter in self.searchFieldList():
            le_iter = self.searchLineEdit(field_iter)
            if le_iter.text():
                search_dict[field_iter] = le_iter.text()

        if search_dict:
            self.getSignalSet().SearchTableRequest.emit(search_dict)
            self.setState(TableSearchDialog.State.Searching)

    @pyqtSlot()
    def beforeButtonClicked(self) -> None:
        self.getSignalSet().BeforeSearchRequest.emit()

    @pyqtSlot()
    def nextButtonClicked(self) -> None:
        self.getSignalSet().NextSearchRequest.emit()

    @pyqtSlot()
    def rewriteButtonClicked(self) -> None:
        self.getSignalSet().FinishSearchRequest.emit()
        self.setState(TableSearchDialog.State.Write)

    def eventFilter(self, widget: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Down:
                tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)  # 탭키 효과로 넘어가게
                QApplication.postEvent(self, tab_event)
                return True
            elif event.key() == Qt.Key_Up:
                shift_tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)  # 탭키 효과로 넘어가게
                QApplication.postEvent(self, shift_tab_event)
                return True
        return super().eventFilter(widget, event)

