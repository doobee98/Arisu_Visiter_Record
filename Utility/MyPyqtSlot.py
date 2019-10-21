from typing import Callable, Union, Optional
from functools import wraps
from Utility.Log.ErrorLogger import *
from PyQt5.QtCore import pyqtSlot
import types
# TODO 여기에서 ErrorLogger를 로딩한 것 때문에 코드가 꼬일 수 있을수도

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


# def MyPyQtSlot(*args):
#     if len(args) == 0 or isinstance(args[0], types.FunctionType):
#         args = []
#     @pyqtSlot(*args)
#     def slotdecorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 func(*args)
#             except:
#                 print("Uncaught Exception in slot")
#                 traceback.print_exc()
#         return wrapper
#
#     return slotdecorator