from View.Database.DatabaseTable.DatabaseTableView import *

from Utility.CommandManager import *
from Model.Command.ConcreteCommand.Model import Model
from Model.Command.ConcreteCommand.View import View


class DatabaseTableController(QObject):
    def __init__(self, model: DatabaseModel, view: DatabaseTableView):
        super().__init__()
        self.model = model
        self.view = view

        self.view.setModel(self.model)

    def Run(self):
        self.model.getSignalSet().TableModelUpdated.connect(self.updateViewRequest)
        self.view.getSignalSet().DeleteDataRequest.connect(CommandSlot(self.deleteVisitorRequest))
        self.view.getSignalSet().ChangeDataRequest.connect(CommandSlot(self.changeVisitorRequest))
        self.view.getSignalSet().SortTableRequest.connect(CommandSlot(self.sortDatabaseRequest))

        self.view.render()

    def Stop(self):
        self.model.getSignalSet().TableModelUpdated.disconnect(self.updateViewRequest)
        self.view.getSignalSet().DeleteDataRequest.disconnect(CommandSlot(self.deleteVisitorRequest))
        self.view.getSignalSet().ChangeDataRequest.disconnect(CommandSlot(self.changeVisitorRequest))

        self.view.render()

    @pyqtSlot()
    def updateViewRequest(self):
        self.view.render()
        #CommandManager.postCommand(View.Table.RenderCommand(self.view), priority=Priority.Low)

    @pyqtSlot(dict)
    def addNewVisitorRequest(self, property_dict: Dict[str, str]):
        idx = self.model.getDataCount()
        CommandManager.postCommand(View.Table.InsertRowCommand(self.view, idx))
        CommandManager.postCommand(Model.AddModelCommand(self.model, property_dict))
        # todo: writeDatabase한 뒤 undo하면 setRowData가 적용이 안됨. 그걸 그냥 여기서 처리하면 좋을듯
        CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx, 1))
        # if self.sender():
        #     print('add')
        #     CommandManager.postCommand(EndCommand())
        # visitor_model = VisitorModel(property_dict)
        # self.model.addData(visitor_model)

    @pyqtSlot(int, dict)
    def changeVisitorRequest(self, idx: int, property_dict: Dict[str, str]):
        if 0 <= idx < self.model.getDataCount():
            CommandManager.postCommand(Model.ChangeModelCommand(self.model, idx, property_dict))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx, 1))
            # if self.sender():
            #     print('change')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}')

    @pyqtSlot(int)
    def deleteVisitorRequest(self, idx: int):
        if 0 <= idx < self.model.getDataCount():
            CommandManager.postCommand(Model.DeleteModelCommand(self.model, idx))
            CommandManager.postCommand(View.Table.RemoveRowCommand(self.view, idx))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx, 1))  # todo removerow 아직 안넣어서 임시
            # if self.sender():
            #     print('delete')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}')

    @pyqtSlot(str)
    def sortDatabaseRequest(self, field: str) -> None:
        CommandManager.postCommand(Model.SortTableModelCommand(self.model, field))
        #self.view.render()
