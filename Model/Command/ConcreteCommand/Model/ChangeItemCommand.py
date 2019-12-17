from Model.Command.AbstractCommand import *
from Model.Table.Abstract.AbstractTableModel import *

"""
ChangeItemCommand
"""


class ChangeItemCommand(AbstractCommand):
    def __init__(self, table_model: AbstractTableModel, idx: int, field_data_dict: Dict[str, str]):
        super().__init__()
        self.__table_model = table_model
        self.__idx = idx
        self.__field_data_dict = field_data_dict
        self.__original_field_data_dict = None

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 변경중')
            item = self.__table_model.item(self.__idx)
            self.__original_field_data_dict = item.fieldDataDictionary()
            item.setFieldDatum(self.__field_data_dict)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 변경 취소중')
            item = self.__table_model.item(self.__idx)
            item.setFieldDatum(self.__original_field_data_dict)
            return True
        else:
            return False
