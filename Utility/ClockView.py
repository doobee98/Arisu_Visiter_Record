from Utility.UI.BaseUI import *
from Utility.Clock import *
from Utility.Log.ErrorLogger import *


class ClockView(QWidget):
    def __init__(self):
        super().__init__()
        self.group = QGroupBox()

        # 시계 위젯
        self.date_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True, point_size=BaseUI.defaultPointSize()+4),
                                           text='DateDefault')
        self.time_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+2),
                                           text='TimeDefault')

        # 시계 데이터 넣기
        self.updateClock()
        Clock.getSignalSet().MinuteOut.connect(self.updateClock)

        # 시계 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(self.date_lbl, 4)
        vbox.addStretch(1)
        vbox.addWidget(self.time_lbl, 3)
        self.group.setLayout(vbox)

        # 전체 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(self.group)
        self.setLayout(hbox)

    @MyPyqtSlot()
    def updateClock(self) -> None:
        if self.time_lbl.text() == Clock.getTime().toString('hh : mm'):
            ErrorLogger.reportError(f'Minute is not updated now ({self.time_lbl.text()}).\n'
                                    f'시계 초기화에 오류가 있습니다. 프로그램을 재시작 해 주세요.')
            return
        self.date_lbl.setText(Clock.getDate().toString('yyyy년 MM월 dd일'))
        self.time_lbl.setText(Clock.getTime().toString('hh : mm'))

    def __str__(self):
        return 'ClockView'