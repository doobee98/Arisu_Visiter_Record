from Excel.ImportExcelDBView import *
import traceback

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        c = ImportExcelDBView()
        c.show()

        app.exec_()
    except Exception as e:
        print(traceback.format_exc())
        os.system("PAUSE")
    finally:
        print('@@Finish program@@')