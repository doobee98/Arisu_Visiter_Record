from View.Record.RecordMainView import *
from Controller.Record.RecordTableController import *
from View.Dialog.DeliveryDialog import *
from View.Dialog.SearchDialog import *
import subprocess

"""
RecordMainController
"""


class RecordMainControllerSignal(QObject):
    RecordTableController_FindDatabaseRequest = pyqtSignal(dict)
    RecordTableController_UpdateDatabaseRequest = pyqtSignal(list)
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class RecordMainController(QObject):
    def __init__(self, view: RecordMainView, parent: QObject = None):
        super().__init__(parent)
        self.__signal_set = RecordMainControllerSignal(self)
        self.__view = view
        self.__table_controller = RecordTableController(view.recordTableView(), self)
        self.__delivery_dialog = DeliveryDialog(DeliveryModel(self.__view.location()))
        self.__search_dialog = SearchDialog(self.tableController().view())

        # controller signal
        self.tableController().signalSet().FindDatabaseRequest.connect(lambda dic: self.signalSet().RecordTableController_FindDatabaseRequest.emit(dic))

        # tableModel signal
        self.tableController().model().signalSet().ItemChanged.connect(lambda: self.modelCountChanged())
        self.tableController().model().signalSet().ItemRemoved.connect(lambda: self.modelCountChanged())
        self.tableController().model().signalSet().ItemInserted.connect(lambda: self.modelCountChanged())

        # tableView signal
        self.view().signalSet().MatchTableView_RowDoubleClicked.connect(CommandSlot(self.rowDoubleClicked))  # todo Exec이 아닌 End로 해도 괜찮을까
        self.view().signalSet().ArriveView_ArriveButtonClicked.connect(CommandSlot(self.arriveButtonClicked))
        self.view().signalSet().LeaveView_LeaveButtonClicked.connect(CommandSlot(self.leaveButtonClicked))
        self.view().signalSet().ScrollView_ScrollButtonClicked.connect(CommandSlot(self.scrollButtonClicked, end_command=ExecCommand()))
        self.view().signalSet().TakeoverView_TakeoverButtonClicked.connect(CommandSlot(self.takeoverButtonClicked))
        self.view().signalSet().TakeoverView_DeliveryButtonClicked.connect(lambda: self.__delivery_dialog.exec_())
        self.view().signalSet().FunctionView_SearchButtonClicked.connect(lambda: self.__search_dialog.exec_())  # todo
        self.view().signalSet().FunctionView_ReportButtonClicked.connect(lambda: self.reportButtonClicked())   # todo

        self.__search_dialog.signalSet().SearchButtonClicked.connect(self.startSearch)
        self.__search_dialog.signalSet().BeforeButtonClicked.connect(self.beforeSearch)
        self.__search_dialog.signalSet().NextButtonClicked.connect(self.nextSearch)
        self.__search_dialog.signalSet().FinishButtonClicked.connect(self.finishSearch)

        self.tableController().start()

    """
    property
    * signalSet
    * view
    * tableController
    * deliveryDialog, searchDialog
    """
    def signalSet(self) -> RecordMainControllerSignal:
        return self.__signal_set

    def view(self) -> RecordMainView:
        return self.__view

    def tableController(self) -> RecordTableController:
        return self.__table_controller

    def deliveryDialog(self) -> DeliveryDialog:
        return self.__delivery_dialog

    def searchDialog(self) -> SearchDialog:
        return self.__search_dialog

    """
    method
    * start, stop
    """
    def start(self) -> None:
        self.blockSignals(False)
        # self.tableController().start()

    def stop(self) -> None:
        self.blockSignals(True)
        # self.tableController().stop()

    """
    model slot
    * modelCountChanged
    """
    @MyPyqtSlot()
    def modelCountChanged(self) -> None:
        inserted_count = 0
        for item_iter in self.tableController().model().itemList():
            if item_iter.state() == RecordModel.State.Inserted:
                inserted_count += 1
        self.view().titleView().setRemainCount(inserted_count)

    """
    view slot
    * rowDoubleClicked
    * arriveButtonClicked
    * leaveButtonClicked
    * scrollButtonClicked
    * takeoverButtonClicked
    * deliveryButtonClicked
    * searchButtonClicked
    * reportButtonClicked
    """
    @MyPyqtSlot(int)
    def rowDoubleClicked(self, row: int) -> None:
        record_table_view, match_table_view = self.tableController().view(), self.view().matchTableView()
        current_row = record_table_view.currentRow()
        if record_table_view.isRowWritable(current_row):
            if match_table_view.rowType(row) == MatchTableView.RowType.Dummy:
                match_table_text_dict = {field_name_iter: RecordModel.DefaultValue
                                         for field_name_iter in match_table_view.fieldNameList()}
                # 이름은 그대로
                match_table_text_dict[TableFieldOption.Necessary.NAME] = record_table_view.fieldText(current_row, TableFieldOption.Necessary.NAME)
                match_table_text_dict[TableFieldOption.Necessary.ID] = RecordModel.IdDefaultValue
            else:
                id_text = record_table_view.fieldText(current_row, TableFieldOption.Necessary.ID)
                if id_text == RecordModel.IdOverlapValue or id_text == RecordModel.DefaultValue:
                    match_table_text_dict = match_table_view.rowTextDictionary(row)
                    delete_field_name_list = []
                    for field_name_iter in match_table_text_dict.keys():
                        is_id_field = field_name_iter == TableFieldOption.Necessary.ID
                        is_key_field = ConfigModule.TableField.fieldModel(field_name_iter).globalOption(TableFieldOption.Global.Key)
                        if is_id_field or is_key_field:
                            continue
                        if record_table_view.fieldText(current_row, field_name_iter) != RecordModel.DefaultValue:
                            delete_field_name_list.append(field_name_iter)
                    for field_name_iter in delete_field_name_list:
                        del match_table_text_dict[field_name_iter]
                else:
                    ErrorLogger.reportError('이미 고유번호가 입력되었거나 신규로 지정된 행은\n덮어쓸 수 없습니다.\n'
                                            'X 버튼을 눌러 삭제한 후 새로 입력해 주세요.')
                    return
            CommandManager.postCommand(View.SetRowTextsCommand(record_table_view, current_row, match_table_text_dict))
            CommandManager.postCommand(View.MyRenderRowCommand(record_table_view, current_row), priority=CommandPriority.Low)
        else:
            ErrorLogger.reportError('수정할 수 없는 행입니다.\nX 버튼을 눌러 삭제한 후 새로 입력해 주세요.')
            return

    @MyPyqtSlot()
    def arriveButtonClicked(self) -> None:
        table_model, table_view = self.tableController().model(), self.tableController().view()
        in_time, in_worker = ClockModule.time().toString('hh:mm'), self.view().currentWorkerView().currentWorkerText()
        key_field_name_list = [field_model_iter.name() for field_model_iter in table_view.fieldModelList()
                               if field_model_iter.globalOption(TableFieldOption.Global.Key) is True]
        table_model.setAutoSave(False)
        try:
            change_list = []
            for row_iter in range(table_view.rowCount()):
                is_row_type_basic = table_view.rowType(row_iter) == RecordTableView.RowType.Basic
                has_key_fields = all([table_view.fieldText(row_iter, field_name_iter) for field_name_iter in key_field_name_list])
                if is_row_type_basic and has_key_fields:
                    changed = True
                    row_text_dict = table_view.rowTextDictionary(row_iter)
                    row_text_dict[TableFieldOption.Necessary.IN_TIME] = in_time
                    row_text_dict[TableFieldOption.Necessary.IN_WORKER] = in_worker
                    if row_text_dict[TableFieldOption.Necessary.ID] == RecordModel.DefaultValue:
                        row_text_dict[TableFieldOption.Necessary.ID] = RecordModel.IdDefaultValue
                    CommandManager.postCommand(View.ClearRowTextCommand(table_view, row_iter))
                    if row_iter < table_model.itemCount():
                        change_list.append(Model.ChangeItemCommand(table_model, row_iter, row_text_dict))
                    else:
                        change_list.append(Model.AddItemCommand(table_model, row_text_dict))
            for change_command_iter in change_list:
                CommandManager.postCommand(change_command_iter)
            CommandManager.addEndFunction(lambda: table_model.setAutoSave(True))
            CommandManager.addEndFunction(lambda: table_model.save())
            if change_list:
                self.scrollButtonClicked()
        except Exception as e:
            table_model.setAutoSave(True)
            raise e

    @MyPyqtSlot()
    def leaveButtonClicked(self) -> None:
        table_model, table_view = self.tableController().model(), self.tableController().view()
        out_time, out_worker = ClockModule.time().toString('hh:mm'), self.view().currentWorkerView().currentWorkerText()
        out_record_id, out_name = self.view().leaveView().recordIdText(), self.view().leaveView().nameText()
        out_record_index_list = []
        table_model.setAutoSave(False)
        try:
            for row_iter in range(table_model.itemCount()):
                item_model_iter = table_model.item(row_iter)
                is_state_inserted = item_model_iter.state() == RecordModel.State.Inserted
                is_record_id_match = out_record_id == item_model_iter.fieldData(TableFieldOption.Necessary.RECORD_ID)
                is_name_match = True if out_name == LeaveView.DefaultNameAll else out_name == item_model_iter.fieldData(TableFieldOption.Necessary.NAME)
                if is_state_inserted and is_record_id_match and is_name_match:
                    out_record_index_list.append(row_iter)
                    out_data_dict = {}
                    out_data_dict[TableFieldOption.Necessary.OUT_TIME] = out_time
                    out_data_dict[TableFieldOption.Necessary.OUT_WORKER] = out_worker
                    CommandManager.postCommand(Model.ChangeItemCommand(table_model, row_iter, out_data_dict))
            if out_record_index_list:
                self.signalSet().RecordTableController_UpdateDatabaseRequest.emit(out_record_index_list)
                CommandManager.postCommand(View.FocusCellCommand(table_view, out_record_index_list[-1], 1))
                self.view().leaveView().setDefault()
            else:
                ErrorLogger.reportError(f'출입증번호: {out_record_id} / 성명: {out_name}\n'
                                        '해당하는 데이터가 기록부에 존재하지 않습니다.')
            CommandManager.addEndFunction(lambda: table_model.setAutoSave(True))
            CommandManager.addEndFunction(lambda: table_model.save())
        except Exception as e:
            table_model.setAutoSave(True)
            raise e

    @MyPyqtSlot()
    def scrollButtonClicked(self) -> None:
        table_view = self.tableController().view()
        row = self.tableController().model().itemCount()
        column = min([table_view.fieldColumn(field_model_iter.name()) for field_model_iter in table_view.fieldModelList()
                      if not field_model_iter.globalOption(TableFieldOption.Global.NoModelData)])
        if row != table_view.currentRow() or column != table_view.currentColumn():
            CommandManager.postCommand(View.FocusCellCommand(table_view, row, column))
        else:
            table_view.setFocus()  # todo Command로?

    @MyPyqtSlot()
    def takeoverButtonClicked(self) -> None:
        table_model, table_view = self.tableController().model(), self.tableController().view()
        time = self.view().takeoverView().timeText()
        team = self.view().takeoverView().teamText()
        worker = self.view().takeoverView().workerText()
        name, name_count = None, 0
        takeover_index = 0
        for item_iter in table_model.itemList():
            in_time_iter = item_iter.fieldData(TableFieldOption.Necessary.IN_TIME)
            out_time_iter = item_iter.fieldData(TableFieldOption.Necessary.OUT_TIME)
            in_time_check = in_time_iter and in_time_iter < time
            out_time_check = (not out_time_iter) or out_time_iter >= time
            if in_time_check:
                takeover_index += 1
                if out_time_check:
                    if item_iter.state() != RecordModel.State.Takeover:
                        name_count += 1
                        if not name:
                            name = item_iter.fieldData(TableFieldOption.Necessary.NAME)
            else:
                break

        takeover_record = RecordModel.createTakeoverRecord(time, team, worker, name, name_count)
        takeover_string = takeover_record.fieldData(TableFieldOption.Necessary.TAKEOVER)
        delivery_string = self.__delivery_dialog.text_edit.toPlainText()

        message_string = '인수인계\n'
        message_string += takeover_string + '\n\n'
        message_string += '전달사항\n'
        message_string += delivery_string + '\n'

        reply = MyMessageBox.question(self.view(), '확인', message_string)
        if reply != MyMessageBox.Yes:
            return
        else:
            CommandManager.postCommand(Model.InsertItemCommand(table_model, takeover_index, takeover_record))
            # todo -- 비고 란으로서 RECORD_ID을 사용함
            CommandManager.postCommand(Model.ChangeItemCommand(table_model, takeover_index, {TableFieldOption.Necessary.RECORD_ID: delivery_string}))
            self.view().currentWorkerView().setCurrentWorkerText(worker)

    @MyPyqtSlot()
    def reportButtonClicked(self) -> None:
        try:
            StatusBarManager.setMessage('엑셀 마감 파일 생성 중')
            subprocess.run([DefaultFilePath.ExcelExportEXE, self.tableController().model().filePath()], check=True)
            MyMessageBox.information(self.view(), '알림', '마감 파일이 생성되었습니다.')
        except Exception as e:
            ErrorLogger.reportError('마감 파일 생성중 오류가 발생했습니다.\n'
                                    f'{DefaultFilePath.ExcelExportEXE} 파일이 존재하는지 확인해 주세요.')
        StatusBarManager.setIdleStatus()

    """
    searchSlot
    * startSearch
    * beforeSearch, nextSearch
    * finishSearch
    """
    @MyPyqtSlot(dict)
    def startSearch(self, find_func_dict: Dict[str, Callable[[str], bool]]) -> None:
        table_view = self.tableController().view()
        match_row_list = []
        for row_iter in range(table_view.rowCount()):
            if table_view.rowType(row_iter) in [RecordTableView.RowType.Takeover]:
                continue
            row_text_dict = table_view.rowTextDictionary(row_iter)
            match_flag = True
            for field_iter, func_iter in find_func_dict.items():
                if row_text_dict.get(field_iter):
                    if func_iter(row_text_dict[field_iter]):
                        continue
                match_flag = False
                break
            if match_flag:
                match_row_list.append(row_iter)

        if match_row_list:
            table_view.setHighLightRowList(match_row_list)
            for match_row_iter in match_row_list:
                table_view.myRenderRow(match_row_iter)
            table_view.selectRow(match_row_list[0])

    @MyPyqtSlot()
    def beforeSearch(self) -> None:
        table_view = self.tableController().view()
        current_row = table_view.currentRow()
        highlight_row_list = table_view.highLightRowList()
        if current_row is not None and highlight_row_list:
            row_iter = current_row - 1
            while row_iter not in highlight_row_list:
                row_iter = (row_iter - 1) if row_iter >= 0 else table_view.rowCount() - 1
            table_view.selectRow(row_iter)

    @MyPyqtSlot()
    def nextSearch(self) -> None:
        table_view = self.tableController().view()
        current_row = table_view.currentRow()
        highlight_row_list = table_view.highLightRowList()
        if current_row is not None and highlight_row_list:
            row_iter = current_row + 1
            while row_iter not in highlight_row_list:
                row_iter = (row_iter + 1) if row_iter < table_view.rowCount() else 0
            table_view.selectRow(row_iter)

    @MyPyqtSlot()
    def finishSearch(self) -> None:
        table_view = self.tableController().view()
        highlight_row_list = table_view.highLightRowList()
        table_view.setHighLightRowList([])
        for row_iter in highlight_row_list:
            table_view.myRenderRow(row_iter)
