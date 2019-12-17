from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Manager.CommandManager import *
from View.Record.RecordMainView import *
from View.Database.DatabaseMainView import *
from Utility.Manager.StatusBarManager import *
from Utility.Manager.ShortCutManager import *

"""
MainView
""" # todo


class MainViewSignal(QObject):
    CurrentRecordMainViewIndexChanged = pyqtSignal(int, int)
    RemoveRecordMainViewRequest = pyqtSignal(int)
    OpenTodayRecordRequest = pyqtSignal()
    OpenRecordRequest = pyqtSignal()
    OpenRecordFileRequest = pyqtSignal(str)
    UndoMenuTriggered = pyqtSignal()
    RedoMenuTriggered = pyqtSignal()
    OptionMenuTriggered = pyqtSignal()

    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class MainView(QMainWindow, ShowingView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.__signal_set = MainViewSignal(self)
        self.__current_record_index = -1
        # TabWidget
        self.__tab_widget = QTabWidget()
        self.__tab_widget.setTabPosition(QTabWidget.South)
        self.__tab_widget.setTabsClosable(True)
        self.__tab_widget.setFont(MyDefaultWidgets.basicQFont())
        self.__tab_widget.setStyleSheet('::{background-color: rgb(255, 255, 255);}')
        self.__tab_widget.tabCloseRequested.connect(self.__tabCloseRequested)
        self.__tab_widget.currentChanged.connect(self.__currentTabWidgetChanged)

        # Menu Bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        #   Menu - File
        file_menu = menubar.addMenu('파일')
        create_record_action = QAction('오늘 날짜 기록부 새로 만들기 / 열기', self)
        create_record_action.triggered.connect(lambda: self.signalSet().OpenTodayRecordRequest.emit())
        open_record_action = QAction('기록부 파일 열기', self)
        open_record_action.triggered.connect(lambda: self.signalSet().OpenRecordRequest.emit())
        file_menu.addAction(create_record_action)
        file_menu.addAction(open_record_action)

        #   Menu - Edit
        edit_menu = menubar.addMenu('편집')
        undo_action = QAction('뒤로가기 (Ctrl + Z)' if ConfigModule.Application.enableShortCut() else '뒤로가기', self)
        undo_action.triggered.connect(lambda: self.signalSet().UndoMenuTriggered.emit())
        edit_menu.addAction(undo_action)
        redo_action = QAction('다시하기 (Ctrl + Y)' if ConfigModule.Application.enableShortCut() else '다시하기', self)
        redo_action.triggered.connect(lambda: self.signalSet().RedoMenuTriggered.emit())
        edit_menu.addAction(redo_action)

        #   Menu - Option
        option_menu = menubar.addMenu('설정')
        open_config_action = QAction('설정', self)
        open_config_action.triggered.connect(lambda: self.signalSet().OptionMenuTriggered.emit())
        option_menu.addAction(open_config_action)

        # Status Bar
        self.statusBar().setFont(MyDefaultWidgets.basicQFont())
        StatusBarManager.setStatusBar(self.statusBar())
        StatusBarManager.setMessage('프로그램 초기화')

        # style
        self.setAcceptDrops(True)
        x, y = ConfigModule.Hidden.windowGeometry()
        self.move(x, y)

        self.setCentralWidget(self.__tab_widget)
        self.setFont(MyDefaultWidgets.basicQFont())
        self.setWindowTitle('아리수 출입자기록부 프로그램')
        self.setWindowIcon(QIcon(DefaultFilePath.Icon))
        StatusBarManager.setIdleStatus()

    """
    property
    * signalSet
    * tabWidget
    * currentRecordIndex
    """
    def signalSet(self) -> MainViewSignal:
        return self.__signal_set

    def tabWidget(self) -> QTabWidget:
        return self.__tab_widget

    def currentRecordIndex(self) -> int:
        return self.__current_record_index

    def setCurrentRecordIndex(self, index: int) -> None:
        if index != self.__current_record_index:
            old_index = self.__current_record_index
            self.__current_record_index = index
            self.signalSet().CurrentRecordMainViewIndexChanged.emit(index, old_index)

    """
    advanced property
    * databaseMainView, recordMainView
    * currentRecordMainViewIndex
    """
    def databaseMainView(self) -> DatabaseMainView:
        if self.tabWidget().count() > 0 and isinstance(self.tabWidget().widget(0), DatabaseMainView):
            return self.tabWidget().widget(0)
        else:
            return None

    def recordMainView(self, location: str, date: str) -> RecordMainView:
        for index in range(1, self.tabWidget().count(), 1):
            record_view_iter: RecordMainView = self.tabWidget().widget(index)
            if isinstance(record_view_iter, RecordMainView):
                if record_view_iter.location() == location and record_view_iter.date() == date:
                    return record_view_iter
        return None

    def currentRecordMainView(self) -> RecordMainView:
        return self.tabWidget().widget(self.currentRecordIndex()) if self.currentRecordIndex() != -1 else None

    """
    method
    * setDatabaseMainView
    * setRecordMainView, removeRecordMainView
    * setNextTab
    """
    def setDatabaseMainView(self, database_view: DatabaseMainView) -> None:
        database_tab_header = database_view.location().replace(' ', '') + 'DB'
        self.tabWidget().insertTab(0, database_view, database_tab_header)
        self.tabWidget().tabBar().tabButton(0, QTabBar.RightSide).hide()
        if ConfigModule.Application.enableShortCut():
            ShortCutManager.addShortCut(database_view, Qt.CTRL + Qt.Key_Tab, lambda: self.setNextTab())

    def setRecordMainView(self, record_view: RecordMainView) -> None:
        self.tabWidget().addTab(record_view, record_view.date())
        self.tabWidget().setCurrentIndex(self.tabWidget().count() - 1)
        if ConfigModule.Application.enableShortCut():
            ShortCutManager.addShortCut(record_view, Qt.CTRL + Qt.Key_Tab, lambda: self.setNextTab())

    def removeRecordMainView(self, record_view: RecordMainView) -> None:
        for index in range(1, self.tabWidget().count(), 1):
            if record_view == self.tabWidget().widget(index):
                if index == self.currentRecordIndex():
                    self.setCurrentRecordIndex(-1)
                self.tabWidget().removeTab(index)
                return
        raise AttributeError

    def setNextTab(self) -> None:
        self.tabWidget().setCurrentIndex((self.tabWidget().currentIndex() + 1) % self.tabWidget().count())

    """
    slot
    * __currentTabWidgetChanged, __tabCloseRequested
    """
    @MyPyqtSlot(int)
    def __currentTabWidgetChanged(self, index: int) -> None:
        if self.databaseMainView() and index != 0:
            self.setCurrentRecordIndex(index)

    @MyPyqtSlot(int)
    def __tabCloseRequested(self, index: int) -> None:
        if self.databaseMainView() and index != 0:
            self.signalSet().RemoveRecordMainViewRequest.emit(index)

    """
    event
    * closeEvent
    * dragEvent
    """
    def closeEvent(self, a0: QCloseEvent) -> None:
        ConfigModule.Hidden.setWindowGeometry(self.pos().x(), self.pos().y())
        super().closeEvent(a0)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            urls: List[QUrl] = event.mimeData().urls()
            for url_iter in urls:
                file_path = url_iter.path()
                if not (len(file_path) > 4 and file_path[-4:] == ConfigModule.FilePath.filePathExtension(FileType.RecordTable)):
                    return
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            urls: List[QUrl] = event.mimeData().urls()
            for url_iter in urls:
                file_path = url_iter.path()[1:].replace('/', '\\')
                self.signalSet().OpenRecordFileRequest.emit(file_path)

    """
    override
    * activeView
    """
    def activeView(self) -> 'ShowingView':
        return self.tabWidget().currentWidget() if self.tabWidget().count() != 0 else self