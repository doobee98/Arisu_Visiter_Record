from PyQt5.QtCore import *
from os.path import isfile
from Utility.CryptListModule import *
from Utility.Error.ErrorLogger import *
from Utility.File.FileNameConfig import *


class DeliveryModel(QObject):
    def __init__(self, location: str):
        super().__init__()
        self.__location = location
        self.__file_name = FileNameConfig.getDeliveryName(location)
        self.__text = ''

        self.load()

    def isFileExist(self) -> bool:
        return self.fileName() and isfile(self.fileName())

    def fileName(self) -> str:
        return self.__file_name

    def setFileName(self, file_name: str) -> None:
        self.__file_name = file_name

    def location(self) -> str:
        return self.__location

    def setLocation(self, location: str) -> None:
        self.__location = location

    def text(self) -> str:
        return self.__text

    def setText(self, text: str) -> None:
        self.__text = text
        self.save()

    def save(self) -> None:
        cipher_text = CryptListModule.encrypt([self.text()])[0]
        with open(self.fileName(), 'wb') as f:
            f.write(cipher_text + b'\n')

    def load(self) -> None:
        if self.isFileExist():
            with open(self.fileName(), 'rb') as f:
                cipher_list = f.readlines()
                decrypt_text = CryptListModule.decrypt(cipher_list, str)[0]
                self.setText(decrypt_text)
        else:
            ErrorLogger.reportError(f'Cannot find file {self.fileName()}.')


