from Model.Table.Field.TableFieldModel import *
from typing import Any

"""
ExcelModuleInformation
전역 클래스
AbstractConfigModel과 다른 방식으로 저장하기에 독자적인 클래스를 사용함
"""


class ExcelModuleInformation:
    DatabaseInformation = 'database_information.json'
    RecordInformation = 'record_information.json'

    class MethodType(Enum):
        RecordFromExcel = auto()
        RecordToExcel = auto()
        DatabaseFromExcel = auto()
        DatabaseToExcel = auto()

    class InfoKey:
        Location = 'location'
        Date = 'date'
        FieldRow = 'field_row'
        DataStartRow = 'data_start_row'
        TakeoverStartCell = 'takeover_start_cell'
        FieldColumn = 'field_column'
        _AllList = [Location, Date, FieldRow, DataStartRow, FieldColumn]
        _From = 'from_excel'
        _To = 'to_excel'

    _INSTANCE = None
    @classmethod
    def instance(cls) -> 'ExcelModuleInformation':
        if cls._INSTANCE is None:
            cls._INSTANCE = ExcelModuleInformation()
        return cls._INSTANCE

    def __init__(self):
        self.__record_dict = None
        self.__database_dict = None
        self.load()

    """
    method
    * excelInformation
    * load, save
    """
    @classmethod
    def excelInformation(cls, method_type: MethodType) -> Dict[str, Any]:
        if method_type == ExcelModuleInformation.MethodType.DatabaseFromExcel:
            return cls.instance().__database_dict[cls.InfoKey._From]
        if method_type == ExcelModuleInformation.MethodType.DatabaseToExcel:
            return cls.instance().__database_dict[cls.InfoKey._To]
        if method_type == ExcelModuleInformation.MethodType.RecordFromExcel:
            return cls.instance().__record_dict[cls.InfoKey._From]
        if method_type == ExcelModuleInformation.MethodType.RecordToExcel:
            return cls.instance().__record_dict[cls.InfoKey._To]

    def load(self):
        database_dict, record_dict = None, None
        if os.path.isfile(os.path.join(DefaultFilePath.SOURCE, ExcelModuleInformation.DatabaseInformation)):
            with open(os.path.join(DefaultFilePath.SOURCE, ExcelModuleInformation.DatabaseInformation), encoding='utf-8') as json_file:
                database_dict = json.load(json_file)
        if database_dict is None:
            self.__setDefaultDatabase()
        else:
            self.__database_dict = database_dict
        if os.path.isfile(os.path.join(DefaultFilePath.SOURCE, ExcelModuleInformation.RecordInformation)):
            with open(os.path.join(DefaultFilePath.SOURCE, ExcelModuleInformation.RecordInformation), encoding='utf-8') as json_file:
                record_dict = json.load(json_file)
        if record_dict is None:
            self.__setDefaultRecord()
        else:
            self.__record_dict = record_dict
        self.save()

    def save(self):
        with open(os.path.join(DefaultFilePath.SOURCE, ExcelModuleInformation.DatabaseInformation), 'w', encoding='utf-8') as json_file:
            json.dump(self.__database_dict, json_file, ensure_ascii=False, indent='\t')
        with open(os.path.join(DefaultFilePath.SOURCE, ExcelModuleInformation.RecordInformation), 'w', encoding='utf-8') as json_file:
            json.dump(self.__record_dict, json_file, ensure_ascii=False, indent='\t')

    """
    default setter
    * __setDefaultDatabase, __setDefaultRecord
    """
    def __setDefaultDatabase(self) -> None:
        database_dict = {
            'location': 'A1',
            'field_row': 5,
            'data_start_row': 7,
            'field_column': {
                TableFieldOption.Necessary.ID: 1,
                TableFieldOption.Necessary.NAME: 2,
                TableFieldOption.Necessary.BIRTHDAY: 3,
                TableFieldOption.Necessary.CAR_NUMBER: 4,
                TableFieldOption.Necessary.COMPANY: 5,
                TableFieldOption.Necessary.PURPOSE: 6,
                '비고': 7,
                TableFieldOption.Necessary.DATE_FIRST: 8,
                TableFieldOption.Necessary.DATE_RECENT: 9
            }
        }
        self.__database_dict = {
            'from_excel': database_dict,
            'to_excel': database_dict
        }

    def __setDefaultRecord(self) -> None:
        record_dict = {
            'location': 'D1',
            'date': 'A1',
            'takeover_start_cell': 'O5',
            'field_row': 5,
            'data_start_row': 7,
            'field_column': {
                TableFieldOption.Necessary.RECORD_ID: 1,
                TableFieldOption.Necessary.NAME: 2,
                TableFieldOption.Necessary.BIRTHDAY: 3,
                '비고': 4,
                TableFieldOption.Necessary.CAR_NUMBER: 5,
                TableFieldOption.Necessary.COMPANY: 6,
                TableFieldOption.Necessary.PURPOSE: 7,
                '반출입\n물품명': 8,
                '반입/반출량': 9,
                TableFieldOption.Necessary.IN_TIME: 10,
                TableFieldOption.Necessary.IN_WORKER: 11,
                TableFieldOption.Necessary.OUT_TIME: 12,
                TableFieldOption.Necessary.OUT_WORKER: 13
            }
        }
        self.__record_dict = {
            'from_excel': record_dict,
            'to_excel': record_dict
        }