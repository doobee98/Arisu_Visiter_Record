from Utility.Abstract.Model.MyModel import *
from Utility.Config.DatabaseFieldModelConfig import *


class VisitorModel(MyModel):
    def __init__(self, args: Union[Dict[str, Any], str]):
        super().__init__(args)

    @classmethod
    def initNull(cls) -> 'VisitorModel':
        return VisitorModel({field: None for field in DatabaseFieldModelConfig.FieldsDictionary.keys()})
