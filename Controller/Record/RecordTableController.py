from View.Record.RecordTable.RecordTableView import *

from Utility.Manager.CommandManager import *
from Model.Command.ConcreteCommand.Model import Model
from Model.Command.ConcreteCommand.View import View
from Controller.AbstractController import *



class RecordTableController(AbstractController):
    def __init__(self, model: RecordTableModel, view: RecordTableView):
        super().__init__()
        self.__model = model
        self.__view = view

    """
    property
    * model (override)
    * view (override)
    """
    def model(self) -> RecordTableModel:
        return self.__model

    def view(self) -> RecordTableView:
        return self.__view

    """
    method
    * Run, Stop  (override)
    """
    def Run(self):
        self._connectSignal(self.model().getSignalSet().ModelUpdated, self.updateRowViewRequest)
        self._connectSignal(self.view().getSignalSet().AppendDataRequest, CommandSlot(self.addRecordRequest))
        self._connectSignal(self.view().getSignalSet().InsertDataRequest, CommandSlot(self.insertRecordRequest))
        self._connectSignal(self.view().getSignalSet().ChangeDataRequest, CommandSlot(self.changeRecordRequest))
        self._connectSignal(self.view().getSignalSet().DeleteDataRequest, CommandSlot(self.deleteRecordRequest))
        self._connectSignal(self.view().getSignalSet().ChangeDataGroupRequest, CommandSlot(self.changeGroupRequest))

        self.view().render()
        self.model().update()  # todo 잔여인원때문에 임시로 들어감

    def Stop(self):
        super().Stop()

    """
    slot
    """
    @MyPyqtSlot(int)
    def updateRowViewRequest(self, row: int):
        self.view().renderRow(row)
        #CommandManager.postCommand(View.Table.RenderRowCommand(self.view, row), priority=Priority.Low)

    @MyPyqtSlot(dict)
    def addRecordRequest(self, property_dict: Dict[str, str]):
        idx = self.model().getDataCount()
        CommandManager.postCommand(View.Table.InsertRowCommand(self.view(), idx))
        CommandManager.postCommand(Model.AddModelCommand(self.model(), property_dict))
        CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx + 1, 1))
        # if self.sender():
        #     print('add')
        #     CommandManager.postCommand(EndCommand())

    @MyPyqtSlot(int, dict)
    def insertRecordRequest(self, idx: int, property_dict: Dict[str, str]):
        if 0 <= idx <= self.model().getDataCount():  # idx == recordCount일땐 addRecord와 같기에 열린범위임: <=
            CommandManager.postCommand(View.Table.InsertRowCommand(self.view(), idx))
            CommandManager.postCommand(Model.InsertModelCommand(self.model(), idx, property_dict))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx, 1))
            # if self.sender():
            #     print('insert')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}', IndexError)

    @MyPyqtSlot(int, dict)
    def changeRecordRequest(self, idx: int, property_dict: Dict[str, str]):
        if 0 <= idx < self.model().getDataCount():
            CommandManager.postCommand(Model.ChangeModelCommand(self.model(), idx, property_dict))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx, 1))
            # if self.sender():
            #     print('change')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}', IndexError)

    @MyPyqtSlot(int)
    def deleteRecordRequest(self, idx: int):
        if 0 <= idx < self.model().getDataCount():
            CommandManager.postCommand(Model.DeleteModelCommand(self.model(), idx))
            CommandManager.postCommand(View.Table.RemoveRowCommand(self.view(), idx))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx, 1))
            # if self.sender():
            #     print('delete')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}', IndexError)

    @MyPyqtSlot(dict)
    def changeGroupRequest(self, idx_property_dict: Dict[int, Dict[str, str]]):
        for idx in idx_property_dict.keys():
            if 0 <= idx < self.model().getDataCount():
                self.changeRecordRequest(idx, idx_property_dict[idx])
            else:
                CommandManager.postCommand(View.Table.SetRowTextCommand(self.view(), idx, idx_property_dict[idx]))


