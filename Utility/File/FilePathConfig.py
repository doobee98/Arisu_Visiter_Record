from typing import Tuple
from Utility.Config import ConfigModule
# todo 순환참조 어떻게 해결할 것인지?

class FilePathConfig:
    @classmethod  # todo Config Path는 변하지 않는 상대 경로로 지정함
    def getConfigPath(cls, file_name: str) -> Tuple[str, str]:
        return 'ProgramFiles\\Config', file_name + '.cfg'  # todo: config 경로지정

    @classmethod
    def getRecordTablePath(cls, location: str, date: str) -> Tuple[str, str]:
        Config, FileType = ConfigModule.Config, ConfigModule.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Record), location.replace(' ', '_') + '_기록부_' + date + '.rcd'

    @classmethod
    def getDatabasePath(cls, location: str) -> Tuple[str, str]:
        Config, FileType = ConfigModule.Config, ConfigModule.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Database), location.replace(' ', '_') + '_출입자DB.iml'

    @classmethod
    def getLogPath(cls, file_name: str) -> Tuple[str, str]:
        Config, FileType = ConfigModule.Config, ConfigModule.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Log), f'{file_name}.txt'

    @classmethod
    def getDeliveryPath(cls, location: str) -> Tuple[str, str]:
        Config, FileType = ConfigModule.Config, ConfigModule.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Delivery), location.replace(' ', '_') + '_전달사항.xt'

    @classmethod
    def getReportPath(cls, location: str, date: str) -> Tuple[str, str]:
        Config, FileType = ConfigModule.Config, ConfigModule.FileType
        return Config.FileDirectoryOption.fileDirectory(FileType.Report), '마감_' + location.replace(' ', '') + '_' + date + '.xlsx'

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

