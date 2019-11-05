from abc import *
from Utility.Manager.StatusBarManager import *


# todo errorlogger에 넣을까?
class AbstractCommand(QObject):
    def __init__(self):
        super().__init__()
        self.__is_executed = False

    def isExecuted(self) -> bool:
        return self.__is_executed

    def setIsExecuted(self, is_executed: bool) -> None:
        self.__is_executed = is_executed

    @abstractmethod
    def execute(self) -> bool:
        if self.isExecuted():
            raise AttributeError('Try to execute while this command is already executed')
            return False
        else:
            self.setIsExecuted(True)
            return True

    @abstractmethod
    def undo(self) -> bool:
        if not self.isExecuted():
            raise AttributeError('Try to undo while this command is still not executed')
            return False
        else:
            self.setIsExecuted(False)
            return True


"""
Command 클래스
* View가 필요하지 않다.


넣어야할 행동 정리
기록부
1. 들어오다 - 다수 대상 Clear Row View, Insert Data Model, Render Row View, Signal to View
2. 나가다 - 다수 대상 Change Row Model, Add or Change Data Model to Database, Signal to View
3. 인수인계 - Get Table Model (Calculate visitor num), Insert Data Model, Render Row View, Save Delivery Data to Report
4. 편집 버튼 - Change Row Model, Render Row View
5. 삭제 버튼 - Remove Row Model, Remove Row View
Open, Close, Change Active View
데이터베이스



"""