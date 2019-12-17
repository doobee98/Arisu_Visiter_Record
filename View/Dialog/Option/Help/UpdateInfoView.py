from Utility.Module.ConfigModule import *
from Utility.MyPyqt.MyDefaultWidgets import *
from View.Dialog.Option.AbstractOptionView import *


class UpdateInfoView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        ready_text = """
    버전: 1.1.0
        """
        ready = QLabel(ready_text)
        vbox = QVBoxLayout()
        vbox.addWidget(ready)
        self.setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize()+2))
        self.setLayout(vbox)

    def myRender(self) -> None:
        pass

    def applyOptionChanges(self) -> None:
        pass





