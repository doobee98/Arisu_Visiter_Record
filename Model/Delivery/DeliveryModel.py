from PyQt5.QtCore import *
from os.path import isfile
from Utility.CryptListModule import *
from Utility.Log.ErrorLogger import *
from Utility.File.FilePathConfig import *
from Utility.Abstract.Model.AbstractModel import *


class DeliveryModel(AbstractModel):
    def __init__(self, location: str):
        super().__init__()
        directory, file_name = FilePathConfig.getDeliveryPath(location)
        self.setDirectory(directory)
        self.setFileName(file_name)
        self.__location = location
        self.__text = ''
        self.load()

    def location(self) -> str:
        return self.__location

    def setLocation(self, location: str) -> None:
        self.__location = location

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        self.save()

    def update(self) -> None:
        self.save()


