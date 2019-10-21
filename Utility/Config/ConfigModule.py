from Model.Config.TotalOptionModel import *
from Model.Config.HiddenOptionModel import *
from Model.Config.RecordOptionModel import *
from Model.Config.DatabaseOptionModel import *
from Model.Config.FileDirectoryOptionModel import *
from tkinter import messagebox
import sys


class Config:

    MainFileExe = 'Arisu.exe'
    MainFileCode = 'Arisu.py'
    try:
        while True:
            current_directory = os.getcwd()
            current_file_list = os.listdir(current_directory)
            if MainFileExe in current_file_list or MainFileCode in current_file_list:
                break
            os.chdir('..\\\\')
            if current_directory == os.getcwd():
                raise RecursionError
    except Exception as e:
        error_string = 'Config 파일을 로드하는 동안 에러가 발생했습니다.\n'
        error_string += f'{MainFileExe}이(가) 존재하지 않거나,\n'
        error_string += f'ProgramFiles 경로의 폴더나 파일, 이름이 손상되었습니다.'
        messagebox.showerror('위험', error_string)
        sys.exit()

    FileDirectoryOption = FileDirectoryOptionModel()
    TotalOption = TotalOptionModel()
    HiddenOption = HiddenOptionModel()
    RecordOption = RecordOptionModel()
    DatabaseOption = DatabaseOptionModel()
