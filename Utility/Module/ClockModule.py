from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Utility.Log.ExecuteLogger import *
from Utility.MyPyqt.MyPyqtSlot import *

"""
ClockModule
자체적인 시계 클래스를 사용함
MinuteOut과 Dayout 시그널을 발생시켜, 다른 위젯에서 이를 받아서 처리할 수 있도록 함
"""


class ClockModuleSignal(QObject):
    MinuteOut = pyqtSignal()
    DayOut = pyqtSignal()


class ClockModule(QObject):
    class MS:
        Second = 1000
        Minute = Second * 60

    _Signal = ClockModuleSignal()
    _DateTime = QDateTime.currentDateTime()
    _Timer = QTimer()

    """
    property
    * signalSet
    * datetime, date, time
    """
    @classmethod
    def signalSet(cls) -> ClockModuleSignal:
        return cls._Signal

    @classmethod
    def datetime(cls) -> QDateTime:
        return cls._DateTime

    @classmethod
    def _setDateTime(cls, date_time: QDateTime) -> None:
        cls._DateTime = date_time

    @classmethod
    def date(cls) -> QDate:
        return cls._DateTime.date()

    @classmethod
    def time(cls) -> QTime:
        return cls._DateTime.time()

    """
    method
    * start
    * updateMinute
    """
    @classmethod
    def start(cls) -> None:
        if cls._Timer.isActive():
            cls._Timer.stop()
            cls._Timer.timeout.disconnect(cls.updateMinute)
        cls._setDateTime(QDateTime.currentDateTime())
        current_time = cls.time()
        current_next_time = current_time.addMSecs(ClockModule.MS.Minute)
        current_next_minute = QTime(current_next_time.hour(), current_next_time.minute())
        remain_time = current_time.msecsTo(current_next_minute)  # 다음 minute까지 남은 시간 ms 단위로 지정
        cls._Timer.setInterval(remain_time)  # 다음 minute까지 남은 시간으로 interval 초기화
        cls._Timer.timeout.connect(cls.updateMinute)  # todo MyPyqtSlot을 여기 넣음(@classmethod때문에 중복)
        cls._Timer.start()  # 지정한 타이머 start
        ExecuteLogger.printLog('Initialize ClockModule: ' + str(current_time) + ' ' + str(remain_time))

    @classmethod
    def updateMinute(cls) -> None:
        current_date_time = QDateTime.currentDateTime()
        interval = cls._Timer.interval()
        old_datetime = cls.datetime()
        cls._setDateTime(cls.datetime().addMSecs(interval))
        diff_time = current_date_time.msecsTo(cls.datetime())
        print(current_date_time)

        if abs(diff_time) >= cls.MS.Minute * 0.05:
            ExecuteLogger.printLog('오차: ' + str(diff_time) + ' ms.')
            cls.start()  # restart
            cls.signalSet().MinuteOut.emit()
        else:
            cls._Timer.setInterval(cls.MS.Minute)
            cls._Timer.start()
            cls.signalSet().MinuteOut.emit()

        if old_datetime.date() != current_date_time.date():
            ExecuteLogger.printLog('Dayout!')
            cls.signalSet().DayOut.emit()

