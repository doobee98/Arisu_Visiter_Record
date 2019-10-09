from Model.Command.AbstractCommand import *
from Utility.TableInterface.Model.MyTableModel import *


class InsertModelCommand(AbstractCommand):
    def __init__(self, table_model: Type[MyTableModel], idx: int, property_dict: Dict[str, str]):
        super().__init__()
        self.__table_model = table_model
        self.__idx = idx
        self.__property_dict = property_dict

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 삽입중')
            data_type = self.__table_model.getDataType()
            self.__table_model.insertData(self.__idx, data_type(self.__property_dict))
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 삽입 취소중')
            self.__table_model.deleteData(self.__idx)
            return True
        else:
            return False
