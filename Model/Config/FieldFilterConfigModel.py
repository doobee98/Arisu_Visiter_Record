from Model.Config.AbstractConfigModel import *
from Model.Table.Field.TableFieldModel import *

"""
FieldFilterConfigModel(AbstractConfigModel)
LineEdit에 입력할 때 사용자의 입력을 필터링해주는 함수 목록을 관리함.
"""
# todo - 테이블 필드가 변경되면 여기에서도 변경되어야 함.

class FieldFilterConfigModel(AbstractConfigModel):
    class FilterFunction(Enum):
        TrimOutSpace = '양옆 공백 제거'
        TrimAllSpace = '모든 공백 제거'
        UpperEnglish = '영어는 대문자만'
        OnlyNumber = '숫자만 입력가능'

        def function(self) -> Callable[[str], str]:
            if self == FieldFilterConfigModel.FilterFunction.TrimOutSpace:
                return lambda text: text.strip()
            elif self == FieldFilterConfigModel.FilterFunction.TrimAllSpace:
                return lambda text: text.replace(' ', '')
            elif self == FieldFilterConfigModel.FilterFunction.UpperEnglish:
                return lambda text: text.upper()
            else:  # self == FieldFilterConfigModel.FilterFunction.OnlyNumber
                return lambda text: "".join(filter(str.isdigit, text))

    def __init__(self, file_path: str):
        super().__init__(file_path)

    """
    advanced property
    * filterFunctionList
    * filterFunctionEnumList
    """
    def filterFunctionEnumList(self, field_name: str) -> List[FilterFunction]:
        if field_name in self._optionNameList():
            return self._option(field_name)
        else:
            return []

    def filterFunctionList(self, field_name: str) -> List[Callable[[str], str]]:
        return [enum_iter.function() for enum_iter in self.filterFunctionEnumList(field_name)]

    def setFilterFunctionList(self, field_name: str, filter_function_list: List[FilterFunction]) -> None:
        self._setOption(field_name, filter_function_list)
        self.update()

    def removeField(self, field_name: str) -> None:
        self._removeOption(field_name)

    """
    override
    * initNull
    * setDefault
    """
    @classmethod
    def initNull(cls) -> 'FieldFilterConfigModel':
        return FieldFilterConfigModel('')

    def setDefault(self) -> None:
        self.setBlockUpdate(True)
        F = FieldFilterConfigModel.FilterFunction
        default_dict = {
            TableFieldOption.Necessary.RECORD_ID: [F.TrimAllSpace, F.UpperEnglish],
            TableFieldOption.Necessary.NAME: [F.TrimAllSpace, F.UpperEnglish],
            TableFieldOption.Necessary.BIRTHDAY: [F.TrimAllSpace, F.OnlyNumber],
            TableFieldOption.Necessary.CAR_NUMBER: [F.TrimAllSpace],
            TableFieldOption.Necessary.COMPANY: [F.TrimOutSpace],
            TableFieldOption.Necessary.PURPOSE: [F.TrimOutSpace],
            '반출입\n물품명': [F.TrimOutSpace],
            '반입/반출량': [F.TrimOutSpace],
            '비고': [F.TrimOutSpace],
            TableFieldOption.Necessary.IN_TIME: [F.TrimAllSpace],
            TableFieldOption.Necessary.IN_WORKER: [F.TrimAllSpace, F.UpperEnglish],
            TableFieldOption.Necessary.OUT_TIME: [F.TrimAllSpace],
            TableFieldOption.Necessary.OUT_WORKER: [F.TrimAllSpace, F.UpperEnglish],
            TableFieldOption.Necessary.ID: [F.TrimAllSpace, F.UpperEnglish],
            TableFieldOption.Necessary.TAKEOVER: [F.TrimOutSpace],
            TableFieldOption.Necessary.DATE_FIRST: [F.TrimOutSpace],
            TableFieldOption.Necessary.DATE_RECENT: [F.TrimOutSpace]
        }
        for field_name_iter, filter_list_iter in default_dict.items():
            self.setFilterFunctionList(field_name_iter, filter_list_iter)
        self._setCloseOptionNameList(list(default_dict.keys()))

        self.setBlockUpdate(False)
        self.save()
