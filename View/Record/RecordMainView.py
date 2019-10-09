from View.Record.RecordTitleView import *
from Utility.ClockView import *
from View.Record.CurWorkerView import *
from View.Record.LeaveView import *
from View.Record.TakeOverView import *
from View.Record.SearchResultTableView import *
from View.Record.ArriveBtnView import *
from View.Record.ScrollButtonView import *
from View.Record.FunctionGroupView import *
from View.Record.RecordTable.RecordTableView import *
from View.Record.RemainNumberBoxView import *

from Utility.TableInterface.View.Search.TableSearchDialog import *
from Utility.DeliveryDialog import *
from Utility.ShortCutManager import *

from Utility.CommandManager import *
import subprocess


class RecordMainViewSignal(QObject):
    SearchRecordRequest = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)


class RecordMainView(QWidget):
    def __init__(self, table_model: RecordTableModel):
        super().__init__()

        self.__table_model = table_model
        date = table_model.getRecordDate()
        location = table_model.getLocation()

        self.record_table = RecordTableView(table_model)

        self.title = RecordTitleView(date, location)
        self.clock = ClockView()
        self.search_table = SearchResultTableView()
        self.take_over = TakeOverView()
        self.cur_worker = CurWorkerView()
        self.scroll_btn = ScrollButtonView()
        self.arrive_btn = ArriveBtnView()
        self.leave = LeaveView()
        self.remain_box = RemainNumberBoxView()
        self.function_group = FunctionGroupView()
        self.search_dialog = TableSearchDialog(self.record_table)
        self.delivery_dialog = DeliveryDialog(DeliveryModel(location))
        self.take_over.getSignalSet().DeliveryBtnClicked.connect(self.deliveryDialogExec)

        self.function_group.setSearchSlot(self.searchDialogExec)
        self.function_group.setReportSlot(self.reportExcel)

        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Q, self.scroll_btn.scrollBtnClicked)
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_A, self.arrive_btn.arriveBtnClicked)
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_D, self.leave.leaveBtnClicked)
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_F, self.searchDialogExec)
                                    #self.function_group.button(ButtonFactory.ButtonType.Search).click)
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Z, lambda: CommandManager.undo())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Y, lambda: CommandManager.redo())
        # todo 임시 테스트

        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.remain_box, 1)
        hbox_top.addWidget(self.title, 7)
        hbox_top.addWidget(self.clock, 2)  # todo 길이가 database랑 다름

        vbox_button = QVBoxLayout()
        vbox_button.addWidget(self.scroll_btn)
        vbox_button.addWidget(self.arrive_btn)

        grid_inout = QGridLayout()
        grid_inout.addWidget(self.cur_worker, 0, 0, 1, 2)
        grid_inout.addLayout(vbox_button, 1, 0)
        grid_inout.addWidget(self.leave, 1, 1)

        hbox_middle = QHBoxLayout()
        hbox_middle.addStretch(1)
        hbox_middle.addWidget(self.search_table)
        hbox_middle.addStretch(2)
        hbox_middle.addWidget(self.take_over)
        hbox_middle.addStretch(2)
        hbox_middle.addLayout(grid_inout)
        hbox_middle.addStretch(2)
        hbox_middle.addWidget(self.function_group)
        hbox_middle.addStretch(1)

        hbox_bottom = QHBoxLayout()
        hbox_bottom.addStretch(1)
        hbox_bottom.addWidget(self.record_table)
        hbox_bottom.addStretch(2)

        vbox_total = QVBoxLayout(self)
        vbox_total.addLayout(hbox_top)
        vbox_total.addStretch(1)
        vbox_total.addLayout(hbox_middle)
        vbox_total.addStretch(1)
        vbox_total.addLayout(hbox_bottom)
        vbox_total.addStretch(1)

        self.setLayout(vbox_total)
        #self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        #self.setFont(BaseUI.basicQFont())  # 전역폰트


    def __str__(self):
        return 'RecordMainView'

    def render(self) -> None:
        self.title.render()
        self.search_table.render()
        self.record_table.render()

    def activeView(self) -> Type[QWidget]:
        if self.search_dialog.isVisible():
            return self.search_dialog
        else:
            return self

    def __tableModel(self) -> RecordTableModel:
        return self.__table_model

    @pyqtSlot()
    def searchDialogExec(self) -> None:
        self.search_dialog.exec_()

    @pyqtSlot()
    def deliveryDialogExec(self) -> None:
        self.delivery_dialog.exec_()

    @pyqtSlot()  # todo 깔끔히 하는법?
    def reportExcel(self) -> None:
        with open('Excel/execute_properties.txt', 'wb') as f:
            f.write((self.__tableModel().getLocation() + '\n').encode())
            f.write((self.__tableModel().getRecordDate() + '\n').encode())

        # QMessageBox.information(self, '알림', '연결이 안 되어 있습니다.')
        StatusBarManager.setMessage('엑셀 마감 파일 생성 중')
        os.chdir('.\\\\Excel')
        subprocess.call('.\\\\ExportExcelRecord.exe')
        os.chdir('..')
        # todo ******************* exe 실행에서 에러발생함
        QMessageBox.information(self, '알림', '마감 파일이 생성되었습니다.')
        StatusBarManager.setIdleStatus()



