from Model.Database.VisitorModel import *
from Model.Record.RecordModel import *
from Utility.Config.DatabaseFieldViewConfig import *
from Utility.TableInterface.View.MyTableWidget import *
from Utility.Config.RecordFieldViewConfig import *


class SearchResultTableViewSignal(QObject):
    WriteVisitorRequest = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)

class SearchResultTableView(MyTableWidget):
    DefaultRowCount = 5
    def __init__(self, parent=None):
        ROW, COL = SearchResultTableView.DefaultRowCount, 6
        super().__init__(ROW, COL, parent)
        self.__signal_set = SearchResultTableViewSignal(self)

        self.setVisibleRowCount(SearchResultTableView.DefaultRowCount)
        self.verticalHeader().setHidden(True)

        self.__field_list = ['성명', '생년월일', '차량번호', '소속', '방문목적', '고유번호']
        self.setHorizontalHeaderLabels(self.__field_list)
        self.__initializeItems()

        self.__visitor_model_list = []

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.horizontalHeader().setHighlightSections(False)
        #self.horizontalHeader().setFixedHeight(int(self.horizontalHeader().height() * 1.2))

        self.renderHeader()

        self.cellDoubleClicked.connect(self.myCellDoubleClicked)
        #Config.TotalOption.getSignalSet().OptionChanged.connect(self.renderHeader)

        # 전체 레이아웃 설정
        self.fixTableWidgetSize()

    def getSignalSet(self) -> SearchResultTableViewSignal:
        return self.__signal_set

    def setModel(self, model_list: List[VisitorModel]):
        if self.__visitor_model_list != model_list:
            self.__visitor_model_list = model_list
            self.clearSelection()
            self.render()  # 바로?

    def getVisitorCount(self) -> int:
        return len(self.__visitor_model_list)

    def __initializeItems(self):
        for row_iter in range(self.rowCount()):
            for col_iter in range(self.columnCount()):
                proto_item = QTableWidgetItem()
                proto_item.setTextAlignment(Qt.AlignCenter)
                proto_item.setFlags(proto_item.flags() & ~Qt.ItemIsEditable)
                proto_item.setFont(BaseUI.basicQFont())

                self.setItem(row_iter, col_iter, proto_item)

    @pyqtSlot(int, int)   # todo - visitor model을 저장하지 말고 그냥 dict만 저장하게 할까?
    def myCellDoubleClicked(self, row: int, col: int):
        """
        visitor를 더블클릭하면 visitor의 데이터로 write 요청을 보냄
        dummy를 더블클릭하면 신규 데이터로 write 요청을 보냄
        """

        if row < self.getVisitorCount():
            selected_visitor = self.__visitor_model_list[row]
            change_dict = {field: selected_visitor.getProperty(field) for field in self.__field_list
                           if selected_visitor.getProperty(field) != VisitorModel.DefaultString}
            self.getSignalSet().WriteVisitorRequest.emit(change_dict)
        elif row == self.getVisitorCount():
            empty_dict = {field: VisitorModel.DefaultString for field in self.__field_list}
            empty_dict['고유번호'] = RecordModel.IdDefaultString
            del empty_dict['성명']  # 성명은 지워지지 않는다
            self.getSignalSet().WriteVisitorRequest.emit(empty_dict)
        self.clearSelection()

    @pyqtSlot()
    def render(self):
        self.clearTexts()
        self.clearSpans()
        model_list_length = self.getVisitorCount()
        rows = model_list_length + 1
        self.setRowCount(rows)

        for row_iter, visitor_iter in enumerate(self.__visitor_model_list):
            for col, field_name in enumerate(self.__field_list):
                self.item(row_iter, col).setText(visitor_iter.getProperty(field_name))
            
        dummy_row = model_list_length
        self.renderDummy(dummy_row)


    def renderHeader(self) -> None:
        super().renderHeader()
        # 헤더 옵션값
        for col_iter, field_iter in enumerate(self.__field_list):
            # 헤더 너비 설정
            if RecordFieldViewConfig.getOption(field_iter, 'fit_type') == RecordFieldViewConfig.Option.FitToContent:
                self.resizeColumnToContents(col_iter)

            elif RecordFieldViewConfig.getOption(field_iter, 'fit_type') == RecordFieldViewConfig.Option.FitTwice:
                default_width = self.horizontalHeader().defaultSectionSize()
                self.setColumnWidth(col_iter, default_width * 2)

            if RecordFieldViewConfig.getOption(field_iter, 'search_field') is True:
                header_item = self.horizontalHeaderItem(col_iter)
                header_item.setForeground(Qt.red)  # 색깔을 뭐로 할까?

                header_font = header_item.font()
                header_font.setBold(True)
                header_item.setFont(header_font)

            # if RecordFieldViewConfig.getOption(field_iter, 'hide_field') is True:
            #     self.setColumnHidden(col_iter, not Config.TotalOption.idShowEnable()) 이제 totaloption에 showenable 없음
            # else:
            #     self.showColumn(col_iter)

        self.fixTableWidgetSize()
    
    def renderDummy(self, row: int) -> None:
        self.setSpan(row, 0, 1, self.columnCount())
        self.item(row, 0).setText('현재 작성 중인 행에 신규 데이터 삽입하기')

    # override
    def setRowCount(self, rows: int) -> None:
        if rows != self.rowCount():
            super().setRowCount(rows)
            self.__initializeItems()
            self.fixTableWidgetSize()
