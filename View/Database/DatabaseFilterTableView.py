from Utility.TableInterface.View.MyTableWidget import *
from Utility.Config.DatabaseFieldViewConfig import *


class DatabaseFilterTableView(MyTableWidget):
    def __init__(self, parent=None):
        ROW, COL = 1, 6
        super().__init__(ROW, COL, parent)

        self.setVisibleRowCount(1)
        self.verticalHeader().setHidden(True)
        self.__field_list = ['성명', '생년월일', '차량번호', '소속', '방문목적', '비고']
        self.setHorizontalHeaderLabels([DatabaseFieldViewConfig.getOption(field_name, 'lined_name')
                                          for field_name in self.__field_list])
        self.renderHeader()

        self.__initializeItems()

    def getRowData(self) -> Dict[str, str]:
        data_dict = {}
        for col, field_name in enumerate(self.__field_list):
            data_dict[field_name] = self.item(0, col).text()
        data_dict['고유번호'] = ''
        data_dict['최근출입날짜'] = ''
        data_dict['최초출입날짜'] = ''
        return data_dict

    def clearTexts(self):
        for col_iter in range(self.columnCount()):
            self.item(0, col_iter).setText('')

    def renderHeader(self) -> None:
        # 헤더 옵션값
        for col, field_name in enumerate(self.__field_list):
            # 헤더 너비 설정
            if DatabaseFieldViewConfig.getOption(field_name, 'fit_type') == DatabaseFieldViewConfig.Option.FitToContent:
                self.resizeColumnToContents(col)
        self.fixTableWidgetSize()

    def __initializeItems(self):
        for col_iter in range(self.columnCount()):
            proto_item = QTableWidgetItem()
            proto_item.setTextAlignment(Qt.AlignCenter)

            self.setItem(0, col_iter, proto_item)
