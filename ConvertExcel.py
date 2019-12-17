import Utility.Info.InitializeArisuRecord
from Utility.Module.Excel.ExcelModule import *
import traceback, sys


if __name__ == '__main__':
    print('Execute ConvertExcel Program')
    try:
        if not QApplication.instance():
            app = QApplication(sys.argv)
        if len(sys.argv) <= 1:
            print('파일을 함께 실행시켜 주세요.')
        else:
            for idx in range(1, len(sys.argv)):
                print(f'[{sys.argv[idx]}] load')
                file_path = sys.argv[idx]
                _, extension = os.path.splitext(file_path)
                if extension == ConfigModule.FilePath.filePathExtension(FileType.DatabaseTable):
                    ExcelModule.convertDatabaseToExcel(file_path)
                elif extension == ConfigModule.FilePath.filePathExtension(FileType.RecordTable):
                    ExcelModule.convertRecordToExcel(file_path)
                elif extension == '.xlsx':
                    # 기록부와 데이터베이스를 구분하는 기준: 파일명에 'DB'가 있는가
                    file_name = os.path.basename(file_path)
                    if 'DB' in file_name:
                        ExcelModule.convertDatabaseFromExcel(file_path)
                    else:
                        ExcelModule.convertRecordFromExcel(file_path)
                else:
                    ErrorLogger.reportError('잘못된 확장자입니다.', NameError)
    except Exception as e:
        print(traceback.format_exc())
    finally:
        os.system("PAUSE")
        print('@@Finish program@@')