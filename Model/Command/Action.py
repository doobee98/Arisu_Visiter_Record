from Model.Command.AbstractCommand import *
from typing import Type, List
import heapq

"""
Action(AbstractCommand)
Command를 Composite 패턴으로 구현함
여러 Command를 하나의 블록으로 묶기 위한 클래스 (undo, redo 단위)
"""


class Action(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.__priority_cmd_queue: List[Tuple[int, int, AbstractCommand]] = []

    def addCommand(self, cmd: AbstractCommand, priority: int):
        count = len(self.__priority_cmd_queue)
        heapq.heappush(self.__priority_cmd_queue, (priority, count, cmd))

    def __commandList(self) -> List[AbstractCommand]:
        return [tuple_iter[2] for tuple_iter in self.__priority_cmd_queue]

    def execute(self) -> bool:
        if super().execute():
            for cmd_iter in self.__commandList():
                if not cmd_iter.execute():
                    return False
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            reverse_queue = []
            for priority_iter, _, cmd_iter in reversed(self.__priority_cmd_queue):
                count = len(reverse_queue)
                heapq.heappush(reverse_queue, (priority_iter, count, cmd_iter))
            for _, _, cmd_iter in reverse_queue:
                if not cmd_iter.undo():
                    return False
            return True
        else:
            return False