from View.Table.DatabaseTableView import *
from Utility.Manager.CommandManager import *

"""
DatabaseTableController
"""


class DatabaseTableControllerSignal(QObject):
    FindDatabaseRequest = pyqtSignal(dict)
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class DatabaseTableController(QObject):
    def __init__(self, view: DatabaseTableView, parent: QObject = None):
        super().__init__(parent)
        self.__signal_set = DatabaseTableControllerSignal(self)
        self.__view: DatabaseTableView = view
        self.__view.show()
        self.__view.signalSet().EditButtonToggled.connect(CommandSlot(self.editButtonToggled, end_command=NullCommand()))  # 경우에 따라 나누어서 직접 처리함
        self.__view.signalSet().RemoveButtonClicked.connect(CommandSlot(self.removeButtonClicked))
        self.__view.signalSet().Paste.connect(CommandSlot(self.paste))
        self.__view.signalSet().FieldHeaderDoubleClicked.connect(CommandSlot(self.sortModel))

    """
    property
    * signalSet
    * model, view
    """
    def signalSet(self) -> DatabaseTableControllerSignal:
        return self.__signal_set

    def model(self) -> DatabaseTableModel:
        return self.__view.myModel()

    def view(self) -> DatabaseTableView:
        return self.__view

    """
    method
    * start, stop
    """
    def start(self) -> None:
        self.blockSignals(False)

    def stop(self) -> None:
        self.blockSignals(True)

    """
    slot
    * editButtonClicked, removeClicked
    """
    @MyPyqtSlot(int, bool)
    def editButtonToggled(self, row: int, checked: bool) -> None:
        if checked:
            for field_model_iter in self.view().fieldModelList():
                if not field_model_iter.globalOption(TableFieldOption.Global.Uneditable):
                    self.view().openPersistentEditor(self.view().fieldItem(row, field_model_iter.name()))
        else:
            field_data_dict = {}
            for field_model_iter in self.view().fieldModelList():
                if not field_model_iter.globalOption(TableFieldOption.Global.Uneditable):
                    self.view().closePersistentEditor(self.view().fieldItem(row, field_model_iter.name()))
                    field_data_dict[field_model_iter.name()] = self.view().fieldText(row, field_model_iter.name())
            CommandManager.postCommand(Model.ChangeItemCommand(self.model(), row, field_data_dict))
            CommandManager.postCommand(EndCommand())

    @MyPyqtSlot(int)
    def removeButtonClicked(self, row: int) -> None:
        if row < self.model().itemCount():
            CommandManager.postCommand(Model.RemoveItemCommand(self.model(), row))
        else:
            CommandManager.postCommand(View.ClearRowTextCommand(self.view(), row))

    @MyPyqtSlot(dict)
    def paste(self, paste_row_text_dict: Dict[int, Dict[str, str]]) -> None:
        self.model().setAutoSave(False)
        try:
            for row_iter, paste_dict_iter in paste_row_text_dict.items():
                CommandManager.postCommand(View.SetRowTextsCommand(self.view(), row_iter, paste_dict_iter))
            CommandManager.addEndFunction(lambda: self.model().setAutoSave(True))
            CommandManager.addEndFunction(lambda: self.model().save())
        except Exception as e:
            self.model().setAutoSave(True)
            raise e

    @MyPyqtSlot(str)
    def sortModel(self, field_name: str) -> None:
        self.model().setAutoSave(False)
        try:
            CommandManager.postCommand(Model.SortItemsCommand(self.model(), field_name))
            CommandManager.addEndFunction(lambda: self.model().setAutoSave(True))
            CommandManager.addEndFunction(lambda: self.model().save())
        except Exception as e:
            self.model().setAutoSave(True)
            raise e

