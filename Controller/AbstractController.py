from PyQt5.QtCore import pyqtSignal, QObject
from typing import Callable, List
from Utility.Log.ErrorLogger import *


class AbstractController(QObject):
    def __init__(self):
        super().__init__()
        self.__connect_list: List[Tuple[pyqtSignal, Callable]] = []

    """
    property
    * model
    * view
    """
    def model(self) -> QObject:
        raise NotImplementedError

    def view(self) -> QObject:
        raise NotImplementedError

    """
    method
    * connectSignal
    * disconnectSignal, disconnectSignalAll
    * Run, Stop
    """
    def _connectSignal(self, signal: pyqtSignal, slot: Callable) -> None:
        signal.connect(slot)
        self.__connect_list.append((signal, slot))

    def _disconnectSignal(self, signal: pyqtSignal, slot: Callable) -> None:
        try:
            signal.disconnect(slot)
            self.__connect_list.remove((signal, slot))
        except Exception as e:
            ErrorLogger.reportError(f'{signal.__class__.__name__}과 {slot}이 연결되어 있지 않습니다.', ConnectionError)

    def _disconnectSignalAll(self) -> None:
        while self.__connect_list:
            signal, slot = self.__connect_list[0]
            self._disconnectSignal(signal, slot)

    def Run(self):
        raise NotImplementedError

    def Stop(self):
        self._disconnectSignalAll()


