from Utility.Config.ConfigSet import *
from Utility.Config.AbstractFieldConfig import *

class DatabaseFieldViewConfig(AbstractFieldConfig):
    class Option(AbstractFieldConfig.Option):
        # fit_type
        FitToContent = -1
        FitTwice = -2

    FieldOptionList = ['fit_type', 'lined_name', 'auto_generate', 'hide_field', 'date_field']

    FieldsDictionary = {
        # value 조건: if value 일시 참이어야함. bool(value) == False이면 안됨
        '고유번호': {
            'auto_generate': True,
            'hide_field': True
        },
        '성명': {
            'fit_type': Option.FitTwice
        },
        '생년월일': {
            'fit_type': Option.FitToContent
        },
        '차량번호': {
            'fit_type': Option.FitTwice
        },
        '소속': {
            'fit_type': Option.FitTwice
        },
        '방문목적': {
            'fit_type': Option.FitTwice
        },
        '비고': {
            'fit_type': Option.FitTwice
        },
        '최초출입날짜': {
            'fit_type': Option.FitToContent,
            'lined_name': '최초 출입날짜',
            'auto_generate': True,
            'date_field': True
        },
        '최근출입날짜': {
            'fit_type': Option.FitToContent,
            'lined_name': '최근 출입날짜',
            'auto_generate': True,
            'date_field': True
        }
    }

    @classmethod
    def getOption(cls, field_name: str, option_name: str) -> Any:
        if option_name == 'lined_name':
            option = super().getOption(field_name, option_name)
            return option if option else field_name
        else:
            return super().getOption(field_name, option_name)
