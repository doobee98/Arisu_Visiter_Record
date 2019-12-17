from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from typing import Dict, List, Callable, Tuple
from Utility.Log.ErrorLogger import *
from Utility.Log.ExecuteLogger import *
from PyQt5.QtWidgets import QApplication

"""
ShortCutManager
One ShortCut at One Active View -> Same One Action (no another action)
"""


class ShortCutManagerSignal(QObject):
    ShortCutFinished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class ShortCutManager(QWidget):
    _INSTANCE = None

    @classmethod
    def instance(cls, parent=None):
        if cls._INSTANCE is None:
            cls._INSTANCE = cls(parent)
        return cls._INSTANCE

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__signal_set: ShortCutManagerSignal = ShortCutManagerSignal(self)
        self.__short_cut_dict: Dict[Tuple[QWidget, int], Callable[[], None]] = {}
        self.__current_widget: QWidget = None

    """
    property
    * signalSet
    * __currentWidget
    """
    @classmethod
    def signalSet(cls) -> ShortCutManagerSignal:
        return cls.instance().signalSet()

    def __currentWidget(self) -> QWidget:
        return self.__current_widget

    """
    advanced property
    * __shortCutKeyList
    * __shortCutFunction
    """
    def __shortCutKeyList(self, widget: QWidget) -> List[int]:
        return [short_cut_iter[1] for short_cut_iter in self.__short_cut_dict.keys() if short_cut_iter[0] == widget]

    def __shortCutFunction(self, widget: QWidget, short_cut: int) -> Callable[[], None]:
        return self.__short_cut_dict.get(tuple([widget, short_cut]))

    """
    method
    * runManager, stopManager
    * addShortCut, removeShortCut
    """
    @classmethod
    def runManager(cls, widget: QWidget) -> None:
        cls.instance().grabKeyboard()
        cls.instance().__current_widget = widget

    @classmethod
    def stopManager(cls) -> None:
        cls.instance().releaseKeyboard()
        cls.instance().__current_widget = None

    @classmethod
    def addShortCut(cls, widget: QWidget, short_cut: int, triggered: Callable[[], None]) -> None:
        cls.instance().__addShortCut(widget, short_cut, triggered)

    @classmethod
    def removeShortCut(cls, widget: QWidget) -> None:
        delete_list = []
        for widget_iter, short_cut_iter in cls.instance().__short_cut_dict.keys():
            if widget_iter == widget:
                func_iter = cls.instance().__shortCutFunction(widget_iter, short_cut_iter)
                delete_list.append((widget_iter, short_cut_iter, func_iter))
        for widget_iter, short_cut_iter, func_iter in delete_list:
            cls.instance().__removeShortCut(widget_iter, short_cut_iter, func_iter)

    def __addShortCut(self, widget: QWidget, short_cut: int, triggered: Callable[[], None]) -> None:
        self.__short_cut_dict[widget, short_cut] = triggered
        widget.destroyed.connect(lambda: lambda widget=widget, short_cut=short_cut, triggerd=triggered:
                                                self.__removeShortCut(widget, short_cut, triggered))

    def __removeShortCut(self, widget: QWidget, short_cut: int, triggered: Callable[[], None]) -> None:
        if self.__shortCutFunction(widget, short_cut) == triggered:
            del self.__short_cut_dict[widget, short_cut]
        else:
            ErrorLogger.reportError('Incorrect shortCut: ' + str(QKeySequence(short_cut)))

    """
    override
    * event
    """
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
        return super().event(event)



