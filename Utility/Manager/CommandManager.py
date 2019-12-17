from Model.Command.Action import *
from Model.Command.AbstractCommand import *
from Model.Command.ConcreteCommand.Model import Model
from Model.Command.ConcreteCommand.View import View
from typing import List, Tuple
from enum import Enum
import heapq


"""
CommandManager
전역 클래스
EventManager와 비슷함. undo, redo를 지원함
1. CommandSlot - End Command를 하나만 두고 싶기에 활용함
2. Exec: End는 하고싶지 않지만 일단 현재까지의 실행 결과를 화면에 보여주고 싶을 때 사용함
3. End: EndCommand가 post되면 Action이 구성되어 CommandBuffer가 실행된다.
4. Action: undo, redo의 단위
"""


class CommandPriority(Enum):
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


def CommandSlot(original_func: Callable[..., bool], end_command: AbstractCommand = EndCommand()) -> Callable[..., bool]:
    def wrapper(*args, **kargs):
        try:
            result = original_func(*args, **kargs)
            if end_command.__class__ != NullCommand:
                CommandManager.postCommand(end_command)
            return result
        except Exception as e:
            ErrorLogger.reportError(f'{original_func.__name__} CommandSlot 실행 도중 에러 발생', e)
    return wrapper


class CommandManager(QObject):
    __INSTANCE = None
    @classmethod
    def __instance(cls):
        if cls.__INSTANCE is None:
            cls.__INSTANCE = cls()
        return cls.__INSTANCE

    __HISTORY_MAX = 15
    def __init__(self):
        super().__init__()
        self.__exec_command_buffer: List[Tuple[int, int, AbstractCommand]] = []
        self.__command_buffers: List[Tuple[int, int, AbstractCommand]] = []
        self.__end_func_list: List[Callable[[None], None]] = []
        self.__action_histories: List[Action] = []  # todo 새로 추가, getter setter 안넣었음 귀찮아서
        self.__current_history_idx = -1

    """
    property
    * __action history List
    * __currentHistoryIndex
    """
    @classmethod
    def __historyList(cls) -> List[AbstractCommand]:
        return cls.__instance().__action_histories

    @classmethod
    def __addHistory(cls, action: Action):
        if cls.__currentHistoryIndex() != cls.__topHistoryIndex():
            cls.__instance().__action_histories = cls.__historyList()[cls.__currentHistoryIndex():]
            cls.__setCurrentHistoryIndex(cls.__topHistoryIndex())
        if cls.__historyCount() == cls.__HISTORY_MAX:
            del cls.__instance().__action_histories[cls.__bottomHistoryIndex()]
        cls.__historyList().insert(cls.__topHistoryIndex(), action)

    @classmethod
    def __currentHistoryIndex(cls) -> int:
        return cls.__instance().__current_history_idx

    @classmethod
    def __setCurrentHistoryIndex(cls, current_index: int) -> None:
        cls.__instance().__current_history_idx = current_index

    """
    advanced property
    * __historyCount
    * isUndoEnable, isRedoEnable
    * __topHistoryIndex, __bottomHistoryIndex
    """
    @classmethod
    def __historyCount(cls) -> int:
        return len(cls.__historyList())

    @classmethod
    def isUndoEnable(cls) -> bool:
        return cls.__historyCount() >= 1 and cls.__currentHistoryIndex() <= cls.__bottomHistoryIndex()

    @classmethod
    def isRedoEnable(cls) -> bool:
        return cls.__historyCount() >= 1 and cls.__currentHistoryIndex() > cls.__topHistoryIndex()

    @classmethod
    def __topHistoryIndex(cls) -> int:
        return 0

    @classmethod
    def __bottomHistoryIndex(cls) -> int:
        return cls.__historyCount() - 1

    """
    method
    * addEndFunction
    * postCommand
    * __addCommandBuffer
    * __execCommandBuffer, __endCommandBuffer
    * undo, redo
    """
    @classmethod
    def addEndFunction(cls, func: Callable[[None], None]) -> None:
        cls.__instance().__end_func_list.append(func)

    @classmethod
    def postCommand(cls, command: AbstractCommand, priority: CommandPriority = CommandPriority.Normal):
        if isinstance(command, EndCommand):
            cls.__endCommandBuffer()  # todo: return 값(bool)을 활용한 게 있어야할까
        elif isinstance(command, ExecCommand):
            cls.__execCommandBuffer()
        else:
            cls.__addCommandBuffer(command, priority.value)

    @classmethod
    def __addExecBuffer(cls, command: AbstractCommand, priority: int):
        count = len(cls.__instance().__exec_command_buffer)
        heapq.heappush(cls.__instance().__exec_command_buffer, (priority, count, command))

    @classmethod
    def __addCommandBuffer(cls, command: AbstractCommand, priority: int):
        count = len(cls.__instance().__command_buffers)
        heapq.heappush(cls.__instance().__command_buffers, (priority, count, command))

    @classmethod
    def __execCommandBuffer(cls) -> bool:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        return_value = True
        while cls.__instance().__command_buffers:
            priority_iter, count_iter, cmd_iter = heapq.heappop(cls.__instance().__command_buffers)
            if cmd_iter.execute() is True:
                cls.__addExecBuffer(cmd_iter, priority_iter)
                # cls.__instance().__exec_command_buffer.append(cmd_iter)
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
        return_value = False
        action = Action()
        if cls.__instance().__exec_command_buffer:
            for exec_iter in cls.__instance().__exec_command_buffer:
                priority_iter, count_iter, cmd_iter = exec_iter
                action.addCommand(cmd_iter, priority_iter)
            cls.__instance().__exec_command_buffer.clear()
        while cls.__instance().__command_buffers:
            priority_iter, count_iter, cmd_iter = heapq.heappop(cls.__instance().__command_buffers)
            if cmd_iter.execute() is True:
                return_value = True
                action.addCommand(cmd_iter, priority_iter)
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

    @classmethod
    def undo(cls) -> bool:
        QApplication.setOverrideCursor(Qt.WaitCursor)
        undo_list = []
        return_value = True
        if cls.isUndoEnable():
            if cls.__instance().__exec_command_buffer:
                for exec_iter in reversed(cls.__instance().__exec_command_buffer):
                    exec_cmd_iter = exec_iter[2]
                    if exec_cmd_iter.undo() is False:
                        for undo_cmd_iter in reversed(undo_list):
                            undo_cmd_iter.execute()
                        return_value = False
                        break
                    undo_list.append(exec_cmd_iter)
                cls.__instance().__exec_command_buffer.clear()
            if return_value and cls.__historyList()[cls.__currentHistoryIndex()].undo():
                undo_list.append(cls.__historyList()[cls.__currentHistoryIndex()])
                cls.__instance().__current_history_idx += 1
            else:
                for undo_cmd_iter in reversed(undo_list):
                    undo_cmd_iter.execute()
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
        # todo: exec_command_list redo에 추가하여야 하는지?
        execute_list = []
        return_value = True
        QApplication.setOverrideCursor(Qt.WaitCursor)
        if cls.isRedoEnable():
            if cls.__historyList()[cls.__currentHistoryIndex() - 1].execute() is True:
                execute_list.append(cls.__historyList()[cls.__currentHistoryIndex() - 1])
                cls.__instance().__current_history_idx -= 1
            else:
                for execute_cmd_iter in reversed(execute_list):
                    execute_cmd_iter.undo()
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


