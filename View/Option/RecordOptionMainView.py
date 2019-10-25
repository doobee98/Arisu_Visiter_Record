from Utility.Config.ConfigModule import *
from Utility.UI.BaseUI import *
from View.Option.AbstractOptionView import *
from Utility.Abstract.View.MyMessageBox import *


# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class RecordOptionMainView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = Config.RecordOption
        self.__field_widget_dict: [str, QWidget] = {field: None for field in self.__model.getFieldList()}
        gbox = QGridLayout()

        for row_iter, field_iter in enumerate(self.__field_widget_dict.keys()):
            option_iter = self.__model.getOption(field_iter)
            lbl = BaseUI.basicQLabel(text=self.__model.fieldPrintText(field_iter), alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 0)

            if type(option_iter) == bool:
                cbox = QCheckBox()
                cbox.setChecked(option_iter)
                gbox.addWidget(cbox, row_iter, 1)
                self.__field_widget_dict[field_iter] = cbox
            else:  # isinstance(self.getModel().getOption(field), int)
                le = BaseUI.basicQLineEdit(text=str(option_iter), alignment=Qt.AlignRight)
                le.setFixedWidth(100)  # todo 왜 minimum가 안될까
                gbox.addWidget(le, row_iter, 1)
                self.__field_widget_dict[field_iter] = le
            gbox.setRowStretch(row_iter, 1)
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(gbox))

    def render(self) -> None:
        for field_iter, widget_iter in self.__field_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                widget_iter.setChecked(bool(self.__model.getOption(field_iter)))
            elif isinstance(widget_iter, QLineEdit):
                widget_iter.setText(str(self.__model.getOption(field_iter)))
            else:
                ErrorLogger.reportError('QCheckbox 또는 QLineEdit중 한 종류여야 합니다.')
                raise AttributeError

    def applyOptionChanges(self) -> None:
        change_dict = {}
        for field_iter, widget_iter in self.__field_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                old_value = bool(self.__model.getOption(field_iter))
                new_value = (widget_iter.checkState() == Qt.Checked)
            elif isinstance(widget_iter, QLineEdit):
                old_value = str(self.__model.getOption(field_iter))
                new_value = widget_iter.text()
            else:
                ErrorLogger.reportError('QCheckbox 또는 QLineEdit중 한 종류여야 합니다.', AttributeError)
                return
            if old_value != new_value:
                change_dict[field_iter] = new_value
        has_close = False
        if any(field_iter in self.__model.getCloseFieldList() for field_iter in change_dict.keys()):
            reply = MyMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?')
            if reply == MyMessageBox.Yes:
                has_close = True
            else:
                self.render()
                return
        self.__model.changeOptions(change_dict)
        if has_close:
            sys.exit()





