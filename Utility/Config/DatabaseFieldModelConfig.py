from typing import Dict, Any
from Utility.Config.AbstractFieldConfig import *


class DatabaseFieldModelConfig(AbstractFieldConfig):
    FieldOptionList = ['auto_generate', 'writing_field']

    FieldsDictionary = {
        '고유번호': {
            'auto_generate': True,
            'writing_field': True
        },
        '성명': {
            'writing_field': True
        },
        '생년월일': {
            'writing_field': True
        },
        '차량번호': {
            'writing_field': True
        },
        '소속': {
            'writing_field': True
        },
        '방문목적': {
            'writing_field': True
        },
        '비고': {},
        '최초출입날짜': {
            'auto_generate': True
        },
        '최근출입날짜': {
            'auto_generate': True
        }
    }

    @classmethod
    def getFieldList(cls) -> List[str]:
        return list(cls.FieldsDictionary.keys())
