from Controller.Record.RecordMainController import *
from Controller.Database.DatabaseMainController import *
from Controller.DB_Record_HubController import *
from Utility.File.LocationSettingDialog import *
from View.MainView import *
from Utility.ShortCutManager import *


class _ActiveControllerSet:
    def __init__(self):
        self.__record_control: RecordMainController = None
        self.__database_control: DatabaseMainController = None
        self.__hub_control: DB_Record_HubController = None
        self.__is_connected: bool = False
        self.__connect_list: List[pyqtSignal, Callable] = []

    def isConnected(self) -> bool:
        return self.__is_connected

    def recordController(self) -> RecordMainController:
        return self.__record_control

    def setRecordController(self, record_control: RecordMainController) -> None:
        if self.isConnected():
            self.disconnectController()
        self.__record_control = record_control

    def databaseController(self) -> DatabaseMainController:
        return self.__database_control

    def setDatabaseController(self, database_control: DatabaseMainController) -> None:
        if self.isConnected():
            self.disconnectController()
        self.__database_control = database_control

    def connectController(self) -> bool:
        if self.isConnected() is False and self.__isConnectable():
            self.__hub_control = DB_Record_HubController(self.databaseController(), self.recordController())
            self.__hub_control.Run()
            CompleterListModule.setDatabase(self.__database_control.control_table.view())
            CompleterListModule.setRecordTable(self.__record_control.control_table.view())
            StatusBarManager.setLabelConnection(True)
            self.__is_connected = True
            return True
        else:
            return False

    def disconnectController(self) -> bool:
        if self.isConnected() is True:
            StatusBarManager.setLabelConnection(False)
            CompleterListModule.setDatabase(None)
            CompleterListModule.setRecordTable(None)
            self.__hub_control.Stop()
            self.__hub_control = None
            self.__is_connected = False
            return True
        else:
            return False

    def __isConnectable(self) -> bool:
        if self.recordController() is None or self.databaseController() is None:
            return False
        return self.recordController().location() == self.databaseController().location()


# todo 런, 스탑 시스템 정리할것. 지금은 임시로 해둔 값들이 굉장히 많음
class MainController(AbstractController):
    MAX_DATABASE = 1
    MAX_RECORD = 5
    def __init__(self):
        super().__init__()
        QApplication.instance().installEventFilter(self)
        if Config.TotalOption.location() is None:
            location_dialog = LocationSettingDialog()
            location_dialog.exec_()

        self.__model = None
        self.__view = MainView()

        self.__database_control_list: List[DatabaseMainController] = []
        self.__record_control_list: List[RecordMainController] = []
        self.__active_control_set = _ActiveControllerSet()
        self.__initializeSystem()

    def __initializeSystem(self) -> None:
        """
        module loading
        오늘날짜 기록부를 연다
        """
        Clock.start()  # todo 여기있어도 되나?
        location, today = Config.TotalOption.location(), Clock.getDate().toString('yyMMdd')
        directory, file_name = FilePathConfig.getRecordTablePath(location, today)
        record_file_path = FilePathConfig.getFilePathString(directory, file_name)
        database_control, record_control = self.openDatabaseFile(location), self.openRecordFile(record_file_path)
        if database_control is None or record_control is None:
            ErrorLogger.reportError('초기 로딩에 오류가 발생했습니다.', FileNotFoundError)
        self.setActiveDatabase(database_control)
        self.setActiveRecord(record_control)
    """
    property
    * model
    * view
    * activeControllerManager
    """
    def model(self) -> None:
        return None

    def view(self) -> MainView:
        return self.__view

    def activeControllerManager(self) -> _ActiveControllerSet:
        return self.__active_control_set

    """
    method
    * Run, Stop
    * activeView
    * addDatabaseController, removeDatabaseController
    * addRecordController, removeRecordController
    * openDatabaseFile
    * openRecordFile
    """
    def Run(self):
        self.view().getSignalSet().OpenDatabaseRequest.connect(
            lambda loc: self.setActiveDatabase(self.openDatabaseFile(loc)))
        self.view().getSignalSet().OpenRecordRequest.connect(
            lambda file_name: self.setActiveRecord(self.openRecordFile(file_name)))
        self.view().getSignalSet().CloseRecordFileRequest.connect(
            lambda idx: self.removeRecordController(self.__record_control_list[idx-len(self.__database_control_list)]))
        self.view().getSignalSet().ChangeRecordTabSignal.connect(
            lambda idx: self.setActiveRecord(self.__record_control_list[idx-len(self.__database_control_list)]))
        # BaseUI.getSignalSet().FontSizeChanged.connect(lambda a, b: self.Run()) 연결 방식 고민하기 stop후 run

        self.activeControllerManager().connectController()
        # self.activeControllerManager().recordController().Run()
        # self.activeControllerManager().databaseController().Run()

        self.view().render()
        self.view().show()

    def Stop(self):
        self.view().getSignalSet().OpenDatabaseRequest.disconnect(self.openDatabaseFile)
        self.view().getSignalSet().OpenRecordRequest.disconnect(self.openRecordFile)
        self.view().getSignalSet().CloseRecordFileRequest.disconnect(self.closeRecord)
        self.view().getSignalSet().ChangeRecordTabSignal.disconnect(self.changeActiveRecordController)
        # BaseUI.getSignalSet().FontSizeChanged.connect(lambda a, b: self.Run()) 연결 방식 고민하기 stop후 run
        self.activeControllerManager().databaseController().Stop()
        self.activeControllerManager().recordController().Stop()

    def activeView(self) -> QWidget:
        if not isinstance(QApplication.activeWindow(), ShowingView):
            ErrorLogger.reportError('Showing View(Window) not implement ShowingView', NotImplementedError)
        return QApplication.activeWindow().activeView()

    def addDatabaseController(self, database_control: DatabaseMainController) -> bool:
        if len(self.__database_control_list) >= MainController.MAX_DATABASE:
            ErrorLogger.reportError(f'데이터베이스를 {MainController.MAX_DATABASE}개 이상 로드할 수 없습니다.')
            return False
        for control_iter in self.__database_control_list:
            if control_iter.location() == database_control.location():
                ErrorLogger.reportError(f'같은 장소의 데이터베이스 로딩 시도 ({database_control.location()})')
                return False
        self.__database_control_list.append(database_control)
        return True

    def removeDatabaseController(self, database_control: DatabaseMainController) -> None:
        try:
            if self.activeControllerManager().databaseController() == database_control:
                self.activeControllerManager().setDatabaseController(None)
                #StatusBarManager.setLabelConnection(False)
            self.__database_control_list.remove(database_control)
        except Exception as e:
            ErrorLogger.reportError(f'존재하지 않는 데이터베이스가 삭제 시도되었습니다.', AttributeError)

    def addRecordController(self, record_control: RecordMainController) -> bool:
        if len(self.__record_control_list) >= MainController.MAX_RECORD:
            ErrorLogger.reportError(f'데이터베이스를 {MainController.MAX_RECORD}개 이상 로드할 수 없습니다.')
            return False
        for control_iter in self.__record_control_list:
            if (control_iter.recordDate(), control_iter.location()) == (record_control.recordDate(), record_control.location()):
                ErrorLogger.reportError(f'중복된 기록부 로딩 시도\n'
                                        f'장소: {record_control.recordDate()}, 날짜: {record_control.location()}')
                return False
        self.__record_control_list.append(record_control)
        return True

    def removeRecordController(self, record_control: RecordMainController) -> None:
        try:
            if self.activeControllerManager().recordController() == record_control:
                self.activeControllerManager().setRecordController(None)
                #StatusBarManager.setLabelConnection(False)
            self.__record_control_list.remove(record_control)
        except Exception as e:
            ErrorLogger.reportError(f'존재하지 않는 기록부가 삭제 시도되었습니다.', AttributeError)

    def setActiveDatabase(self, database_control: DatabaseMainController) -> None:
        if database_control and self.activeControllerManager().databaseController() != database_control:
            if self.activeControllerManager().databaseController():
                self.activeControllerManager().databaseController().Stop()
            self.activeControllerManager().setDatabaseController(database_control)
            self.activeControllerManager().connectController()
            database_control.Run()
            # if self.activeControllerManager().connectController() is True:
            #     StatusBarManager.setLabelConnection(True)
            # else:
            #     StatusBarManager.setLabelConnection(False)

    def setActiveRecord(self, record_control: RecordMainController) -> None:
        if record_control and self.activeControllerManager().recordController() != record_control:
            if self.activeControllerManager().recordController():
                self.activeControllerManager().recordController().Stop()
            self.activeControllerManager().setRecordController(record_control)
            self.activeControllerManager().connectController()
            record_control.Run()
            # if self.activeControllerManager().connectController() is True:
            #     StatusBarManager.setLabelConnection(True)
            # else:
            #     StatusBarManager.setLabelConnection(False)

    def openDatabaseFile(self, location_string: str) -> Optional[DatabaseMainController]:
        table_model= DatabaseModel(location_string)
        view = DatabaseMainView(table_model)
        new_database_control = DatabaseMainController(table_model, view)
        if self.addDatabaseController(new_database_control):
            self.view().addDatabaseTab(new_database_control.view())
            self.view().tabWidget().setCurrentIndex(0)
            return new_database_control
        else:
            return None

    @MyPyqtSlot()
    def closeDatabase(self) -> None:
        pass

    def openRecordFile(self, record_file_name: str) -> Optional[RecordMainController]:
        extension = '.rcd'
        directory, file_name = '\\'.join(record_file_name.split('/')[:-1]), record_file_name.split('/').pop(-1)
        file_name_split = file_name.split('_')
        location_string = file_name_split[0] + ' ' + file_name_split[1]
        date_string = file_name_split[3].replace(extension, '')

        table_model = RecordTableModel(location_string, date_string, load=False)
        table_model.setDirectory(directory)
        table_model.load()
        view = RecordMainView(table_model)
        new_record_control = RecordMainController(table_model, view)
        if self.addRecordController(new_record_control) is True:
            self.view().addRecordTab(new_record_control.view())
            self.view().tabWidget().setCurrentIndex(self.__view.tabWidget().count() - 1)
            return new_record_control
        else:
            return None

    @MyPyqtSlot(str)
    def closeRecord(self, date_string: str) -> None:
        if date_string in self.control_dict.keys():
            del self.control_dict[date_string]
            self.active_date = None
            self.record_control = None
            self.hub_control = None

    def eventFilter(self, widget: 'QObject', event: 'QEvent') -> bool:
        if isinstance(widget, QWindow):
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Control:
                    # todo: focus widget으로 qlineedit일 때, ctrl c를 허용? 어떤 방법을 사용할지 고민
                    # todo: table이 아닌, 근무자 등의 다른 창을 보고 있을 때 ctrl c를 어떻게 허용할 지 고민하는 중 (옵션 등에서)
                    #print(QApplication.activeWindow().focusWidget()) 
                    print('ShortCutMode: active view -', self.activeView())
                    ShortCutManager.runManager(self.activeView())
                    #ShortCutManager.instance().getSignalSet().ShortCutFinished.connect(ShortCutManager.instance().releaseKeyboard)
                    return True
            elif event.type() == QEvent.KeyRelease:
                if event.key() == Qt.Key_Control:
                    print('FinishShortCutMode')
                    ShortCutManager.stopManager()
                    return True
        return QApplication.eventFilter(QApplication.instance(), widget, event)
