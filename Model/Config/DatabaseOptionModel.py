
from Utility.File.FileNameConfig import *
from Model.Config.AbstractOptionModel import *

# todo: fieldview config와 fieldmodel config를 어떻게 할지, 그룹을 어떻게 할지
class DatabaseOptionModel(AbstractOptionModel):
    def __init__(self):
        file_name = FileNameConfig.getConfigName('DatabaseConfig')
        self.__printed_dict = {
            'showing_id': '고유번호를 보이기',
            'enable_fix_id': '고유번호 수정 가능',
            #'base_font_size': '표 글씨 크기',
            'save_deadline': '최대 저장 기간(일)'
        }
        field_list = list(self.__printed_dict.keys())
        super().__init__(file_name, field_list)
        if self.isFileExist():
            self._load()
        else:
            # todo: 임시로 대충 만듦
            print('cannot find file')
            proto = MyModel({
                'showing_id': True,
                'enable_fix_id': False,
                #'base_font_size': 12,
                'save_deadline': 90
            })
            self._setOptionList(proto)
            self.update()

    def fieldPrintText(self, field: str) -> str:
        return self.__printed_dict[field]

    def enableShowId(self) -> bool:
        return self._getOptionList().getProperty('showing_id')

    def setEnableShowId(self, enable: bool) -> None:
        self._getOptionList().changeProperty('showing_id', enable)

    def enableFixId(self) -> bool:
        return self._getOptionList().getProperty('enable_fix_id')

    def setEnableFixId(self, enable: bool) -> None:
        self._getOptionList().changeProperty('enable_fix_id', enable)

    # def baseFontSize(self) -> int:
    #     return int(self._getOptionList().getProperty('base_font_size'))
    #
    # def setBaseFontSize(self, font_size: int) -> None:
    #     self._getOptionList().changeProperty('base_font_size', str(font_size))

    def saveDeadLine(self) -> int:
        return int(self._getOptionList().getProperty('save_deadline'))

    def setSaveDeadline(self, save_deadline: int) -> None:
        self._getOptionList().changeProperty('save_deadline', str(save_deadline))
