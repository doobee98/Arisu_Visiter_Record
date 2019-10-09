
class FileNameConfig:
    @classmethod
    def getRecordTableName(cls, location: str, date: str) -> str:
        return location.replace(' ', '_') + '_기록부_' + date + '.rcd'

    @classmethod
    def getDatabaseName(cls, location: str) -> str:
        return location.replace(' ', '_') + '_출입자DB.iml'

    @classmethod
    def getConfigName(cls, file_name: str) -> str:
        return 'ProgramFiles/Config/' + file_name + '.cfg'  # todo: config 경로지정

    @classmethod
    def getDeliveryName(cls, location: str) -> str:
        return location.replace(' ', '_') + '_전달사항.xt'

    @classmethod
    def getReportName(cls, location: str,  date: str) -> str:
        return '마감_' + location.replace(' ', '') + '_' + date + '.xlsx'

    @classmethod
    def __removeSpace(cls, string: str) -> str:
        copy = string.replace(' ', '')
        return copy

    @classmethod
    def __replaceSpaceToUnderbar(cls, string: str) -> str:
        copy = string.replace(' ', '_')
        return copy

