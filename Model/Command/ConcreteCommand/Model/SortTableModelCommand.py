from Model.Command.AbstractCommand import *
from Utility.Abstract.Model.MyTableModel import *


class SortTableModelCommand(AbstractCommand):
    def __init__(self, table_model: MyTableModel, field: str):
        super().__init__()
        self.__table_model = table_model
        self.__field = field
        self.__original_id_idx_dict = None

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 정렬중')
            self.__original_id_idx_dict = {data.getProperty('고유번호'): idx
                                           for idx, data in enumerate(self.__table_model.getDataList())}
            self.__table_model.sortData(self.__field)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 정렬 취소중')
            self.__table_model.unsortData(self.__original_id_idx_dict)
            return True
        else:
            return False
