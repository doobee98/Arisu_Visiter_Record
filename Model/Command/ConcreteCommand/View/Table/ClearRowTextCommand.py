from Model.Command.AbstractCommand import *
from Utility.TableInterface.View.MyTableView import *


class ClearRowTextCommand(AbstractCommand):
    def __init__(self, table_view: Type[MyTableView], row: int):
        super().__init__()
        self.__table_view = table_view
        self.__row = row
        self.__original_row_text_dict = None

    def execute(self) -> bool:
        if super().execute():
            # todo text_dict는 부분만 바꾸는 반면에 original_text_dict는 그냥 전체를 다 가져와서 바꿔버림. 오버헤드 발생할 수 있음
            self.__original_row_text_dict = self.__table_view.getRowTexts(self.__row)
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
