from typing import Callable
from Utility.Config.ConfigModule import *
from Utility.UI.BaseUI import *


# class MyButtonWidget(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         hbox = QHBoxLayout()
#         hbox.setContentsMargins(0, 0, 0, 0)
#         self.setLayout(hbox)
#         self.__button_dict: Dict['ButtonFactory.ButtonType', QPushButton] = {}
#
#     def __getButtonDictionary(self) -> Dict['ButtonFactory.ButtonType', QPushButton]:
#         return self.__button_dict
#
#     def button(self, button_type: 'ButtonFactory.ButtonType') -> QPushButton:
#         if self.__getButtonDictionary().get(button_type) is None:
#             ErrorLogger.reportError('Cannot Find ' + button_type.name + ' button in this widget.')
#             raise AttributeError()
#         return self.__getButtonDictionary()[button_type]
#
#     def addButton(self, button_type: 'ButtonFactory.ButtonType', button_widget: QPushButton) -> None:
#         self.layout().addWidget(button_widget)
#         self.__getButtonDictionary()[button_type] = button_widget


class MyButtonInput:
    def __init__(self, button_type: 'ButtonFactory.ButtonType', *, enable: bool = False, hidden: bool = False):
        self.__data_tuple = (button_type, enable, hidden)

    def dataTuple(self) -> Tuple['ButtonFactory.ButtonType', bool, bool]:
        return self.__data_tuple

    def __copy__(self):
        data_tuple = self.dataTuple()
        new_obj = MyButtonInput(data_tuple[0], enable=data_tuple[1], hidden=data_tuple[2])
        return new_obj


class ButtonFactory(QObject):
    class ButtonType(Enum):
        Add = auto()
        Check = auto()
        Delete = auto()
        Edit = auto()
        Search = auto()
        Option = auto()
        Report = auto()

        # def isSingleState(self) -> bool:
        #     return bin(self.value).count('1') == 1

    class ButtonTrigger(Enum):
        Clicked = auto()
        Toggled = auto()
        Default = Clicked

        def signal(self, btn: QPushButton):
            if self == ButtonFactory.ButtonTrigger.Clicked:
                if btn.isCheckable() is True:
                    btn.setCheckable(False)
                return btn.clicked
            elif self == ButtonFactory.ButtonTrigger.Toggled:
                if btn.isCheckable() is False:
                    btn.setCheckable(True)
                return btn.toggled
            else:
                ErrorLogger.reportError('Unexpected button trigger.')

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__button_dict: Dict[ButtonFactory.ButtonType,
                                 List[Union[ButtonFactory.ButtonTrigger, List[Callable], List[QPushButton]]]] = {
            # Button Type: [Trigger, SlotList, ButtonList]
            ButtonFactory.ButtonType.Add: [ButtonFactory.ButtonTrigger.Default, [], []],
            ButtonFactory.ButtonType.Check: [ButtonFactory.ButtonTrigger.Default, [], []],
            ButtonFactory.ButtonType.Delete: [ButtonFactory.ButtonTrigger.Default, [], []],
            ButtonFactory.ButtonType.Edit: [ButtonFactory.ButtonTrigger.Default, [], []],
            ButtonFactory.ButtonType.Search: [ButtonFactory.ButtonTrigger.Default, [], []],
            ButtonFactory.ButtonType.Option: [ButtonFactory.ButtonTrigger.Default, [], []],
            ButtonFactory.ButtonType.Report: [ButtonFactory.ButtonTrigger.Default, [], []]
        }

    """
    property
    * buttonDict
    
    * buttonTrigger(button_type)
    * buttonFunction(button_type)
    * buttonList(button_type)
    """

    def __buttonDict(self):
        return self.__button_dict

    def __buttonTrigger(self, button_type: ButtonType) -> ButtonTrigger:
        return self.__buttonDict()[button_type][0]

    def setButtonTrigger(self, button_type: ButtonType, trigger: ButtonTrigger) -> None:
        old_trigger, new_trigger = self.__buttonTrigger(button_type), trigger
        if old_trigger != new_trigger:
            for btn in self.__buttonList(button_type):
                for func in self.buttonSlotList(button_type):
                    old_trigger.signal(btn).disconnect(func)
                new_trigger.signal(btn)  # setCheckable
            self.__button_dict[button_type][0] = new_trigger
            self.__setButtonSlotList(button_type, [])
    
    def buttonSlotList(self, button_type: ButtonType) -> List[Callable[[Any], None]]:
        return self.__buttonDict()[button_type][1].copy()

    def __setButtonSlotList(self, button_type: ButtonType, func_list: List[Callable[[Any], None]]) -> None:
        self.__button_dict[button_type][1] = func_list

    def addButtonSlot(self, button_type: ButtonType, func: Callable[[Any], None]) -> None:
        trigger = self.__buttonTrigger(button_type)
        slot_list = self.buttonSlotList(button_type)
        slot_list.append(func)
        self.__setButtonSlotList(button_type, slot_list)
        for btn in self.__buttonList(button_type):
            trigger.signal(btn).connect(func)

    def removeButtonSlot(self, button_type: ButtonType, func: Callable[[Any], None]) -> None:
        trigger = self.__buttonTrigger(button_type)
        for func_iter in self.buttonSlotList(button_type):
            if func_iter == func:
                slot_list = self.buttonSlotList(button_type)
                slot_list.remove(func)
                self.__setButtonSlotList(button_type, slot_list)
                for btn in self.__buttonList(button_type):
                    trigger.signal(btn).disconnect(func)
                return
        ErrorLogger.reportError('Cannot find argument function: ' + str(func))

    def __buttonList(self, button_type: ButtonType) -> List[QPushButton]:
        return self.__buttonDict()[button_type][2]

    def removeButton(self, button_type: ButtonType, button: QPushButton) -> None:
        self.__buttonList(button_type).remove(button)

    """
    method
    
    * createButtonWidget
    """

    def createButtonWidget(self, button_input_list: List[MyButtonInput]) -> QWidget:
        btn_widget = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        btn_widget.setLayout(hbox)

        for index, button_input in enumerate(button_input_list):
            btn = None
            button_type, enable, hidden = button_input.dataTuple()
            if button_type == ButtonFactory.ButtonType.Add:
                btn = self._getAddBtn(enable, hidden)
            elif button_type == ButtonFactory.ButtonType.Check:
                btn = self._getCheckBtn(enable, hidden)
            elif button_type == ButtonFactory.ButtonType.Edit:
                btn = self._getEditBtn(enable, hidden)
            elif button_type == ButtonFactory.ButtonType.Delete:
                btn = self._getDeleteBtn(enable, hidden)
            elif button_type == ButtonFactory.ButtonType.Search:
                btn = self._getSearchBtn(enable, hidden)
            elif button_type == ButtonFactory.ButtonType.Option:
                btn = self._getOptionBtn(enable, hidden)
            elif button_type == ButtonFactory.ButtonType.Report:
                btn = self._getReportBtn(enable, hidden)

            if btn is None:
                ErrorLogger.reportError('Unexpected argument list.')
            else:
                hbox.addWidget(btn)
        btn_widget.setLayout(hbox)
        return btn_widget

    def _getAddBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Add, enable, hidden)
        btn.setText('+')
        btn_font = btn.font()
        btn_font.setBold(True)
        btn.setFont(btn_font)
        return btn

    def _getCheckBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Check, enable, hidden)
        btn.setText('✓')
        btn.id_text = ''
        return btn

    def _getDeleteBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Delete, enable, hidden)
        btn.setText('✗')
        return btn

    def _getEditBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Edit, enable, hidden)
        btn.setText('✎')
        return btn

    def _getSearchBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Search, enable, hidden)
        btn.setText('🔍')
        return btn

    def _getOptionBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Option, enable, hidden)
        btn.setText('⚙')
        return btn

    def _getReportBtn(self, enable: bool, hidden: bool) -> QPushButton:
        btn = self._getBasicButton(ButtonFactory.ButtonType.Report, enable, hidden)
        btn.setText('📄')
        return btn

    def _getBasicButton(self, button_type: ButtonType, enable: bool, hidden: bool) -> QPushButton:
        trigger = self.__buttonTrigger(button_type)
        btn = BaseUI.basicQPushButton(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+2))
        btn.setMinimumWidth(30)
        self.__buttonList(button_type).append(btn)

        btn.setEnabled(enable)
        if hidden:
            btn_size_policy = btn.sizePolicy()
            btn_size_policy.setRetainSizeWhenHidden(True)
            btn.setSizePolicy(btn_size_policy)
            btn.setHidden(hidden)

        btn_trigger = trigger.signal(btn)
        for func in self.buttonSlotList(button_type):
            btn_trigger.connect(func)
        btn.destroyed.connect(lambda: self.removeButton(button_type, btn))
        return btn