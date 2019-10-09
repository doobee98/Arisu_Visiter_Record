from View.Record.RecordMainView import *
from Controller.Record.RecordTableController import *

from Utility.CommandManager import *
from Model.Command.ConcreteCommand.View import View


class RecordControllerSignal(QObject):
    WriteDatabaseRequest = pyqtSignal(RecordModel)

    def __init__(self, parent=None):
        super().__init__(parent)


class RecordController(QObject):
    def __init__(self, table_model: RecordTableModel, view: RecordMainView):
        super().__init__()
        self.__signal_set = RecordControllerSignal(self)
        self.__connect_list: List[Tuple[pyqtSignal, Callable]] = []
        #model = table_model
        self.view = view
        self.control_table = RecordTableController(table_model, self.view.record_table)

        self.__search_row_match_list: List[int] = []

    def __connect(self, signal: pyqtSignal, slot: Callable) -> None:
        signal.connect(slot)
        self.__connect_list.append((signal, slot))

    def Run(self):
        self.__connect(self.control_table.model.getSignalSet().TableModelUpdated, self.tableModelUpdated)
        self.__connect(self.view.scroll_btn.getSignalSet().ScrollBtnClicked, CommandSlot(self.scrollNextRequest, end_command=ExecCommand()))
        self.__connect(self.view.leave.getSignalSet().LeaveBtnClicked, CommandSlot(self.leaveRecordRequest))
        self.__connect(self.view.arrive_btn.getSignalSet().ArriveBtnClicked, CommandSlot(self.arriveRequest))
        self.__connect(self.view.take_over.getSignalSet().TakeOverBtnClicked, CommandSlot(self.takeOverRequest))
        self.__connect(self.view.search_table.getSignalSet().WriteVisitorRequest, CommandSlot(self.writeDataToRecordTableRequest, end_command=ExecCommand()))
        self.__connect(self.view.search_dialog.getSignalSet().SearchTableRequest, self.searchRecordViewRequest)
        self.__connect(self.view.search_dialog.getSignalSet().BeforeSearchRequest, self.beforeSearchRequest)
        self.__connect(self.view.search_dialog.getSignalSet().NextSearchRequest, self.nextSearchRequest)
        self.__connect(self.view.search_dialog.getSignalSet().FinishSearchRequest, self.finishSearchRequest)

        self.control_table.Run()
        self.view.render()  # todo: 대체할 방법?

    def Stop(self):
        # self.control_table.model.getSignalSet().TableModelUpdated.disconnect(self.tableModelUpdated)
        # self.view.scroll_btn.getSignalSet().ScrollBtnClicked.disconnect(CommandSlot(self.scrollNextRequest, end_command=ExecCommand()))
        # self.view.leave.getSignalSet().LeaveBtnClicked.disconnect(CommandSlot(self.leaveRecordRequest))
        # self.view.arrive_btn.getSignalSet().ArriveBtnClicked.disconnect(CommandSlot(self.arriveRequest))
        # self.view.take_over.getSignalSet().TakeOverBtnClicked.disconnect(CommandSlot(self.takeOverRequest))
        # self.view.search_table.getSignalSet().WriteVisitorRequest.disconnect(CommandSlot(self.writeDataToRecordTableRequest, end_command=ExecCommand()))
        # self.view.search_dialog.getSignalSet().SearchTableRequest.disconnect(self.searchRecordViewRequest)
        # self.view.search_dialog.getSignalSet().BeforeSearchRequest.disconnect(self.beforeSearchRequest)
        # self.view.search_dialog.getSignalSet().NextSearchRequest.disconnect(self.nextSearchRequest)
        # self.view.search_dialog.getSignalSet().FinishSearchRequest.disconnect(self.finishSearchRequest)
        for signal, slot in self.__connect_list:
            signal.disconnect(slot)
        self.__connect_list.clear()

        self.control_table.Stop()

    def getSignalSet(self) -> RecordControllerSignal:
        return self.__signal_set

    def getRecordDate(self) -> str:
        return self.getRecordTableController().getTableModel().getRecordDate()

    def getRecordTableController(self) -> RecordTableController:
        return self.control_table

    def __getSearchRowList(self) -> List[int]:
        return self.__search_row_match_list.copy()

    def __setSearchRowList(self, row_list: List[int]) -> None:
        self.__search_row_match_list = row_list

    # 슬롯
    @pyqtSlot()
    def tableModelUpdated(self) -> None:
        current_count = 0
        for data_iter in self.control_table.model.getDataList():
            if data_iter.getState() == RecordModel.State.Inserted:
                current_count += 1
        self.view.remain_box.setCurrentVisitorNumber(current_count)

    @pyqtSlot()
    def scrollNextRequest(self) -> None:
        table_view = self.control_table.view
        table_model = self.control_table.getTableModel()
        CommandManager.postCommand(View.Table.FocusCellCommand(table_view, table_model.getDataCount(), 1))
        #table_view.setFocusCell(table_model.getDataCount(), 1)

    @pyqtSlot(str, str)
    def leaveRecordRequest(self, visitor_num: str, visitor_name: str):
        if visitor_num == LeaveView.DefaultIDNumBlank:
            ErrorLogger.reportError('Blank ID Number')
            return

        now_time = QTime().currentTime().toString('hh:mm')
        now_worker = self.view.cur_worker.line.text()

        leave_property_dict = {
            '나가다시간': now_time,
            '나가다근무자': now_worker
        }

        for row in range(self.control_table.model.getDataCount()):
            record_model = self.control_table.model.getData(row)
            if record_model.getState() == RecordModel.State.Inserted:
                if visitor_num == record_model.getProperty('출입증번호'):
                    if visitor_name == LeaveView.DefaultNameAll or visitor_name == record_model.getProperty('성명'):
                        self.control_table.changeRecordRequest(row, leave_property_dict)
                        self.getSignalSet().WriteDatabaseRequest.emit(self.control_table.model.getData(row))

        self.view.leave.setLineEditsDefault()
        # if self.sender():
        #     print('leave')
        #     CommandManager.postCommand(EndCommand())

        # 존재하지 않는 번호, 성명 경우?

    @pyqtSlot()
    def arriveRequest(self):
        # 입력되지 않은 데이터를 모두 레코드에 넣음
        def setArriveData(property_dict: Dict[str, Any]) -> Dict[str, Any]:
            copy_dict = property_dict
            copy_dict['들어오다시간'] = Clock.getTime().toString('hh:mm')
            copy_dict['들어오다근무자'] = self.view.cur_worker.line.text()
            if copy_dict.get('고유번호') == RecordModel.DefaultString:
                copy_dict['고유번호'] = RecordModel.IdDefaultString
            return copy_dict

        table_model = self.control_table.model
        table_view = self.control_table.view

        for current_row in range(table_view.rowCount()):
            current_row_type = table_view.rowType(current_row)
            current_property_dict = table_view.getRowTexts(current_row)
            table_model_record_count = table_model.getDataCount()
            is_current_row_any_texts = table_view.isRowAnyTexts(current_row)

            if (current_row_type in [RecordTableView.Option.Row.Basic, RecordTableView.Option.Row.NotInserted]) \
                    and is_current_row_any_texts:
                change_dict = setArriveData(current_property_dict)  # custom method
                CommandManager.postCommand(View.Table.ClearRowTextCommand(table_view, current_row))
                if current_row < table_model_record_count:
                    self.control_table.changeRecordRequest(current_row, change_dict)
                else:
                    self.control_table.addRecordRequest(change_dict)
                CommandManager.postCommand(ExecCommand())
        #CommandManager.postCommand(View.Table.FocusCellCommand(table_view, table_model.getDataCount(), 1))


    @pyqtSlot(str, str, str)
    def takeOverRequest(self, time: str, team: str, worker: str):
        time_idx, takeover_string = self.control_table.model.generateTakeoverInfo(time, team, worker)
        # todo: 아직도 default string 사용? recordmodel 생성자에서 사용하는 _adjustState때문에 필드가 존재해야함;
        takeover_property_dict = {field: RecordModel.DefaultString for field in RecordFieldModelConfig.getFieldList()}
        takeover_property_dict['인수인계'] = takeover_string
        takeover_property_dict['들어오다시간'] = time
        takeover_property_dict['들어오다근무자'] = worker
        takeover_property_dict['나가다시간'] = time
        takeover_property_dict['나가다근무자'] = worker
        self.control_table.insertRecordRequest(time_idx, takeover_property_dict)

        # 현재근무자 텍스트를 교대자 이름으로 바꾸기
        self.view.cur_worker.line.setText(worker)

        #self.view.record_table.setFocusNextRow()

    @pyqtSlot(dict)
    def writeDataToRecordTableRequest(self, property_dict: Dict[str, str]):
        """
        searchResultView에서 작성해달라는 요청을 받아 처리함
        현재 recordTableView의 currentRow가 작성 가능한 상태라면 작성함
        """
        table_view = self.control_table.view
        if table_view.currentItem():
            if table_view.isRowWritable(table_view.currentRow()):
                writing_data = {}
                for field_iter in property_dict.keys():
                    if DatabaseFieldModelConfig.getOption(field_iter, 'writing_field') is True:
                        writing_data[field_iter] = property_dict[field_iter]
                CommandManager.postCommand(View.Table.SetRowTextCommand(table_view, table_view.currentRow(), writing_data))
                birtyday_column = table_view.fieldColumn('생년월일')
                CommandManager.postCommand(View.Table.FocusCellCommand(table_view, table_view.currentRow(), birtyday_column))
                #table_view.setRowTexts(table_view.currentRow(), writing_data)

    def __setTableCurrentCellNoFocus(self, row: int, column: int) -> None:
        table_view = self.control_table.view
        table_view.blockSignals(True)
        table_view.setCurrentCell(row, column)
        table_view.blockSignals(False)

    @pyqtSlot(dict)
    def searchRecordViewRequest(self, search_dict: Dict[str, str]) -> None:
        table_view = self.control_table.view
        match_row_list = []
        for row_iter in range(table_view.rowCount()):
            property_dict = table_view.getRowTexts(row_iter)
            match_flag = True
            for field_iter, property_iter in search_dict.items():
                if property_dict.get(field_iter):
                    if property_dict[field_iter].find(property_iter) != -1:
                        continue
                match_flag = False
                break
            if match_flag:
                match_row_list.append(row_iter)

        if match_row_list:
            self.__setSearchRowList(match_row_list)
            for match_row_iter in match_row_list:
                table_view.highlightRow(match_row_iter)
                table_view.renderRow(match_row_iter)
            #self.__setTableCurrentCellNoFocus(match_row_list[0], 1)
            table_view.selectRow(match_row_list[0])
        #table_view.render()

    @pyqtSlot()
    def beforeSearchRequest(self) -> None:
        table_view = self.control_table.view
        current_focus_row = table_view.currentRow()
        current_match_idx = self.__getSearchRowList().index(current_focus_row)

        if current_match_idx == 0:
            #self.__setTableCurrentCellNoFocus(self.__getSearchRowList()[-1], 1)
            table_view.selectRow(self.__getSearchRowList()[-1])
        else:
            #self.__setTableCurrentCellNoFocus(self.__getSearchRowList()[current_match_idx - 1], 1)
            table_view.selectRow(self.__getSearchRowList()[current_match_idx - 1])


    @pyqtSlot()
    def nextSearchRequest(self) -> None:
        table_view = self.control_table.view
        current_focus_row = table_view.currentRow()
        current_match_idx = self.__getSearchRowList().index(current_focus_row)

        if current_match_idx == len(self.__getSearchRowList()) - 1:
            #self.__setTableCurrentCellNoFocus(self.__getSearchRowList()[0], 1)
            table_view.selectRow(self.__getSearchRowList()[0])
        else:
            #self.__setTableCurrentCellNoFocus(self.__getSearchRowList()[current_match_idx + 1], 1)
            table_view.selectRow(self.__getSearchRowList()[current_match_idx + 1])

    @pyqtSlot()
    def finishSearchRequest(self) -> None:
        table_view = self.control_table.view
        table_view.clearHighlight()
        self.__setSearchRowList([])
        table_view.render()


