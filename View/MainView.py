import sys
from PyQt5.QtWidgets import *  # QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout

from View.Record.RecordMainView import *
from View.Database.DatabaseMainView import DatabaseMainView
from View.Option.OptionDialog import *
from Utility.ShowingView import *
from Utility.StatusBarManager import *


class MainViewSignal(QObject):
    OpenRecordRequest = pyqtSignal(str, str)
    OpenDatabaseRequest = pyqtSignal(str)
    CloseFileRequest = pyqtSignal(str)
    ChangeRecordTabSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)


class MainView(QMainWindow, ShowingView):
    class State(Enum):
        Database = auto()
        Record = auto()
        # Option = auto()
        # Alert = auto()

    def __init__(self):
        super().__init__()

        self.__signal_set = MainViewSignal(self)
        self.record = None
        self.database = None

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
        
        #   메뉴 파일
        file_menu = menubar.addMenu('파일')
        open_record_action = QAction('기록부 파일 열기', self)
        open_record_action.triggered.connect(self.openRecordView)
        change_database_action = QAction('데이터베이스 파일 변경하기(미완성)', self)
        change_database_action.triggered.connect(self.openDatabaseView)
        #open_record_action.setEnabled(False)
        change_database_action.setEnabled(False)
        file_menu.addAction(open_record_action)
        file_menu.addAction(change_database_action)

        #   편집 파일
        edit_menu = menubar.addMenu('편집')
        undo_action = QAction('뒤로가기 (Ctrl + Z)', self)
        undo_action.triggered.connect(CommandManager.undo)
        edit_menu.addAction(undo_action)
        redo_action = QAction('다시하기 (Ctrl + Y)', self)
        redo_action.triggered.connect(CommandManager.redo)
        edit_menu.addAction(redo_action)

        #   설정 파일
        self.config_view = OptionDialog()
        # todo 테스트: config setting
        config_menu = menubar.addMenu('설정')
        open_config_action = QAction('설정', self)
        open_config_action.triggered.connect(self.configDialogExec)
        config_menu.addAction(open_config_action)

        # 하단 상태바
        self.statusBar().setFont(BaseUI.basicQFont())
        StatusBarManager.setStatusBar(self.statusBar())
        StatusBarManager.setMessage('프로그램 초기화', 3000)

        # 메인화면 레이아웃
        self.setCentralWidget(self.__tab_widget)
        self.setWindowTitle('아리수 정수센터 관리 시스템')

        self.move(50, 0)  # 임시값
        self.showNormal()


    def __str__(self):
        return 'MainView'

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
        self.config_view.exec_()

    def openDatabaseView(self) -> None:
        file_name = QFileDialog.getOpenFileName(self, '파일 열기', './', '*.iml')  # , '*.iml'
        if file_name[0]:
            file_pos = file_name[0].find('암사')  # todo: 파일 모듈로 옮길것
            database_location = file_name[0][file_pos:file_pos+4]
            database_location = database_location[0:2] + ' ' + database_location[2:4]
            self.getSignalSet().OpenDatabaseRequest.emit(database_location)
            #self.tabWidget().setCurrentIndex(0)
        else:
            ErrorLogger.reportError('File Open Error')

    def openRecordView(self) -> None:
        extension = '.rcd'
        file_name = QFileDialog.getOpenFileName(self, '파일 열기', './', '*' + extension)  # , '*.iml'
        if file_name[0]:
            """
            1. 마지막 슬래시(/) 이후의 문자열을 파일 이름으로 -> {head}_{tail}_기록부_{date}.rcd
            2. 언더바(_) 기준으로 split 한 뒤 location과 record_date에 입력함
            """
            file_name = file_name[0].split('/').pop(-1)
            file_name_split = file_name.split('_')
            location = file_name_split[0] + ' ' + file_name_split[1]
            record_date = file_name_split[3].replace(extension, '')

            self.getSignalSet().OpenRecordRequest.emit(location, record_date)
            self.tabWidget().setCurrentIndex(self.tabWidget().count() - 1)
            #self.getSignalSet().ChangeRecordTabSignal.emit(file_name[0])
        else:
            ErrorLogger.reportError('File Open Error')

    def addDatabaseTab(self, database_view: DatabaseMainView) -> None:
        print('addDB')
        self.database = database_view
        self.database.function_group.setOptionSlot(self.configDialogExec)
        if self.tabWidget().widget(0):
            self.closeTab(0)
        self.tabWidget().insertTab(0, database_view, 'DB')
        self.tabWidget().tabBar().tabButton(0, QTabBar.RightSide).hide()
        ShortCutManager.addShortCut(database_view, Qt.CTRL + Qt.Key_Tab, self.setNextTab)

    def addRecordTab(self, record_view: RecordMainView) -> None:
        if record_view.record_table.getRecordDate() is not None:
            tab_string = record_view.record_table.getRecordDate()
        else:
            tab_string = '기록부'
        print('add tab', tab_string)
        self.record = record_view
        self.record.function_group.setOptionSlot(self.configDialogExec)
        self.tabWidget().addTab(record_view, tab_string)
        ShortCutManager.addShortCut(record_view, Qt.CTRL + Qt.Key_Tab, self.setNextTab)

    @pyqtSlot(int)
    def closeTab(self, idx: int) -> None:
        if idx == 0:
            for i in range(self.tabWidget().count() - 1, 0, -1):
                self.closeTab(i)
            self.database = None
        else:
            close_date = self.tabWidget().tabText(idx)
            self.getSignalSet().CloseFileRequest.emit(close_date)
        self.tabWidget().removeTab(idx)

    """
    slot
    * activeRecordChanged
    """

    @pyqtSlot(int)
    def activeRecordChanged(self, idx: int) -> None:
        if idx == 0:
            pass
            # state: MainView.State.Database
        elif idx > 0:
            print('change tab to', self.tabWidget().tabText(idx))
            self.getSignalSet().ChangeRecordTabSignal.emit(self.tabWidget().tabText(idx))
            # state: MainView.State.Record

    """
    render
    """
    def render(self):
        pass



