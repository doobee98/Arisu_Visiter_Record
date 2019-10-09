
from Utility.File.FileNameConfig import *
from Model.Config.AbstractOptionModel import *

# todo: fieldview config와 fieldmodel config를 어떻게 할지, 그룹을 어떻게 할지
class TotalOptionModel(AbstractOptionModel):
    def __init__(self):
        file_name = FileNameConfig.getConfigName('TotalConfig')
        self.__printed_dict = {
            #'showing_id': '고유번호를 보이기',
            'base_font_size': '표 글씨 크기',
            'head_location': '지역',
            'tail_location': '근무지'
        }
        field_list = list(self.__printed_dict.keys())
        super().__init__(file_name, field_list)
        if self.isFileExist():
            self._load()
        else:
            # todo: 임시로 대충 만듦
            print('cannot find file')
            proto = MyModel({
                #'showing_id': True,
                'base_font_size': 12,
                'head_location': None,
                'tail_location': None
            })
            self._setOptionList(proto)
            self.update()

    def fieldPrintText(self, field: str) -> str:
        return self.__printed_dict[field]

    # def idShowEnable(self) -> bool:
    #     return self._getOptionList().getProperty('showing_id')
    #
    # def setIdShowEnable(self, enable: bool) -> None:
    #     self._getOptionList().changeProperty('showing_id', enable)

    def baseFontSize(self) -> int:
        return int(self._getOptionList().getProperty('base_font_size'))

    def setBaseFontSize(self, font_size: int) -> None:
        self._getOptionList().changeProperty('base_font_size', str(font_size))

    def location(self) -> str:
        head = self._getOptionList().getProperty('head_location')
        tail = self._getOptionList().getProperty('tail_location')
        if head is None or tail is None:
            return None
        else:
            return head + ' ' + tail

    def setHeadLocation(self, head_location: str) -> None:
        self._getOptionList().changeProperty('head_location', head_location)

    def setTailLocation(self, tail_location: str) -> None:
        self._getOptionList().changeProperty('tail_location', tail_location)






