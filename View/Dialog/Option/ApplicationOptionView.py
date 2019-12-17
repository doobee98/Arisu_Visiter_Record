from View.Dialog.Option.AbstractOptionView import *
from Utility.Module.ConfigModule import *
from Utility.MyPyqt.MyMessageBox import *

"""
ApplicationOptionView(AbstractOptionView)
""" # todo 이쁘게 정리하기

# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class ApplicationOptionView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = ConfigModule.Application
        self.__option_widget_dict: [ApplicationConfigModel.OptionName, QWidget] = {
            option_enum_iter: None for option_enum_iter in ApplicationConfigModel.OptionName
        }

        gbox = QGridLayout()
        for row_iter, option_enum_iter in enumerate(ApplicationConfigModel.OptionName):
            field_name_iter = option_enum_iter.value
            lbl = MyDefaultWidgets.basicQLabel(text=field_name_iter, alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 0)

            option_iter = self.__model.option(option_enum_iter)
            if type(option_iter) == bool:
                cbox = QCheckBox(self)
                cbox.setChecked(option_iter)
                gbox.addWidget(cbox, row_iter, 1)
                self.__option_widget_dict[option_enum_iter] = cbox
            else:
                le = MyDefaultWidgets.basicQLineEdit(text=str(option_iter), alignment=Qt.AlignRight)
                le.setFixedWidth(100)  # todo 왜 minimum가 안될까
                gbox.addWidget(le, row_iter, 1)
                self.__option_widget_dict[option_enum_iter] = le
            gbox.setRowStretch(row_iter, 1)  # todo: row stretch? 의도는 높이를 모두 같게 하기 위해서
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(gbox))
        #self.myRender()

    def widget(self, option_enum: ApplicationConfigModel.OptionName) -> Union[QCheckBox, QLineEdit]:
        return self.__option_widget_dict[option_enum]

    def myRender(self) -> None:
        for option_enum_iter, widget_iter in self.__option_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                widget_iter.setChecked(bool(self.__model.option(option_enum_iter)))
            elif isinstance(widget_iter, QLineEdit):
                widget_iter.setText(str(self.__model.option(option_enum_iter)))
            else:
                ErrorLogger.reportError('QCheckbox 또는 QLineEdit중 한 종류여야 합니다.')
                raise AttributeError

    def applyOptionChanges(self) -> None:
        change_dict = {}
        for option_enum_iter, widget_iter in self.__option_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                old_value = bool(self.__model.option(option_enum_iter))
                new_value = (widget_iter.checkState() == Qt.Checked)
            elif isinstance(widget_iter, QLineEdit):
                old_value = str(self.__model.option(option_enum_iter))
                new_value = widget_iter.text()
            else:
                ErrorLogger.reportError('QCheckbox 또는 QLineEdit중 한 종류여야 합니다.', AttributeError)
                return
            if old_value != new_value:
                change_dict[option_enum_iter] = new_value
        has_close = False
        if any(option_enum_iter.value in self.__model.closeOptionNameList() for option_enum_iter in change_dict.keys()):
            reply = MyMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?')
            if reply == MyMessageBox.Yes:
                has_close = True
            else:
                self.myRender()
                return
        for option_enum_iter, data_iter in change_dict.items():
            self.__model.setOption(option_enum_iter, data_iter)
        if has_close:
            sys.exit()





