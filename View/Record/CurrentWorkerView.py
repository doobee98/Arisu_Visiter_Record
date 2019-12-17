from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ConfigModule import *

"""
CurrentWorkerView
"""


class CurrentWorkerView(QGroupBox):
    DefaultWorker = '근무자'
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 현재 근무자 위젯
        default_worker = ConfigModule.Hidden.currentWorker()  # todo 이걸 컨트롤러에서 줄것
        if not default_worker:
            default_worker = CurrentWorkerView.DefaultWorker

        current_worker_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize()+2),
                                                          text='현재 근무자')
        self.__current_worker_le = MyDefaultWidgets.basicQLineEdit(text=default_worker)
        self.__current_worker_le.installFilterFunctions(ConfigModule.FieldFilter.filterFunctionList(TableFieldOption.Necessary.NAME))
        self.__current_worker_le.textChanged.connect(ConfigModule.Hidden.setCurrentWorker)

        # 현재 근무자 레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(current_worker_lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.__current_worker_le)
        hbox.addStretch(1)
        self.setLayout(hbox)

    """
    property
    * currentWorkerText
    """
    def currentWorkerText(self) -> str:
        return self.__current_worker_le.text()

    def setCurrentWorkerText(self, text: str) -> None:
        self.__current_worker_le.setText(text)

