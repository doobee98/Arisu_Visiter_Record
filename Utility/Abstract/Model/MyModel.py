from Utility.Abstract.Model.AbstractModel import *


class MyModelSignal(QObject):
    """
    MyModelSignal
    Updated: setProperty, setProperties 등을 통해 Model의 Property가 변경되었을때 방출
    """
    Updated = pyqtSignal()
    DataChanged = pyqtSignal(dict)  # Dict[str, Tuple[str, str]]

    def __init__(self, parent=None):
        super().__init__(parent)


class MyModel(AbstractModel):
    """
    MyModel: Abstract Class
    __signal_set
    __property_dict: field를 key로 하고, property를 value로 하는 데이터 셋. field는 각 FieldModelConfig를 중심으로 함.
    """
    DefaultString = ''  # property 기본값

    def __init__(self, property_dict: Dict[str, AbstractModel.AttrType]):
        """
        :param args: property_dict 또는 str을 인자로 받음.
                property_dict: 인자를 바탕으로 model 초기화
                str: __initWithStr에 주어진 규약을 통해 model 초기화
        """
        super().__init__()
        self._setSignalSet(MyModelSignal(self))
        self.__property_dict: Dict[str, AbstractModel.AttrType] = {}

        for field in property_dict.keys():
            self._setProperty(field, property_dict[field])

    @classmethod
    def initNull(cls) -> 'MyModel':
        return MyModel({})

    """
    property
    * signalSet
    * propertyList (properties)
    * property
    """
    def getSignalSet(self) -> MyModelSignal:  # override
        return super().getSignalSet()

    def getProperties(self) -> Dict[str, AbstractModel.AttrType]:
        return self.__property_dict.copy()

    def getProperty(self, field: str) -> AbstractModel.AttrType:
        if field not in self.getProperties().keys():
            ErrorLogger.reportError(f'존재하지 않는 필드에 대한 읽기 요청입니다. {field}', AttributeError)
        return self.getProperties()[field]

    def _setProperty(self, field: str, property: AbstractModel.AttrType) -> None:
        self.__property_dict[field] = property
        self.update()

    """
    method
    * hasField
    * changeProperty, changeProperties <signal DataChanged>
    * update <signal Updated>
    """
    def hasField(self, field: str) -> bool:
        return field in self.getProperties().keys()

    def changeProperty(self, field: str, property: AbstractModel.AttrType) -> bool:
        """
        field의 property가 기존 데이터와 다를 경우 변경함.
        :return: 변경에 성공하면 True, 실패하면 False
        """
        old_property, new_property = self.getProperty(field), property
        if old_property != new_property:

            self._setProperty(field, new_property)
            self.getSignalSet().DataChanged.emit({field: (new_property, old_property)})
            return True
        else:
            return False

    def changeProperties(self, property_dict: Dict[str, AbstractModel.AttrType]) -> bool:
        """
        두 개 이상의 property를 바꿔야 할 때, setProperty를 사용하면
        adjustState와 propertyChanged가 여러번 호출되며 오버헤드 및 오작동 가능성이 있어서
        별도의 함수로 정의
        :return: 하나라도 변경에 성공하면 True, 실패하면 False
        """

        changed_dict: Dict[str, Tuple[AbstractModel.AttrType, AbstractModel.AttrType]] = {}
        self.blockSignals(True)
        for field, new_property in property_dict.items():
            old_property = self.getProperty(field)
            if self.changeProperty(field, new_property) is True:
                changed_dict[field] = (new_property, old_property)
        self.blockSignals(False)

        if changed_dict:
            self.update()
            self.getSignalSet().DataChanged.emit(changed_dict)
            return True
        else:
            return False

    def update(self) -> None:
        self.getSignalSet().Updated.emit()



