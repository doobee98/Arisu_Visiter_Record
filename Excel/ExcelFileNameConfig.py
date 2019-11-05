from Utility.File.BasicFileTable import *


class ExcelFileNameConfig:
    @classmethod
    def getExcelDatabaseSheetName(cls) -> str:
        return 'Sheet1'

    @classmethod
    def getExcelReportSampleName(cls) -> str:
        return BasicFileTable.ReportSample

    @classmethod
    def __removeSpace(cls, string: str) -> str:
        copy = string.replace(' ', '')
        return copy

