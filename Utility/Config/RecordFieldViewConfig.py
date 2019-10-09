from Utility.Config.ConfigModule import *
from Utility.Config.AbstractFieldConfig import *

class RecordFieldViewConfig(AbstractFieldConfig):
    class Option(AbstractFieldConfig.Option):
        # fit_type
        FitToContent = -1
        FitTwice = -2

    FieldOptionList = ['fit_type', 'lined_name', 'base_unactivated', 'group_field', 'search_field', 'hide_field']

    FieldsDictionary = {
        # value 조건: if value 일시 참이어야함. bool(value) == False이면 안됨
        '출입증번호': {
            'fit_type': Option.FitToContent,
            'lined_name': '출입증\n번호',
            'group_field': True
        },
        '성명': {
            'search_field': True
        },
        '생년월일': {
            'search_field': True
        },
        '차량번호': {
            'fit_type': Option.FitTwice,
            'group_field': True
        },
        '소속': {
            'fit_type': Option.FitTwice,
            'group_field': True
        },
        '방문목적': {
            'fit_type': Option.FitTwice,
            'group_field': True
        },
        '반출입물품명': {
            'lined_name': '반출입\n물품명'
        },
        '반입/반출량': {},
        '비고': {
            'fit_type': Option.FitTwice,
            'lined_name': '비고\n(연락처)'
        },
        '들어오다시간': {
            'fit_type': Option.FitToContent,
            'lined_name': '들어오다\n시간',
            'base_unactivated': True
        },
        '들어오다근무자': {
            'fit_type': Option.FitToContent,
            'lined_name': '들어오다\n근무자',
            'base_unactivated': True
        },
        '나가다시간': {
            'fit_type': Option.FitToContent,
            'lined_name': '\0나가다\0\n시간',
            'base_unactivated': True
        },
        '나가다근무자': {
            'fit_type': Option.FitToContent,
            'lined_name': '\0나가다\0\n근무자',
            'base_unactivated': True
        },
        '고유번호': {
            'base_unactivated': True,
            'hide_field': True
        },
        '인수인계': {
        }
    }

    @classmethod
    def getOption(cls, field_name: str, option_name: str) -> Any:
        if option_name == 'lined_name':
            option = super().getOption(field_name, option_name)
            return option if option else field_name
        else:
            return super().getOption(field_name, option_name)


