from View.Database.DatabaseTable.DatabaseTableView import *
from View.Database.DatabaseTitleView import *
from View.Database.DatabaseFilterView import *
from View.Database.DatabaseButtonView import *
from View.Database.FunctionGroupView import *
from Utility.ClockView import *
from Utility.Abstract.View.Table.Search.TableSearchDialog import *
from Utility.Manager.ShortCutManager import *
from Utility.Manager.CommandManager import *


class DatabaseMainView(QWidget):
    def __init__(self, table_model: DatabaseModel):
        super().__init__()

        self.database_table = DatabaseTableView(table_model)
        self.title = DatabaseTitleView(table_model.getLocation())
        self.clock = ClockView()
        self.filter = DatabaseFilterView()
        self.button = DatabaseButtonView()
        self.function_group = FunctionGroupView()
        self.search_dialog = TableSearchDialog(self.database_table)

        self.function_group.setSearchSlot(self.searchDialogExec)
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_F,
                                    self.function_group.button(ButtonFactory.ButtonType.Search).click)
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Z, lambda: CommandManager.undo())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Y, lambda: CommandManager.redo())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_X, lambda: self.database_table.cutSelectedItems())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_C, lambda: self.database_table.copySelectedItems())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_V, lambda: self.database_table.pasteSelectedItems())
        # todo 임시 테스트

        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.title, 4)
        hbox_top.addWidget(self.clock, 1)

        hbox_middle = QHBoxLayout()
        hbox_middle.addWidget(self.filter)
        hbox_middle.addWidget(self.function_group)

        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(self.database_table)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_top)
        vbox.addStretch(1)
        vbox.addLayout(hbox_middle)
        vbox.addStretch(1)
        vbox.addLayout(hbox_bottom)

        vbox.setAlignment(Qt.AlignCenter)
        self.setLayout(vbox)

    def __str__(self):
        return 'DatabaseMainView'

    @MyPyqtSlot()
    def render(self):
        self.database_table.render()

    def activeView(self) -> QWidget:
        if self.search_dialog.isVisible():
            return self.search_dialog
        else:
            return self

    @MyPyqtSlot()
    def searchDialogExec(self) -> None:
        self.search_dialog.exec_()

