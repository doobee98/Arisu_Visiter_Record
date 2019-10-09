from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import Dict, List, Callable, Tuple, Type
from Utility.Error.ErrorLogger import *
from PyQt5.QtWidgets import QApplication


class ShortCutManagerSignal(QObject):
    ShortCutFinished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class ShortCutManager(QWidget):
    """
    ShortCutManager
    One ShortCut at One Active View -> Same One Action (no another action)

    """
    _INSTANCE = None
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__signal_set: ShortCutManagerSignal = ShortCutManagerSignal(self)
        self.__short_cut_dict: Dict[Tuple[Type[QWidget], int], Callable[[None], None]] = {}
        self.__current_widget: Type[QWidget] = None

    @classmethod
    def instance(cls, parent=None):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(parent)
        return cls._INSTANCE

    @classmethod
    def runManager(cls, widget: Type[QWidget]) -> None:
        cls.instance().grabKeyboard()
        cls.instance().__current_widget = widget

    @classmethod
    def stopManager(cls) -> None:
        cls.instance().releaseKeyboard()
        cls.instance().__current_widget = None

    @classmethod
    def getSignalSet(cls) -> ShortCutManagerSignal:
        return cls.instance().getSignalSet()

    @classmethod
    def addShortCut(cls, widget: Type[QWidget], short_cut: int, triggered: Callable[[None], None]) -> None:
        cls.instance().__addShortCut(widget, short_cut, triggered)
        widget.destroyed.connect(lambda w=widget, s=short_cut, t=triggered: cls.removeShortCut(w, s, t))# todo 자동삭제를 넣고싶음 근데 적용이 안되네

    @classmethod
    def removeShortCut(cls, widget: Type[QWidget], short_cut: int, triggered: Callable[[None], None]) -> None:
        print('destroyed', widget, QKeySequence(short_cut).toString())  
        cls.instance().removeShortCut(widget, short_cut, triggered)

    def __getSignalSet(self) -> ShortCutManagerSignal:
        return self.__signal_set

    def __currentWidget(self) -> Type[QWidget]:
        return self.__current_widget

    def __shortCutKeyList(self, widget: Type[QWidget]) -> List[int]:
        return [short_cut_iter[1] for short_cut_iter in self.__short_cut_dict.keys() if short_cut_iter[0] == widget]

    def __shortCutFunction(self, widget: Type[QWidget], short_cut: int) -> Callable[[None], None]:
        return self.__short_cut_dict.get(tuple([widget, short_cut]))

    def __addShortCut(self, widget: Type[QWidget], short_cut: int, triggered: Callable[[None], None]) -> None:
        self.__short_cut_dict[widget, short_cut] = triggered

    def __removeShortCut(self, widget: Type[QWidget], short_cut: int, triggered: Callable[[None], None]) -> None:
        if self.__shortCutFunction(widget, short_cut) == triggered:
            del self.__short_cut_dict[widget, short_cut]
        else:
            ErrorLogger.reportError('Incorrect shortCut: ' + str(QKeySequence(short_cut)))

    def event(self, event: 'QEvent') -> bool:
        if event.type() == QEvent.KeyPress:
            for key_iter in self.__shortCutKeyList(self.__currentWidget()):
                if event.key() == key_iter - Qt.CTRL:
                    print(f'Exec ShortCut: {QKeySequence(key_iter).toString()} at {self.__currentWidget()}')
                    func = self.__shortCutFunction(self.__currentWidget(), key_iter)
                    func()
                    if QApplication.activeWindow().activeView() != self.__currentWidget():
                        self.__current_widget = QApplication.activeWindow().activeView()
                    return True

        # elif event.type() == QEvent.KeyRelease and event.key() == Qt.Key_Control:
        #     print('shortcut manager finish')
        #     self.getSignalSet().ShortCutFinished.emit()
        #     print('signal')
        #     return True
        return super().event(event)

#
# from PyQt5.QtWidgets import *
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from typing import Dict, List, Callable
# from Utility.Error.ErrorLogger import *
#
#
# class ShortCutManagerSignal(QObject):
#     ShortCutFinished = pyqtSignal()
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#
# class ShortCutManager(QWidget):
#     _signalSet: ShortCutManagerSignal = ShortCutManagerSignal()
#     _shortCutDict: Dict[str, Callable[[None], None]] = {}
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.__signal_set: ShortCutManagerSignal = ShortCutManagerSignal(self)
#
#     @classmethod
#     def getSignalSet(cls) -> ShortCutManagerSignal:
#         return cls._signalSet
#
#     @classmethod
#     def shortCutList(cls) -> List[str]:
#         return list(cls._shortCutDict.keys())
#
#     @classmethod
#     def addShortCut(cls, short_cut: str, func: Callable[[None], None]) -> None:
#         cls._shortCutDict[short_cut] = func
#
#     @classmethod
#     def removeShortCut(cls, short_cut: str, func: Callable[[None], None]) -> None:
#         if cls._shortCutDict.get(short_cut) == func:
#
#             del cls._shortCutDict[short_cut]
#         else:
#             ErrorLogger.reportError('Incorrect shortCut: ' + short_cut)
#
#     def event(self, event: 'QEvent') -> bool:
#         if event.type() == QEvent.KeyPress:
#             print('shortcut manager grab keypress')
#
#         elif event.type() == QEvent.KeyRelease:
#             print('shortcut manager finish')
#             ShortCutManager.getSignalSet().ShortCutFinished.emit()
#             print('signal')
#             return True
#         return super().event(event)


