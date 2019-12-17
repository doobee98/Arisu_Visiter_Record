from Model.Config.AbstractConfigModel import *
from Utility.Info.DefaultFilePath import *
import os

"""
FilePathConfigModel(AbstractConfigModel)
다른 Config들을 로드하기 위해 최우선적으로 로딩되어야하는 Config 파일이다.
따라서 InitializeArisuRecord에서 로드하고, 싱글톤 패턴을 사용함.
1. 주어진 파일 타입 각각에 대한 경로(directory), 확장자(extension)을 관리함.
    파일 타입에 대한 이름 부여 함수도 관리하나, 이것은 변경할 수 없음.
2. FilePathConfigModel의 경로와 파일 이름, 확장자는 고정되어 있음('.\\FilePathConfig.cfg')
"""


class FileType(Enum):
    Config = '설정'
    RecordTable = '기록부'
    DatabaseTable = 'DB'
    ExcelRecord = '마감(엑셀 기록부)'
    ExcelDatabase = '엑셀 DB'
    Delivery = '전달사항'


class FilePathConfigModel(AbstractConfigModel):
    _INSTANCE = None
    @classmethod
    def instance(cls) -> 'FilePathConfigModel':
        if cls._INSTANCE is None:
            cls._INSTANCE = FilePathConfigModel()
        return cls._INSTANCE

    def __init__(self):
        super().__init__(os.path.join(DefaultFilePath.Config, 'FilePathConfig.cfg'))  # 다른 Config와 다르게 경로가 고정되어 있음

    """
    advanced property
    * directory
    * extension
    """
    def filePathDirectory(self, file_type: FileType) -> str:
        return self._option(file_type.value)[0]

    def setFilePathDirectory(self, file_type: FileType, directory: str) -> None:
        current = self._option(file_type.value)
        current[0] = directory
        self._setOption(file_type.value, current)

    def filePathExtension(self, file_type: FileType) -> str:
        return self._option(file_type.value)[1]

    def setFilePathExtension(self, file_type: FileType, extension: str) -> None:
        current = self._option(file_type.value)
        current[1] = extension
        self._setOption(file_type.value, current)

    """
    method
    * createFilePath, each fileType filePath
    * fileNameToData
    """
    def _createFilePath(self, file_type: FileType, file_name: str) -> str:
        directory, extension = self.filePathDirectory(file_type), self.filePathExtension(file_type)
        return os.path.join(directory, file_name + extension)

    def configFilePath(self, file_name: str) -> str:
        return self._createFilePath(FileType.Config, file_name)

    def recordTableFilePath(self, location: str, date: str) -> str:
        file_name = location.replace(' ', '_') + '_기록부_' + date
        return self._createFilePath(FileType.RecordTable, file_name)

    def databaseTableFilePath(self, location: str) -> str:
        file_name = location.replace(' ', '_') + '_출입자DB'
        return self._createFilePath(FileType.DatabaseTable, file_name)

    def excelRecordFilePath(self, location: str, date: str) -> str:
        file_name = '마감_' + location.replace(' ', '_') + '_' + date
        return self._createFilePath(FileType.ExcelRecord, file_name)

    def excelDatabaseFilePath(self, location: str) -> str:
        file_name = location.replace(' ', '_') + '_출입자DB_엑셀'
        return self._createFilePath(FileType.ExcelDatabase, file_name)

    def deliveryFilePath(self, location: str) -> str:
        file_name = location.replace(' ', '_') + '_전달사항'
        return self._createFilePath(FileType.Delivery, file_name)

    def fileNameToData(self, file_type: FileType, file_path_or_name: str) -> List[str]:
        if file_type == FileType.RecordTable:
            extension = self.filePathExtension(FileType.RecordTable)
            record_file_path = file_path_or_name.replace('/', '\\')
            file_name = record_file_path.split('\\').pop(-1)
            file_name_split = file_name.split('_')
            location_string = file_name_split[0] + ' ' + file_name_split[1]
            date_string = file_name_split[3].replace(extension, '')
            return [location_string, date_string]
        elif file_type == FileType.DatabaseTable:
            extension = self.filePathExtension(FileType.DatabaseTable)
            database_file_path = file_path_or_name.replace('/', '\\')
            file_name = database_file_path.split('\\').pop(-1)
            file_name_split = file_name.split('_')
            location_string = file_name_split[0] + ' ' + file_name_split[1]
            return [location_string]
        else:
            return None

    """
    override
    * initNull
    * setDefault
    """
    def initNull(cls) -> 'FilePathConfigModel':
        return cls.instance()

    def setDefault(self) -> None:
        # data example: List[Directory, extension]
        self.setBlockUpdate(True)
        self._setOption(FileType.Config.value, [DefaultFilePath.Config, '.cfg'])
        self._setOption(FileType.RecordTable.value, [DefaultFilePath.Record, '.rcd'])
        self._setOption(FileType.DatabaseTable.value, [DefaultFilePath.Database, '.iml'])
        self._setOption(FileType.ExcelRecord.value, [DefaultFilePath.ExcelExport, '.xlsx'])
        self._setOption(FileType.ExcelDatabase.value, [DefaultFilePath.ExcelExport, '.xlsx'])
        self._setOption(FileType.Delivery.value, [DefaultFilePath.Delivery, '.xt'])
        self.setBlockUpdate(False)
        self.save()
