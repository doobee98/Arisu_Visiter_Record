from View.Database.DatabaseTable.DatabaseTableView import *
from Utility.Manager.CommandManager import *
from Controller.AbstractController import *
from Model.Command.ConcreteCommand.Model import Model
from Model.Command.ConcreteCommand.View import View


class DatabaseTableController(AbstractController):
    def __init__(self, model: DatabaseModel, view: DatabaseTableView):
        super().__init__()
        self.__model = model
        self.__view = view

        self.__view.setModel(self.__model)

    """
    property
    * model (override)
    * view (override)
    """
    def model(self) -> DatabaseModel:
        return self.__model

    def view(self) -> DatabaseTableView:
        return self.__view

    """
    method
    * Run, Stop  (override)
    """
    def Run(self):
        self._connectSignal(self.model().getSignalSet().TableModelUpdated, self.updateViewRequest)
        self._connectSignal(self.view().getSignalSet().DeleteDataRequest, CommandSlot(self.deleteVisitorRequest))
        self._connectSignal(self.view().getSignalSet().ChangeDataRequest, CommandSlot(self.changeVisitorRequest))
        self._connectSignal(self.view().getSignalSet().SortTableRequest, CommandSlot(self.sortDatabaseRequest))
        self._connectSignal(self.view().getSignalSet().ChangeDataGroupRequest, CommandSlot(self.changeGroupRequest))
        self.view().render()

    def Stop(self):
        super().Stop()
        self.view().render()

    """
    slot
    """
    @MyPyqtSlot()
    def updateViewRequest(self):
        self.view().render()
        #CommandManager.postCommand(View.Table.RenderCommand(self.view), priority=Priority.Low)

    @MyPyqtSlot(dict)
    def addNewVisitorRequest(self, property_dict: Dict[str, str]):
        idx = self.model().getDataCount()
        #CommandManager.postCommand(View.Table.InsertRowCommand(self.view(), idx))
        CommandManager.postCommand(Model.AddModelCommand(self.model(), property_dict))
        CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx, 1))

    @MyPyqtSlot(int, dict)
    def changeVisitorRequest(self, idx: int, property_dict: Dict[str, str]):
        if 0 <= idx < self.model().getDataCount():
            CommandManager.postCommand(Model.ChangeModelCommand(self.model(), idx, property_dict))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx, 1))
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}', IndexError)

    @MyPyqtSlot(int)
    def deleteVisitorRequest(self, idx: int):
        if 0 <= idx < self.model().getDataCount():
            CommandManager.postCommand(Model.DeleteModelCommand(self.model(), idx))
            #CommandManager.postCommand(View.Table.RemoveRowCommand(self.view(), idx))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view(), idx, 1))  # todo removerow 아직 안넣어서 임시
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}', IndexError)

    @MyPyqtSlot(str)
    def sortDatabaseRequest(self, field: str) -> None:
        CommandManager.postCommand(Model.SortTableModelCommand(self.model(), field))

    @MyPyqtSlot(dict)
    def changeGroupRequest(self, idx_property_dict: Dict[int, Dict[str, str]]):
        for idx in idx_property_dict.keys():
            if 0 <= idx < self.model().getDataCount():
                self.changeVisitorRequest(idx, idx_property_dict[idx])
            else:
                CommandManager.postCommand(View.Table.SetRowTextCommand(self.view(), idx, idx_property_dict[idx]))

