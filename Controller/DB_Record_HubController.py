from Controller.Database.DatabaseController import *
from Controller.Record.RecordController import *

from Utility.CommandManager import *
from Model.Command.ConcreteCommand.Model import Model


class DB_Record_HubController(QObject):
    def __init__(self, db_control: DatabaseController,  record_control: RecordController):
        super().__init__()

        self.database_control = db_control
        self.database_model = self.database_control.control_table.model
        self.database_view = self.database_control.view

        self.record_control = record_control
        self.record_model = self.record_control.control_table.model
        self.record_view = self.record_control.view

    def Run(self):
        self.record_view.record_table.getSignalSet().FindDatabaseRequest.connect(self.findDatabaseRequest)
        self.record_control.getSignalSet().WriteDatabaseRequest.connect(self.writeDatabaseRequest)

    def Stop(self):
        self.record_view.record_table.getSignalSet().FindDatabaseRequest.disconnect(self.findDatabaseRequest)
        self.record_control.getSignalSet().WriteDatabaseRequest.disconnect(self.writeDatabaseRequest)

    @pyqtSlot(dict)
    def findDatabaseRequest(self, property_dict: Dict[str, str]):
        if property_dict:
            visitor_list = self.database_model.findData(property_dict)
        else:
            visitor_list = []
        self.record_view.search_table.setModel(visitor_list)

        record_table_view = self.record_control.control_table.view
        current_row = record_table_view.currentRow()
        current_row_type = record_table_view.rowType(current_row)
        current_row_id_text = record_table_view.item(current_row, record_table_view.fieldColumn('고유번호')).text()

        if len(visitor_list) == 1 and current_row_id_text == RecordModel.DefaultString:
            if current_row_type in [RecordTableView.Option.Row.Basic, RecordTableView.Option.Row.NotInserted]:
                self.record_view.search_table.myCellDoubleClicked(0, 0)  # auto double click: auto fill the blank
    
    # Todo: 깔끔히 정리하기
    @pyqtSlot(RecordModel)
    def writeDatabaseRequest(self, record: RecordModel):
        update_dict = {}
        for field_name in RecordFieldModelConfig.getFieldList():
            if RecordFieldModelConfig.getOption(field_name, 'writing_field') == True:
                update_dict[field_name] = record.getProperty(field_name)

        update_dict['최근출입날짜'] = Clock.getDate().toString('yyyy-MM-dd')
        if update_dict['고유번호'] == RecordModel.IdDefaultString:
            update_dict['고유번호'] = RecordModel.DefaultString
        #     id = RecordModel.DefaultString
        # else:
        #     id = update_dict['고유번호']
        find_visitor = self.database_model.findData({'고유번호': update_dict['고유번호']})

        if find_visitor:
            if len(find_visitor) != 1:
                ErrorLogger.reportError(f'고유번호 중복: 해당 번호 - {update_dict["고유번호"]}')
                return
            idx = self.database_model.getDataIndex(find_visitor[0])
            CommandManager.postCommand(Model.ChangeModelCommand(self.database_model, idx, update_dict))
            #find_visitor[0].changeProperties(property_dict)
        else:
            update_dict['최초출입날짜'] = ''
            self.database_control.control_table.addNewVisitorRequest(update_dict)
            CommandManager.postCommand(ExecCommand())  # 추가된 데이터의 index를 알기 위해서 일단 exec함
            record_idx = self.record_model.getDataIndex(record)
            new_idx = self.database_model.getDataCount() - 1
            new_id_dict = {'고유번호': self.database_model.getData(new_idx).getProperty('고유번호')}
            CommandManager.postCommand(Model.ChangeModelCommand(self.record_model, record_idx, new_id_dict))