from Model.Command.AbstractCommand import *
from Utility.Abstract.View.Table.MyTableView import *


class InsertRowCommand(AbstractCommand):
    def __init__(self, table_view: MyTableView, row: int):
        super().__init__()
        self.__table_view = table_view
        self.__row = row

    def execute(self) -> bool:
        if super().execute():
            self.__table_view.insertRow(self.__row)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            self.__table_view.removeRow(self.__row)
            return True
        else:
            return False
