from Model.Database.DatabaseModel import *
from View.Database.DatabaseMainView import *
from Controller.Database.DatabaseTableController import *
from Controller.AbstractController import *


class DatabaseMainController(AbstractController):
    def __init__(self, table_model: DatabaseModel, view: DatabaseMainView):
        super().__init__()
        model = table_model
        self.__view = view
        self.control_table = DatabaseTableController(model, view.database_table)
        self.__search_row_match_list: List[int] = []

    """
    property
    * model (override)
    * view (override)
    * location
    """
    def model(self) -> None:
        return None

    def view(self) -> DatabaseMainView:
        return self.__view

    def location(self) -> str:
        return self.control_table.model().getLocation()

    def __getSearchRowList(self) -> List[int]:
        return self.__search_row_match_list.copy()

    def __setSearchRowList(self, row_list: List[int]) -> None:
        self.__search_row_match_list = row_list
    """
    method
    * Run, Stop  (override)
    """
    def Run(self):
        self._connectSignal(self.view().filter.getSignalSet().AddNewVisitorRequest, CommandSlot(self.addNewVisitorRequest))
        self._connectSignal(self.view().search_dialog.getSignalSet().SearchTableRequest, self.searchRecordViewRequest)
        self._connectSignal(self.view().search_dialog.getSignalSet().BeforeSearchRequest, self.beforeSearchRequest)
        self._connectSignal(self.view().search_dialog.getSignalSet().NextSearchRequest, self.nextSearchRequest)
        self._connectSignal(self.view().search_dialog.getSignalSet().FinishSearchRequest, self.finishSearchRequest)

        self.control_table.Run()
        self.view().render()

    def Stop(self):
        self.control_table.Stop()
        super().Stop()

    """
    slot
    """
    @MyPyqtSlot(dict)
    def addNewVisitorRequest(self, property_dict: Dict[str, str]):
        self.control_table.addNewVisitorRequest(property_dict)
        self.view().filter.table.clearTexts()

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