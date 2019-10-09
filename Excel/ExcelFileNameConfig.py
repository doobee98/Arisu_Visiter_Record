
class ExcelFileNameConfig:
    @classmethod
    def getExcelDatabaseName(cls) -> str:
        return '출입자DB.xlsm'

    @classmethod
    def getExcelDatabaseSheetName(cls) -> str:
        return 'Sheet1'

    @classmethod
    def getExcelReportSampleName(cls) -> str:
        return 'ProgramFiles/ReportSample.xlsx'

    @classmethod
    def __removeSpace(cls, string: str) -> str:
        copy = string.replace(' ', '')
        return copy

