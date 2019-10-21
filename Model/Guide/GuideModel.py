from Model.Guide.RegexModel import *
from typing import List
from PyQt5.QtCore import QObject


class GuideModelSignal(QObject):
    Updated = pyqtSignal(int)
    def __init__(self, parent=None):
        super().__init__(parent)

class GuideModel(AbstractModel):
    def __init__(self):
        super().__init__()
        self._setSignalSet(GuideModelSignal(self))
        self.__regex_list: List[RegexModel] = []
        self.__exception_list: List[str] = []

    @classmethod
    def initNull(cls) -> 'GuideModel':
        return GuideModel()

    def getSignalSet(self) -> 'GuideModelSignal':
        return super().getSignalSet()

    def regexList(self) -> List[RegexModel]:
        return self.__regex_list

    def andRegexList(self) -> List[RegexModel]:
        return [regex for regex in self.__regex_list if regex.patternType() == RegexModel.Type.AND]

    def orRegexList(self) -> List[RegexModel]:
        return [regex for regex in self.__regex_list if regex.patternType() == RegexModel.Type.OR]

    def addRegex(self, regex: RegexModel) -> None:
        self.__regex_list.append(regex)
        regex.getSignalSet().Updated.connect(self.regexChanged)

    def removeRegex(self, regex: RegexModel) -> None:
        self.__regex_list.remove(regex)

    def exceptionList(self) -> List[str]:
        return self.__exception_list

    def addException(self, exception: str) -> None:
        self.__exception_list.append(exception)

    def removeException(self, exception: str) -> None:
        self.__exception_list.remove(exception)

    def isValid(self, text: str) -> bool:
        if text in self.__exception_list:
            return True

        for regex_iter in self.andRegexList():
            if not regex_iter.isValid(text):
                return False

        for regex_iter in self.orRegexList():
            if regex_iter.isValid(text):
                return True

        return False

    @MyPyqtSlot()
    def regexChanged(self) -> None:
        idx = self.__regex_list.index(self.sender().parent())
        if idx is None:
            ErrorLogger.reportError('Why this data is connected to table model?')
        else:
            self.getSignalSet().Updated.emit(idx)
            #self.update()
            return

    # todo deserialize 오버라이딩 필요 (regex 연결)
