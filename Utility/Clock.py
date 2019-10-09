from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from enum import Enum
# todo 더 정확하게 못만들까. 지금은 약 1초정도 오차가 있음. 이유불명

class ClockSignal(QObject):
    SecondOut = pyqtSignal()
    MinuteOut = pyqtSignal()


class Clock(QObject):
    class MS:
        Second = 1000
        Minute = Second * 60

    _Signal = ClockSignal()
    _DateTime = QDateTime.currentDateTime()
    _Timer = QTimer()

    @classmethod
    def start(cls) -> None:
        if cls._Timer.isActive():
            cls._Timer.stop()
        cls._setDateTime(QDateTime.currentDateTime())
        current_time = cls.getTime()  # 현재 시간 측정
        current_next_time = current_time.addMSecs(Clock.MS.Minute)
        current_next_minute = QTime(current_next_time.hour(), current_next_time.minute())  # todo 여유 ms를 더 두었음
        remain_time = current_time.msecsTo(current_next_minute)  # 다음 minute까지 남은 시간 ms 단위로 지정
        cls._getTimer().setInterval(remain_time)  # 다음 minute까지 남은 시간으로 interval 초기화
        cls._getTimer().timeout.connect(cls.updateMinute)
        cls._getTimer().start()  # 지정한 타이머 start
        print('Initialize Clock:', current_time, remain_time)
        #cls.updateMinute()

    @classmethod
    def getSignalSet(cls) -> ClockSignal:
        return cls._Signal

    @classmethod
    def _getTimer(cls) -> QTimer:
        return cls._Timer

    @classmethod
    def getDateTime(cls) -> QDateTime:
        return cls._DateTime

    @classmethod
    def _setDateTime(cls, date_time: QDateTime) -> None:
        cls._DateTime = date_time

    @classmethod
    def getDate(cls) -> QDate:
        return cls._DateTime.date()

    @classmethod
    def getTime(cls) -> QTime:
        return cls._DateTime.time()

    @classmethod
    def updateMinute(cls) -> None:
        current_date_time = QDateTime.currentDateTime()
        interval = cls._getTimer().interval()
        cls._setDateTime(cls.getDateTime().addMSecs(interval))
        diff_time = current_date_time.msecsTo(cls.getDateTime())

        if abs(diff_time) >= cls.MS.Minute * 0.05:
            print('오차:', diff_time, 'ms.')
            cls.start()
            cls.getSignalSet().MinuteOut.emit()
        else:
            print('오차:', diff_time, 'ms.')
            cls._getTimer().setInterval(cls.MS.Minute)
            cls._getTimer().start()
            cls.getSignalSet().MinuteOut.emit()
