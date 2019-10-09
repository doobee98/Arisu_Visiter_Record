from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import os
from typing import List
from Utility.TableInterface.Model.MyModel import *
from Utility.CryptListModule import *


class AbstractOptionModelSignal(QObject):
    OptionChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class AbstractOptionModel(QObject):
    """
    AbstractOptionModel
    str field와 그에 해당하는 value(str, bool)를 대입할 수 있음.
    관리 클래스로 MyModel 객체를 사용함(Dict[str, Union[str, bool]])
    """
    OptionType = Union[str, bool]

    def __init__(self, file_name: str, field_list: List[str]):
        super().__init__()
        self.__signal_set: Type[AbstractOptionModelSignal] = AbstractOptionModelSignal(self)
        self.__file_name: str = file_name
        self.__field_list: List[str] = field_list
        self.__options: MyModel = None
        #self._load()

    def getSignalSet(self) -> Type[AbstractOptionModelSignal]:
        return self.__signal_set

    def _setSignalSet(self, signal_set: Type[AbstractOptionModelSignal]) -> None:
        self.__signal_set = signal_set

    def _getFileName(self) -> str:
        return self.__file_name

    def _setFileName(self, file_name: str) -> None:
        self.__file_name = file_name

    def isFileExist(self) -> bool:
        return self._getFileName() and os.path.isfile(self._getFileName())

    def getFieldList(self) -> List[str]:
        return self.__field_list.copy()

    def _setFieldList(self, field_list: List[str]) -> None:
        self.__field_list = field_list

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

    @pyqtSlot()
    def optionChanged(self) -> None:
        self.getSignalSet().OptionChanged.emit()
        self.update()

    def update(self) -> None:
        self.save()

    def save(self) -> None:
        cipher_list = CryptListModule.encrypt([self._getOptionList()]) # only one MyModel
        with open(self._getFileName(), 'wb') as f:
            for cipher_text in cipher_list:
                f.write(cipher_text + b'\n')

    def _load(self) -> None:
        if self.isFileExist():
            with open(self._getFileName(), 'rb') as f:
                cipher_list = f.readlines()
                option_object = CryptListModule.decrypt(cipher_list, MyModel)[0]  # only one MyModel
                self._setOptionList(option_object)
                self.update()  # 이전에 켰을때와 뭔가 바뀐게 있다면 저장하기위해서 로드 하자마자 저장함
        else:
            ErrorLogger.reportError(f'Cannot find file {self._getFileName()}.')

    def blockSignals(self, b: bool) -> bool:
        self.getSignalSet().blockSignals(b)
        return super().blockSignals(b)

