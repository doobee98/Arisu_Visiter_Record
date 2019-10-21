from Model.Command.AbstractCommand import *
from typing import Type, List


class Action(AbstractCommand):
    def __init__(self):
        super().__init__()
        self.__cmd_list: List[AbstractCommand] = []

    def addCommand(self, cmd: AbstractCommand):
        self.__cmd_list.append(cmd)

    def removeCommand(self, cmd: AbstractCommand):
        self.__cmd_list.remove(cmd)

    def execute(self) -> bool:
        if super().execute():
            for cmd_iter in self.__cmd_list:
                if not cmd_iter.execute():
                    return False
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            for cmd_iter in reversed(self.__cmd_list):
                if not cmd_iter.undo():
                    return False
            return True
        else:
            return False