from Utility.UI.BaseUI import *


class RemainNumberBoxView(QWidget):

    def __init__(self):
        super().__init__()

        # 전체 그룹 박스
        self.group = QGroupBox()

        # 제목
        self.title_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize()+4),
                                            text='잔여인원')

        # 잔여인원
        self.remain_number = 0
        self.remain_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+2),
                                            text=f'{self.remain_number}명')

        # 전체 레이아웃
        vbox_inner = QVBoxLayout()
        vbox_inner.addWidget(self.title_lbl)
        vbox_inner.addWidget(self.remain_lbl)
        self.group.setLayout(vbox_inner)

        vbox = QVBoxLayout()
        vbox.addWidget(self.group)
        self.setLayout(vbox)

    def __str__(self):
        return 'RemainNumberBoxView'

    def setCurrentVisitorNumber(self, visitor_num: int) -> None:
        self.remain_number = visitor_num
        self.remain_lbl.setText(f'{self.remain_number}명')

