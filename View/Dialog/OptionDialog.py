from View.Dialog.Option.Help.UpdateInfoView import *
from View.Dialog.Option.Help.HelpShortCutView import *
from View.Dialog.Option.ApplicationOptionView import *
from View.Dialog.Option.FilePathOptionView import *
from View.Dialog.Option.FieldFilterOptionView import *
from View.Dialog.Option.TableFieldOptionView import *
from View.Dialog.Option.Help.MakerView import *
from Utility.MyPyqt.ShowingView import *

"""
OptionDialog(QDialog, ShowingView)
여러 옵션들을 편집하고 볼 수 있는 다이얼로그를 관리한다.
2개의 List Widget으로 우측에 노출시킬 optionView를 설정하며,
optionView는 미리 생성해서 우측에서 stackedWidget으로 관리한다.
"""


class OptionDialog(QDialog, ShowingView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.__options_info_dict: Dict[str, Dict[str, AbstractOptionView]] = {
            '통합': {
                '일반': ApplicationOptionView(self)
            },
            # 입력필터와 필드 옵션은 두번째 list를 자체적으로 쪼개서(field 목록으로) 사용
            '입력 필터': {field_model_iter.printedName(): FieldFilterOptionView(field_model_iter.name(), self)
                      for field_model_iter in ConfigModule.TableField.fieldModelList()
                      if not field_model_iter.globalOption(TableFieldOption.Global.NoModelData)
                      },
            '필드': {field_model_iter.printedName(): TableFieldOptionView(field_model_iter.name(), self)
                      for field_model_iter in ConfigModule.TableField.fieldModelList()
                      if field_model_iter.globalOption(TableFieldOption.Global.NameChangeable)
                      },
            '파일': {
                '경로': FilePathOptionView(self)
            },
            '도움말': {
                '단축키': HelpShortCutView(self),
                '업데이트': UpdateInfoView(self),
                '제작자': MakerView(self)
            }

        }
        max_tail_string = '들어오다 근무자'

        # 테이블 필드 뷰 시그널 연결
        for table_field_view_iter in self.__options_info_dict['필드'].values():
            f: TableFieldOptionView = table_field_view_iter
            f.signalSet().ChangeButtonClicked.connect(self.__changeFieldName)
            f.signalSet().AddButtonClicked.connect(self.__addField)
            f.signalSet().RemoveButtonClicked.connect(self.__removeField)

        # 옵션 head list widget
        self.__head_list_widget = QListWidget()
        self.__head_list_widget.addItems(self.headTitleList())

        # 옵션 tail list widget
        self.__tail_list_widget = QListWidget()

        #   tail list widget 너비 설정용 임시값
        self.__tail_list_widget.addItems([max_tail_string])

        # 리스트 위젯 스타일링
        self.__head_list_widget.setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 1))
        self.__tail_list_widget.setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 1))
        self.__head_list_widget.setFixedWidth(self.__head_list_widget.sizeHintForColumn(0)
                                              + 2 * self.__head_list_widget.frameWidth())
        self.__tail_list_widget.setFixedWidth(self.__tail_list_widget.sizeHintForColumn(0)
                                              + 2 * self.__tail_list_widget.frameWidth()
                                              + self.__tail_list_widget.verticalScrollBar().sizeHint().width())

        #   tail list widget 너비 설정용 임시값 초기화
        self.__tail_list_widget.takeItem(0)

        # 옵션 stacked widget
        self.__stacked_widget = QStackedWidget()
        for head_iter in self.headTitleList():
            for tail_iter in self.tailTitleList(head_iter):
                self.__stacked_widget.addWidget(self.optionView(head_iter, tail_iter))

        # 버튼 위젯
        apply_button = MyDefaultWidgets.basicQPushButton(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 1),
                                                         text='적용')
        confirm_button = MyDefaultWidgets.basicQPushButton(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 1),
                                                           text='확인')
        cancel_button = MyDefaultWidgets.basicQPushButton(font=MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize() + 1),
                                                          text='취소')
        apply_button.clicked.connect(self.applyButtonClicked)
        confirm_button.clicked.connect(self.confirmButtonClicked)
        cancel_button.clicked.connect(self.cancelButtonClicked)

        # 버튼 레이아웃
        button_hbox = QHBoxLayout()
        button_hbox.addStretch(2)
        button_hbox.addWidget(apply_button)
        button_hbox.addStretch(1)
        button_hbox.addWidget(confirm_button)
        button_hbox.addStretch(1)
        button_hbox.addWidget(cancel_button)
        button_hbox.addStretch(2)

        # 우측 레이아웃
        right_vbox = QVBoxLayout()
        right_vbox.addStretch(3)
        right_vbox.addWidget(self.__stacked_widget)
        right_vbox.addStretch(7)
        right_vbox.addLayout(button_hbox)
        right_vbox.addStretch(1)
        margin = 30
        right_vbox.setContentsMargins(margin, margin, margin, margin)

        # 모든 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(self.__head_list_widget)
        hbox.addWidget(self.__tail_list_widget)
        hbox.addLayout(right_vbox)

        self.resize(700, 400)
        self.setLayout(hbox)
        self.setWindowTitle('설정')

        # 리스트 위젯 연결
        self.__head_list_widget.currentTextChanged.connect(self.__headChanged)
        self.__tail_list_widget.currentTextChanged.connect(self.__tailChanged)

        # 초기값
        self.__head_list_widget.setCurrentRow(0)

    """
    advanced property
    * headList, tailList
    * optionView  
    """
    def headTitleList(self) -> List[str]:
        return list(self.__options_info_dict.keys())

    def tailTitleList(self, head: str) -> List[str]:
        return list(self.__options_info_dict[head].keys())

    def optionView(self, head: str, tail: str) -> AbstractOptionView:
        return self.__options_info_dict[head][tail]

    """
    slot
    * __headChanged, __tailChanged
    * applyButtonClicked, confirmButtonClicked, cancelButtonClicked
    * __addField, __removeField, __changeFieldName
    """
    @MyPyqtSlot(str)
    def __headChanged(self, head: str) -> None:
        self.__tail_list_widget.blockSignals(True)
        for row_count in range(self.__tail_list_widget.count()):
            self.__tail_list_widget.takeItem(0)
        self.__tail_list_widget.blockSignals(False)
        self.__tail_list_widget.addItems(self.tailTitleList(head))
        self.__tail_list_widget.setCurrentRow(0)

    @MyPyqtSlot(str)
    def __tailChanged(self, tail: str) -> None:
        head = self.__head_list_widget.currentItem().text()
        self.__stacked_widget.setCurrentWidget(self.optionView(head, tail))

    @MyPyqtSlot()
    def applyButtonClicked(self) -> None:
        for head_iter in self.headTitleList():
            for tail_iter in self.tailTitleList(head_iter):
                self.optionView(head_iter, tail_iter).applyOptionChanges()

    @MyPyqtSlot()
    def confirmButtonClicked(self) -> None:
        self.applyButtonClicked()
        self.close()

    @MyPyqtSlot()
    def cancelButtonClicked(self) -> None:
        for head_iter in self.headTitleList():
            for tail_iter in self.tailTitleList(head_iter):
                self.optionView(head_iter, tail_iter).myRender()
        self.close()

    @MyPyqtSlot()
    def __addField(self) -> None:
        field_view_dict: Dict[str, TableFieldOptionView] = self.__options_info_dict['필드']
        current_field_list = [field_model_iter.name() for field_model_iter in ConfigModule.TableField.fieldModelList()]
        new_field_name = '1'
        while new_field_name in current_field_list:
            new_field_name = str(int(new_field_name) + 1)
        ConfigModule.TableField.addField(TableFieldModel(new_field_name))
        ConfigModule.FieldFilter.setFilterFunctionList(new_field_name, [FieldFilterConfigModel.FilterFunction.TrimOutSpace])

        new_field_view = TableFieldOptionView(new_field_name, self)
        new_field_view.signalSet().ChangeButtonClicked.connect(self.__changeFieldName)
        new_field_view.signalSet().AddButtonClicked.connect(self.__addField)
        new_field_view.signalSet().RemoveButtonClicked.connect(self.__removeField)
        field_view_dict[new_field_name] = new_field_view
        self.__stacked_widget.addWidget(new_field_view)
        self.__headChanged('필드')
        self.__tail_list_widget.setCurrentRow(self.__tail_list_widget.count() - 1)

    @MyPyqtSlot()
    def __removeField(self) -> None:
        sender_view = self.sender().parent()
        field_view_dict: Dict[str, TableFieldOptionView] = self.__options_info_dict['필드']

        for view_iter in field_view_dict.values():
            if view_iter.fieldName() == sender_view.fieldName():
                field_name_iter = view_iter.fieldName()
                field_printed_name_iter = ConfigModule.TableField.fieldModel(field_name_iter).printedName()
                ConfigModule.TableField.removeField(field_name_iter)
                ConfigModule.FieldFilter.removeField(field_name_iter)
                del field_view_dict[field_printed_name_iter]

                self.__stacked_widget.removeWidget(view_iter)
                self.__headChanged('필드')
                if self.__tail_list_widget.count():
                    self.__tail_list_widget.setCurrentRow(0)
                return

    @MyPyqtSlot()
    def __changeFieldName(self) -> None:
        sender_view = self.sender().parent()
        field_view_dict: Dict[str, TableFieldOptionView] = self.__options_info_dict['필드']

        for view_iter in field_view_dict.values():
            if view_iter.fieldName() == sender_view.fieldName():
                old_name = view_iter.fieldName()
                del field_view_dict[ConfigModule.TableField.fieldModel(old_name).printedName()]
                text, ok = QInputDialog.getMultiLineText(self, '필드 이름 변경', '이름 변경:', text=old_name)
                if ok:
                    new_name = text
                    ConfigModule.TableField.changeFieldName(old_name, new_name)
                    view_iter.setFieldName(new_name)
                    new_print_text = ConfigModule.TableField.fieldModel(new_name).printedName()
                    field_view_dict[new_print_text] = view_iter

                    # filter Function Update
                    old_enum_list = ConfigModule.FieldFilter.filterFunctionEnumList(old_name)
                    ConfigModule.FieldFilter.setFilterFunctionList(new_name, old_enum_list)
                    ConfigModule.FieldFilter.removeField(old_name)

                    self.__headChanged('필드')
                return

    """
    override
    * activeView
    """
    def activeView(self) -> 'ShowingView':
        return self