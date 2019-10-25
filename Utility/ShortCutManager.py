from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import Dict, List, Callable, Tuple
from Utility.Log.ErrorLogger import *
from Utility.Log.ExecuteLogger import *
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
        self.__short_cut_dict: Dict[Tuple[QWidget, int], Callable[[None], None]] = {}
        self.__current_widget: QWidget = None

    @classmethod
    def instance(cls, parent=None):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(parent)
        return cls._INSTANCE

    @classmethod
    def runManager(cls, widget: QWidget) -> None:
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
    def addShortCut(cls, widget: QWidget, short_cut: int, triggered: Callable[[None], None]) -> None:
        cls.instance().__addShortCut(widget, short_cut, triggered)

    @classmethod
    def removeShortCut(cls, widget: QWidget, short_cut: int, triggered: Callable[[None], None]) -> None:
        print('destroyed', widget, QKeySequence(short_cut).toString())  
        cls.instance().removeShortCut(widget, short_cut, triggered)

    def __getSignalSet(self) -> ShortCutManagerSignal:
        return self.__signal_set

    def __currentWidget(self) -> QWidget:
        return self.__current_widget

    def __shortCutKeyList(self, widget: QWidget) -> List[int]:
        return [short_cut_iter[1] for short_cut_iter in self.__short_cut_dict.keys() if short_cut_iter[0] == widget]

    def __shortCutFunction(self, widget: QWidget, short_cut: int) -> Callable[[None], None]:
        return self.__short_cut_dict.get(tuple([widget, short_cut]))

    def __addShortCut(self, widget: QWidget, short_cut: int, triggered: Callable[[None], None]) -> None:
        self.__short_cut_dict[widget, short_cut] = triggered
        widget.destroyed.connect(lambda: lambda widget=widget, short_cut=short_cut, triggerd=triggered:
                                                self.__removeShortCut(widget, short_cut, triggered))

    def __removeShortCut(self, widget: QWidget, short_cut: int, triggered: Callable[[None], None]) -> None:
        print('removeCall', widget, short_cut, triggered)
        if self.__shortCutFunction(widget, short_cut) == triggered:
            del self.__short_cut_dict[widget, short_cut]
        else:
            ErrorLogger.reportError('Incorrect shortCut: ' + str(QKeySequence(short_cut)))

    def event(self, event: 'QEvent') -> bool:
        if event.type() == QEvent.KeyPress:
            for key_iter in self.__shortCutKeyList(self.__currentWidget()):
                if event.key() == key_iter - Qt.CTRL:
                    ExecuteLogger.printLog(f'Exec ShortCut: {QKeySequence(key_iter).toString()} at {self.__currentWidget()}')
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



