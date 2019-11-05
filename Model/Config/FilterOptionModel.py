from Model.Config.AbstractOptionModel import *
from Utility.Config.RecordFieldViewConfig import *
from Utility.File.FilePathConfig import *


class FilterOptionModel(AbstractOptionModel):
    class FilterFunction:
        def trimOutSpace(text: str) -> str:
            return text.strip()

        def trimAllSpace(text: str) -> str:
            return text.replace(' ', '')

        def upperEnglish(text: str) -> str:
            return text.upper()

        def onlyNumber(text: str) -> str:
            return "".join(filter(str.isdigit, text))

        # def time(text: str) -> str:
        #     split = text.split(':')
        #     for number_string in split:
        #         while len(number_string) < 2:
        #             number_string = '0' + number_string
        #     return ":".join(split)

    def __init__(self):
        directory, file_name = FilePathConfig.getConfigPath('FilterConfig')
        field_list = list(RecordFieldViewConfig.FieldsDictionary.keys())
        super().__init__(file_name, field_list)
        self.__printed_dict = {field: field for field in field_list}
        self.setDirectory(directory)

        default_dict = {field: [True for i in range(len(FilterOptionModel.definedFunctionList(field)))]
                        for field in field_list}
        self._setDefaultOptions(MyModel(default_dict))
        self._setCloseFieldList(field_list)

        if self.hasFile():
            self.load()
            for field_iter in default_dict.keys():
                if not self._getOptionList().hasField(field_iter):
                    self._getOptionList()._setProperty(field_iter, default_dict[field_iter])
        else:
            self._setOptionList(self.getDefaultOptions())
            self.update()

    def fieldPrintText(self, field: str) -> str:
        return self.__printed_dict[field]

    @classmethod
    def functionPrintText(cls, func: Callable[[str], str]) -> str:
        F = cls.FilterFunction
        if func == F.trimOutSpace:
            return '양옆 공백 제거'
        elif func == F.trimAllSpace:
            return '모든 공백 제거'
        elif func == F.upperEnglish:
            return '영어는 대문자만'
        elif func == F.onlyNumber:
            return '숫자만 입력 가능'
        # elif func == F.time:
        #     return '24시 시간(hh:mm)'
        else:
            ErrorLogger.reportError('잘못된 인자: ' + func.__name__, EOFError)

    def activeList(self, field: str) -> List[bool]:
        return self._getOptionList().getProperty(field)

    def activeFunctionList(self, field: str) -> List[Callable[[str], str]]:
        defined_list = FilterOptionModel.definedFunctionList(field)
        filter_list = [func for idx, func in enumerate(defined_list) if self.activeList(field)[idx] is True]
        return filter_list

    @classmethod
    def definedFunctionList(cls, field: str) -> List[Callable[[str], str]]:
        return FilterOptionModel.filterDictionary().get(field)

    @classmethod
    def filterDictionary(cls) -> Dict[str, List[Callable[[str], str]]]:
        F = cls.FilterFunction
        return {
            '출입증번호': [F.trimAllSpace, F.upperEnglish],
            '성명': [F.trimAllSpace, F.upperEnglish],
            '생년월일': [F.trimAllSpace, F.onlyNumber],
            '차량번호': [F.trimAllSpace],
            '소속': [F.trimOutSpace],
            '방문목적': [F.trimOutSpace],
            '반출입물품명': [F.trimOutSpace],
            '반입/반출량': [F.trimOutSpace],
            '비고': [F.trimOutSpace],
            '들어오다시간': [F.trimAllSpace],  #, F.time],
            '들어오다근무자': [F.trimAllSpace, F.upperEnglish],
            '나가다시간': [F.trimAllSpace],  #, F.time],
            '나가다근무자': [F.trimAllSpace, F.upperEnglish],
            '고유번호': [F.trimAllSpace, F.upperEnglish],
            '인수인계': [F.trimOutSpace]
        }
