from View.Table.DatabaseTableView import *
from View.Database.TitleView import *
from View.Database.FunctionView import *
from View.Database.AddGroupView import *
from View.Database.SortInformationView import *
from Utility.Manager.ShortCutManager import *
from Utility.Manager.CommandManager import *

"""
DatabaseMainView
* 타이틀 (제목, 장소, 시계)
* 데이터베이스 테이블
* 아이템 추가 테이블
* 정렬 정보
* 기능 박스
"""


class DatabaseMainViewSignal(QObject):
    FunctionView_SearchButtonClicked = pyqtSignal()
    FunctionView_OptionButtonClicked = pyqtSignal()
    AddGroupView_AddButtonClicked = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)


class DatabaseMainView(QWidget, ShowingView):
    def __init__(self, table_view: DatabaseTableView, parent: QWidget = None):
        super().__init__(parent)
        self.__signal_set = DatabaseMainViewSignal(self)
        self.__database_table_view = table_view
        self.__title_view = TitleView(self)
        self.__function_view = FunctionView(self)
        self.__add_group_view = AddGroupView(self)
        self.__sort_info_view = SortInformationView(self)

        self.__function_view.signalSet().SearchButtonClicked.connect(lambda: self.signalSet().FunctionView_SearchButtonClicked.emit())
        self.__add_group_view.signalSet().AddButtonClicked.connect(lambda: self.signalSet().AddGroupView_AddButtonClicked.emit())

        if ConfigModule.Application.enableShortCut():
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_F, lambda: self.functionView().signalSet().SearchButtonClicked.emit())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Z, lambda: CommandManager.undo())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Y, lambda: CommandManager.redo())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_X, lambda: self.databaseTableView().cutSelectedItems())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_C, lambda: self.databaseTableView().copySelectedItems())
            ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_V, lambda: self.databaseTableView().pasteSelectedItems())

        # 레이아웃 구성
        middle_hbox = QHBoxLayout()
        middle_hbox.addWidget(self.__sort_info_view)
        middle_hbox.addWidget(self.__add_group_view)
        middle_hbox.addWidget(self.__function_view)

        # 전체 레이아웃 구성
        vbox = QVBoxLayout()
        vbox.addWidget(self.__title_view)
        vbox.addStretch(1)
        vbox.addLayout(middle_hbox)
        vbox.addStretch(1)
        vbox.addWidget(self.__database_table_view)
        self.setLayout(vbox)
        self.setFont(MyDefaultWidgets.basicQFont())
        self.__add_group_view.setFont(MyDefaultWidgets.basicQFont())
        # self.__function_view.setFont()

    """
    property
    * signalSet
    * location
    * databaseTableView
    * titleView, functionView, addGroupView, sortInformationView
    """
    def signalSet(self) -> DatabaseMainViewSignal:
        return self.__signal_set

    def location(self) -> str:
        return self.__tableModel().location() if self.__tableModel() else None

    def databaseTableView(self) -> DatabaseTableView:
        return self.__database_table_view

    def titleView(self) -> TitleView:
        return self.__title_view

    def functionView(self) -> FunctionView:
        return self.__function_view

    def addGroupView(self) -> AddGroupView:
        return self.__add_group_view

    def sortInformationView(self) -> SortInformationView:
        return self.__sort_info_view

    """
    advanced property
    * __tableModel
    """
    def __tableModel(self) -> DatabaseTableModel:
        return self.databaseTableView().myModel()

    """
    override
    * activeView
    """
    def activeView(self) -> 'ShowingView':
        return self
