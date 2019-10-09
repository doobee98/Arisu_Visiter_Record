from typing import Dict, Any, Union, Tuple, Type
from enum import Flag, IntFlag, auto, Enum
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Utility.Error.ErrorLogger import *


class MyModelSignal(QObject):
    """
    MyModelSignal
    PropertyChanged: setProperty, setProperties 등을 통해 Model의 Property가 변경되었을때 방출
    """
    Updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class MyModel(QObject):
    """
    MyModel: Abstract Class
    __signal_set
    __property_dict: field를 key로 하고, property를 value로 하는 데이터 셋. field는 각 FieldModelConfig를 중심으로 함.
                     property의 조건: 구분자(@#@#@)를 포함하지 않는 str, 또는 bool 타입
    """
    DefaultString = ''  # property 기본값


    def __init__(self, args: Union[Dict[str, Union[str, bool]], str]):
        """
        :param args: property_dict 또는 str을 인자로 받음.
                property_dict: 인자를 바탕으로 model 초기화
                str: __initWithStr에 주어진 규약을 통해 model 초기화
        """
        super().__init__()
        self.__signal_set: Type[MyModelSignal] = MyModelSignal(self)
        self.__property_dict: Dict[str, Union[str, bool]] = {}

        if isinstance(args, dict):
            for field in args.keys():
                self._setProperty(field, args[field])
        elif isinstance(args, str):
            self._initWithStr(args)
        else:
            ErrorLogger.reportError('Unexpected args type')

    def _initWithStr(self, obj_str: str) -> None:
        """
        __str__ 함수를 거쳐 문자열화 된 객체를 다시 읽어들임
        :param obj_str: 문자열화 된 객체
        """
        line_delimeter, arg_delimeter = '\n', '@#@#@'  # 구분자가 사용자 입력과 겹치지 않도록 조금 특이하게 만듬
        read_mode = 'parameter_load'

        for line in obj_str.split(line_delimeter):
            args = line.split(arg_delimeter)
            head = args[0]

            if head == 'MyModel_Start':
                continue
            elif head == 'MyModel_End':
                break

            if read_mode == 'parameter_load':
                if head == 'property_dict':
                    read_mode = 'property_dict_load'
            elif read_mode == 'property_dict_load':
                if head != 'property_dict':
                    key_str, value_str = args[0], args[1]
                    if value_str == '_##_True_##_' or value_str == '_##_False_##_':
                        self._setProperty(key_str, (value_str == '_##_True_##_'))
                    else:
                        self._setProperty(key_str, value_str)
                else:  # head == 'property_dict'
                    read_mode = 'parameter_load'

    def __str__(self) -> str:
        """
        정해둔 규약을 통해 객체를 문자열화함
        :return: 문자열
        """
        obj_str = 'MyModel_Start\n'
        obj_str += 'property_dict@#@#@Dict\n'
        for field, property in self.__property_dict.items():
            if isinstance(property, bool):
                obj_str += f'{field}@#@#@_##_{property}_##_\n'
            else:
                obj_str += f'{field}@#@#@{property}\n'
        obj_str += 'property_dict@#@#@Dict\n'
        obj_str += 'MyModel_End\n'
        return obj_str

    def getSignalSet(self) -> Type[MyModelSignal]:
        return self.__signal_set

    def _setSignalSet(self, signal: Type[MyModelSignal]) -> None:
        self.__signal_set = signal

    def update(self) -> None:
        self.getSignalSet().Updated.emit()

    def isFieldExist(self, field: str) -> bool:
        return field in self.getProperties().keys()

    def getProperty(self, field: str) -> Union[str, bool]:
        if field not in self.getProperties().keys():
            ErrorLogger.reportError(f'Field does not exist in properties: {field}')
            raise AttributeError()
            #return self._getProperties().get(field)
        return self.getProperties()[field]

    def getProperties(self) -> Dict[str, Union[str, bool]]:
        return self.__property_dict.copy()

    def _setProperty(self, field: str, property: Union[str, bool]) -> None:
        self.__property_dict[field] = property
        self.update()

    def changeProperty(self, field: str, property: Union[str, bool]) -> bool:
        """
        field의 property가 기존 데이터와 다를 경우 변경함.
        :return: 변경에 성공하면 True, 실패하면 False
        """
        if self.getProperty(field) != property:
            self._setProperty(field, property)
            return True
        else:
            return False

    def changeProperties(self, property_dict: Dict[str, Union[str, bool]]) -> bool:
        """
        두 개 이상의 property를 바꿔야 할 때, setProperty를 사용하면
        adjustState와 propertyChanged가 여러번 호출되며 오버헤드 및 오작동 가능성이 있어서
        별도의 함수로 정의
        :return: 하나라도 변경에 성공하면 True, 실패하면 False
        """
        changed_flag = False
        self.blockSignals(True)
        for field, property in property_dict.items():
            changed_flag = self.changeProperty(field, property) or changed_flag
        self.blockSignals(False)

        if changed_flag:
            self.update()
        return changed_flag

    def blockSignals(self, b: bool) -> bool:
        self.getSignalSet().blockSignals(b)
        return super().blockSignals(b)
