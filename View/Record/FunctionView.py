from View.ButtonFactory import *
from typing import Callable

"""
FunctionView
"""


class FunctionViewSignal(QObject):
    SearchButtonClicked = pyqtSignal()
    ReportButtonClicked = pyqtSignal()
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)


class FunctionView(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.__signal_set = FunctionViewSignal(self)
        gbox = QGridLayout()

        # 검색 버튼
        search_text = '검색 (Ctrl + F)' if ConfigModule.Application.enableShortCut() else '검색'
        search_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize()+1),
                                                  text=search_text, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.__search_btn = ButtonFactory.createCustomButton('🔍')
        self.__search_btn.clicked.connect(lambda: self.signalSet().SearchButtonClicked.emit())

        # 마감
        report_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize()+1),
                                                  text='마감', alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.__report_btn = ButtonFactory.createCustomButton('📄')
        self.__report_btn.clicked.connect(lambda: self.signalSet().ReportButtonClicked.emit())

        # 전체 레이아웃
        gbox.addWidget(search_lbl, 0, 0)
        gbox.addWidget(self.__search_btn, 0, 1)
        gbox.addWidget(report_lbl, 1, 0)
        gbox.addWidget(self.__report_btn, 1, 1)
        gbox.setColumnStretch(0, 1)  # todo
        self.setLayout(gbox)

    """
    property
    * signalSet
    """
    def signalSet(self) -> FunctionViewSignal:
        return self.__signal_set



