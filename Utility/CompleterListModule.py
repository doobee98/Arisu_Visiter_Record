from Utility.Abstract.View.Table.MyTableView import *
from Utility.Config.RecordFieldViewConfig import *
from Utility.Config.DatabaseFieldViewConfig import *
from Utility.Config.ConfigModule import *

class CompleterListModule:
    _INSTANCE = None
    _LIST_SIZE_MAX = 5

    def __init__(self):
        self.__record_table: MyTableView = None
        self.__database_table: MyTableView = None

    @classmethod
    def instance(cls) -> 'CompleterListModule':
        if cls._INSTANCE is None:
            cls._INSTANCE = CompleterListModule()
        return cls._INSTANCE

    @classmethod
    def setRecordTable(cls, record_table: MyTableView):
        cls.instance().__record_table = record_table

    @classmethod
    def setDatabase(cls, database: MyTableView):
        cls.instance().__database_table = database

    @classmethod
    def getCompleterList(cls, record_row: int, record_column: int) -> Optional[List[str]]:
        record_table, database = cls.instance().__record_table, cls.instance().__database_table
        if record_table is None or database is None:
            return None
            #ErrorLogger.reportError(f'자동완성 모듈의 초기화에 문제가 발생했습니다.', ReferenceError)
        field_name = record_table.fieldList()[record_column]

        record_text_dict = {}
        if RecordFieldViewConfig.getOption(field_name, 'completer_field') is not True:
            return None
        for row_iter in range(record_row):
            item_text = record_table.item(row_iter, record_column).text()
            if item_text:
                if record_text_dict.get(item_text) is None:
                    record_text_dict[item_text] = 1
                else:
                    record_text_dict[item_text] += 1

        database_text_dict = {}
        if Config.RecordOption.getOption('completer_from_db') is True:
            if field_name in DatabaseFieldViewConfig.FieldsDictionary.keys():
                database_column = database.fieldColumn(field_name)
                for row_iter in range(database.rowCount()):
                    item_text = database.item(row_iter, database_column).text()
                    recent_date_text = database.item(row_iter, database.fieldColumn('최근출입날짜')).text()
                    if item_text:
                        if database_text_dict.get(item_text) is None:
                            database_text_dict[item_text] = recent_date_text
                        else:
                            if database_text_dict[item_text] < recent_date_text:
                                database_text_dict[item_text] = recent_date_text

        text_set = set(record_text_dict.keys())
        text_set.update(database_text_dict.keys())
        text_list = list(text_set)

        def textCompare(string: str) -> Tuple[int, str]:
            record_count, database_date = 0, '0000-00-00'
            if record_text_dict.get(string) is not None:
                record_count = record_text_dict[string]
            if database_text_dict.get(string) is not None:
                database_date = database_text_dict[string]
            return record_count, database_date

        text_list.sort(key=textCompare, reverse=True)
        return text_list



