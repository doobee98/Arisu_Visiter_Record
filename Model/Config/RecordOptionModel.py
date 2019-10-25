
from Utility.File.FilePathConfig import *
from Model.Config.AbstractOptionModel import *

# todo: fieldview config와 fieldmodel config를 어떻게 할지, 그룹을 어떻게 할지
class RecordOptionModel(AbstractOptionModel):
    def __init__(self):
        directory, file_name = FilePathConfig.getConfigPath('RecordConfig')
        self.__printed_dict = {
            'showing_id': '고유번호를 보이기',
            'enable_fix_id': '고유번호 수정 가능',
            'completer_from_db': '데이터베이스에서 자동완성 텍스트 가져오기\n(한글 반응성은 좋지 않습니다.)',
            'auto_update_db_with_leave': '[나가기] 클릭시 데이터베이스 자동 업데이트\n(사용 시 프로그램 속도가 저하됩니다.)'
            #'base_font_size': '표 글씨 크기'
        }
        field_list = list(self.__printed_dict.keys())
        super().__init__(file_name, field_list)
        self.setDirectory(directory)

        default_dict = {
            'showing_id': True,
            'enable_fix_id': False,
            'completer_from_db': True,
            'auto_update_db_with_leave': True
        }
        self._setDefaultOptions(MyModel(default_dict))

        if self.hasFile():
            self.load()
            for field_iter in default_dict.keys():
                if not self._getOptionList().hasField(field_iter):
                    self._getOptionList()._setProperty(field_iter, default_dict[field_iter])
        else:
            self._setOptionList(self.getDefaultOptions())
            self.update()

    def enableShowId(self) -> bool:
        return self._getOptionList().getProperty('showing_id')

    def setEnableShowId(self, enable: bool) -> None:
        self._getOptionList().changeProperty('showing_id', enable)

    def enableFixId(self) -> bool:
        return self._getOptionList().getProperty('enable_fix_id')

    def setEnableFixId(self, enable: bool) -> None:
        self._getOptionList().changeProperty('enable_fix_id', enable)

    def enableCompleterFromDB(self) -> bool:
        return self._getOptionList().getProperty('completer_from_db')

    def setEnableCompleterFromDB(self, enable: bool) -> None:
        self._getOptionList().changeProperty('completer_from_db', enable)

    def autoUpdateDB(self) -> bool:
        return self._getOptionList().getProperty('auto_update_db_with_leave')

    def setAutoUpdateDB(self, enable: bool) -> None:
        self._getOptionList().changeProperty('auto_update_db_with_leave', enable)

    # def baseFontSize(self) -> int:
    #     return int(self._getOptionList().getProperty('base_font_size'))
    #
    # def setBaseFontSize(self, font_size: int) -> None:
    #     self._getOptionList().changeProperty('base_font_size', str(font_size))

    def fieldPrintText(self, field: str) -> str:
        return self.__printed_dict[field]
