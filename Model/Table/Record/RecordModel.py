from Model.Table.Abstract.AbstractTableItemModel import *
from Utility.Module.ConfigModule import *

"""
RecordModel(AbstractTableItemModel)
1. SearchState Property를 통해 RecordModel을 분류함
"""


class RecordModel(AbstractTableItemModel):
    IdDefaultValue = '* 신규 *'
    IdOverlapValue = '* 중복 *'

    class State(Enum):
        Basic = auto()
        Inserted = auto()
        Finished = auto()
        Takeover = auto()

    def __init__(self, field_data_dict: Dict[str, str], parent: QObject):
        super().__init__(field_data_dict, parent)

    """
    takeover initializer
    * createTakeover
    """
    @classmethod
    def createTakeoverRecord(cls, time: str, team: str, worker: str, name: str = None, name_count: int = 0) -> 'RecordModel':
        if name_count == 0:
            name_string = '인수대상 없음'
        elif name_count == 1:
            name_string = name + ' 인수인계'
        else:
            name_string = f'{name} 외 {name_count - 1}인 인수인계'
        takeover_string = f'{time} {name_string} - {team} {worker}'
        field_data_dict = {TableFieldOption.Necessary.TAKEOVER: takeover_string,
                           TableFieldOption.Necessary.IN_TIME: time,
                           TableFieldOption.Necessary.OUT_TIME: time}
        return RecordModel(field_data_dict, None)

    """
    advanced property
    * state
    """
    def state(self) -> State:
        if self.hasFieldData(TableFieldOption.Necessary.TAKEOVER):
            return RecordModel.State.Takeover
        elif self.hasFieldData(TableFieldOption.Necessary.OUT_TIME) or self.hasFieldData(TableFieldOption.Necessary.OUT_WORKER):
            return RecordModel.State.Finished
        elif self.hasFieldData(TableFieldOption.Necessary.IN_TIME) or self.hasFieldData(TableFieldOption.Necessary.IN_WORKER):
            return RecordModel.State.Inserted
        else:
            return RecordModel.State.Basic

    """
    override
    * initNull
    """
    @classmethod
    def initNull(cls) -> 'RecordModel':
        return RecordModel({}, None)


