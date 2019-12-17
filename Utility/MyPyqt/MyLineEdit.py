# from Utility.Config.ConfigSet import *
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from typing import List, Callable
from Utility.MyPyqt.MyPyqtSlot import *

"""
MyLineEdit(QLineEdit)
* Filter Function Setter 지원 (str을 받아 걸러준 str을 내보냄)
* InputMask 설정 지원 (Time, Date)
"""


class MyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__input_mask = ''
        self.__filter_function_list: List[Callable[[str], str]] = []
        self.setAlignment(Qt.AlignCenter)
        self.editingFinished.connect(self._myEditingFinished)

    """
    method
    * setTimeMask, setDateMask
    * installFilterFunction
    """
    # todo: mask 처리를 어떻게 해야할까?
    def setTimeMask(self) -> None:
        self.__input_mask = '99:99'

    def setDateMask(self) -> None:
        self.__input_mask = '9999-99-99'

    def installFilterFunctions(self, func_list: List[Callable[[str], str]]):
        self.__filter_function_list = func_list

    """
    event
    * focusInEvent, focusOutEvent
    """
    def focusInEvent(self, a0: QFocusEvent) -> None:
        super().focusInEvent(a0)
        if self.__input_mask and not self.inputMask():
            self.setInputMask(self.__input_mask)
        self.selectAll()

    def focusOutEvent(self, a0: QFocusEvent) -> None:
        if not self.hasAcceptableInput():
            self.setInputMask('')
            self.setText('')
        super().focusOutEvent(a0)

    """
    slot
    * _myEditingFinished
    """
    @MyPyqtSlot()
    def _myEditingFinished(self) -> None:
        text = self.text()
        for func_iter in self.__filter_function_list:
            text = func_iter(text)
        if text != self.text():
            self.setText(text)