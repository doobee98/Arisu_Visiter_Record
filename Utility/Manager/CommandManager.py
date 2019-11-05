from Model.Command.Action import *
from Model.Command.AbstractCommand import *
from typing import List, Tuple
from enum import Enum
from PyQt5.QtCore import pyqtSlot
import heapq


class Priority(Enum):
    End = 10000
    Low = 1000
    Normal = 0
    High = -1000
    RightAway = -10000


class NullCommand(AbstractCommand):
    def __init__(self):
        super().__init__()

    def execute(self) -> bool:
        return super().execute()

    def undo(self) -> bool:
        return super().undo()


class ExecCommand(NullCommand):
    pass


class EndCommand(NullCommand):
    pass


class FlushCommand(NullCommand):
    pass


def CommandSlot(original_func: Callable[..., bool], end_command=EndCommand()) -> Callable[..., bool]:
    def wrapper(*args, **kargs):
        try:
            result = original_func(*args, **kargs)
            if end_command:
                CommandManager.postCommand(end_command)
            return result
        except Exception as e:
            ErrorLogger.reportError(f'{original_func.__name__} CommandSlot 실행 도중 에러 발생', e)
    return wrapper


class CommandManager(QObject):
    __INSTANCE = None
    __HISTORY_MAX = 10
    __TOP = 0
    def __init__(self):
        super().__init__()
        self.__exec_command_list: List[AbstractCommand] = []
        self.__command_buffers: List[Tuple[int, int, AbstractCommand]] = []
        self.__end_func_list: List[Callable[[None], None]] = []
        self.__action_histories: List[Action] = []  # todo 새로 추가, getter setter 안넣었음 귀찮아서
        self.__current_history_idx = -1

    @classmethod
    def __instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    @classmethod
    def isUndoEnable(cls) -> bool:
        return cls.__historyCount() >= 1 and cls.__currentHistoryIndex() <= cls.__bottomHistoryIndex()

    @classmethod
    def isRedoEnable(cls) -> bool:
        return cls.__historyCount() >= 1 and cls.__currentHistoryIndex() > cls.__topHistoryIndex()

    @classmethod
    def postCommand(cls, command: AbstractCommand, priority: Priority = Priority.Normal):
        if isinstance(command, EndCommand):
            cls.__endCommandBuffer()  # todo: return 값(bool)을 활용한 게 있어야할까
        elif isinstance(command, ExecCommand):
            cls.__execCommandBuffer()
        else:
            cls.__addCommandBuffer(command, priority)

    @classmethod
    def addEndFunction(cls, func: Callable[[None], None]) -> None:
        cls.__instance().__end_func_list.append(func)

    @classmethod
    def __addCommandBuffer(cls, command: AbstractCommand, priority: Priority):
        count = len(cls.__instance().__command_buffers)
        heapq.heappush(cls.__instance().__command_buffers, (priority.value, count, command))

    @classmethod
    def __execCommandBuffer(cls) -> bool:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        return_value = True
        while cls.__instance().__command_buffers:
            cmd_iter = heapq.heappop(cls.__instance().__command_buffers)[2]
            if cmd_iter.execute() is True:
                cls.__instance().__exec_command_list.append(cmd_iter)
            else:
                return_value = False
                break

        QApplication.restoreOverrideCursor()
        if return_value is True:
            StatusBarManager.setIdleStatus()
            return True
        else:
            StatusBarManager.setMessage('실행 실패')
            return False

    @classmethod
    def __endCommandBuffer(cls) -> bool:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        return_value = True
        action = Action()
        if cls.__instance().__exec_command_list:
            for exec_cmd_iter in cls.__instance().__exec_command_list:
                action.addCommand(exec_cmd_iter)
            cls.__instance().__exec_command_list.clear()
        while cls.__instance().__command_buffers:
            cmd_iter = heapq.heappop(cls.__instance().__command_buffers)[2]
            if cmd_iter.execute() is True:
                action.addCommand(cmd_iter)
            else:
                return_value = False
                break

        QApplication.restoreOverrideCursor()
        if return_value is True:
            action.setIsExecuted(True)
            cls.__addHistory(action)
            for func_iter in cls.__instance().__end_func_list:
                func_iter()
            cls.__instance().__end_func_list.clear()
            StatusBarManager.setIdleStatus()
            return True
        else:
            StatusBarManager.setMessage('실행 실패')
            return False

    @classmethod  # todo: exec_command_list undo에 추가하여야 하는지?
    def undo(cls) -> bool:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        return_value = True
        if cls.isUndoEnable():
            if cls.__instance().__exec_command_list:
                for exec_cmd_iter in reversed(cls.__instance().__exec_command_list):
                    if exec_cmd_iter.undo() is False:
                        return_value = False
                        break
                cls.__instance().__exec_command_list.clear()
            if return_value and cls.__histories()[cls.__currentHistoryIndex()].undo():
                cls.__instance().__current_history_idx += 1
            else:
                return_value = False
        else:
            return_value = False

        QApplication.restoreOverrideCursor()
        if return_value is True:
            StatusBarManager.setIdleStatus()
            return True
        else:
            StatusBarManager.setMessage('취소 실패')
            return False

    @classmethod
    def redo(cls) -> bool:
        return_value = True
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if cls.isRedoEnable():
            if cls.__histories()[cls.__currentHistoryIndex() - 1].execute() is True:
                cls.__instance().__current_history_idx -= 1
            else:
                return_value = False
        else:
            return_value = False

        QApplication.restoreOverrideCursor()
        if return_value is True:
            StatusBarManager.setIdleStatus()
            return True
        else:
            StatusBarManager.setMessage('재실행 실패')
            return False

    @classmethod
    def __histories(cls) -> List[AbstractCommand]:
        return cls.__instance().__action_histories

    @classmethod
    def __historyCount(cls) -> int:
        return len(cls.__histories())

    @classmethod
    def __addHistory(cls, action: Action):
        if cls.__currentHistoryIndex() != cls.__topHistoryIndex():
            cls.__instance().__action_histories = cls.__histories()[cls.__currentHistoryIndex():]
            cls.__setCurrentHistoryIndex(cls.__topHistoryIndex())
        if cls.__historyCount() == cls.__HISTORY_MAX:
            del cls.__instance().__action_histories[cls.__bottomHistoryIndex()]
        cls.__histories().insert(cls.__topHistoryIndex(), action)

    @classmethod
    def __currentHistoryIndex(cls) -> int:
        return cls.__instance().__current_history_idx

    @classmethod
    def __setCurrentHistoryIndex(cls, current_index: int) -> None:
        cls.__instance().__current_history_idx = current_index

    @classmethod
    def __topHistoryIndex(cls) -> int:
        return 0

    @classmethod
    def __bottomHistoryIndex(cls) -> int:
        return cls.__historyCount() - 1
