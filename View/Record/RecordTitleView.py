from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Utility.UI.BaseUI import *
from Utility.Clock import *


class RecordTitleView(QWidget):
    def __init__(self, date: str, location: str):
        super().__init__()

        # 기록부 제목 생성
        group = QGroupBox()
        header_font = BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize()+12)
        convert_date = datetime.strptime(date, '%y%m%d').strftime('%Y-%m-%d')
        self.main_lbl = BaseUI.basicQLabel(font=header_font, text='출입자 및 물품 반출입 기록부')
        self.place_lbl = BaseUI.basicQLabel(font=header_font, text=location)
        self.date_lbl = BaseUI.basicQLabel(font=header_font, text=convert_date)

        # 라벨 스타일링
        date_font = self.date_lbl.font()
        if Clock.getDate().toString('yyMMdd') != date:
            date_font.setUnderline(True)
            self.date_lbl.setText(' ' + self.date_lbl.text() + ' ')  # todo 임시방편
        self.date_lbl.setFont(date_font)



        # 라벨 레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.main_lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.place_lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.date_lbl)
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
        self.setLayout(vbox_total)


    def __str__(self):
        return 'RecordTitleView'

    def render(self) -> None:
        pass



