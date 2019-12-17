from typing import Callable, Optional
from Utility.Log.ErrorLogger import *
from PyQt5.QtCore import pyqtSlot
import types

"""
MyPyqtSlot
pyqtSlot에서 에러가 발생할 경우 캐치해 ErrorLogger에 알리기 위해서 만들어짐
"""


def MyPyqtSlot(*args):
    if len(args) == 0 or isinstance(args[0], types.FunctionType):
        args = []
    @pyqtSlot(*args)
    def Slot(original_func: Callable[..., Optional[bool]]) -> Callable[..., Optional[bool]]:
        def wrapper(*inner_args, **inner_kargs) -> Optional[bool]:
            try:
                if len(inner_args) > len(args) + 1:  # because of self argument (1)
                    inner_args = inner_args[:len(args) + 1]
                result = original_func(*inner_args, **inner_kargs)
                return result
            except Exception as e:
                ErrorLogger.reportError(f'{original_func.__name__} Slot 실행 도중 에러 발생', e)
        return wrapper
    return Slot
