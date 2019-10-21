import os
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Utility.Abstract.Model.MyModel import *
from Utility.CryptListModule import *


class AbstractOptionModelSignal(QObject):
    OptionChanged = pyqtSignal()
    CloseRequest = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class AbstractOptionModel(AbstractModel):
    """
    AbstractOptionModel
    str field와 그에 해당하는 value를 대입할 수 있음.
    관리 클래스로 MyModel 객체를 사용함(Dict[str, AttrType])
    """
    OptionType = AbstractModel.AttrType

    def __init__(self, file_name: str, field_list: List[str]):
        super().__init__()
        self._setSignalSet(AbstractOptionModelSignal(self))
        self.setDirectory('')
        self.setFileName(file_name)
        self.__field_list: List[str] = field_list
        self.__close_field_list: List[str] = []
        self.__options: MyModel = None
        self.__default_options: MyModel = None

    def getSignalSet(self) -> AbstractOptionModelSignal:
        return super().getSignalSet()

    def getFieldList(self) -> List[str]:
        return self.__field_list.copy()

    def _setFieldList(self, field_list: List[str]) -> None:
        self.__field_list = field_list

    def getCloseFieldList(self) -> List[str]:
        return self.__close_field_list.copy()

    def _setCloseFieldList(self, close_field_list: List[str]) -> None:
        self.__close_field_list = close_field_list

    def getDefaultOptions(self) -> MyModel:
        return self.__default_options

    def _setDefaultOptions(self, options: MyModel):
        self.__default_options = options

    def _getOptionList(self) -> MyModel:
        return self.__options

    def _setOptionList(self, options: MyModel) -> None:
        self.__options = options
        self.__options.getSignalSet().Updated.connect(self.optionChanged)

    def getOption(self, field: str) -> OptionType:
        return self._getOptionList().getProperty(field)

    def changeOption(self, field: str, property: OptionType) -> None:
        self._getOptionList().changeProperty(field, property)

    def changeOptions(self, option_dict: Dict[str, OptionType]) -> None:
        self._getOptionList().changeProperties(option_dict)

    @MyPyqtSlot()
    def optionChanged(self) -> None:
        self.update()
        self.getSignalSet().OptionChanged.emit()

    def update(self) -> None:
        self.save()

    def _deserialize(self, obj_str: str) -> None:
        super()._deserialize(obj_str)
        self.__options.getSignalSet().Updated.connect(self.optionChanged)


