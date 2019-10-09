import inspect
from datetime import datetime


# 에러 로거에서 에러가 발생할 경우를 처리하여야함
# try except
class ErrorLogger:
    __FileName = 'ErrorReport.txt'

    @classmethod
    def reportError(cls, what: str = None):
        caller_frame = inspect.currentframe().f_back
        error_string = cls.__createBaseErrorString(inspect.getframeinfo(caller_frame))
        if what:
            error_string += '           What: ' + what + '\n'

        cls.__debugPrint(inspect.getframeinfo(caller_frame), what)
        cls.__writeReportFile(error_string)

    @classmethod
    def __createBaseErrorString(cls, args) -> str:
        (filepath, line_number, function_name, lines, index) = args
        filename = filepath.split('\\')[-1]
        result = ''
        result += 'Error Date&Time: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'
        result += '   CodeFileName: ' + filename + '\n'
        result += '     MethodName: ' + function_name + '\n'
        return result

    @classmethod
    def __writeReportFile(cls, error_string: str):
        error_string += '\n\n'

        with open(cls.__FileName, 'a', encoding='utf-8') as f:
            f.write(error_string)

    @classmethod
    def __debugPrint(cls, caller, what):
        (filepath, line_number, function_name, lines, index) = caller
        filename = filepath.split('\\')[-1]
        print(filename, '/', function_name, end='')
        if what:
            print(':', what, end='')
        print()