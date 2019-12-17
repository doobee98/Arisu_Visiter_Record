from Model.Config.AbstractConfigModel import *
from Model.Table.Field.TableFieldModel import *

"""
HiddenConfigModel(AbstractConfigModel)
설정 창에 드러나지 않는 숨겨진 설정값들을 다룸
"""


class HiddenConfigModel(AbstractConfigModel):
    class OptionName(Enum):
        CurrentWorker = '현재 근무자'
        WindowGeometry = '윈도우 위치'
        RecordFieldOrder = '기록부 필드순서'
        DatabaseFieldOrder = '데이터베이스 필드순서'

    def __init__(self, file_path: str):
        super().__init__(file_path)

    """
    advanced property
    * option
    * currentWorker
    * windowGeometry
    * databaseVisualIndexes, recordVisualIndexes
    """ # todo FieldOrderList 작업할것
    def option(self, option_name: OptionName) -> AbstractConfigModel.AttrType:
        return self._option(option_name.value)

    def setOption(self, option_name: OptionName, data: AbstractConfigModel.AttrType) -> None:
        self._setOption(option_name.value, data)

    def currentWorker(self) -> str:
        return self._option(HiddenConfigModel.OptionName.CurrentWorker.value)

    def setCurrentWorker(self, current_worker: str) -> None:
        self._setOption(HiddenConfigModel.OptionName.CurrentWorker.value, current_worker)

    def windowGeometry(self) -> Tuple[int, int]:
        return self._option(HiddenConfigModel.OptionName.WindowGeometry.value)

    def setWindowGeometry(self, window_x: int, window_y: int) -> None:
        self._setOption(HiddenConfigModel.OptionName.WindowGeometry.value, (window_x, window_y))

    def databaseFieldOrder(self) -> List[str]:
        return self._option(HiddenConfigModel.OptionName.DatabaseFieldOrder.value)

    def setDatabaseFieldOrder(self, field_order: List[str]) -> None:
        self._setOption(HiddenConfigModel.OptionName.DatabaseFieldOrder.value, field_order)

    def recordFieldOrder(self) -> List[str]:
        return self._option(HiddenConfigModel.OptionName.RecordFieldOrder.value)

    def setRecordFieldOrder(self, field_order: List[str]) -> None:
        self._setOption(HiddenConfigModel.OptionName.RecordFieldOrder.value, field_order)

    """
    override
    * initNull
    * setDefault
    """
    @classmethod
    def initNull(cls) -> 'HiddenConfigModel':
        return HiddenConfigModel('')

    def setDefault(self) -> None:
        self.setBlockUpdate(True)
        self.setCurrentWorker('근무자')
        self.setWindowGeometry(0, 0)
        self.setDatabaseFieldOrder([])  # todo
        self.setRecordFieldOrder([])
        self.setBlockUpdate(False)
        self.save()
