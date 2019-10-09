from Excel.ImportExcelDBView import *

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        c = ImportExcelDBView()
        c.show()

        app.exec_()
    except Exception as e:
        print(e)
    finally:
        print('@@Finish program@@')