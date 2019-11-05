from View.Record.RecordMainView import *
from View.Database.DatabaseMainView import DatabaseMainView
from View.Option.OptionDialog import *
from Utility.Manager.StatusBarManager import *


class MainViewSignal(QObject):
    OpenRecordRequest = pyqtSignal(str)
    OpenDatabaseRequest = pyqtSignal(str)
    CloseRecordFileRequest = pyqtSignal(int)
    ChangeRecordTabSignal = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)


class MainView(QMainWindow, ShowingView):
    def __init__(self):
        super().__init__()

        self.__signal_set = MainViewSignal(self)
        self.__record: RecordMainView = None
        self.__database: DatabaseMainView = None

        # 하단 탭 생성
        self.__tab_widget = QTabWidget()
        self.__tab_widget.setTabPosition(QTabWidget.South)
        self.__tab_widget.setTabsClosable(True)
        self.__tab_widget.currentChanged.connect(self.activeRecordChanged)
        self.__tab_widget.tabCloseRequested.connect(self.closeTab)

        # 하단 탭 스타일링
        tabs_font = self.__tab_widget.font()
        tabs_font.setPointSize(12)  # todo font size
        self.__tab_widget.setFont(tabs_font)

        # 상단 메뉴바 생성
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        
        #   파일 메뉴
        file_menu = menubar.addMenu('파일')
        create_record_action = QAction('오늘 날짜 기록부 새로 만들기 / 열기', self)
        create_record_action.triggered.connect(lambda: self.createTodayRecord())
        open_record_action = QAction('기록부 파일 열기', self)
        open_record_action.triggered.connect(lambda: self.openRecordView())
        file_menu.addAction(create_record_action)
        file_menu.addAction(open_record_action)

        #   편집 메뉴
        edit_menu = menubar.addMenu('편집')
        undo_action = QAction('뒤로가기 (Ctrl + Z)', self)
        undo_action.triggered.connect(lambda: CommandManager.undo())
        edit_menu.addAction(undo_action)
        redo_action = QAction('다시하기 (Ctrl + Y)', self)
        redo_action.triggered.connect(lambda: CommandManager.redo())
        edit_menu.addAction(redo_action)

        #   설정 메뉴
        config_menu = menubar.addMenu('설정')
        self.__config_view = OptionDialog()
        open_config_action = QAction('설정', self)
        open_config_action.triggered.connect(lambda: self.configDialogExec())
        config_menu.addAction(open_config_action)

        # 하단 상태바 초기화 및 statusBar Manager 초기화
        self.statusBar().setFont(BaseUI.basicQFont())
        StatusBarManager.setStatusBar(self.statusBar())
        StatusBarManager.setMessage('프로그램 초기화')

        # 메인화면 레이아웃
        self.setCentralWidget(self.__tab_widget)
        self.setWindowTitle('아리수 출입자기록부 프로그램')
        self.setWindowIcon(QIcon(BasicFileTable.Icon))

        # 시계 날짜 지나는 것과 연결하기
        Clock.getSignalSet().DayOut.connect(lambda: self.dayoutDialogExec())

        self.setFont(BaseUI.basicQFont())
        self.setAcceptDrops(True)

        x, y = Config.HiddenOption.windowGeometry()
        self.move(x, y)
        self.showNormal()

    """
    property
    * signalSet
    * tabWidget
    """

    def getSignalSet(self) -> MainViewSignal:
        return self.__signal_set

    def tabWidget(self) -> QTabWidget:
        return self.__tab_widget

    """
    method
    * activeView
    * setNextTab
    * configDialogExec
    * dayoutDialogExec
    * create recordView
    * open/close recordView
    * open/close databaseView
    * addRecordTab
    * addDatabaseTab
    """

    def activeView(self):
        return self.tabWidget().currentWidget() if self.tabWidget().count() != 0 else self

    def setNextTab(self) -> None:
        self.tabWidget().setCurrentIndex((self.tabWidget().currentIndex() + 1) % self.tabWidget().count())

    def configDialogExec(self) -> None:
        self.__config_view.exec_()

    def dayoutDialogExec(self) -> None:
        reply = MyMessageBox.question(self, '알림', '날짜가 바뀌었습니다.\n', '마감 후 새로운 기록부를 만드시겠습니까?')
        if reply == MyMessageBox.Yes:
            try:
                self.__record.reportExcel()
                self.createTodayRecord()
            except Exception as e:
                ErrorLogger.reportError('날짜 바꿈 에러', e)
        else:
            return

    def createTodayRecord(self) -> None:
        directory, file_name = FilePathConfig.getRecordTablePath(Config.TotalOption.location(), Clock.getDate().toString('yyMMdd'))
        record_file_path = FilePathConfig.getFilePathString(directory, file_name)
        self.getSignalSet().OpenRecordRequest.emit(record_file_path)

    def openRecordView(self) -> None:
        extension = '.rcd'
        file_name = QFileDialog.getOpenFileName(self, '파일 열기', './', '*' + extension)
        if file_name[0]:
            self.getSignalSet().OpenRecordRequest.emit(file_name[0])
            #self.tabWidget().setCurrentIndex(self.tabWidget().count() - 1)
        else:
            pass  # todo 맞나?

    def addDatabaseTab(self, database_view: DatabaseMainView) -> None:
        ExecuteLogger.printLog('addDB')
        self.__database = database_view
        self.__database.function_group.setOptionSlot(lambda: self.configDialogExec())
        if self.tabWidget().widget(0):
            self.closeTab(0)
        self.tabWidget().insertTab(0, database_view, 'DB')
        self.tabWidget().tabBar().tabButton(0, QTabBar.RightSide).hide()
        ShortCutManager.addShortCut(database_view, Qt.CTRL + Qt.Key_Tab, lambda: self.setNextTab())

    def addRecordTab(self, record_view: RecordMainView) -> None:
        if record_view.record_table.getRecordDate() is not None:
            tab_string = record_view.record_table.getRecordDate()
        else:
            tab_string = '기록부'
        ExecuteLogger.printLog('add tab ' + tab_string)
        self.__record = record_view
        self.__record.function_group.setOptionSlot(lambda: self.configDialogExec())
        self.tabWidget().addTab(record_view, tab_string)
        ShortCutManager.addShortCut(record_view, Qt.CTRL + Qt.Key_Tab, lambda: self.setNextTab())

    @MyPyqtSlot(int)
    def closeTab(self, idx: int) -> None:
        if idx == 0:
            for i in range(self.tabWidget().count() - 1, 0, -1):
                self.closeTab(i)
            self.__database = None
        else:
            # close_date = self.tabWidget().tabText(idx)
            self.getSignalSet().CloseRecordFileRequest.emit(idx)
        self.tabWidget().removeTab(idx)

    """
    event
    * closeEvent
    * dragEnterEvent, dropEvent
    """
    def closeEvent(self, a0: QCloseEvent) -> None:
        Config.HiddenOption.setWindowGeometry((self.pos().x(), self.pos().y()))
        super().closeEvent(a0)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            urls: List[QUrl] = event.mimeData().urls()
            for url_iter in urls:
                file_path = url_iter.path()
                if not (len(file_path) > 4 and file_path[-4:] == '.rcd'):
                    return
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        if event.mimeData().hasUrls():
            urls: List[QUrl] = event.mimeData().urls()
            for url_iter in urls:
                file_path = url_iter.path()[1:].replace('/', '\\')
                self.getSignalSet().OpenRecordRequest.emit(file_path)

    """
    slot
    * activeRecordChanged
    """

    @MyPyqtSlot(int)
    def activeRecordChanged(self, idx: int) -> None:
        if idx == 0:
            pass
            # state: MainView.State.Database
        elif idx > 0:
            ExecuteLogger.printLog('change tab to ' + self.tabWidget().tabText(idx))
            self.getSignalSet().ChangeRecordTabSignal.emit(idx)
            # state: MainView.State.Record

    """
    render
    """
    def render(self):
        StatusBarManager.setIdleStatus()



