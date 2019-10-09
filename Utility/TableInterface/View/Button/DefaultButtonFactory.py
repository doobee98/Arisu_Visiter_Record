from Utility.TableInterface.View.Button.ButtonFactory import *
from PyQt5.QtGui import *


class DefaultButtonFactory(ButtonFactory):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setButtonTrigger(ButtonFactory.ButtonType.Check, ButtonFactory.ButtonTrigger.Toggled)
        self.addButtonSlot(ButtonFactory.ButtonType.Check, self.defaultCheckToggled)
        self.setButtonTrigger(ButtonFactory.ButtonType.Edit, ButtonFactory.ButtonTrigger.Toggled)
        self.addButtonSlot(ButtonFactory.ButtonType.Edit, self.defaultEditToggled)

    def _getCheckBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = super()._getCheckBtn(enable, hidden)
        btn.blockSignals(True)
        btn.setChecked(True)
        btn.blockSignals(False)
        return btn

    def _getEditBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = super()._getEditBtn(enable, hidden)
        palette = btn.palette()
        palette.setColor(QPalette.ButtonText, Qt.lightGray)
        btn.setPalette(palette)
        return btn

    @pyqtSlot(bool)
    def defaultCheckToggled(self, checked: bool) -> None:
        btn: QPushButton = self.sender()
        if btn:
            palette = btn.palette()
            palette.setColor(QPalette.ButtonText, Qt.black if checked else Qt.lightGray)
            btn.setPalette(palette)

    @pyqtSlot(bool)
    def defaultEditToggled(self, checked: bool) -> None:
        btn = self.sender()
        if btn:
            btn.setText('✐' if checked else '✎')
            palette = btn.palette()
            palette.setColor(QPalette.ButtonText, Qt.black if checked else Qt.lightGray)
            btn.setPalette(palette)

