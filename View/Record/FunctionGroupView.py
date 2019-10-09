from Utility.UI.BaseUI import *
from Utility.TableInterface.View.Button.ButtonFactory import *
from typing import Callable


# todo: 버튼 굳이 buttonFactory에?
class FunctionGroupView(QWidget):
    def __init__(self):
        super().__init__()

        self.__button_factory = ButtonFactory(self)
        group = QGroupBox()
        gbox = QGridLayout()
        space_string = '  '
        row = 0

        # 검색
        self.find_short_cut_text = 'Ctrl + F'
        find_text = '검색 (' + self.find_short_cut_text + ')' + space_string
        self.find_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1),
                                           text=find_text, alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.search_btn = self.buttonFactory().createButtonWidget([MyButtonInput(ButtonFactory.ButtonType.Search, enable=True)])
        gbox.addWidget(self.find_lbl, row, 0)
        gbox.addWidget(self.search_btn, row, 1)
        row += 1

        # 설정
        self.option_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1),
                                             text='설정', alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.option_btn = self.buttonFactory().createButtonWidget([MyButtonInput(ButtonFactory.ButtonType.Option, enable=True)])
        gbox.addWidget(self.option_lbl, row, 0)
        gbox.addWidget(self.option_btn, row, 1)
        row += 1

        # 마감
        self.report_lbl = BaseUI.basicQLabel(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1),
                                             text='마감', alignment=Qt.AlignVCenter | Qt.AlignLeft)
        self.report_btn = self.buttonFactory().createButtonWidget([MyButtonInput(ButtonFactory.ButtonType.Report, enable=True)])
        gbox.addWidget(self.report_lbl, row, 0)
        gbox.addWidget(self.report_btn, row, 1)
        row += 1

        group.setLayout(gbox)
        vbox = QVBoxLayout()
        vbox.addWidget(group)
        self.setLayout(vbox)

    def __str__(self):
        return 'FunctionGroupView'

    def buttonFactory(self) -> ButtonFactory:
        return self.__button_factory

    def button(self, button_type: ButtonFactory.ButtonType) -> QPushButton:
        if button_type == ButtonFactory.ButtonType.Search:
            return self.search_btn.layout().itemAt(0).widget()
        elif button_type == ButtonFactory.ButtonType.Option:
            return self.option_btn.layout().itemAt(0).widget()
        elif button_type == ButtonFactory.ButtonType.Report:
            return self.report_btn.layout().itemAt(0).widget()
        else:
            ErrorLogger.reportError('Unexpected button type:' + str(button_type))

    def setSearchSlot(self, search_func: Callable[[None], None]) -> None:
        self.buttonFactory().addButtonSlot(ButtonFactory.ButtonType.Search, search_func)

    def setOptionSlot(self, option_func: Callable[[None], None]) -> None:
        self.buttonFactory().addButtonSlot(ButtonFactory.ButtonType.Option, option_func)

    def setReportSlot(self, report_func: Callable[[None], None]) -> None:
        self.buttonFactory().addButtonSlot(ButtonFactory.ButtonType.Report, report_func)

