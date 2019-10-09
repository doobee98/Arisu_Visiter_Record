from typing import Dict, Any
from Utility.Config.AbstractFieldConfig import *

class RecordFieldModelConfig(AbstractFieldConfig):
    FieldOptionList = ['insert_field', 'finish_field', 'writing_field']

    FieldsDictionary = {
        '출입증번호': {},
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
        '반출입물품명': {},
        '반입/반출량': {},
        '비고': {
            'writing_field': True
        },
        '들어오다시간': {
            'insert_field': True
        },
        '들어오다근무자': {
            'insert_field': True
        },
        '나가다시간': {
            'finish_field': True
        },
        '나가다근무자': {
            'finish_field': True
        },
        '고유번호': {
            'writing_field': True
        },
        '인수인계': {}
    }

    @classmethod
    def getFieldList(cls) -> List[str]:
        return list(cls.FieldsDictionary.keys())
