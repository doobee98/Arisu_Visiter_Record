from Model.Command.AbstractCommand import *
from Model.Table.Abstract.AbstractTableModel import *

"""
AddItemCommand
"""


class AddItemCommand(AbstractCommand):
    @overload
    def __init__(self, table_model: AbstractTableModel, item: AbstractTableItemModel):
        pass

    @overload
    def __init__(self, table_model: AbstractTableModel, field_data_dict: Dict[str, str]):
        pass

    def __init__(self, table_model: AbstractTableModel, args):
        super().__init__()
        self.__table_model = table_model
        self.__args = args

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 추가중')
            self.__table_model.addItem(self.__args)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 추가 취소중')
            self.__table_model.removeItem(self.__table_model.itemCount() - 1)
            return True
        else:
            return False
