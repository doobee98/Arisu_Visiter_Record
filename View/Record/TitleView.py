from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ClockModule import *
from View.ClockView import *
from datetime import datetime

"""
TitleView
타이틀, 잔여인원, 시계
"""


class TitleView(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        date, location = self.parent().date(), self.parent().location()

        # 잔여인원 그룹박스
        remain_group = QGroupBox()
        title_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 4),
                                                 text='잔여인원')
        self.__remain_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 2))
        self.setRemainCount(0)
        remain_vbox = QVBoxLayout()
        remain_vbox.addWidget(title_lbl)
        remain_vbox.addWidget(self.__remain_lbl)
        remain_group.setLayout(remain_vbox)

        # 타이틀 그룹박스
        title_group = QGroupBox()
        header_font = MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 12)
        convert_date = datetime.strptime(date, '%y%m%d').strftime('%Y-%m-%d')
        main_lbl = MyDefaultWidgets.basicQLabel(font=header_font, text='출입자 및 물품 반출입 기록부')
        place_lbl = MyDefaultWidgets.basicQLabel(font=header_font, text=location)
        date_lbl = MyDefaultWidgets.basicQLabel(font=header_font, text=convert_date)

        date_font = date_lbl.font()
        if ClockModule.date().toString('yyMMdd') != date:
            date_font.setUnderline(True)
            date_lbl.setText(' ' + date_lbl.text() + ' ')  # todo 임시방편
        date_lbl.setFont(date_font)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(main_lbl)
        hbox.addStretch(2)
        hbox.addWidget(place_lbl)
        hbox.addStretch(2)
        hbox.addWidget(date_lbl)
        hbox.addStretch(1)
        temp_widget = QWidget()
        temp_widget.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addSpacing(temp_widget.sizeHint().height() // 7)  # 나누기 7 몫은 임의값임, 나누기를 안하면 생각보다 너무 큼
        vbox.addWidget(temp_widget)
        vbox.addSpacing(temp_widget.sizeHint().height() // 7)
        title_group.setLayout(vbox)

        # 시계 그룹박스
        clock_group = ClockView(self)

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(remain_group, 1)
        hbox.addWidget(title_group, 7)
        hbox.addWidget(clock_group, 2)
        self.setLayout(hbox)

    """
    property
    * remainCount
    """
    def remainCount(self) -> int:
        return int(filter(str.isdigit, self.__remain_lbl.text()))

    def setRemainCount(self, count: int) -> None:
        self.__remain_lbl.setText(str(count) + '명')
