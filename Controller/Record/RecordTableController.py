from View.Table.RecordTableView import *
from Utility.Manager.CommandManager import *

"""
RecordTableController
"""


class RecordTableControllerSignal(QObject):
    FindDatabaseRequest = pyqtSignal(dict)
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class RecordTableController(QObject):
    def __init__(self, view: RecordTableView, parent: QObject = None):
        super().__init__(parent)
        self.__signal_set = RecordTableControllerSignal(self)
        self.__view: RecordTableView = view

        self.__view.signalSet().AddButtonClicked.connect(CommandSlot(self.addButtonClicked))
        self.__view.signalSet().EditButtonToggled.connect(CommandSlot(self.editButtonToggled, end_command=NullCommand()))  # 경우에 따라 나누어서 직접 처리함
        self.__view.signalSet().RemoveButtonClicked.connect(CommandSlot(self.removeButtonClicked))
        self.__view.signalSet().CellFocusChanged.connect(CommandSlot(self.cellFocusChanged, end_command=ExecCommand()))
        self.__view.signalSet().Paste.connect(CommandSlot(self.paste))

    """
    property
    * signalSet
    * model, view
    """
    def signalSet(self) -> RecordTableControllerSignal:
        return self.__signal_set

    def model(self) -> RecordTableModel:
        return self.__view.myModel()

    def view(self) -> RecordTableView:
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
    * addButtonClicked, editButtonClicked, removeClicked
    * cellFocusChanged
    """
    @MyPyqtSlot(int)
    def addButtonClicked(self, row: int) -> None:
        new_data_dict = {field_name_iter: data_iter for field_name_iter, data_iter in self.view().rowTextDictionary(row).items()
                         if ConfigModule.TableField.fieldModel(field_name_iter).recordOption(TableFieldOption.Record.Group)}
        CommandManager.postCommand(Model.InsertItemCommand(self.model(), row + 1, new_data_dict))

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
            CommandManager.postCommand(View.MyRenderRowCommand(self.view(), row))  # todo 중복행 렌더링때문에 추가했음

    @MyPyqtSlot(int, int)
    def cellFocusChanged(self, row: int, column: int) -> None:
        """
        1. 조건 충족 확인
        2. 조건 충족하면 Find Request 발생 (완성)
        3. 자동입력 조건 충족 확인
        4. 자동입력 조건 충족하면 AutoFill Request 발생
        5.
        """
        key_data_dict = {}
        for field_model_iter in self.view().fieldModelList():
            if field_model_iter.globalOption(TableFieldOption.Global.Key) is True:
                key_iter, data_iter = field_model_iter.name(), self.view().fieldText(row, field_model_iter.name())
                if data_iter:
                    key_data_dict[key_iter] = data_iter
        self.signalSet().FindDatabaseRequest.emit(key_data_dict)

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



