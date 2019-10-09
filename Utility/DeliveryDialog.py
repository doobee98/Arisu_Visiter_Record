from Utility.TableInterface.View.MyTableView import *
from Utility.ShowingView import *
from Utility.UI.BaseUI import *
from Model.Delivery.DeliveryModel import *


class DeliveryDialogSignal(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

class DeliveryDialog(QDialog, ShowingView):
    def __init__(self, model: DeliveryModel):
        super().__init__()
        self.__model = model
        self.__signal_set = DeliveryDialogSignal(self)
        location = self.__model.location()
        
        vbox = QVBoxLayout()
        self.title_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(bold=True), text=location+' 인수인계 전달 사항')
        self.text_edit = QTextEdit()
        self.text_edit.setAcceptRichText(False)
        self.text_edit.setFont(BaseUI.basicQFont())
        self.text_edit.setText(self.__model.text())

        vbox.addWidget(self.title_lbl)
        vbox.addWidget(self.text_edit)
        
        self.setLayout(vbox)
        self.resize(500, 400)
        self.setWindowTitle('전달사항')
        

    def getSignalSet(self) -> DeliveryDialogSignal:
        return self.__signal_set

    def activeView(self) -> Type['ShowingView']:
        return self

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__model.setText(self.text_edit.toPlainText())
        super().closeEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)



