from Model.AbstractSerializeModel import *

"""
AbstractConfigModel(AbstractSerializeModel)
Config 파일을 담는 모델
1. 생성자 호출시 파일을 로드함
2. str 키를 통해 옵션 값들을 딕셔너리 형태로 관리함
3. setDefault method로 옵션의 초기값을 할당함
"""


class AbstractOptionModelSignal(QObject):
    OptionChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class AbstractConfigModel(AbstractSerializeModel):
    def __init__(self, file_path: str):
        super().__init__()
        self.setFilePath(file_path)
        self._setSignalSet(AbstractOptionModelSignal(self))
        self.__option_dict: Dict[str, AbstractSerializeModel.AttrType] = {}
        self.__close_option_name_list: List[str] = []

        if self.hasFile():
            self.load()
        else:
            self.setDefault()
            self.save()

    """
    property
    * _optionDict
    * closeOptionNameList
    """
    def _optionDictionary(self) -> Dict[str, AbstractSerializeModel.AttrType]:
        return self.__option_dict

    def closeOptionNameList(self) -> List[str]:
        return self.__close_option_name_list

    def _setCloseOptionNameList(self, option_list: List[str]) -> None:
        self.__close_option_name_list = option_list

    """
    advanced property
    * _optionNameList
    * _option (set, remove)
    """
    def _optionNameList(self) -> List[str]:
        return list(self._optionDictionary().keys())

    def _option(self, option_name: str) -> AbstractSerializeModel.AttrType:
        return self._optionDictionary()[option_name]

    def _setOption(self, option_name: str, option_value: AbstractSerializeModel.AttrType) -> None:
        self.__option_dict[option_name] = option_value
        self.update()

    def _removeOption(self, option_name: str) -> None:
        del self.__option_dict[option_name]
        self.update()

    """
    default setting
    * setDefault
    """
    def setDefault(self) -> None:
        raise NotImplementedError

    """
    override
    * update
    """
    def update(self) -> None:
        super().update()
        self.signalSet().OptionChanged.emit()

    """
    return type override
    """
    def signalSet(self) -> AbstractOptionModelSignal:
        return super().signalSet()
