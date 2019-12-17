from View.Table.RecordTableView import *
from Utility.Manager.CommandManager import *

"""
ConfigController
"""
# todo


class ConfigControllerSignal(QObject):

    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class ConfigController(QObject):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.__signal_set = ConfigControllerSignal(self)
        # self.__view: RecordTableView = view

    """
    property
    * signalSet
    * model, view
    """
    def signalSet(self) -> ConfigControllerSignal:
        return self.__signal_set

    # def model(self) -> RecordTableModel:
    #     return self.__view.myModel()
    #
    # def view(self) -> RecordTableView:
    #     return self.__view

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

    """
