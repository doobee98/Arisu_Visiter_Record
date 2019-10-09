from Utility.UI.BaseUI import *
from abc import abstractmethod


class AbstractOptionView(QWidget):
    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def applyOptionChanges(self) -> None:
        pass

    @classmethod
    def getCenterWrapperLayout(cls, layout: QLayout) -> QLayout:
        layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(layout)
        vbox.addStretch(1)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        return hbox




