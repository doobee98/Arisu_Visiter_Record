from Utility.UI.BaseUI import *
from Excel.ExcelFileModule import *
import traceback

if __name__ == '__main__':
    print('Execute')
    try:
        with open('Excel\\execute_properties.txt', 'rb') as f:
            location = f.readline().decode().replace('\n', '')
            record_date = f.readline().decode().replace('\n', '')
        ExcelFileModule.exportExcelRecord(location, record_date)
    except Exception as e:
        print(traceback.format_exc())
        os.system("PAUSE")
    finally:
        print('@@Finish program@@')