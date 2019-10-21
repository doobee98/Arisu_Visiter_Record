from Utility.Abstract.View.ShowingView import *
from Utility.UI.BaseUI import *
from Model.Delivery.DeliveryModel import *
from Utility.ShortCutManager import *


class CheckTakeoverDialog(QDialog, ShowingView):
    def __init__(self, takeover_string: str, delivery_string: str, parent=None):
        super().__init__(parent=parent)
        self.setWindowTitle('확인')

        # todo 여유있을 때 제작하기

    def activeView(self) -> 'ShowingView':
        return self




