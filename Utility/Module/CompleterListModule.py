from View.Table.AbstractTableView import *
from Utility.Module.ConfigModule import *


class CompleterListModule:
    _INSTANCE = None

    @classmethod
    def instance(cls) -> 'CompleterListModule':
        if cls._INSTANCE is None:
            cls._INSTANCE = CompleterListModule()
        return cls._INSTANCE

    def __init__(self):
        self.__record_table: AbstractTableView = None
        self.__database_table: AbstractTableView = None

    """
    * property
    """

    @classmethod
    def setRecordTable(cls, record_table: AbstractTableView):
        cls.instance().__record_table = record_table

    @classmethod
    def setDatabase(cls, database: AbstractTableView):
        cls.instance().__database_table = database

    @classmethod
    def generateCompleterList(cls, record_row: int, record_column: int) -> Optional[List[str]]:
        record_table, database_table = cls.instance().__record_table, cls.instance().__database_table
        if record_table is None or database_table is None:
            return None
            #ErrorLogger.reportError(f'자동완성 모듈의 초기화에 문제가 발생했습니다.', ReferenceError)
        field_model = record_table.fieldModel(record_column)

        record_text_dict = {}
        if field_model.recordOption(TableFieldOption.Record.Completer) is not True:
            return None
        for row_iter in range(record_row):
            item_text = record_table.item(row_iter, record_column).text()
            if item_text:
                if record_text_dict.get(item_text) is None:
                    record_text_dict[item_text] = 1
                else:
                    record_text_dict[item_text] += 1

        database_text_dict = {}
        if field_model.name() in database_table.fieldNameList():
            for row_iter in range(database_table.rowCount()):
                item_text = database_table.fieldText(row_iter, field_model.name())
                recent_date_text = database_table.fieldText(row_iter, TableFieldOption.Necessary.DATE_RECENT)
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



