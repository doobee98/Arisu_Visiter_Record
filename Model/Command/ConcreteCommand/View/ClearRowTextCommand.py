from Model.Command.AbstractCommand import *
from View.Table.AbstractTableView import *

"""
ClearRowText
- 해당 열의 텍스트를 비움. SetRowText와는 다르게 모델 변화 시그널을 방출하지 않음.
"""


class ClearRowTextCommand(AbstractCommand):
    def __init__(self, table_view: AbstractTableView, row: int):
        super().__init__()
        self.__table_view = table_view
        self.__row = row
        self.__original_row_text_dict = None

    def execute(self) -> bool:
        if super().execute():
            self.__original_row_text_dict = self.__table_view.rowTextDictionary(self.__row)
            self.__table_view.clearRowTexts(self.__row)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            self.__table_view.setRowTexts(self.__row, self.__original_row_text_dict)
            return True
        else:
            return False
