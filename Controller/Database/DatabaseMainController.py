from Controller.Database.DatabaseTableController import *
from View.Database.DatabaseMainView import *
from View.Dialog.SearchDialog import *

"""
RecordMainController
"""


class DatabaseMainControllerSignal(QObject):

    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class DatabaseMainController(QObject):
    def __init__(self, view: DatabaseMainView, parent: QObject = None):
        super().__init__(parent)
        self.__signal_set = DatabaseMainControllerSignal(self)
        self.__view = view
        self.__table_controller = DatabaseTableController(view.databaseTableView(), self)
        self.__search_dialog = SearchDialog(self.tableController().view())

        # tableModel signal
        self.tableController().model().signalSet().SortInfoChanged.connect(self.sortInfoChanged)

        # tableView signal
        self.view().signalSet().FunctionView_SearchButtonClicked.connect(lambda: self.__search_dialog.exec_())  # todo
        self.view().signalSet().AddGroupView_AddButtonClicked.connect(CommandSlot(self.addButtonClicked, end_command=NullCommand()))

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
    """
    def signalSet(self) -> DatabaseMainControllerSignal:
        return self.__signal_set

    def view(self) -> DatabaseMainView:
        return self.__view

    def tableController(self) -> DatabaseTableController:
        return self.__table_controller

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
    * sortInfoChanged
    """
    @MyPyqtSlot()
    def sortInfoChanged(self) -> None:
        sort_field_name, sort_order = self.tableController().model().sortFieldName(), self.tableController().model().sortOrder()
        if sort_field_name:
            field_text, order_text = sort_field_name, '오름차순' if sort_order else '내림차순'
        else:
            field_text, order_text = '없음', '---'
        self.view().sortInformationView().setSortFieldNameText(field_text)
        self.view().sortInformationView().setSortOrderText(order_text)

    """
    view slot
    * addButtonClicked
    """
    @MyPyqtSlot()
    def addButtonClicked(self) -> None:
        database_model = self.tableController().model()
        add_table_view = self.view().addGroupView().tableView()
        field_data_dict = {}
        for column_iter in range(add_table_view.columnCount()):
            field_name_iter = add_table_view.horizontalHeaderItem(column_iter).text()
            data_iter = add_table_view.item(0, column_iter).text()
            if data_iter:
                field_data_dict[field_name_iter] = data_iter
        if field_data_dict:
            CommandManager.postCommand(Model.AddItemCommand(database_model, field_data_dict))
            CommandManager.postCommand(EndCommand())
            add_table_view.clearSelection()  # todo 좀더 깔끔하게 할 방법? clear 두개
            for column_iter in range(add_table_view.columnCount()):
                add_table_view.item(0, column_iter).setText('')

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
