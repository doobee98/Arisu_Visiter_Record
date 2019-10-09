from Utility.UI.BaseUI import *
from Excel.ExcelFileModule import *

class ImportExcelDBView(QDialog):
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

        import_btn = BaseUI.basicQPushButton(text='엑셀에서 가져오기')
        import_btn.clicked.connect(self.importButtonClicked)

        vbox = QVBoxLayout()
        vbox.addLayout(location_layout)
        vbox.addWidget(import_btn)
        self.setLayout(vbox)

    def importButtonClicked(self) -> None:
        if not (self.first_location_le.text() or self.second_location_le.text()):
            QMessageBox.information(self, '알림', '장소와 근무지를 입력해 주세요.')
            return
        else:
            location_string = self.first_location_le.text() + ' ' + self.second_location_le.text()
            reply = QMessageBox.question(self, '알림', f'<{location_string}>이 맞습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            else:
                result = ExcelFileModule.importExcelDatabase(location_string, '../출입자DB.xlsm')
                if result is None:
                    QMessageBox.information(self, '알림', '로딩 실패 - 이미 해당 지역의 DB가 존재합니다.')
                else:
                    QMessageBox.information(self, '알림', result.getFileName() + ' 저장 완료')
