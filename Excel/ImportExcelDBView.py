from Utility.UI.BaseUI import *
from Excel.ExcelFileModule import *
from Utility.Abstract.View.MyMessageBox import *

class ImportExcelDBView(QDialog):
    def __init__(self):
        super().__init__()

        head_location_lbl = BaseUI.basicQLabel(text='지역', alignment=Qt.AlignLeft)
        tail_location_lbl = BaseUI.basicQLabel(text='근무지', alignment=Qt.AlignLeft)
        self.head_location_le = BaseUI.basicQLineEdit(alignment=Qt.AlignRight)
        self.tail_location_le = BaseUI.basicQLineEdit(alignment=Qt.AlignRight)
        self.head_location_le.setFixedWidth(70)
        self.tail_location_le.setFixedWidth(70)

        location_layout = QGridLayout()
        location_layout.addWidget(head_location_lbl, 0, 0)
        location_layout.addWidget(self.head_location_le, 0, 1)
        location_layout.addWidget(tail_location_lbl, 1, 0)
        location_layout.addWidget(self.tail_location_le, 1, 1)

        import_btn = BaseUI.basicQPushButton(text='엑셀에서 가져오기')
        import_btn.clicked.connect(self.importButtonClicked)

        vbox = QVBoxLayout()
        vbox.addLayout(location_layout)
        vbox.addWidget(import_btn)
        self.setLayout(vbox)

    @MyPyqtSlot()
    def importButtonClicked(self) -> None:
        if not (self.head_location_le.text() or self.tail_location_le.text()):
            MyMessageBox.information(self, '알림', '장소와 근무지를 모두 입력해 주세요.')
            return
        else:
            location_string = self.head_location_le.text() + ' ' + self.tail_location_le.text()
            reply = MyMessageBox.question(self, '알림', f'<{location_string}>이 맞습니까?')
            if reply != MyMessageBox.Yes:
                return
            else:
                name = QFileDialog.getOpenFileName(self, '엑셀 파일 열기', './', '*.xlsm')
                if len(name) == 2:
                    file_name = name[0]
                    result = ExcelFileModule.importExcelDatabase(location_string, file_name)
                    if result is None:
                        MyMessageBox.information(self, '알림', '로딩 실패 - 이미 해당 지역의 DB가 존재합니다.')
                    else:
                        MyMessageBox.information(self, '알림', result.fileName() + ' 저장 완료')
                else:
                    MyMessageBox.information(self, '알림', '잘못된 파일입니다.')

