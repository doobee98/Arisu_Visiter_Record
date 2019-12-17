from Model.Command.AbstractCommand import *
from View.Table.AbstractTableView import *

"""
MyRenderRow
반드시 postCommand할 때 priority를 Low나 End로 주어야함.
그래야 undo가 정상적으로 작동함
"""


class MyRenderRowCommand(AbstractCommand):
    def __init__(self, table_view: AbstractTableView, row: int):
        super().__init__()
        self.__table_view = table_view
        self.__row = row

    def execute(self) -> bool:
        if super().execute():
            self.__table_view.myRenderRow(self.__row)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            self.__table_view.myRenderRow(self.__row)
            return True
        else:
            return False
