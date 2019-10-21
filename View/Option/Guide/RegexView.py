from Model.Guide.RegexModel import *
from Utility.UI.BaseUI import *

class RegexView(QWidget):
    def __init__(self, model: RegexModel):
        super().__init__()
        self.__model: RegexModel = model
        self.__model.getSignalSet().Updated.connect(self.render)

        # 패턴 타입박스
        self.__all_lbl = BaseUI.basicQLabel(text='반드시 ')
        self.__or_lbl = BaseUI.basicQLabel(text='또는 ')
        self.__all_rbox = QRadioButton()
        self.__or_rbox = QRadioButton()
        if self.__model.patternType() == RegexModel.Type.AND:
            self.__all_rbox.setChecked(True)
        else:
            self.__or_rbox.setChecked(True)
        
        # 패턴 타입박스 레이아웃
        type_hbox = QHBoxLayout()
        type_hbox.addStretch(1)
        type_hbox.addWidget(self.__all_lbl)
        type_hbox.addWidget(self.__all_rbox)
        type_hbox.addStretch(1)
        type_hbox.addWidget(self.__or_lbl)
        type_hbox.addWidget(self.__or_rbox)
        type_hbox.addStretch(1)

        # 제목, 패턴, 오류 라벨과 편집창
        title_lbl = BaseUI.basicQLabel(text='제목 ')
        pattern_lbl = BaseUI.basicQLabel(text='패턴 ')
        invalid_lbl = BaseUI.basicQLabel(text='오류 ')

        self.__title_le = BaseUI.basicQLineEdit(text=self.__model.title())
        self.__pattern_le = BaseUI.basicQLineEdit(text=self.__model.toRepr())
        self.__invalid_le = BaseUI.basicQLineEdit(text=self.__model.invalidMessage())

        # self.__pattern_hint_lbl = BaseUI.basicQLabel(alignment=Qt.AlignLeft)
        hint_string = ''
        hint_string += '<시작>, <끝>: 문자열의 시작과 끝' + '\n'
        hint_string += '<한>: 완성된 한글 문자' + '\n'
        hint_string += '<영>: 영어 문자' + '\n'
        hint_string += '<영소>: 영어 소문자' + '\n'
        hint_string += '<영대>: 영어 대문자' + '\n'
        hint_string += '<수>: 0부터 9까지의 숫자 문자' + '\n'
        hint_string += '<자연수>: 0을 제외한 숫자 문자' + '\n'
        hint_string += '<공백>: 공백 문자'
        # self.__pattern_hint_lbl.setText(hint_string)

        gbox = QGridLayout()
        gbox.addWidget(title_lbl, 0, 0)
        gbox.addWidget(pattern_lbl, 1, 0)
        gbox.addWidget(invalid_lbl, 2, 0)
        gbox.addWidget(self.__title_le, 0, 1)
        gbox.addWidget(self.__pattern_le, 1, 1)
        gbox.addWidget(self.__invalid_le, 2, 1)

        # 기능 버튼
        self.__change_button = BaseUI.basicQPushButton(text='변경')
        self.__change_button.clicked.connect(self.changeButtonClicked)
        self.__delete_button = BaseUI.basicQPushButton(text='삭제')
        self.__delete_button.clicked.connect(self.deleteButtonClicked)

        # 기능 버튼 레이아웃
        button_hbox = QHBoxLayout()
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.__change_button)
        button_hbox.addStretch(1)
        button_hbox.addWidget(self.__delete_button)
        button_hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(type_hbox)
        vbox.addStretch(1)
        vbox.addLayout(gbox)
        vbox.addStretch(1)
        vbox.addLayout(button_hbox)
        self.setLayout(vbox)

    def getDataFromView(self) -> Dict[str, str]:
        if self.__all_rbox.isChecked() is True:
            pattern_type = RegexModel.Type.AND
        else:
            pattern_type = RegexModel.Type.OR
        return {
            'pattern_type': pattern_type,
            'title': self.__title_le.text(),
            'input_pattern': self.__pattern_le.text(),
            'invalid_message': self.__invalid_le.text()
        }

    def changeModel(self) -> None:
        if self.__all_rbox.isChecked() is True:
            pattern_type = RegexModel.Type.AND
        else:
            pattern_type = RegexModel.Type.OR
        # TODO 한번에 바뀌는게 아니라 하나씩 바뀌어서 render가 먼저 호출되어 버림
        self.__model.setPatternType(pattern_type)
        self.__model.setPattern(self.__pattern_le.text())
        self.__model.setTitle(self.__title_le.text())
        self.__model.setInvalidMessage(self.__invalid_le.text())

    def render(self) -> None:
        if self.__model.patternType() == RegexModel.Type.AND:
            self.__all_rbox.setChecked(True)
        else:
            self.__or_rbox.setChecked(True)
        self.__title_le.setText(self.__model.title())
        self.__pattern_le.setText(self.__model.toRepr())
        self.__invalid_le.setText(self.__model.invalidMessage())

    @MyPyqtSlot()
    def changeButtonClicked(self) -> None:
        self.changeModel()

    @MyPyqtSlot()
    def deleteButtonClicked(self) -> None:
        pass

