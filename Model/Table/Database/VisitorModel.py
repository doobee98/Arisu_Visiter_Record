from Model.Table.Abstract.AbstractTableItemModel import *

"""
VisitorModel
"""


class VisitorModel(AbstractTableItemModel):
    def __init__(self, field_data_dict: Dict[str, str], parent: QObject):
        super().__init__(field_data_dict, parent)

    """
    override
    * initNull
    """
    @classmethod
    def initNull(cls) -> 'VisitorModel':
        return VisitorModel({}, None)

