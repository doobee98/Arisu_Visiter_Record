from Utility.UI.BaseUI import *


class DatabaseTitleView(QWidget):
    def __init__(self, location: str):
        super().__init__()

        # 데이터베이스 제목 생성
        group = QGroupBox()
        header_font = BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize()+12)
        self.main_lbl = BaseUI.basicQLabel(font=header_font, text='아리수정수센터 출입자 데이터베이스')
        self.place_lbl = BaseUI.basicQLabel(font=header_font, text=location)

        # 데이터베이스 제목 스타일링
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.main_lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.place_lbl)
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

