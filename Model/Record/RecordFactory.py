from Model.Record.RecordModel import *
from enum import Enum

class RecordFactory:
    def createRecord(cls, property_dict: Dict[str, str]):
        return RecordModel(property_dict)

    def createTakeOverRecord(cls, take_over_str: str):
        record = RecordFactory.createEmptyRecord()
        record.changeProperty('고유번호', take_over_str)
        return record

    def createEmptyRecord(cls):
        property_dict = {field: RecordModel.DefaultString for field in RecordFieldModelConfig.getFieldList()}
        return RecordModel(property_dict)