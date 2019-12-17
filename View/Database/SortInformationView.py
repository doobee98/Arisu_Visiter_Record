from Utility.MyPyqt.MyDefaultWidgets import *

"""
SortInformationView
"""


class SortInformationView(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setTitle('정렬 기준')
        self.setFont(MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 2))
        self.__field_lbl = MyDefaultWidgets.basicQLabel(text='없음')
        self.__order_lbl = MyDefaultWidgets.basicQLabel(text='---')

        # 전체 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(self.__field_lbl)
        vbox.addWidget(self.__order_lbl)
        self.setLayout(vbox)

    """
    advanced property
    * sortFieldNameText, sortOrderText
    """
    def sortFieldNameText(self) -> str:
        return self.__field_lbl.text()

    def setSortFieldNameText(self, text: str) -> None:
        self.__field_lbl.setText(text)

    def sortOrderText(self) -> str:
        return self.__order_lbl.text()

    def setSortOrderText(self, text: str) -> None:
        self.__order_lbl.setText(text)



