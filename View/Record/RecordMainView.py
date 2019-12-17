from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.MyPyqt.ShowingView import *
from View.Table.RecordTableView import *
from View.Record.TitleView import *
from View.Record.TakeoverView import *
from View.Record.CurrentWorkerView import *
from View.Record.ArriveView import *
from View.Record.ScrollView import *
from View.Record.LeaveView import *
from View.Table.MatchTableView import *
from View.Record.FunctionView import *
from Utility.Manager.ShortCutManager import *
from Utility.Manager.CommandManager import *

"""
RecordMainView
* 타이틀 (제목, 장소, 날짜, 잔여인원, 시계)
* 기록부 테이블
* 검색 결과 테이블
* 현재근무자 박스, 들어오다 박스, 이어쓰기 박스, 나가다 박스, 인수인계 박스
* 기능 박스
"""


class RecordMainViewSignal(QObject):
    MatchTableView_RowDoubleClicked = pyqtSignal(int)
    ArriveView_ArriveButtonClicked = pyqtSignal()
    LeaveView_LeaveButtonClicked = pyqtSignal()
    ScrollView_ScrollButtonClicked = pyqtSignal()
    TakeoverView_TakeoverButtonClicked = pyqtSignal()
    TakeoverView_DeliveryButtonClicked = pyqtSignal()
    FunctionView_SearchButtonClicked = pyqtSignal()
    FunctionView_OptionButtonClicked = pyqtSignal()
    FunctionView_ReportButtonClicked = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)


class RecordMainView(QWidget, ShowingView):
    def __init__(self, table_view: RecordTableView, parent: QWidget = None):
        super().__init__(parent)
        self.__signal_set = RecordMainViewSignal(self)
        self.__record_table_view: RecordTableView = table_view

        self.__title_view = TitleView(self)
        self.__match_table_view = MatchTableView(self)
        self.__takeover_view = TakeoverView(self)
        self.__current_worker_view = CurrentWorkerView(self)
        self.__arrive_view = ArriveView(self)
        self.__scroll_view = ScrollView(self)
        self.__leave_view = LeaveView(self)
        self.__function_view = FunctionView(self)

        # connect
        self.__match_table_view.signalSet().RowDoubleClicked.connect(lambda row: self.signalSet().MatchTableView_RowDoubleClicked.emit(row))
        self.__arrive_view.signalSet().ArriveButtonClicked.connect(lambda: self.signalSet().ArriveView_ArriveButtonClicked.emit())
        self.__leave_view.signalSet().LeaveButtonClicked.connect(lambda: self.signalSet().LeaveView_LeaveButtonClicked.emit())
        self.__takeover_view.signalSet().TakeoverButtonClicked.connect(lambda: self.signalSet().TakeoverView_TakeoverButtonClicked.emit())
        self.__takeover_view.signalSet().DeliveryButtonClicked.connect(lambda: self.signalSet().TakeoverView_DeliveryButtonClicked.emit())
        self.__scroll_view.signalSet().ScrollButtonClicked.connect(lambda: self.signalSet().ScrollView_ScrollButtonClicked.emit())
        self.__function_view.signalSet().SearchButtonClicked.connect(lambda: self.signalSet().FunctionView_SearchButtonClicked.emit())
        self.__function_view.signalSet().ReportButtonClicked.connect(lambda: self.signalSet().FunctionView_ReportButtonClicked.emit())

        if ConfigModule.Application.enableShortCut():
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Q, lambda: self.scrollView().signalSet().ScrollButtonClicked.emit())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_A, lambda: self.arriveView().signalSet().ArriveButtonClicked.emit())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_D, lambda: self.leaveView().leaveButtonClicked())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_F, lambda: self.functionView().signalSet().SearchButtonClicked.emit())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Z, lambda: CommandManager.undo())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Y, lambda: CommandManager.redo())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_X, lambda: self.recordTableView().cutSelectedItems())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_C, lambda: self.recordTableView().copySelectedItems())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_V, lambda: self.recordTableView().pasteSelectedItems())

        # 레이아웃 구성
        vbox_button = QVBoxLayout()
        vbox_button.addWidget(self.__scroll_view)
        vbox_button.addWidget(self.__arrive_view)

        grid_inout = QGridLayout()
        grid_inout.addWidget(self.__current_worker_view, 0, 0, 1, 2)
        grid_inout.addLayout(vbox_button, 1, 0)
        grid_inout.addWidget(self.__leave_view, 1, 1)
        group_inout = QGroupBox()
        group_inout.setLayout(grid_inout)

        middle_hbox = QHBoxLayout()
        middle_hbox.addStretch(1)
        middle_hbox.addWidget(self.__match_table_view)
        middle_hbox.addStretch(2)
        middle_hbox.addWidget(self.__takeover_view)
        middle_hbox.addStretch(2)
        middle_hbox.addWidget(group_inout)
        middle_hbox.addStretch(2)
        middle_hbox.addWidget(self.__function_view)
        middle_hbox.addStretch(1)

        bottom_hbox = QHBoxLayout()
        bottom_hbox.addStretch(1)
        bottom_hbox.addWidget(self.__record_table_view)
        bottom_hbox.addStretch(2)

        # 전체 레이아웃 구성
        vbox = QVBoxLayout()
        vbox.addWidget(self.__title_view)
        vbox.addStretch(1)
        vbox.addLayout(middle_hbox)
        vbox.addStretch(1)
        vbox.addLayout(bottom_hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)
        self.setFont(MyDefaultWidgets.basicQFont())
        self.matchTableView().setFont(MyDefaultWidgets.basicQFont())  # todo 얘는 왜 자동으로 안되지?

    """
    property
    * signalSet
    * location, date
    * recordTableView, matchTableView
    * arriveView, leaveView, takeoverView, scrollView, currentWorkerView, titleView, functionView
    """
    def signalSet(self) -> RecordMainViewSignal:
        return self.__signal_set

    def location(self) -> str:
        return self.__tableModel().location() if self.__tableModel() else None

    def date(self) -> str:
        return self.__tableModel().date() if self.__tableModel() else None

    def recordTableView(self) -> RecordTableView:
        return self.__record_table_view

    def matchTableView(self) -> MatchTableView:
        return self.__match_table_view

    def arriveView(self) -> ArriveView:
        return self.__arrive_view

    def leaveView(self) -> LeaveView:
        return self.__leave_view

    def takeoverView(self) -> TakeoverView:
        return self.__takeover_view

    def scrollView(self) -> ScrollView:
        return self.__scroll_view

    def currentWorkerView(self) -> CurrentWorkerView:
        return self.__current_worker_view

    def titleView(self) -> TitleView:
        return self.__title_view

    def functionView(self) -> FunctionView:
        return self.__function_view

    """
    advanced property
    * __tableModel
    """
    def __tableModel(self) -> RecordTableModel:
        return self.recordTableView().myModel()

    """
    override
    * activeView
    """
    def activeView(self) -> 'ShowingView':
        return self