from Model.Command.AbstractCommand import *
from Utility.Abstract.Model.MyTableModel import *


class AddModelCommand(AbstractCommand):
    def __init__(self, table_model: MyTableModel, property_dict: Dict[str, str]):
        super().__init__()
        self.__table_model = table_model
        self.__property_dict = property_dict

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 추가중')
            data_type = self.__table_model.getDataType()
            self.__table_model.addData(data_type(self.__property_dict))
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 추가 취소중')
            self.__table_model.deleteData(self.__table_model.getDataCount() - 1)
            return True
        else:
            return False
