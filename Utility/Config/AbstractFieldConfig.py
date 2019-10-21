from enum import Enum
from typing import List, Dict, Any
from Utility.Log.ErrorLogger import *


class AbstractFieldConfig:
    class Option(Enum):
        pass

    # todo 예외를 대체할 방법?
    FieldOptionList: List[str] = NotImplementedError

    FieldsDictionary: Dict[str, Dict[str, Any]] = NotImplementedError

    @classmethod
    def getOption(cls, field_name: str, option_name: str) -> Any:
        # 필드 이름에 해당하는 옵션이 존재하면 그 옵션을 리턴, 없으면 None을 리턴
        if field_name not in cls.FieldsDictionary.keys():
            ErrorLogger.reportError(f'{field_name} 필드가 {cls.__class__}에 존재하지 않습니다.')
        else:
            options = cls.FieldsDictionary[field_name]
            if option_name not in cls.FieldOptionList:
                ErrorLogger.reportError(f'{field_name} 필드에 {option_name} 옵션이 존재하지 않습니다.')
            return options.get(option_name)  # 존재하지 않으면 None 반환
