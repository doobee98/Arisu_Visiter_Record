from Utility.UI.BaseUI import *
from Utility.Config.ConfigModule import *


class CurWorkerView(QWidget):
    def __init__(self):
        super().__init__()

        self.group = QGroupBox()

        # 현재 근무자 위젯

        base_worker = Config.HiddenOption.worker()
        if not base_worker:
            base_worker = '근무자'

        self.lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize()+2),
                                      text='현재 근무자')
        self.line = BaseUI.basicQLineEdit(text=base_worker)
        self.line.textEdited.connect(Config.HiddenOption.setWorker)

        # 현재 근무자 스타일링
        #   lineEdit
        #self.line.setFixedWidth(100)

        # 현재 근무자 레이아웃
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.lbl)
        hbox.addStretch(2)
        hbox.addWidget(self.line)
        hbox.addStretch(1)
        self.group.setLayout(hbox)

        # 전체 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(self.group)
        self.setLayout(vbox)

    def __str__(self):
        return 'CurWorkerView'
