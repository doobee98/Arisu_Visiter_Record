from Utility.MyPyqt.MyTableWidget import *
from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ConfigModule import *
from View.Table.TableItemView import *

"""
AddGroupView
"""


class AddGroupViewSignal(QObject):
    AddButtonClicked = pyqtSignal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)


class AddGroupView(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.__signal_set = AddGroupViewSignal(self)

        # 라벨 위젯
        add_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 3),
                                               text='데이터 추가하기')

        # 테이블 위젯
        field_name_list = [field_model_iter.name() for field_model_iter in ConfigModule.TableField.databaseFieldModelList()
                           if not (field_model_iter.databaseOption(TableFieldOption.Database.AutoComplete) or field_model_iter.globalOption(TableFieldOption.Global.NoModelData))]
        ROW, COLUMN = 1, len(field_name_list)
        self.__add_table_view = MyTableWidget(ROW, COLUMN)
        self.__add_table_view.setHorizontalHeaderLabels(field_name_list)
        self.__add_table_view.verticalHeader().setHidden(True)
        self.__add_table_view.setVisibleRowCount(ROW)
        self.__add_table_view.setItemPrototype(TableItemView())
        for column_iter in range(self.__add_table_view.columnCount()):
            item_iter: TableItemView = self.__add_table_view.item(0, column_iter)
            item_iter.myRender()
        self.__add_table_view.fixTableWidgetSize()

        # 버튼 위젯
        add_btn = MyDefaultWidgets.basicQPushButton(text='추가')
        add_btn.clicked.connect(lambda: self.signalSet().AddButtonClicked.emit())

        hbox = QHBoxLayout()
        hbox.addStretch(2)
        hbox.addWidget(add_lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.__add_table_view)
        hbox.addStretch(3)
        hbox.addWidget(add_btn)
        hbox.addStretch(4)
        self.setLayout(hbox)

    """
    property
    * signalSet
    * tableView
    """
    def signalSet(self) -> AddGroupViewSignal:
        return self.__signal_set

    def tableView(self) -> MyTableWidget:
        return self.__add_table_view