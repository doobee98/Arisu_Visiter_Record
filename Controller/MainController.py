from Controller.Record.RecordController import *
from Controller.Database.DatabaseController import *
from Controller.DB_Record_HubController import *
from Utility.File.LocationSettingDialog import *
from View.MainView import *
from Utility.ShortCutManager import *

# todo 런, 스탑 시스템 정리할것. 지금은 임시로 해둔 값들이 굉장히 많음
class MainController(QObject):
    def __init__(self):
        super().__init__()
        QApplication.instance().installEventFilter(self)
        self.model = None
        self.view = None

        self.active_date = None
        self.control_dict: Dict[str, Tuple[RecordController, DB_Record_HubController]] = {}
        self.record_control = None
        self.database_control = None
        self.hub_control = None

        self.__initializeSystem()
        #self.addRecordController(RecordController(today_string, self.view.record))

    def __initializeSystem(self) -> None:
        """
        module loading
        오늘날짜 기록부를 연다
        """
        Clock.start()
        if Config.TotalOption.location() is None:
            location_dialog = LocationSettingDialog()
            location_dialog.exec_()
        # todo 임시로 main_view의 렌더링을 늦춰서 location dialog를 통해 입력받은 location이 view에 반영되지 않는 점을 수정함.
        self.view = MainView()
        location_string = Config.TotalOption.location()
        today_string = Clock.getDate().toString('yyMMdd')
        self.active_date = today_string

        self.openDatabase(location_string)
        self.openRecord(location_string, today_string)

    def Run(self):
        self.view.getSignalSet().OpenDatabaseRequest.connect(self.openDatabase)
        self.view.getSignalSet().OpenRecordRequest.connect(self.openRecord)
        self.view.getSignalSet().CloseFileRequest.connect(self.closeRecord)
        self.view.getSignalSet().ChangeRecordTabSignal.connect(self.changeActiveRecordController)
        # BaseUI.getSignalSet().FontSizeChanged.connect(lambda a, b: self.Run()) 연결 방식 고민하기 stop후 run

        self.runDatabaseController()
        self.runActiveRecordController(self.active_date)
        self.view.render()
        #self.record_control.Run() # todo run을 빼는게 맞나? 아닌데...
        #self.hub_control.Run()

    def Stop(self):
        self.view.getSignalSet().OpenDatabaseRequest.disconnect(self.openDatabase)
        self.view.getSignalSet().OpenRecordRequest.disconnect(self.openRecord)
        self.view.getSignalSet().CloseFileRequest.disconnect(self.closeRecord)
        self.view.getSignalSet().ChangeRecordTabSignal.disconnect(self.changeActiveRecordController)
        # BaseUI.getSignalSet().FontSizeChanged.connect(lambda a, b: self.Run()) 연결 방식 고민하기 stop후 run

        self.record_control.Stop()
        self.database_control.Stop()
        self.hub_control.Stop()

    def activeView(self) -> QWidget:
        if not isinstance(QApplication.activeWindow(), ShowingView):
            ErrorLogger.reportError('Showing View(Window) not implement ShowingView')
        return QApplication.activeWindow().activeView()

    def runActiveRecordController(self, record_date: str) -> None:
        if self.database_control:
            if self.record_control != self.control_dict[record_date][0]:
                if self.record_control and self.hub_control:
                    print(self.record_control.getRecordDate())
                    self.record_control.Stop()
                    self.hub_control.Stop()
                print('Run', record_date)
                self.record_control = self.control_dict[record_date][0]
                self.hub_control = self.control_dict[record_date][1]
                self.active_date = record_date
                self.record_control.Run()
                self.hub_control.Run()

    def runDatabaseController(self):
        if self.database_control:
            self.database_control.Run()

    def addRecordController(self, record_control: RecordController) -> None:
        hub_control = DB_Record_HubController(self.database_control, record_control)
        self.control_dict[record_control.getRecordDate()] = (record_control, hub_control)

    def changeActiveRecordController(self, record_date: str) -> None:
        if self.active_date != record_date:
            self.runActiveRecordController(record_date)

    @pyqtSlot(str)
    def openDatabase(self, location_string: str) -> None:
        #self.Stop()
        self.database_control = self.__createDatabaseController(location_string)
        self.view.addDatabaseTab(self.database_control.view)
        self.view.tabWidget().setCurrentIndex(0)
        #self.runDatabaseController()
        #self.Run()

    @pyqtSlot()
    def closeDatabase(self) -> None:
        pass

    @pyqtSlot(str, str)
    def openRecord(self, location_string: str, date_string: str) -> None:
        if self.database_control == None:
            ErrorLogger.reportError('데이터베이스가 열려있지 않습니다.')
            return
        if date_string not in self.control_dict.keys():
            record_control = self.__createRecordController(location_string, date_string)
            self.view.addRecordTab(record_control.view)
            self.addRecordController(record_control)
            self.runActiveRecordController(date_string)
            self.view.tabWidget().setCurrentIndex(self.view.tabWidget().count() - 1)

    @pyqtSlot(str)
    def closeRecord(self, date_string: str) -> None:
        if date_string in self.control_dict.keys():
            del self.control_dict[date_string]
            self.active_date = None
            self.record_control = None
            self.hub_control = None

    def __createRecordController(self, location: str, record_date: str) -> RecordController:
        table_model = RecordTableModel(location, record_date)
        view = RecordMainView(table_model)
        return RecordController(table_model, view)

    def __createDatabaseController(self, location: str) -> DatabaseController:
        table_model = DatabaseModel(location)
        view = DatabaseMainView(table_model)
        return DatabaseController(table_model, view)

    @pyqtSlot()
    def connectStatusChanged(self):
        pass


    def eventFilter(self, widget: 'QObject', event: 'QEvent') -> bool:
        if isinstance(widget, QWindow):
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Control:
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


