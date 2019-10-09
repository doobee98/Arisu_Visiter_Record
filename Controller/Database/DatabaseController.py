from Model.Database.DatabaseModel import *
from View.Database.DatabaseMainView import *
from Controller.Database.DatabaseTableController import *

class DatabaseController(QObject):
    def __init__(self, table_model: DatabaseModel, view: DatabaseMainView):
        super().__init__()
        model = table_model
        self.view = view
        self.control_table = DatabaseTableController(model, view.database_table)
        self.__search_row_match_list: List[int] = []

    def Run(self):
        self.view.filter.getSignalSet().AddNewVisitorRequest.connect(CommandSlot(self.addNewVisitorRequest))
        self.view.search_dialog.getSignalSet().SearchTableRequest.connect(self.searchRecordViewRequest)
        self.view.search_dialog.getSignalSet().BeforeSearchRequest.connect(self.beforeSearchRequest)
        self.view.search_dialog.getSignalSet().NextSearchRequest.connect(self.nextSearchRequest)
        self.view.search_dialog.getSignalSet().FinishSearchRequest.connect(self.finishSearchRequest)

        self.control_table.Run()

    def Stop(self):
        self.view.filter.getSignalSet().AddNewVisitorRequest.disconnect(CommandSlot(self.addNewVisitorRequest))
        self.view.search_dialog.getSignalSet().SearchTableRequest.disconnect(self.searchRecordViewRequest)
        self.view.search_dialog.getSignalSet().BeforeSearchRequest.disconnect(self.beforeSearchRequest)
        self.view.search_dialog.getSignalSet().NextSearchRequest.disconnect(self.nextSearchRequest)
        self.view.search_dialog.getSignalSet().FinishSearchRequest.disconnect(self.finishSearchRequest)

        self.control_table.Stop()

    def __getSearchRowList(self) -> List[int]:
        return self.__search_row_match_list.copy()

    def __setSearchRowList(self, row_list: List[int]) -> None:
        self.__search_row_match_list = row_list

    @pyqtSlot(dict)
    def addNewVisitorRequest(self, property_dict: Dict[str, str]):
        self.control_table.addNewVisitorRequest(property_dict)
        self.view.filter.table.clearTexts()

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
            table_view.selectRow(match_row_list[0])#setFocusCell(match_row_list[0], 1)
        #table_view.render()

    @pyqtSlot()
    def beforeSearchRequest(self) -> None:
        table_view = self.control_table.view
        current_focus_row = table_view.currentRow()
        current_match_idx = self.__getSearchRowList().index(current_focus_row)

        if current_match_idx == 0:
            print('맨앞')
        else:
            table_view.selectRow(self.__getSearchRowList()[current_match_idx - 1])#setFocusCell(self.__getSearchRowList()[current_match_idx - 1], 1)

    @pyqtSlot()
    def nextSearchRequest(self) -> None:
        table_view = self.control_table.view
        current_focus_row = table_view.currentRow()
        current_match_idx = self.__getSearchRowList().index(current_focus_row)

        if current_match_idx == len(self.__getSearchRowList()) - 1:
            print('맨뒤')
        else:
            table_view.selectRow(self.__getSearchRowList()[current_match_idx + 1]) #setFocusCell(self.__getSearchRowList()[current_match_idx + 1], 1)

    @pyqtSlot()
    def finishSearchRequest(self) -> None:
        table_view = self.control_table.view
        table_view.clearHighlight()
        self.__setSearchRowList([])
        table_view.render()