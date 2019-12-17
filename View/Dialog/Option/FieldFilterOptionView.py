from View.Dialog.Option.AbstractOptionView import *
from Utility.Module.ConfigModule import *
from Utility.MyPyqt.MyMessageBox import *

"""
FieldFilterOptionView(AbstractOptionView)
다른 OptionView와 다르게, FieldFilterConfigModel 모두를 이 곳에 표현하지 않고
Field별로 하나씩 표시한다.
Field 선택은 상위 OptionDialog에서 처리한다.
"""  # todo 이쁘게 정리좀 하자


class FieldFilterOptionView(AbstractOptionView):
    ON = 1
    OFF = 2

    def __init__(self, field_name: str, parent=None):
        super().__init__(parent)
        self.__model: FieldFilterConfigModel = ConfigModule.FieldFilter
        self.__model.signalSet().OptionChanged.connect(self.myRender)

        self.__field_name = field_name
        self.__button_group_dict: Dict[FieldFilterConfigModel.FilterFunction, QButtonGroup] = {}

        gbox = QGridLayout()
        gbox.addWidget(MyDefaultWidgets.basicQLabel(text='ON'), 0, 1)
        gbox.addWidget(MyDefaultWidgets.basicQLabel(text='OFF'), 0, 2)

        for idx_iter, func_enum_iter in enumerate(FieldFilterConfigModel.FilterFunction):
            row_iter = idx_iter + 1
            func_iter, func_text_iter = func_enum_iter.function(), func_enum_iter.value
            # 라벨
            lbl = MyDefaultWidgets.basicQLabel(text=func_text_iter, alignment=Qt.AlignLeft)
            gbox.addWidget(lbl, row_iter, 0)
            # 라디오 버튼
            btn_group = QButtonGroup()
            on_btn, off_btn = QRadioButton(), QRadioButton()
            btn_group.addButton(on_btn, FieldFilterOptionView.ON)
            btn_group.addButton(off_btn, FieldFilterOptionView.OFF)
            self.__button_group_dict[func_enum_iter] = btn_group
            gbox.addWidget(on_btn, row_iter, 1)
            gbox.addWidget(off_btn, row_iter, 2)
            gbox.setRowStretch(row_iter, 1)
        gbox.setHorizontalSpacing(40) # todo 임의값
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(gbox))
        self.myRender()

    """
    property
    """

    """
    advanced property
    * button
    """
    def button(self, func_enum: FieldFilterConfigModel.FilterFunction, button_type: int) -> QRadioButton:
        return self.__button_group_dict[func_enum].button(button_type)

    """
    method
    * myRender (override)
    * applyOptionChanges (override)
    """
    def myRender(self) -> None:
        active_func_list = self.__model.filterFunctionEnumList(self.__field_name)
        for func_enum_iter in FieldFilterConfigModel.FilterFunction:
            current_button_type = FieldFilterOptionView.ON if func_enum_iter in active_func_list else FieldFilterOptionView.OFF
            self.button(func_enum_iter, current_button_type).setChecked(True)

    def applyOptionChanges(self) -> None:
        current_func_list = self.__model.filterFunctionEnumList(self.__field_name)
        change_func_list = []
        for func_enum_iter in FieldFilterConfigModel.FilterFunction:
            if self.button(func_enum_iter, FieldFilterOptionView.ON).isChecked():
                change_func_list.append(func_enum_iter)

        if current_func_list != change_func_list:
            has_close = False
            if self.__field_name in self.__model.closeOptionNameList():
                reply = MyMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?')
                if reply == MyMessageBox.No:
                    self.myRender()
                    return
                else:
                    has_close = True
            self.__model._setOption(self.__field_name, change_func_list)  # option changed
            if has_close:
                sys.exit()





