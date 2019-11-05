
from Utility.File.FilePathConfig import *
from Model.Config.AbstractOptionModel import *

# todo: fieldview config와 fieldmodel config를 어떻게 할지, 그룹을 어떻게 할지
class FileType:
    Record = 'record'
    Database = 'database'
    Config = 'config'
    Report = 'report'
    Delivery = 'delivery'


class FileDirectoryOptionModel(AbstractOptionModel):
    def __init__(self):
        directory, file_name = FilePathConfig.getConfigPath('FileDirectoryConfig')
        self.__printed_dict = {
            FileType.Record: '기록부',
            FileType.Database: '데이터베이스',
            FileType.Report: '마감 파일',
            FileType.Delivery: '전달사항'
        }
        field_list = list(self.__printed_dict.keys())
        super().__init__(file_name, field_list)
        self.setDirectory(directory)
        default_dict = {
            FileType.Record: BasicFileTable.Record,
            FileType.Database: BasicFileTable.Database,
            FileType.Report: BasicFileTable.Report,
            FileType.Delivery: BasicFileTable.Delivery
        }
        self._setDefaultOptions(MyModel(default_dict))
        self._setCloseFieldList([FileType.Record, FileType.Database])

        if self.hasFile():
            self.load()
            for field_iter in default_dict.keys():
                if not self._getOptionList().hasField(field_iter):
                    self._getOptionList()._setProperty(field_iter, default_dict[field_iter])
        else:
            self._setOptionList(self.getDefaultOptions())
            self.update()

    def fileDirectory(self, file_type: str) -> str:
        return self._getOptionList().getProperty(file_type)

    def setFileDirectory(self, file_type: str, directory: str) -> None:
        self._getOptionList().changeProperty(file_type, directory)

    def currentAbsoluteDirectory(self) -> str:
        return os.getcwd()

    def convertDirectory(self, directory: str) -> str:
        directory = directory.replace('/', '\\')
        current_directory = self.currentAbsoluteDirectory()
        if directory.startswith(current_directory):
            directory = directory.replace(current_directory, '')
            if directory.startswith('\\'):
                directory = directory[1:]
        return directory

    def fieldPrintText(self, field: str) -> str:
        return self.__printed_dict[field]
