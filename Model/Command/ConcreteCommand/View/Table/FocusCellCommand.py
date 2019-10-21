from Model.Command.AbstractCommand import *
from Utility.Abstract.View.Table.MyTableView import *


class FocusCellCommand(AbstractCommand):
    def __init__(self, table_view: MyTableView, row: int, column: int):
        super().__init__()
        self.__table_view = table_view
        self.__row, self.__column = row, column
        self.__original_row, self.__original_column = None, None

    def execute(self) -> bool:
        if super().execute():
            self.__original_row = self.__table_view.currentRow()
            self.__original_column = self.__table_view.currentColumn()
            self.__table_view.setFocusCell(self.__row, self.__column)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            self.__table_view.setFocusCell(self.__original_row, self.__original_column)
            return True
        else:
            return False
