from Utility.TableInterface.Model.MyModel import *
from Utility.Config.DatabaseFieldModelConfig import *



class VisitorModelSignal(MyModelSignal):
    def __init__(self, parent=None):
        super().__init__(parent)

class VisitorModel(MyModel):
    def __init__(self, args: Union[Dict[str, Any], str]):
        super().__init__(args)
        self._setSignalSet(VisitorModelSignal(self))

