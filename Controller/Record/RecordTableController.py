from View.Record.RecordTable.RecordTableView import *

from Utility.CommandManager import *
from Model.Command.ConcreteCommand.Model import Model
from Model.Command.ConcreteCommand.View import View



class RecordTableController(QObject):
    def __init__(self, model: RecordTableModel, view: RecordTableView):
        super().__init__()
        self.__connect_list: List[Tuple[pyqtSignal, Callable]] = []
        self.model = model
        self.view = view

    def __connect(self, signal: pyqtSignal, slot: Callable) -> None:
        signal.connect(slot)
        self.__connect_list.append((signal, slot))

    def Run(self):
        # self.model.getSignalSet().RecordTableModelUpdated.connect(self.updateViewRequest) 전체 뷰를 렌더링 하지 않음
        # self.model.getSignalSet().ModelUpdated.connect(self.updateRowViewRequest)
        # self.view.getSignalSet().AppendDataRequest.connect(CommandSlot(self.addRecordRequest))
        # self.view.getSignalSet().InsertDataRequest.connect(CommandSlot(self.insertRecordRequest))
        # self.view.getSignalSet().ChangeDataRequest.connect(CommandSlot(self.changeRecordRequest))
        # self.view.getSignalSet().DeleteDataRequest.connect(CommandSlot(self.deleteRecordRequest))
        self.__connect(self.model.getSignalSet().ModelUpdated, self.updateRowViewRequest)
        self.__connect(self.view.getSignalSet().AppendDataRequest, CommandSlot(self.addRecordRequest))
        self.__connect(self.view.getSignalSet().InsertDataRequest, CommandSlot(self.insertRecordRequest))
        self.__connect(self.view.getSignalSet().ChangeDataRequest, CommandSlot(self.changeRecordRequest))
        self.__connect(self.view.getSignalSet().DeleteDataRequest, CommandSlot(self.deleteRecordRequest))

        self.view.render()
        self.model.update()  # todo 잔여인원때문에 임시로 들어감

    def Stop(self):
        # self.model.getSignalSet().RecordTableModelUpdated.connect(self.updateViewRequest) 전체 뷰를 렌더링 하지 않음
        # self.model.getSignalSet().ModelUpdated.disconnect(self.updateRowViewRequest)
        # self.view.getSignalSet().AppendDataRequest.disconnect(CommandSlot(self.addRecordRequest))
        # self.view.getSignalSet().InsertDataRequest.disconnect(CommandSlot(self.insertRecordRequest))
        # self.view.getSignalSet().ChangeDataRequest.disconnect(CommandSlot(self.changeRecordRequest))
        # self.view.getSignalSet().DeleteDataRequest.disconnect(CommandSlot(self.deleteRecordRequest))
        for signal, slot in self.__connect_list:
            signal.disconnect(slot)
        self.__connect_list.clear()

    def getTableModel(self) -> RecordTableModel:
        return self.model

    @pyqtSlot(int)
    def updateRowViewRequest(self, row: int):
        self.view.renderRow(row)
        #CommandManager.postCommand(View.Table.RenderRowCommand(self.view, row), priority=Priority.Low)

    @pyqtSlot(dict)
    def addRecordRequest(self, property_dict: Dict[str, str]):
        idx = self.model.getDataCount()
        CommandManager.postCommand(View.Table.InsertRowCommand(self.view, idx))
        CommandManager.postCommand(Model.AddModelCommand(self.model, property_dict))
        CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx + 1, 1))
        # if self.sender():
        #     print('add')
        #     CommandManager.postCommand(EndCommand())

    @pyqtSlot(int, dict)
    def insertRecordRequest(self, idx: int, property_dict: Dict[str, str]):
        if 0 <= idx <= self.model.getDataCount():  # idx == recordCount일땐 addRecord와 같기에 열린범위임: <=
            CommandManager.postCommand(View.Table.InsertRowCommand(self.view, idx))
            CommandManager.postCommand(Model.InsertModelCommand(self.model, idx, property_dict))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx, 1))
            # if self.sender():
            #     print('insert')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}')

    @pyqtSlot(int, dict)
    def changeRecordRequest(self, idx: int, property_dict: Dict[str, str]):
        if 0 <= idx < self.model.getDataCount():
            CommandManager.postCommand(Model.ChangeModelCommand(self.model, idx, property_dict))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx, 1))
            # if self.sender():
            #     print('change')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}')

    @pyqtSlot(int)
    def deleteRecordRequest(self, idx: int):
        if 0 <= idx < self.model.getDataCount():
            CommandManager.postCommand(Model.DeleteModelCommand(self.model, idx))
            CommandManager.postCommand(View.Table.RemoveRowCommand(self.view, idx))
            CommandManager.postCommand(View.Table.FocusCellCommand(self.view, idx, 1))
            # if self.sender():
            #     print('delete')
            #     CommandManager.postCommand(EndCommand())
        else:
            ErrorLogger.reportError(f'Invalid Idx: {idx}')

