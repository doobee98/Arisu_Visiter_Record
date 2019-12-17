from Utility.MyPyqt.MyDefaultWidgets import *
from Utility.Module.ClockModule import *
from Utility.Log.ErrorLogger import *

"""
ClockView
"""


class ClockView(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        # 시계 위젯
        self.__date_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 4),
                                                       text='DateDefault')
        self.__time_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 2),
                                                       text='TimeDefault')

        # 시계 데이터 넣기
        self.__updateClock()
        ClockModule.signalSet().MinuteOut.connect(self.__updateClock)

        # 시계 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(self.__date_lbl, 4)
        vbox.addStretch(1)
        vbox.addWidget(self.__time_lbl, 3)
        self.setLayout(vbox)

    @MyPyqtSlot()
    def __updateClock(self) -> None:
        if self.__time_lbl.text() == ClockModule.time().toString('hh : mm'):
            ErrorLogger.reportError(f'Minute is not updated now ({self.__time_lbl.text()}).\n'
                                    f'시계 초기화에 오류가 있습니다.'
                                    f'정확한 시간을 나타내지 않는다면 프로그램을 재시작 해 주세요.')
            return
        self.__date_lbl.setText(ClockModule.date().toString('yyyy년 MM월 dd일'))
        self.__time_lbl.setText(ClockModule.time().toString('hh : mm'))
