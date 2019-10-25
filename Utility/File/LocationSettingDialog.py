from Utility.UI.BaseUI import *


class LocationSettingDialog(QDialog):
    def __init__(self):
        super().__init__()

        first_location_lbl = BaseUI.basicQLabel(text='지역', alignment=Qt.AlignLeft)
        second_location_lbl = BaseUI.basicQLabel(text='근무지', alignment=Qt.AlignLeft)
        self.first_location_le = BaseUI.basicQLineEdit(alignment=Qt.AlignRight)
        self.second_location_le = BaseUI.basicQLineEdit(alignment=Qt.AlignRight)
        self.first_location_le.setFixedWidth(70)
        self.second_location_le.setFixedWidth(70)

        location_layout = QGridLayout()
        location_layout.addWidget(first_location_lbl, 0, 0)
        location_layout.addWidget(self.first_location_le, 0, 1)
        location_layout.addWidget(second_location_lbl, 1, 0)
        location_layout.addWidget(self.second_location_le, 1, 1)

        location_button = BaseUI.basicQPushButton(text='지역 입력하기')
        location_button.clicked.connect(self.locationButtonClicked)

        vbox = QVBoxLayout()
        vbox.addLayout(location_layout)
        vbox.addWidget(location_button)
        self.setLayout(vbox)

    def locationButtonClicked(self) -> None:
        if not (self.first_location_le.text() or self.second_location_le.text()):
            MyMessageBox.information(self, '알림', '장소와 근무지를 입력해 주세요.')
            return
        else:
            head_location = self.first_location_le.text()
            tail_location = self.second_location_le.text()
            location_string = head_location + ' ' + tail_location
            reply = MyMessageBox.question(self, '알림', f'<{location_string}>이 맞습니까?')
            if reply == MyMessageBox.Yes:
                Config.TotalOption.setHeadLocation(head_location)
                Config.TotalOption.setTailLocation(tail_location)
                self.close()
            else:
                return