import InitializeArisuRecord
from Utility.UI.BaseUI import *
from Excel.ExcelFileModule import *
import traceback, sys

if __name__ == '__main__':
    print('Execute')
    try:
        print(sys.argv)
        record_file_path = sys.argv[1]
        ExcelFileModule.exportExcelRecord(record_file_path)
    except Exception as e:
        print(traceback.format_exc())
        os.system("PAUSE")
    finally:
        print('@@Finish program@@')