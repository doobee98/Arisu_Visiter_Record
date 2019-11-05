import sys, os
from Utility.File.BasicFileTable import *
from tkinter import messagebox


class InitializeArisuRecord:
    _first_directory = os.path.dirname(sys.argv[0])
    os.chdir(_first_directory)
    try:
        while True:
            current_directory = os.getcwd()
            if os.path.isdir(current_directory) and current_directory.endswith(BasicFileTable.MainFile):
                break
            os.chdir('..\\')
            if current_directory == os.getcwd():
                raise RecursionError
    except Exception as e:
        error_string = '기본 파일을 로드하는 동안 에러가 발생했습니다.\n'
        error_string += f'{BasicFileTable.MainFile} 경로가 존재하지 않습니다.\n'
        error_string += f'로드위치: {_first_directory}\n'
        messagebox.showerror('위험', error_string)
        sys.exit()