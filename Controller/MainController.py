from Controller.Record.RecordMainController import *
from Controller.Database.DatabaseMainController import *
from View.MainView import *
from Utility.Manager.ShortCutManager import *
from View.Dialog.OptionDialog import *
from View.Dialog.LocationSettingDialog import *

"""
MainController
"""


class MainController(QObject):
    def __init__(self, view: MainView, parent: QObject = None):
        super().__init__(parent)
        QApplication.instance().installEventFilter(self)
        if ConfigModule.Application.location() is None:
            location_dialog = LocationSettingDialog()
            location_dialog.exec_()

        location, date = ConfigModule.Application.location(), ClockModule.date().toString('yyMMdd')
        open_record_func = lambda: self.openRecordFile(self.showFileFinderView(ConfigModule.FilePath.filePathExtension(FileType.RecordTable)))
        open_today_record_func = lambda: self.openRecordFile(ConfigModule.FilePath.recordTableFilePath(
            ConfigModule.Application.location(), ClockModule.date().toString('yyMMdd')
        ))
        self.__view = view
        self.__option_dialog = OptionDialog(self.__view)
        self.__database_controller: DatabaseMainController = None
        self.__record_controller_dictionary = {}

        self.__view.signalSet().CurrentRecordMainViewIndexChanged.connect(self.__currentRecordIndexChanged)  # todo
        self.__view.signalSet().RemoveRecordMainViewRequest.connect(self.__removeRecordMainView)
        self.__view.signalSet().OpenRecordRequest.connect(open_record_func)
        self.__view.signalSet().OpenRecordFileRequest.connect(lambda path: self.openRecordFile(path))
        self.__view.signalSet().OpenTodayRecordRequest.connect(open_today_record_func)
        self.__view.signalSet().UndoMenuTriggered.connect(lambda: CommandManager.undo())
        self.__view.signalSet().RedoMenuTriggered.connect(lambda: CommandManager.redo())
        self.__view.signalSet().OptionMenuTriggered.connect(lambda: self.__option_dialog.exec_())  # todo

        self.openDatabaseFile(ConfigModule.FilePath.databaseTableFilePath(location))
        self.openRecordFile(ConfigModule.FilePath.recordTableFilePath(location, date))
        self.__view.show()

    """
    property
    * view
    * databaseController
    * recordControllerDictionary
    """
    def view(self) -> MainView:
        return self.__view

    def databaseController(self) -> DatabaseMainController:
        return self.__database_controller

    def setDatabaseController(self, database_controller: DatabaseMainController) -> None:
        self.__database_controller = database_controller
        CompleterListModule.setDatabase(database_controller.tableController().view())

    def recordControllerDictionary(self) -> Dict[Tuple[str, str], RecordMainController]:
        return self.__record_controller_dictionary

    def addRecordController(self, record_controller: RecordMainController) -> None:
        location, date = record_controller.view().location(), record_controller.view().date()
        self.__record_controller_dictionary[(location, date)] = record_controller
        if location == self.databaseController().view().location():
            self.connectRecordController(record_controller)

    def removeRecordController(self, location: str, date: str) -> None:
        del self.__record_controller_dictionary[(location, date)]
        self.view().removeRecordMainView(self.view().recordMainView(location, date))

    """
    advanced property
    * recordController, currentRecordController
    * activeView
    """
    def recordController(self, location: str, date: str) -> RecordMainController:
        return self.recordControllerDictionary().get((location, date))

    def currentRecordController(self) -> RecordMainController:
        current_view = self.view().currentRecordMainView()
        return self.recordController(current_view.location(), current_view.date()) if current_view else None

    def activeView(self) -> QWidget:
        if not isinstance(QApplication.activeWindow(), ShowingView):
            ErrorLogger.reportError('Showing View(Window) not implement ShowingView', NotImplementedError)
        return QApplication.activeWindow().activeView()

    """
    method
    * start, stop
    * showFileFinderView
    * openDatabaseFile, openRecordFile
    * connectRecordController
    """
    def start(self) -> None:
        ClockModule.start()
        self.blockSignals(False)
        if self.databaseController():
            self.databaseController().start()
        if self.currentRecordController():
            self.currentRecordController().start()

    def stop(self) -> None:
        self.blockSignals(True)
        if self.databaseController():
            self.databaseController().stop()
        if self.currentRecordController():
            self.currentRecordController().stop()

    def showFileFinderView(self, extension: str) -> str:
        file_name = QFileDialog.getOpenFileName(self.view(), '파일 열기', DefaultFilePath.Record, '*' + extension)
        return file_name[0] if file_name[0] else None

    def openDatabaseFile(self, file_path: str) -> None:
        if file_path:
            [location] = ConfigModule.FilePath.fileNameToData(FileType.DatabaseTable, file_path)
            database_table_model = DatabaseTableModel(location)
            database_table_view = DatabaseTableView()
            database_table_view.setMyModel(database_table_model)
            database_table_view.myRender()
            database_main_view = DatabaseMainView(database_table_view)
            database_controller = DatabaseMainController(database_main_view)
            self.setDatabaseController(database_controller)
            self.view().setDatabaseMainView(database_main_view)

    def openRecordFile(self, file_path: str) -> None:
        if file_path:
            [location, date] = ConfigModule.FilePath.fileNameToData(FileType.RecordTable, file_path)
            if self.recordController(location, date) is not None:
                ErrorLogger.reportError(f'{location} / {date}\n중복된 기록부 로딩 시도')
                return
            record_table_model = RecordTableModel(file_path)
            record_table_view = RecordTableView()
            record_table_view.setMyModel(record_table_model)
            record_table_view.myRender()
            record_main_view = RecordMainView(record_table_view)
            record_controller = RecordMainController(record_main_view)
            self.addRecordController(record_controller)
            self.view().setRecordMainView(record_main_view)

    def connectRecordController(self, record_controller: RecordMainController) -> None:
        record_controller.signalSet().RecordTableController_FindDatabaseRequest.connect(self.__findDatabaseRequest)
        record_controller.signalSet().RecordTableController_UpdateDatabaseRequest.connect(self.__updateDatabaseRequest)
        #CompleterListModule.setRecordTable(record_controller.tableController().view())

    """
    view slot
    * __currentRecordMainViewChanged
    * __removeRecordMainView
    """
    @MyPyqtSlot(int, int)
    def __currentRecordIndexChanged(self, new_index: int, old_index: int) -> None:
        old_view: RecordMainView = self.view().tabWidget().widget(old_index)
        if old_view and self.recordController(old_view.location(), old_view.date()):
            self.recordController(old_view.location(), old_view.date()).stop()
        if new_index != -1:
            self.currentRecordController().start()
            CompleterListModule.setRecordTable(self.currentRecordController().tableController().view())
        else:
            CompleterListModule.setRecordTable(None)

    @MyPyqtSlot(int)
    def __removeRecordMainView(self, index: int) -> None:
        requested_record_view: RecordMainView = self.view().tabWidget().widget(index)
        location, date = requested_record_view.location(), requested_record_view.date()
        self.removeRecordController(location, date)
        if ConfigModule.Application.enableShortCut():
            ShortCutManager.removeShortCut(requested_record_view)

    """
    controller slot
    * __findDatabaseRequest
    * __updateDatabaseRequest
    """
    @MyPyqtSlot(dict)
    def __findDatabaseRequest(self, field_data_dict: Dict[str, str]) -> None:
        """
        1. 주어진 정보로 Database Table Model에서 해당 데이터를 찾고
        2. 그 데이터 리스트를 Match Table View에 보여줌
        """
        database_table_model = self.databaseController().tableController().model()
        record_table_view = self.currentRecordController().tableController().view()
        match_table_view = self.currentRecordController().view().matchTableView()
        if not field_data_dict:
            match_table_view.setMyModel([])
        else:
            match_visitor_list = database_table_model.findItems(field_data_dict)
            match_table_view.setMyModel(match_visitor_list)

            # AutoFill 또는 Overlap에 대한 처리
            current_row = record_table_view.currentRow()
            is_row_type_basic = record_table_view.rowType(current_row) == RecordTableView.RowType.Basic
            is_id_field_empty = record_table_view.fieldText(current_row, TableFieldOption.Necessary.ID) == RecordModel.DefaultValue
            if is_row_type_basic and is_id_field_empty:
                if len(match_visitor_list) == 1:
                    match_table_view.signalSet().RowDoubleClicked.emit(0)
                elif len(match_visitor_list) > 1:
                    current_row_text_dict = record_table_view.rowTextDictionary(current_row)
                    current_row_text_dict[TableFieldOption.Necessary.ID] = RecordModel.IdOverlapValue
                    CommandManager.postCommand(View.SetRowTextsCommand(record_table_view, current_row, current_row_text_dict))
                    CommandManager.postCommand(View.MyRenderRowCommand(record_table_view, current_row), priority=CommandPriority.Low)
                    CommandManager.postCommand(EndCommand())
                    record_table_view.closeEditItem(record_table_view.currentItem())  # todo 임시 땜빵
                    record_table_view.setFocus()

    @MyPyqtSlot(list)
    def __updateDatabaseRequest(self, record_index_list: List[int]) -> None:
        record_model = self.currentRecordController().tableController().model()
        database_model = self.databaseController().tableController().model()
        database_model.setAutoSave(False)
        try:
            update_field_name_list = [field_name_iter for field_name_iter in record_model.fieldNameList()
                                      if ConfigModule.TableField.fieldModel(field_name_iter).recordOption(TableFieldOption.Record.ShareOn)]
            for record_index_iter in record_index_list:
                record_item_iter = record_model.item(record_index_iter)
                update_dict = {field_name_iter: record_item_iter.fieldData(field_name_iter)
                               for field_name_iter in update_field_name_list}
                if update_dict[TableFieldOption.Necessary.ID] == RecordModel.IdDefaultValue:
                    update_dict[TableFieldOption.Necessary.ID] = RecordModel.DefaultValue
                else:
                    find_item_list = database_model.findItems({TableFieldOption.Necessary.ID: update_dict[TableFieldOption.Necessary.ID]})
                    if len(find_item_list) == 1:
                        update_dict[TableFieldOption.Necessary.DATE_RECENT] = ClockModule.date().toString('yyyy-MM-dd')
                        target_index = database_model.itemList().index(find_item_list[0])
                        CommandManager.postCommand(Model.ChangeItemCommand(database_model, target_index, update_dict))
                        continue
                    elif len(find_item_list) == 2:
                        ErrorLogger.reportError(f'고유번호 중복: {update_dict[TableFieldOption.Necessary.ID]}\n'
                                                f'데이터베이스에서 해당 번호를 수정해 주세요.')
                # 새로 추가하기
                CommandManager.postCommand(Model.AddItemCommand(database_model, update_dict))
                CommandManager.postCommand(ExecCommand())
                added_visitor = database_model.item(database_model.itemCount() - 1)
                new_id = added_visitor.fieldData(TableFieldOption.Necessary.ID)
                CommandManager.postCommand(Model.ChangeItemCommand(record_model, record_index_iter, {TableFieldOption.Necessary.ID: new_id}))
            CommandManager.addEndFunction(lambda: database_model.setAutoSave(True))
            CommandManager.addEndFunction(lambda: database_model.save())
        except Exception as e:
            database_model.setAutoSave(True)
            raise e

    """
    override
    * eventFilter
    """
    def eventFilter(self, widget: 'QObject', event: 'QEvent') -> bool:
        if ConfigModule.Application.enableShortCut():
            if isinstance(widget, QWindow):
                if event.type() == QEvent.KeyPress:
                    if event.key() == Qt.Key_Control:
                        # todo: focus widget으로 qlineedit일 때, ctrl c를 허용? 어떤 방법을 사용할지 고민
                        # todo: table이 아닌, 근무자 등의 다른 창을 보고 있을 때 ctrl c를 어떻게 허용할 지 고민하는 중 (옵션 등에서)
                        print('ShortCutMode: active view -', self.activeView())
                        ShortCutManager.runManager(self.activeView())
                        return True
                elif event.type() == QEvent.KeyRelease:
                    if event.key() == Qt.Key_Control:
                        print('FinishShortCutMode')
                        ShortCutManager.stopManager()
                        return True
        return QApplication.eventFilter(QApplication.instance(), widget, event)

