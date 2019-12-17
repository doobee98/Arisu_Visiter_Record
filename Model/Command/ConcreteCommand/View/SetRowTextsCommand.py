from Model.Command.AbstractCommand import *
from View.Table.AbstractTableView import *

"""
SetRowTextsCommand
"""


class SetRowTextsCommand(AbstractCommand):
    def __init__(self, table_view: AbstractTableView, row: int, text_dict: Dict[str, str]):
        super().__init__()
        self.__table_view = table_view
        self.__row = row
        self.__row_text_dict = text_dict
        self.__original_row_text_dict = None

    def execute(self) -> bool:
        if super().execute():
            current_dict = self.__table_view.rowTextDictionary(self.__row)
            self.__original_row_text_dict = {field_name_iter: current_dict[field_name_iter]
                                             for field_name_iter in self.__row_text_dict.keys()}
            self.__table_view.setRowTexts(self.__row, self.__row_text_dict)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            self.__table_view.setRowTexts(self.__row, self.__original_row_text_dict)
            return True
        else:
            return False
