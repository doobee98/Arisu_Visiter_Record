from Excel.ExcelFileModule import *

if __name__ == '__main__':
    print('Execute')

    with open('execute_properties.txt', 'rb') as f:
        location = f.readline().decode().replace('\n', '')
        record_date = f.readline().decode().replace('\n', '')
    table_model = RecordTableModel(location, record_date, file_decorator='../')
    ExcelFileModule.exportExcelRecord(table_model)

    print('@@Finish program@@')