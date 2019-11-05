from Setup.View.InnerView.AbstractInnerView import *
import os, shutil


class ProgramPathView(AbstractInnerView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.default_path = os.environ["ProgramFiles"]

        content_text = ''
        content_text += '설치할 경로를 지정해주세요.'
        lbl = QLabel(content_text)

        self.path_le = QLineEdit(self.default_path)

        btn = QPushButton('...')
        btn.clicked.connect(self.programPathDialogExec)
        btn.setFixedWidth(50)

        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(self.path_le)
        hbox_bottom.addWidget(btn)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(lbl)
        vbox.addLayout(hbox_bottom)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

    def installDirectory(self) -> str:
        return self.path_le.text()

    def installPath(self) -> str:
        return os.path.join(self.installDirectory(), 'ArisuRecord')

    def verify(self) -> bool:
        try:
            if os.path.isdir(self.installDirectory()):
                file_path = self.installPath()
                if os.path.isdir(file_path):
                    reply = self.question('현재 선택한 경로에 ArisuRecord 폴더가 존재합니다.\n'
                                          '해당 폴더를 삭제 후 설치하시겠습니까?\n'
                                          f'경로: {file_path}')
                    if reply == QMessageBox.Yes:
                        shutil.rmtree(file_path)
                    else:
                        return False
                os.makedirs(file_path)
                return True
            else:
                return False

        except Exception as e:
            self.warning(str(e))
            return False

    def errorMessage(self) -> str:
        return f'{self.installDirectory()}가 폴더 경로가 아닙니다. (올바른 경로를 입력하세요)'

    @pyqtSlot()
    def programPathDialogExec(self) -> None:
        file_dialog = QFileDialog(self, '폴더 찾기', self.path_le.text())
        file_dialog.setFileMode(QFileDialog.Directory)
        if file_dialog.exec_():
            folder_path = file_dialog.selectedFiles()[0].replace('/', '\\')
            self.path_le.setText(folder_path)
