from PyQt5.QtCore import *
from os.path import isfile
from Utility.Log.ErrorLogger import *
from Utility.Module.ConfigModule import *
from Model.AbstractSerializeModel import *

"""
DeliveryModel
전달사항 데이터를 저장하기 위한 모델
location(지역)과 text(전달사항) 두 개의 유효 데이터를 가지고 있다.
"""


class DeliveryModel(AbstractSerializeModel):
    def __init__(self, location: str):
        super().__init__()
        self.setFilePath(ConfigModule.FilePath.deliveryFilePath(location))
        self.__location = location
        self.__text = ''
        if self.hasFile():
            self.load()
        else:
            self.save()

    """
    property
    * location
    * text
    """
    def location(self) -> str:
        return self.__location

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        self.update()



