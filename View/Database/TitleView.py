from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ClockModule import *
from View.ClockView import *
from datetime import datetime

"""
TitleView
타이틀, 시계
"""


class TitleView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        hbox = QHBoxLayout()
        hbox.addLayout(self.__createTitleLayout(), 8)
        hbox.addLayout(self.__createClockLayout(), 2)
        self.setLayout(hbox)

    def __createTitleLayout(self) -> QLayout:
        location = self.parent().location()
        group = QGroupBox()
        header_font = MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 12)
        main_lbl = MyDefaultWidgets.basicQLabel(font=header_font, text='아리수정수센터 출입자 데이터베이스')
        place_lbl = MyDefaultWidgets.basicQLabel(font=header_font, text=location)

        # 라벨 레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(main_lbl)
        hbox.addStretch(2)
        hbox.addWidget(place_lbl)
        hbox.addStretch(1)
        temp_widget = QWidget()
        temp_widget.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addSpacing(temp_widget.sizeHint().height() // 7)  # 나누기 7 몫은 임의값임, 나누기를 안하면 생각보다 너무 큼
        vbox.addWidget(temp_widget)
        vbox.addSpacing(temp_widget.sizeHint().height() // 7)
        group.setLayout(vbox)

        vbox_total = QVBoxLayout()
        vbox_total.addWidget(group)
        return vbox_total

    def __createClockLayout(self) -> QLayout:
        vbox = QVBoxLayout()
        vbox.addWidget(ClockView(self))
        return vbox
