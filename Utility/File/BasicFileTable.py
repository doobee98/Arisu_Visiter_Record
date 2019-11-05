import os, sys
from tkinter import messagebox
# todo 더 작업해서 추가할것

class BasicFileTable:
    MainFile = 'ArisuRecord'

    HOME = os.getcwd()
    ExportEXE = 'Excel\\ExportExcelRecord.exe'

    DATA = os.path.expanduser("~\\ArisuRecordData")
    Log = os.path.join(DATA, 'AppData\\log')
    Config = os.path.join(DATA, 'AppData\\bin\\config')
    ReportSample = os.path.join(DATA, 'AppData\\src\\ReportSample.xlsx')
    Icon = os.path.join(DATA, 'AppData\\src\\ArisuIcon.ico')
    Database = os.path.join(DATA, 'UserData\\Database')
    Delivery = os.path.join(DATA, 'UserData\\Delivery')
    Record = os.path.join(DATA, 'UserData\\Record')
    Report = os.path.expanduser("~\\Desktop")
