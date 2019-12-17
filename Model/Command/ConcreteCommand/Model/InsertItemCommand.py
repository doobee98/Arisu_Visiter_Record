from Model.Command.AbstractCommand import *
from Model.Table.Abstract.AbstractTableModel import *

"""
InsertItemCommand
"""


class InsertItemCommand(AbstractCommand):
    @overload
    def __init__(self, table_model: AbstractTableModel, idx: int, item: AbstractTableItemModel):
        pass

    @overload
    def __init__(self, table_model: AbstractTableModel, idx: int, field_data_dict: Dict[str, str]):
        pass

    def __init__(self, table_model: AbstractTableModel, idx: int, args):
        super().__init__()
        self.__table_model = table_model
        self.__idx = idx
        self.__args = args

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 삽입중')
            self.__table_model.insertItem(self.__idx, self.__args)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 추가 취소중')
            self.__table_model.removeItem(self.__idx)
            return True
        else:
            return False
