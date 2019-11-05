from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from typing import Optional


class AbstractInnerView(QWidget):
    InstallPathRequest = pyqtSignal()

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.__before_view = None
        self.__next_view = None

    def beforeView(self) -> Optional['AbstractInnerView']:
        return self.__before_view

    def setBeforeView(self, view: 'AbstractInnerView') -> None:
        self.__before_view = view

    def nextView(self) -> Optional['AbstractInnerView']:
        return self.__next_view

    def setNextView(self, view: 'AbstractInnerView') -> None:
        self.__next_view = view

    def render(self) -> None:
        pass

    def verify(self) -> bool:
        raise NotImplementedError

    def errorMessage(self) -> str:
        return '다음으로 넘어갈 수 없습니다.'


    def warning(self, text: str) -> None:
        QMessageBox.warning(self, '위험', text)

    def question(self, text: str) -> QMessageBox.StandardButton:
        return QMessageBox.question(self, '확인', text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    def setCenterWidget(self, widget: QWidget) -> None:
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(widget)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def setCenterLayout(self, layout: QLayout) -> None:
        if isinstance(layout, QVBoxLayout):
            wrapper = QHBoxLayout()
            wrapper.addLayout(layout)
        elif isinstance(layout, QHBoxLayout):
            wrapper = QVBoxLayout()
            wrapper.addLayout(layout)
        else:
            hbox = QHBoxLayout()
            wrapper = QVBoxLayout()
            hbox.addLayout(layout)
            wrapper.addLayout(hbox)
        self.setLayout(wrapper)