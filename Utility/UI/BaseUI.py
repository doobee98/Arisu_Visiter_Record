from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Utility.Config.ConfigModule import *
from Utility.Abstract.View.MyLineEdit import *
from Utility.MyPyqtSlot import *
from typing import Union


class MyLineEdit2(MyLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if not self.hasSelectedText():
            self.selectAll()
        else:
            super().mousePressEvent(event)


class BaseUISignalSet(QObject):
    FontSizeChanged = pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)


class BaseUI(QObject):
    __DefaultPointSize = Config.TotalOption.baseFontSize()
    __SignalSet = BaseUISignalSet()

    @classmethod
    def getSignalSet(cls) -> BaseUISignalSet:
        return cls.__SignalSet

    @classmethod
    def defaultPointSize(cls) -> int:
        return cls.__DefaultPointSize

    @classmethod
    def __setDefaultPointSize(cls, point_size: int) -> None:
        old, new = cls.__DefaultPointSize, point_size
        if old != new:
            cls.__DefaultPointSize = point_size
            cls.getSignalSet().FontSizeChanged.emit(new, old)

    @classmethod
    def basicQFont(cls, *, bold: bool = False, point_size: int = __DefaultPointSize) -> QFont:
        font = QFont()
        font.setPointSize(point_size)
        font.setBold(bold)
        return font

    #
    # @classmethod
    # def __adjustQFontSize(cls, font: QFont, new_size: int, old_size: int) -> QFont:
    #     size_diff = new_size - old_size
    #     font.setPointSize(font.pointSize() + size_diff)
    #     return font

    @classmethod
    def basicQLabel(cls, *, font: QFont = None, text: str = None,  #auto_resize: bool = True,
                    alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignCenter,
                    parent: QWidget = None) -> QLabel:
        if font is None:
            font = cls.basicQFont()
        lbl = QLabel(parent)
        lbl.setFont(font)
        lbl.setAlignment(alignment)
        if text is not None:
            lbl.setText(text)
        # cls.getSignalSet().FontSizeChanged.connect(lambda new, old, lbl=lbl, font=font: lbl.setFont(cls.__adjustQFontSize(font, new, old)))
        # if auto_resize:
        #     lbl.adjustSize()
        #     lbl.installEventFilter(BaseUI.__instance())
        return lbl

    @classmethod
    def basicQPushButton(cls, *, font: QFont = None, text: str = None,  #auto_resize: bool = True
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
        # cls.getSignalSet().FontSizeChanged.connect(lambda new, old, btn=btn, font=font: btn.setFont(cls.__adjustQFontSize(font, new, old)))
        # if auto_resize:
        #     btn.adjustSize()
        #     btn.installEventFilter(cls.__instance())
        return btn

    @classmethod
    def basicQLineEdit(cls, *, font: QFont = None, text: str = None,
                       alignment: Union[Qt.Alignment, Qt.AlignmentFlag] = Qt.AlignCenter,
                       parent: QWidget = None) -> MyLineEdit:
        if font is None:
            font = cls.basicQFont()
        le = MyLineEdit2(parent)
        le.setFont(font)
        le.setAlignment(alignment)
        if text is not None:
            le.setText(text)
        return le

    def eventFilter(self, widget: 'QObject', event: 'QEvent') -> bool:
        if isinstance(widget, QLineEdit) and event.type() == QEvent.FocusIn:
            widget.selectAll()
        return QObject.eventFilter(self, widget, event)

    @classmethod
    def configChanged(cls) -> None:
        if cls.defaultPointSize() != Config.TotalOption.baseFontSize():
            cls.__setDefaultPointSize(Config.TotalOption.baseFontSize())


Config.TotalOption.getSignalSet().OptionChanged.connect(BaseUI.configChanged)

