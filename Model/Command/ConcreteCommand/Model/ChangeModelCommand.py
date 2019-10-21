from Model.Command.AbstractCommand import *
from Utility.Abstract.Model.MyTableModel import *


class ChangeModelCommand(AbstractCommand):
    def __init__(self, table_model: MyTableModel, idx: int, property_dict: Dict[str, str]):
        super().__init__()
        self.__table_model = table_model
        self.__idx = idx
        self.__property_dict = property_dict
        self.__original_property_dict = None

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 변경중')
            data = self.__table_model.getData(self.__idx)
            self.__original_property_dict = data.getProperties()
            data.changeProperties(self.__property_dict)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 변경 취소중')
            data = self.__table_model.getData(self.__idx)
            data.changeProperties(self.__original_property_dict)
            return True
        else:
            return False
