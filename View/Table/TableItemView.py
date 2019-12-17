from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from enum import Flag, auto
from typing import Union, Dict, overload
from Utility.Log.ErrorLogger import *

"""
TableItemView(QTableWidgetItem)
주로 색상이나 글꼴 등의 렌더링 정보를 myFlag로 관리함
"""


class TableItemOption(Flag):
    # BackGround Color & Pattern
    Black = auto()
    White = auto()
    LightGray = auto()
    Gray = auto()
    DarkGray = auto()
    Dotted = auto()
    LightBlue = auto()
    Red = auto()
    Yellow = auto()
    _ColorSet = Black | White | LightGray | Gray | DarkGray | Dotted | LightBlue | Red | Yellow

    # Text Style
    TextBold = auto()
    TextLeft = auto()

    # Editable & Enable
    UnEditable = auto()
    UnFocusable = auto()

    # Span Option
    Span = auto()

    Default = White

    def __or__(self, other):
        if self & TableItemOption._ColorSet and other & TableItemOption._ColorSet:
            remove_color = self & ~TableItemOption._ColorSet
            return remove_color | other
        return super().__or__(other)

    def color(self):
        if self & TableItemOption._ColorSet:
            color_dict: Dict[TableItemOption, Union[Qt.GlobalColor, QColor, QBrush]] = {
                TableItemOption.White: Qt.white,
                TableItemOption.LightGray: Qt.lightGray,
                TableItemOption.Gray: Qt.gray,
                TableItemOption.DarkGray: Qt.darkGray,
                TableItemOption.Black: Qt.black,
                TableItemOption.Dotted: QBrush(Qt.Dense4Pattern),
                TableItemOption.LightBlue: QColor(0x99ffff),  # 99ffff
                TableItemOption.Red: Qt.red,
                TableItemOption.Yellow: QColor(0xFFE13C)
            }
            return color_dict[self & TableItemOption._ColorSet]
        else:
            ErrorLogger.reportError('No Color Config.')
            raise AttributeError


class TableItemView(QTableWidgetItem):
    @overload
    def __init__(self):
        pass

    @overload
    def __init__(self, text: str):
        pass

    @overload
    def __init__(self, other: QTableWidgetItem):
        pass

    def __init__(self, *args):
        my_flags = TableItemOption.Default
        if args:
            if isinstance(args[0], TableItemView):
                my_flags = args[0].myFlags()
            super().__init__(args[0])
        else:
            super().__init__()
        self.__my_flags: TableItemOption = my_flags

    """
    property
    * myFlags
    """
    def myFlags(self) -> TableItemOption:
        return self.__my_flags

    def setMyFlags(self, my_flags: TableItemOption) -> None:
        self.__my_flags = my_flags

    """
    advanced property
    * widget
    """
    def widget(self) -> QWidget:
        return self.tableWidget().cellWidget(self.row(), self.column())

    def setWidget(self, widget: QWidget) -> None:
        self.tableWidget().setCellWidget(self.row(), self.column(), widget)

    """
    method
    * removeWidget
    * myRender
    """
    def removeWidget(self) -> None:
        self.tableWidget().removeCellWidget(self.row(), self.column())

    def myRender(self) -> None:
        # color
        self.setBackground(self.myFlags().color())

        # text
        self.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter if self.myFlags() & TableItemOption.TextLeft else Qt.AlignCenter)
        font = self.font()
        font.setBold(bool(self.myFlags() & TableItemOption.TextBold))
        self.setFont(font)

        # focus and editable
        flags = self.flags()
        if self.myFlags() & TableItemOption.UnEditable:
            flags &= ~Qt.ItemIsEditable
        else:
            flags |= Qt.ItemIsEditable
        if self.myFlags() & TableItemOption.UnFocusable:
            flags &= ~Qt.ItemIsEnabled
        else:
            flags |= Qt.ItemIsEnabled
        self.setFlags(flags)

    """
    override
    * clone
    """
    def clone(self) -> 'TableItemView':
        return TableItemView(self)

