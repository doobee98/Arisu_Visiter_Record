from Model.Table.Abstract.AbstractTableModel import *
from Model.Table.Record.RecordModel import *
from Utility.Module.ConfigModule import *

"""
RecordTableModel(AbstractTableModel)
1. location과 date를 키로 하여 구분됨
2. load시 State가 Basic인 Record는 삭제하고 로드함
3. init시 file_path 또는 (location, date)를 받아서 초기화함
"""


class RecordTableModelSignal(AbstractTableModelSignal):
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class RecordTableModel(AbstractTableModel):
    @overload
    def __init__(self, file_path: str):
        pass

    @overload
    def __init__(self, location: str, date: str):
        pass

    def __init__(self, *args):
        if len(args) == 1:
            [file_path] = args
            [self.__location, self.__date] = ConfigModule.FilePath.fileNameToData(FileType.RecordTable, file_path)
            super().__init__(file_path)
        else:  # len(args) == 2
            [location, date] = args
            # custom 필드를 제외한 나머지 필드를 로딩함
            file_path = ConfigModule.FilePath.recordTableFilePath(location,date)
            self.__location: str = location
            self.__date: str = date
            super().__init__(file_path)

    """
    property
    * location, date
    """
    def location(self) -> str:
        return self.__location

    def date(self) -> str:
        return self.__date

    """
    advanced property
    * fieldNameList
    """
    def fieldNameList(self) -> List[str]:
        return [field_iter.name() for field_iter in ConfigModule.TableField.recordFieldModelList()
                if not field_iter.globalOption(TableFieldOption.Global.NoModelData)]

    """
    override
    * initNull
    * _createItem
    * load
    """
    @classmethod
    def initNull(cls) -> 'RecordTableModel':
        return RecordTableModel('', '')

    def _createItem(self, field_data_dict: Dict[str, str]) -> RecordModel:
        return RecordModel(field_data_dict, self)

    def load(self) -> None:
        super().load()
        delete_list = []
        for index, item_iter in enumerate(self.itemList()):
            if item_iter.state() == RecordModel.State.Basic:
                delete_list.append(index)
        for index in reversed(delete_list):
            self.removeItem(index)

    """
    return type override
    """
    def signalSet(self) -> RecordTableModelSignal:
        return super().signalSet()

    def itemList(self) -> List[RecordModel]:
        return super().itemList()

    def item(self, index: int) -> RecordModel:
        return super().item(index)

    def findItems(self, field_data_dict: Dict[str, str]) -> List[RecordModel]:
        return super().findItems(field_data_dict)

