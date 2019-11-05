from Utility.UI.BaseUI import *
from Model.Delivery.DeliveryModel import *
from Utility.Manager.ShortCutManager import *


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

        vbox.addWidget(self.title_lbl)
        vbox.addWidget(self.text_edit)
        
        self.setLayout(vbox)
        self.resize(500, 400)
        self.setWindowTitle('전달사항')
        self.render()

        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_X, lambda: self.text_edit.cut())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_C, lambda: self.text_edit.copy())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_V, lambda: self.text_edit.paste())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Z, lambda: self.text_edit.undo())
        ShortCutManager.addShortCut(self, Qt.CTRL + Qt.Key_Y, lambda: self.text_edit.redo())

    def getSignalSet(self) -> DeliveryDialogSignal:
        return self.__signal_set

    def activeView(self) -> 'ShowingView':
        return self

    def render(self) -> None:
        self.text_edit.setText(self.__model.text())

    def showEvent(self, event: QShowEvent) -> None:
        self.render()  # render
        super().showEvent(event)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.__model.setText(self.text_edit.toPlainText())
        super().closeEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
            return
        super().keyPressEvent(event)



