from Controller.Database.DatabaseMainController import *
from Controller.Record.RecordMainController import *

from Controller.AbstractController import *


class DB_Record_HubController(AbstractController):
    def __init__(self, db_control: DatabaseMainController, record_control: RecordMainController):
        super().__init__()

        self.database_control = db_control
        self.database_model = self.database_control.control_table.model()
        self.database_view = self.database_control.view()

        self.record_control = record_control
        self.record_model = self.record_control.control_table.model()
        self.record_view = self.record_control.view()

    """
    property
    * model
    * view
    """
    def model(self) -> None:
        return None

    def view(self) -> None:
        return None

    """
    method
    * Run, Stop  (override)
    """
    def Run(self):
        self._connectSignal(self.record_view.record_table.getSignalSet().FindDatabaseRequest, self.findDatabaseRequest)
        self._connectSignal(self.record_control.getSignalSet().WriteDatabaseRequest, self.writeDatabaseRequest)

    def Stop(self):
        super().Stop()

    """
    slot
    * findDatabase
    * writeDatabase
    """
    @MyPyqtSlot(dict)
    def findDatabaseRequest(self, property_dict: Dict[str, str]):
        if property_dict:
            visitor_list = self.database_model.findData(property_dict)
        else:
            visitor_list = []
        self.record_view.search_table.setModel(visitor_list)

        record_table_view = self.record_control.control_table.view()
        current_row= record_table_view.currentRow()
        current_row_type = record_table_view.rowType(current_row)
        current_row_id_text = record_table_view.item(current_row, record_table_view.fieldColumn('고유번호')).text()
        is_match_count_only_one = len(visitor_list) == 1
        is_current_id_default = (current_row_id_text == RecordModel.DefaultString)
        is_current_row_white = current_row_type in [RecordTableView.Option.Row.Basic, RecordTableView.Option.Row.NotInserted]

        if is_match_count_only_one and is_current_id_default and is_current_row_white:
            self.record_view.search_table.myCellDoubleClicked(0, 0)  # auto double click: auto fill the blank
    
    # Todo: 속도 개선하고 깔끔하게 정리하기.
    @MyPyqtSlot(list)
    def writeDatabaseRequest(self, record_list: List[RecordModel]):
        self.database_model.setAutoSave(False)
        try:
            for record_iter in record_list:
                update_dict = {}
                for field_name in RecordFieldModelConfig.getFieldList():
                    if RecordFieldModelConfig.getOption(field_name, 'writing_field') is True:
                        update_dict[field_name] = record_iter.getProperty(field_name)
                update_dict['최근출입날짜'] = datetime.strptime(self.record_model.getRecordDate(), '%y%m%d').strftime('%Y-%m-%d')
                if update_dict['고유번호'] == RecordModel.IdDefaultString:
                    update_dict['고유번호'] = RecordModel.DefaultString
                find_visitor = self.database_model.findData({'고유번호': update_dict['고유번호']})

                if len(find_visitor) == 0:
                    update_dict['최초출입날짜'] = ''
                    self.database_control.control_table.addNewVisitorRequest(update_dict)
                    CommandManager.postCommand(ExecCommand())  # 추가된 데이터의 index를 알기 위해서 일단 exec함
                    record_idx = self.record_model.getDataIndex(record_iter)
                    new_idx = self.database_model.getDataCount() - 1
                    new_id_dict = {'고유번호': self.database_model.getData(new_idx).getProperty('고유번호')}
                    CommandManager.postCommand(Model.ChangeModelCommand(self.record_model, record_idx, new_id_dict))
                elif len(find_visitor) == 1:
                    idx = self.database_model.getDataIndex(find_visitor[0])
                    CommandManager.postCommand(Model.ChangeModelCommand(self.database_model, idx, update_dict))
                else:
                    ErrorLogger.reportError(f'고유번호 중복: {update_dict["고유번호"]}\n'
                                            f'데이터베이스에서 해당 번호를 수정해 주세요.')
            CommandManager.addEndFunction(lambda: self.database_model.setAutoSave(True))  # todo 최근 수정함! 오토세이브
            CommandManager.addEndFunction(lambda: self.database_model.save())
        except Exception as e:
            self.database_model.setAutoSave(True)
            raise e

