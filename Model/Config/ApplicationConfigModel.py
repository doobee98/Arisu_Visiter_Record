from Model.Config.AbstractConfigModel import *
from Model.Table.Field.TableFieldModel import *

"""
ApplicationConfigModel(AbstractConfigModel)
어플리케이션 전역적인 설정을 다룸
"""


class ApplicationConfigModel(AbstractConfigModel):
    class OptionName(Enum):
        PointSize = '글씨 사이즈'
        MajorLocation = '지역'
        MinorLocation = '근무지'
        AlertRemove = '삭제시 알림 여부'
        SaveDeadline = '데이터베이스 저장 기간'
        EnableShortCut = '단축키 사용'

    def __init__(self, file_path: str):
        super().__init__(file_path)

    """
    advanced property
    * option (하단에 각각의 설정에 대한 getter와 setter가 주어지지만, 옵션을 일괄적으로 처리하고 싶을때 사용하면 되는 메소드)
    * pointSize
    * majorLocation, minorLocation
    * enableAlertRemove
    * saveDeadline
    * enableShortCut
    * location
    """
    def option(self, option_enum: OptionName) -> AbstractConfigModel.AttrType:
        return self._option(option_enum.value)

    def setOption(self, option_enum: OptionName, data: AbstractConfigModel.AttrType) -> None:
        self._setOption(option_enum.value, data)

    def pointSize(self) -> int:
        return int(self._option(ApplicationConfigModel.OptionName.PointSize.value))

    def setPointSize(self, point_size: int) -> None:
        self._setOption(ApplicationConfigModel.OptionName.PointSize.value, str(point_size))

    def majorLocation(self) -> str:
        return self._option(ApplicationConfigModel.OptionName.MajorLocation.value)

    def setMajorLocation(self, major_location: str) -> None:
        self._setOption(ApplicationConfigModel.OptionName.MajorLocation.value, major_location)

    def minorLocation(self) -> str:
        return self._option(ApplicationConfigModel.OptionName.MinorLocation.value)

    def setMinorLocation(self, minor_location: str) -> None:
        self._setOption(ApplicationConfigModel.OptionName.MinorLocation.value, minor_location)

    def enableAlertRemove(self) -> bool:
        return self._option(ApplicationConfigModel.OptionName.AlertRemove.value)

    def setEnableAlertRemove(self, enable: bool) -> None:
        self._setOption(ApplicationConfigModel.OptionName.AlertRemove.value, enable)

    def saveDeadline(self) -> int:
        return int(self._option(ApplicationConfigModel.OptionName.SaveDeadline.value))

    def setSaveDeadline(self, save_deadline: int) -> None:
        self._setOption(ApplicationConfigModel.OptionName.SaveDeadline.value, str(save_deadline))

    def enableShortCut(self) -> bool:
        return self._option(ApplicationConfigModel.OptionName.EnableShortCut.value)

    def setEnableShortCut(self, enable: bool) -> None:
        self._setOption(ApplicationConfigModel.OptionName.EnableShortCut.value, enable)

    def location(self) -> str:
        if self.majorLocation() and self.minorLocation():
            return self.majorLocation() + ' ' + self.minorLocation()
        else:
            return None

    """
    override
    * initNull
    * setDefault
    """
    @classmethod
    def initNull(cls) -> 'ApplicationConfigModel':
        return ApplicationConfigModel('')

    def setDefault(self) -> None:
        self.setBlockUpdate(True)
        self.setPointSize(11)
        self.setMajorLocation(None)
        self.setMinorLocation(None)
        self.setEnableAlertRemove(True)
        self.setEnableShortCut(True)
        self.setSaveDeadline(90)
        self._setCloseOptionNameList([ApplicationConfigModel.OptionName.PointSize.value,
                                      ApplicationConfigModel.OptionName.MajorLocation.value,
                                      ApplicationConfigModel.OptionName.MinorLocation.value,
                                      ApplicationConfigModel.OptionName.EnableShortCut.value])
        self.setBlockUpdate(False)
        self.save()
