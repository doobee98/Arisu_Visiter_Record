from Utility.MyPyqt.MyDefaultWidgets import *
from enum import Enum, auto


"""
ButtonFactory
정해진 규격으로 버튼을 만들어냄. 이 어플리케이션에서 버튼을 사용할 때는 반드시 이 곳을 거치도록 함
"""


class ButtonFactory(QObject):
    class ButtonType(Enum):
        Add = auto()
        Edit = auto()
        Remove = auto()

    class ButtonWrapper(QWidget):
        def __init__(self, parent: QWidget = None):
            super().__init__(parent)
            self.__button_type_list: List['ButtonFactory.ButtonType'] = []
            hbox = QHBoxLayout()
            hbox.setContentsMargins(0, 0, 0, 0)
            self.setLayout(hbox)

        def _addButtonWidget(self, button_type: 'ButtonFactory.ButtonType', button: QPushButton):
            self.__button_type_list.append(button_type)
            self.layout().addWidget(button)

        def buttonWidget(self, button_type: 'ButtonFactory.ButtonType') -> QPushButton:
            return self.layout().itemAt(self.__button_type_list.index(button_type)).widget()

    @classmethod
    def createButtonWrapper(cls, *args: ButtonType):
        btn_widget = ButtonFactory.ButtonWrapper()
        for button_type_iter in args:
            if button_type_iter == ButtonFactory.ButtonType.Add:
                btn_widget._addButtonWidget(ButtonFactory.ButtonType.Add, cls._createAddButton())
            elif button_type_iter == ButtonFactory.ButtonType.Edit:
                btn_widget._addButtonWidget(ButtonFactory.ButtonType.Edit, cls._createEditButton())
            elif button_type_iter == ButtonFactory.ButtonType.Remove:
                btn_widget._addButtonWidget(ButtonFactory.ButtonType.Remove, cls._createRemoveButton())
            else:
                ErrorLogger.reportError('Unexpected argument list.')
        return btn_widget

    @classmethod
    def createCustomButton(cls, text: str, width: int = 30):
        return cls._createButton(text, width)

    @classmethod
    def _createButton(cls, text: str, width: int = 30, fix_width: bool = False) -> QPushButton:
        btn = QPushButton(text)
        if fix_width:
            btn.setFixedWidth(width)
        else:
            btn.setMinimumWidth(width)
        btn.setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 2))
        return btn

    @classmethod
    def _createAddButton(cls) -> QPushButton:
        return cls._createButton('+')

    @classmethod
    def _createEditButton(cls) -> QPushButton:
        def setButtonPalette(btn, color):
            palette = btn.palette()
            palette.setColor(QPalette.ButtonText, color)
            btn.setPalette(palette)
        btn = cls._createButton('✎')
        btn.setCheckable(True)
        setButtonPalette(btn, Qt.lightGray)
        btn.toggled.connect(lambda checked, btn=btn: setButtonPalette(btn, Qt.black if checked else Qt.lightGray))
        btn.toggled.connect(lambda checked, btn=btn: btn.setText('✐' if checked else '✎'))
        return btn

    @classmethod
    def _createRemoveButton(cls) -> QPushButton:
        return cls._createButton('✗')