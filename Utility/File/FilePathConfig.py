from Utility.File.BasicFileTable import *
from typing import Tuple
from Utility.Config import ConfigSet
# todo 순환참조 어떻게 해결할 것인지?

class FilePathConfig:
    @classmethod
    def getConfigPath(cls, file_name: str) -> Tuple[str, str]:
        return BasicFileTable.Config, file_name + '.cfg'

    @classmethod
    def getRecordTablePath(cls, location: str, date: str) -> Tuple[str, str]:
        Config, FileType = ConfigSet.Config, ConfigSet.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Record), location.replace(' ', '_') + '_기록부_' + date + '.rcd'

    @classmethod
    def getDatabasePath(cls, location: str) -> Tuple[str, str]:
        Config, FileType = ConfigSet.Config, ConfigSet.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Database), location.replace(' ', '_') + '_출입자DB.iml'

    @classmethod
    def getDeliveryPath(cls, location: str) -> Tuple[str, str]:
        Config, FileType = ConfigSet.Config, ConfigSet.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Delivery), location.replace(' ', '_') + '_전달사항.xt'

    @classmethod
    def getReportPath(cls, location: str, date: str) -> Tuple[str, str]:
        Config, FileType = ConfigSet.Config, ConfigSet.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Report), '마감_' + location.replace(' ', '') + '_' + date + '.xlsx'

    @classmethod
    def getFilePathString(cls, directory: str, file_name: str) -> str:
        if directory:
            return directory + '\\' + file_name
        else:
            return file_name

    # @classmethod
    # def getExcelModuleDirectory(cls) -> str:
    #     Config, FileType = ConfigModule.Config, ConfigModule.FileType
    #     return '..\\..\\'

    @classmethod
    def __removeSpace(cls, string: str) -> str:
        copy = string.replace(' ', '')
        return copy

    @classmethod
    def __replaceSpaceToUnderbar(cls, string: str) -> str:
        copy = string.replace(' ', '_')
        return copy

