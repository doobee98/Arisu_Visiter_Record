from View.Option.AbstractOptionView import *
from Utility.Config.RecordFieldViewConfig import *
from Utility.Abstract.View.MyMessageBox import *


# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class FieldFilterOptionView(AbstractOptionView):
    ON = 1
    OFF = 2

    def __init__(self, field: str, parent=None):
        super().__init__(parent)
        self.__model: FilterOptionModel = Config.FilterOption
        self.__model.getSignalSet().OptionChanged.connect(self.render)

        self.__field = field
        self.__func_list = FilterOptionModel.definedFunctionList(self.__field)
        self.__button_group_list = [QButtonGroup(self) for func in self.__func_list]
        gbox = QGridLayout()

        gbox.addWidget(BaseUI.basicQLabel(text='ON'), 0, 1)
        gbox.addWidget(BaseUI.basicQLabel(text='OFF'), 0, 2)
        for idx_iter, func_iter in enumerate(self.__func_list):
            row_iter = idx_iter + 1
            function_text = FilterOptionModel.functionPrintText(func_iter)
            lbl = BaseUI.basicQLabel(text=function_text, alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 0)

            btn_group = self.__button_group_list[idx_iter]
            on_btn, off_btn = QRadioButton(), QRadioButton()
            btn_group.addButton(on_btn, FieldFilterOptionView.ON)
            btn_group.addButton(off_btn, FieldFilterOptionView.OFF)
            gbox.addWidget(on_btn, row_iter, 1)
            gbox.addWidget(off_btn, row_iter, 2)

            gbox.setRowStretch(row_iter, 1)
        gbox.setHorizontalSpacing(40) # todo 임의값
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(gbox))
        self.render()

    def render(self) -> None:
        active_list = self.__model.activeList(self.__field)
        for idx_iter, button_group_iter in enumerate(self.__button_group_list):
            current_id = FieldFilterOptionView.ON if active_list[idx_iter] is True else FieldFilterOptionView.OFF
            button_group_iter.button(current_id).setChecked(True)

    def applyOptionChanges(self) -> None:
        current_active_list = self.__model.activeList(self.__field)
        changed_list = []
        for idx_iter, button_group_iter in enumerate(self.__button_group_list):
            current_state = button_group_iter.checkedId() == FieldFilterOptionView.ON
            changed_list.append(current_state)
        if current_active_list != changed_list:
            has_close = False
            if self.__field in self.__model.getCloseFieldList():
                reply = MyMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?')
                if reply == MyMessageBox.No:
                    self.render()
                    return
                else:
                    has_close = True
            self.__model.changeOption(self.__field, changed_list)
            if has_close:
                sys.exit()





