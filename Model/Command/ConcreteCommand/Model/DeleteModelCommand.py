from Model.Command.AbstractCommand import *
from Utility.TableInterface.Model.MyTableModel import *


class DeleteModelCommand(AbstractCommand):
    def __init__(self, table_model: Type[MyTableModel], idx: int):
        super().__init__()
        self.__table_model = table_model
        self.__idx = idx
        self.__original_data = None

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 삭제중')
            self.__original_data = self.__table_model.getData(self.__idx)
            self.__table_model.deleteData(self.__idx)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 삭제 취소중')
            self.__table_model.insertData(self.__idx, self.__original_data)
            return True
        else:
            return False
