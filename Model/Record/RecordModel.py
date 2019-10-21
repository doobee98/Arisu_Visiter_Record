from Utility.Config.RecordFieldModelConfig import *
from Utility.Abstract.Model.MyModel import *


class RecordModelSignal(MyModelSignal):
    StateChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class RecordModel(MyModel):
    """
    RecordModel
    * TakeOverRecord가 존재함
    """
    IdDefaultString = '* 신규 *'

    class State(Enum):
        """
            RecordModel.State: Enum class
            Default State: Generated
            Generated: 생성만 되어 있음, 비어있을 수 있으며, 기록부에 등재되지 않았을 수 있음
            Inserted: 기록부에 등재됨. 일반적으로 '들어오다'버튼을 통해 입력된 상태
            Finished: '나가다'버튼을 통해 일반적으로 더이상 편집할 일이 없는 상태
        """
        Generated = auto()
        Inserted = auto()
        Finished = auto()
        DefaultState = Generated

    def __init__(self, property_dict: Dict[str, AbstractModel.AttrType]):
        self.__state: RecordModel.State = RecordModel.State.DefaultState
        super().__init__(property_dict)
        self._setSignalSet(RecordModelSignal(self))
        self._adjustState() # todo: deserialize할때도 저 함수를 호출해야 할까

    @classmethod
    def initNull(cls) -> 'RecordModel':
        return RecordModel({field: None for field in RecordFieldModelConfig.FieldsDictionary.keys()})

    """
    MyOverride
    * _initWithStr
    * __str__
    * getSignalSet
    * changeProperty, changeProperties
    """
    def getSignalSet(self) -> RecordModelSignal:
        return super().getSignalSet()

    def changeProperty(self, field: str, property: str) -> bool:
        if super().changeProperty(field, property) is True:
            self._adjustState()
            # if field == '고유번호':
            #     self.getSignalSet().IdPropertyChanged.emit()
            return True
        else:
            return False

    def changeProperties(self, property_dict: Dict[str, str]) -> bool:
        if super().changeProperties(property_dict) is True:
            self._adjustState()
            # if '고유번호' in property_dict.keys():
            #     self.getSignalSet().IdPropertyChanged.emit()
            return True
        else:
            return False

    """
    property
    * state
    """
    def getState(self) -> State:
        return self.__state

    def _setState(self, state: State) -> None:
        self.__state = state

    def _adjustState(self):
        """
        __state를 __property_dict에 맞춰서 변경함
            Generated: inserted_field와 finished_field가 모두 비어있을 때 - 들어오다도 누르지 않음
            Inserted: inserted_field는 채워져있고 finished_field는 비어있을 때 - 들어오다는 눌렀으나 나가다는 누르지 않음
            Finished: finished_field가 채워져 있을 때 or 인수인계 기록일때 - 인수인계나 나가다를 누름
        """
        state_adjusted = RecordModel.State.Generated

        if self.isTakeoverRecord():
            # 인수인계 데이터라면 State를 Finished로 바꿈
            state_adjusted = RecordModel.State.Finished
        else:
            for field_iter in self.getProperties().keys():
                if RecordFieldModelConfig.getOption(field_iter, 'finish_field') is True:
                    if self.getProperty(field_iter) != RecordModel.DefaultString:
                        state_adjusted = RecordModel.State.Finished
                        break
                if RecordFieldModelConfig.getOption(field_iter, 'insert_field') is True:
                    if self.getProperty(field_iter) != RecordModel.DefaultString:
                        state_adjusted = RecordModel.State.Inserted

        if self.getState() != state_adjusted:
            self._setState(state_adjusted)
            self.getSignalSet().Updated.emit()

    """
    method
    * isTakeoverRecord
    * isRemainAtTime
    """
    def isTakeoverRecord(self) -> bool:
        take_over_string = self.getProperties().get('인수인계')
        return take_over_string != RecordModel.DefaultString and take_over_string is not None
        #return self.getProperty('인수인계') != RecordModel.DefaultString and self.getProperty('인수인계') != None

    def isRemainAtTime(self, time: str) -> bool:
        arrive_time = self.getProperty('들어오다시간')
        leave_time = self.getProperty('나가다시간')
        if not arrive_time:
            return True
        else:
            if leave_time:
                return time > arrive_time and time <= leave_time
            else:
                return time > arrive_time
