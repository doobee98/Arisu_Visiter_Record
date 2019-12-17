from abc import *
from Utility.Manager.StatusBarManager import *

"""
AbstractCommand(QObject)
사용자의 특정 행동을 캡슐화하는 Command의 인터페이스
CommandManager로 관리되며, Undo와 Redo를 지원함
"""


class AbstractCommand(QObject):
    def __init__(self):
        super().__init__()
        self.__is_executed = False

    """
    property
    * isExecuted
    """
    def isExecuted(self) -> bool:
        return self.__is_executed

    def setIsExecuted(self, is_executed: bool) -> None:
        self.__is_executed = is_executed

    """
    method
    * execute
    * undo
    """
    @abstractmethod
    def execute(self) -> bool:
        if self.isExecuted():
            raise AttributeError('Try to execute while this command is already executed')
        else:
            self.setIsExecuted(True)
            return True

    @abstractmethod
    def undo(self) -> bool:
        if not self.isExecuted():
            raise AttributeError('Try to undo while this command is still not executed')
        else:
            self.setIsExecuted(False)
            return True
