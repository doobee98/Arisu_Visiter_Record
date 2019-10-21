from View.Option.AbstractOptionView import *
from View.Option.Guide.RegexView import *
from Model.Guide.GuideModel import *
from Utility.Config.RecordFieldViewConfig import *


# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class GuideOptionView(AbstractOptionView):
    def __init__(self, guide_model: GuideModel, parent=None):
        super().__init__(parent)
        self.__model: GuideModel = guide_model
        self.__model.getSignalSet().Updated.connect(self.render)

        # field list widget
        self.__field_list_widget = QListWidget()

        # regex list widget
        self.__regex_list_widget = QListWidget()

        # list widget 스타일링
        self.__field_list_widget.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()))
        self.__regex_list_widget.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()))
        self.__field_list_widget.setFixedWidth(120)  # todo 고정
        self.__regex_list_widget.setFixedWidth(150)

        # regex 추가 버튼 todo 추가기능 넣기
        self.__add_regex_button = BaseUI.basicQPushButton(text='패턴 추가')
        self.__add_regex_button.clicked.connect(self.addRegexButtonClicked)

        # regex stacked widget
        self.__stacked_widget = QStackedWidget()
        self.__regex_list_widget.currentRowChanged.connect(self.__stacked_widget.setCurrentIndex)

        # regex text widget
        self.__test_regex_lbl = BaseUI.basicQLabel(text='입력 테스트', font=BaseUI.basicQFont(bold=True))
        self.__test_regex_le = BaseUI.basicQLineEdit()
        self.__test_one_button = BaseUI.basicQPushButton(text='하나 테스트')
        self.__test_all_button = BaseUI.basicQPushButton(text='모두 테스트')

        test_gbox = QGridLayout()
        test_gbox.addWidget(self.__test_regex_lbl, 0, 0)
        test_gbox.addWidget(self.__test_regex_le, 1, 0)
        test_gbox.addWidget(self.__test_one_button, 0, 1)
        test_gbox.addWidget(self.__test_all_button, 1, 1)

        self.__test_one_button.clicked.connect(self.testOneButtonClicked)
        self.__test_all_button.clicked.connect(self.testAllButtonClicked)


        # 전체 레이아웃
        regex_list_vbox = QVBoxLayout()
        regex_list_vbox.addWidget(self.__regex_list_widget)
        regex_list_vbox.addWidget(self.__add_regex_button)

        top_right_hbox = QHBoxLayout()
        top_right_hbox.addLayout(regex_list_vbox)
        top_right_hbox.addWidget(self.__stacked_widget)

        right_vbox = QVBoxLayout()
        right_vbox.addLayout(top_right_hbox)
        right_vbox.addSpacing(20)
        right_vbox.addLayout(test_gbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.__field_list_widget)
        hbox.addLayout(right_vbox)
        self.setLayout(hbox)

        self.render()
        self.__field_list_widget.setCurrentRow(0)
        self.__regex_list_widget.setCurrentRow(0)

    def render(self) -> None:
        self.__field_list_widget.clear()
        self.__regex_list_widget.clear()
        for idx in range(self.__stacked_widget.count()):
            self.__stacked_widget.removeWidget(self.__stacked_widget.widget(0))

        self.__field_list_widget.addItems(RecordFieldViewConfig.FieldsDictionary.keys())
        # self.__regex_list_widget.addItems(regex.title() for regex in self.__model.regexList())
        self.__regex_list_widget.addItems('AND: ' + regex.title() for regex in self.__model.andRegexList())
        self.__regex_list_widget.addItems('  OR: ' + regex.title() for regex in self.__model.orRegexList())
        for regex in self.__model.andRegexList() + self.__model.orRegexList():
            self.__stacked_widget.addWidget(RegexView(regex))

    def applyOptionChanges(self) -> None:
        pass

    @MyPyqtSlot()
    def addRegexButtonClicked(self) -> None:
        self.__model.addRegex(RegexModel())
        self.render()

    @MyPyqtSlot()
    def testOneButtonClicked(self) -> None:
        text = self.__test_regex_le.text()
        current_regex = self.__model.regexList()[self.__regex_list_widget.currentRow()]
        is_valid = current_regex.isValid(text)
        print(current_regex.toRepr(), ' // ', current_regex.toString())
        self.__test_regex_lbl.setText('Valid' if is_valid else 'Invalid')

    @MyPyqtSlot()
    def testAllButtonClicked(self) -> None:
        text = self.__test_regex_le.text()
        is_valid = self.__model.isValid(text)
        self.__test_regex_lbl.setText('Valid' if is_valid else 'Invalid')





