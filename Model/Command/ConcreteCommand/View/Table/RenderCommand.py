from Model.Command.AbstractCommand import *
from Utility.TableInterface.View.MyTableView import *


class RenderCommand(AbstractCommand):
    def __init__(self, table_view: Type[MyTableView]):
        super().__init__()
        self.__table_view = table_view

    def execute(self) -> bool:
        if super().execute():
            self.__table_view.render()
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            # todo: ignore?
            return True
        else:
            return False
