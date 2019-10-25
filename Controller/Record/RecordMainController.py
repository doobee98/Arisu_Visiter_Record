from View.Record.RecordMainView import *
from Controller.Record.RecordTableController import *
from Utility.Abstract.View.MyMessageBox import *
from Controller.AbstractController import *


class RecordMainControllerSignal(QObject):
    WriteDatabaseRequest = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)


class RecordMainController(AbstractController):
    def __init__(self, table_model: RecordTableModel, view: RecordMainView):
        super().__init__()
        self.__signal_set = RecordMainControllerSignal(self)
        self.__connect_list: List[Tuple[pyqtSignal, Callable]] = []
        self.__model = None
        self.__view = view
        self.control_table = RecordTableController(table_model, self.view().record_table)

        self.__search_row_match_list: List[int] = []

    """
    property
    * signalSet
    * model (override)
    * view (override)
    * recordDate
    * location
    """
    def getSignalSet(self) -> RecordMainControllerSignal:
        return self.__signal_set

    def model(self) -> None:
        return None

    def view(self) -> RecordMainView:
        return self.__view

    def recordDate(self) -> str:
        return self.getRecordTableController().model().getRecordDate()

    def location(self) -> str:
        return self.getRecordTableController().model().getLocation()

    def getRecordTableController(self) -> RecordTableController:
        return self.control_table

    def __getSearchRowList(self) -> List[int]:
        return self.__search_row_match_list.copy()

    def __setSearchRowList(self, row_list: List[int]) -> None:
        self.__search_row_match_list = row_list

    """
    method
    * Run, Stop  (override)
    """
    def Run(self):
        self._connectSignal(self.control_table.model().getSignalSet().TableModelUpdated, self.tableModelUpdated)
        self._connectSignal(self.view().scroll_btn.getSignalSet().ScrollBtnClicked,
                            CommandSlot(self.scrollNextRequest, end_command=ExecCommand()))
        # 나가기가 실패했을 경우 EndCommand하지 않기 위해서 함수 내에서 직접 EndCommand를 처리함, 단 외부에서 호출하면 안됨.
        self._connectSignal(self.view().leave.getSignalSet().LeaveBtnClicked,
                            CommandSlot(self.leaveRecordRequest, end_command=None))
        self._connectSignal(self.view().arrive_btn.getSignalSet().ArriveBtnClicked, CommandSlot(self.arriveRequest))
        self._connectSignal(self.view().take_over.getSignalSet().TakeoverBtnClicked, CommandSlot(self.takeoverRequest))
        self._connectSignal(self.view().search_table.getSignalSet().WriteVisitorRequest,
                            CommandSlot(self.writeDataToRecordTableRequest, end_command=ExecCommand()))
        self._connectSignal(self.view().getSignalSet().UpdateDatabaseRequest, self.updateDatabase)
        self._connectSignal(self.view().search_dialog.getSignalSet().SearchTableRequest, self.searchRecordViewRequest)
        self._connectSignal(self.view().search_dialog.getSignalSet().BeforeSearchRequest, self.beforeSearchRequest)
        self._connectSignal(self.view().search_dialog.getSignalSet().NextSearchRequest, self.nextSearchRequest)
        self._connectSignal(self.view().search_dialog.getSignalSet().FinishSearchRequest, self.finishSearchRequest)

        self.control_table.Run()
        self.view().render()  # todo: 대체할 방법?

    def Stop(self):
        self.control_table.Stop()
        super().Stop()

    """
    slot
    """
    @MyPyqtSlot()
    def tableModelUpdated(self) -> None:
        current_count = 0
        for data_iter in self.control_table.model().getDataList():
            if data_iter.getState() == RecordModel.State.Inserted:
                current_count += 1
        self.view().remain_box.setCurrentVisitorNumber(current_count)

    @MyPyqtSlot()
    def scrollNextRequest(self) -> None:
        table_view = self.control_table.view()
        table_model = self.control_table.model()
        CommandManager.postCommand(View.Table.FocusCellCommand(table_view, table_model.getDataCount(), 1))

    @MyPyqtSlot(str, str)
    def leaveRecordRequest(self, visitor_num: str, visitor_name: str) -> None:
        if visitor_num == LeaveView.DefaultIDNumBlank:
            ErrorLogger.reportError('출입증 번호가 비어있습니다.')
            return

        now_time = QTime().currentTime().toString('hh:mm')
        now_worker = self.view().cur_worker.line.text()
        leave_property_dict = {
            '나가다시간': now_time,
            '나가다근무자': now_worker
        }
        matched_record_list = []
        for row in range(self.control_table.model().getDataCount()):
            record_model = self.control_table.model().getData(row)
            if record_model.getState() == RecordModel.State.Inserted:
                if visitor_num == record_model.getProperty('출입증번호'):
                    if visitor_name == LeaveView.DefaultNameAll or visitor_name == record_model.getProperty('성명'):
                        #is_matched = True
                        self.control_table.changeRecordRequest(row, leave_property_dict)
                        matched_record_list.append(self.control_table.model().getData(row))
                        #self.getSignalSet().WriteDatabaseRequest.emit(self.control_table.model().getData(row))
        # todo 속도 개선 위해 우선 change한 결과를 먼저 보여주는 방향으로 바꾸었음
        CommandManager.postCommand(ExecCommand())
        if matched_record_list:
            if Config.RecordOption.autoUpdateDB():
                self.getSignalSet().WriteDatabaseRequest.emit(matched_record_list)
            # todo 데이터베이스의 저장이 오래 걸림 - hub controller에서 작업하기
            CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'출입증번호: {visitor_num} / 성명: {visitor_name}\n'
                                    '해당하는 데이터가 기록부에 존재하지 않습니다.')
        self.view().leave.setLineEditsDefault()


    @MyPyqtSlot()
    def arriveRequest(self):
        # 입력되지 않은 데이터를 모두 레코드에 넣음
        def setArriveData(property_dict: Dict[str, Any]) -> Dict[str, Any]:
            copy_dict = property_dict
            copy_dict['들어오다시간'] = Clock.getTime().toString('hh:mm')
            copy_dict['들어오다근무자'] = self.view().cur_worker.line.text()
            if copy_dict.get('고유번호') == RecordModel.DefaultString:
                copy_dict['고유번호'] = RecordModel.IdDefaultString
            return copy_dict

        table_model = self.control_table.model()
        table_view = self.control_table.view()

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


    @MyPyqtSlot(str, str, str)
    def takeoverRequest(self, time: str, team: str, worker: str):
        time_idx, takeover_string = self.control_table.model().generateTakeoverInfo(time, team, worker)
        delivery_string = self.view().delivery_dialog.text_edit.toPlainText()

        message_string = '인수인계\n'
        message_string += takeover_string + '\n\n'
        message_string += '전달사항\n'
        message_string += delivery_string + '\n'

        reply = MyMessageBox.question(self.view(), '확인', message_string)
        if reply != MyMessageBox.Yes:
            return
        else:
            try:
                # todo: 아직도 default string 사용? recordmodel 생성자에서 사용하는 _adjustState때문에 필드가 존재해야함;
                takeover_property_dict = {field: RecordModel.DefaultString for field in
                                          RecordFieldModelConfig.getFieldList()}
                takeover_property_dict['인수인계'] = takeover_string
                takeover_property_dict['들어오다시간'] = time
                takeover_property_dict['들어오다근무자'] = worker
                takeover_property_dict['나가다시간'] = time
                takeover_property_dict['나가다근무자'] = worker
                takeover_property_dict['비고'] = delivery_string

                self.control_table.insertRecordRequest(time_idx, takeover_property_dict)

                # 현재근무자 텍스트를 교대자 이름으로 바꾸기
                self.view().cur_worker.line.setText(worker)
            except Exception as e:
                ErrorLogger.reportError('인수인계 도중 에러 발생', e)

    @MyPyqtSlot()
    def updateDatabase(self) -> None:
        table_model = self.control_table.model()
        record_list = list(filter(lambda data: not data.isTakeoverRecord(), table_model.getDataList()))
        self.getSignalSet().WriteDatabaseRequest.emit(record_list)
        CommandManager.postCommand(EndCommand())

    @MyPyqtSlot(dict)
    def writeDataToRecordTableRequest(self, property_dict: Dict[str, str]):
        """
        searchResultView에서 작성해달라는 요청을 받아 처리함
        현재 recordTableView의 currentRow가 작성 가능한 상태라면 작성함
        빈칸만 채워서 넣음
        """

        table_view = self.control_table.view()
        error_string: str = None
        if table_view.currentItem():
            current_row = table_view.currentRow()
            if table_view.isRowWritable(current_row):
                is_already_new_name_row = table_view.item(current_row, table_view.fieldColumn('고유번호')).text() == RecordModel.IdDefaultString
                if not is_already_new_name_row:
                    writing_data = {}
                    is_new_name_visitor = property_dict.get('고유번호') == RecordModel.IdDefaultString
                    for field_iter in property_dict.keys():
                        if field_iter in table_view.fieldList():
                            is_write_field = DatabaseFieldModelConfig.getOption(field_iter, 'writing_field') is True
                            is_empty_field = table_view.item(current_row, table_view.fieldColumn(field_iter)).text() == ''
                            if is_write_field and (is_new_name_visitor or is_empty_field):
                                writing_data[field_iter] = property_dict[field_iter]
                    CommandManager.postCommand(View.Table.SetRowTextCommand(table_view, current_row, writing_data))
                else:
                    error_string = '[* 신규 *] 행에서는 데이터베이스를 이용한 입력이 불가능합니다.\n'
                    error_string += 'X버튼을 눌러 데이터 삭제 후 다시 시도해 주세요.'
            else:
                error_string = '이미 데이터가 입력된 행입니다.'
        else:
            error_string = '현재 선택된 셀이 없습니다.'

        if error_string:
            ErrorLogger.reportError(error_string)

        # table_view = self.control_table.view()
        # if table_view.currentItem():
        #     if table_view.isRowWritable(table_view.currentRow()):
        #         writing_data = {}
        #         for field_iter in property_dict.keys():
        #             if DatabaseFieldModelConfig.getOption(field_iter, 'writing_field') is True:
        #                 writing_data[field_iter] = property_dict[field_iter]
        #         CommandManager.postCommand(View.Table.SetRowTextCommand(table_view, table_view.currentRow(), writing_data))
        #         birtyday_column = table_view.fieldColumn('생년월일')
        #         CommandManager.postCommand(View.Table.FocusCellCommand(table_view, table_view.currentRow(), birtyday_column))

    @MyPyqtSlot(dict)
    def searchRecordViewRequest(self, search_dict: Dict[str, str]) -> None:
        table_view = self.control_table.view()
        match_row_list = []
        for row_iter in range(table_view.rowCount()):
            if table_view.columnSpan(row_iter, 1) != 1:
                continue
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
            table_view.selectRow(match_row_list[0])
        #table_view.render()

    @MyPyqtSlot()
    def beforeSearchRequest(self) -> None:
        table_view = self.control_table.view()
        current_focus_row = table_view.currentRow()
        current_match_idx = self.__getSearchRowList().index(current_focus_row)

        if current_match_idx == 0:
            table_view.selectRow(self.__getSearchRowList()[-1])
        else:
            table_view.selectRow(self.__getSearchRowList()[current_match_idx - 1])


    @MyPyqtSlot()
    def nextSearchRequest(self) -> None:
        table_view = self.control_table.view()
        current_focus_row = table_view.currentRow()
        current_match_idx = self.__getSearchRowList().index(current_focus_row)

        if current_match_idx == len(self.__getSearchRowList()) - 1:
            table_view.selectRow(self.__getSearchRowList()[0])
        else:
            table_view.selectRow(self.__getSearchRowList()[current_match_idx + 1])

    @MyPyqtSlot()
    def finishSearchRequest(self) -> None:
        table_view = self.control_table.view()
        table_view.clearHighlight()
        self.__setSearchRowList([])
        table_view.render()


