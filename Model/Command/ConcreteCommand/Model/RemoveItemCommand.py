from Model.Command.AbstractCommand import *
from Model.Table.Abstract.AbstractTableModel import *

"""
RemoveItemCommand
"""


class RemoveItemCommand(AbstractCommand):
    def __init__(self, table_model: AbstractTableModel, idx: int):
        super().__init__()
        self.__table_model = table_model
        self.__idx = idx
        self.__original_item = None

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 삭제중')
            self.__original_item = self.__table_model.item(self.__idx)
            self.__table_model.removeItem(self.__idx)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 삭제 취소중')
            self.__table_model.insertItem(self.__idx, self.__original_item)
            return True
        else:
            return False
