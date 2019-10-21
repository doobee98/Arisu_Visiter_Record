import re
from enum import Enum, auto
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Utility.Abstract.Model.AbstractModel import *

class RegexModelSignal(QObject):
    Updated = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)

class RegexModel(AbstractModel):
    DefaultPattern = '<시작><끝>'

    class Type(Enum):
        AND = auto()
        OR = auto()

    def __init__(self, input_pattern: str = DefaultPattern,
                 *, pattern_type: Type = Type.OR, title: str = '새로운 패턴', invalid_message: str = None):
        super().__init__()
        self._setSignalSet(RegexModelSignal(self))
        self.__pattern_repr: str = input_pattern
        self.__pattern: str = self.__createPattern(input_pattern)
        self.__pattern_type: RegexModel.Type = pattern_type
        self.__title: str = title
        self.__invalid_message: str = invalid_message

    @classmethod
    def initNull(cls) -> 'RegexModel':
        return RegexModel()

    def getSignalSet(self) -> RegexModelSignal:
        return super().getSignalSet()

    def toRepr(self) -> str:
        return self.__pattern_repr

    def toString(self) -> str:
        return self.__pattern

    def setPattern(self, input_pattern: str) -> None:
        self.__pattern_repr = input_pattern
        self.__pattern = self.__createPattern(input_pattern)
        self.getSignalSet().Updated.emit()

    def patternType(self) -> Type:
        return self.__pattern_type

    def setPatternType(self, pattern_type: Type) -> None:
        self.__pattern_type = pattern_type
        self.getSignalSet().Updated.emit()


    def title(self) -> str:
        return self.__title

    def setTitle(self, title: str) -> None:
        self.__title = title
        self.getSignalSet().Updated.emit()

    def invalidMessage(self) -> str:
        return self.__invalid_message

    def setInvalidMessage(self, invalid_message: str) -> None:
        self.__invalid_message = invalid_message
        self.getSignalSet().Updated.emit()

    def isValid(self, text: str) -> bool:
        return bool(re.search(self.__pattern, text))

    def __createPattern(self, input_pattern: str) -> str:
        pattern_dict = {
            '<시작>': '^',
            '<끝>': '$',
            '<한>': '[가-힣]',
            '<영소>': '[a-z]',
            '<영대>': '[A-Z]',
            '<영>': '[a-zA-Z]',
            '<수>': '[0-9]',
            '<자연수>': '[1-9]',
            '<공백>': '( |\\t)'
        }
        new_pattern = input_pattern
        for custom_pattern in pattern_dict.keys():
            new_pattern = new_pattern.replace(custom_pattern, pattern_dict[custom_pattern])
        return new_pattern



