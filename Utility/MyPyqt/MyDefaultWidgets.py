from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Utility.Log.ErrorLogger import *
from Utility.Log.ExecuteLogger import *
from Utility.MyPyqt.MyLineEdit import *
from Utility.MyPyqt.MyPyqtSlot import *
from Utility.Module.ConfigModule import *
from typing import Union

"""
MyDefaultWidgets
View에서 사용할 Widget에 규격을 주기 위한 클래스
basic한 폰트, 라벨, 버튼 등을 제공함
"""


class _MyLineEdit(MyLineEdit):
    # 마우스 선택시 모든 텍스트를 선택하도록 오버라이딩
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.hasSelectedText():
            super().mousePressEvent(event)
            self.selectAll()
        else:
            super().mousePressEvent(event)


class MyDefaultWidgets(QObject):
    """
    method
    * basicPointSize, basicQFont
    * basicQLabel, basicQPushButton, basicQLineEdit
    """
    @classmethod
    def basicPointSize(cls) -> int:
        return ConfigModule.Application.pointSize()

    @classmethod
    def basicQFont(cls, *, bold: bool = False, point_size: int = None) -> QFont:
        if point_size is None:
            point_size = cls.basicPointSize()
        font = QFont()
        font.setPointSize(point_size)
        font.setBold(bold)
        return font

    @classmethod
    def basicQLabel(cls, *, font: QFont = None, text: str = None,
                    alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignCenter,
                    parent: QWidget = None) -> QLabel:
        if font is None:
            font = cls.basicQFont()
        lbl = QLabel(parent)
        lbl.setFont(font)
        lbl.setAlignment(alignment)
        if text is not None:
            lbl.setText(text)
        return lbl

    @classmethod
    def basicQPushButton(cls, *, font: QFont = None, text: str = None,
                         parent: QWidget = None) -> QPushButton:
        if font is None:
            font = cls.basicQFont()
        btn = QPushButton(parent)
        btn.setFont(font)
        if text is not None:
            btn.setText(text)
        btn_size_policy = btn.sizePolicy()
        btn_size_policy.setRetainSizeWhenHidden(True)
        btn.setSizePolicy(btn_size_policy)
        return btn

    @classmethod
    def basicQLineEdit(cls, *, font: QFont = None, text: str = None,
                       alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignCenter,
                       parent: QWidget = None) -> MyLineEdit:
        if font is None:
            font = cls.basicQFont()
        le = _MyLineEdit(parent)
        le.setFont(font)
        le.setAlignment(alignment)
        if text is not None:
            le.setText(text)
        return le
