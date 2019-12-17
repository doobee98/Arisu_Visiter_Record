from View.Table.AbstractTableView import *
from Utility.MyPyqt.ShowingView import *
from Utility.MyPyqt.MyDefaultWidgets import *
from View.Dialog.SearchDataWidget import *

"""
SearchDialog(QDialog, ShowingView)
각각의 필드에 대해 lineedit를 제공하여 검색 조건을 설정할 수 있게 한다.
1. 시간과 날짜 데이터의 범위 설정 검색에는 lineEdit가 2개 필요하므로, 그를 관리할 수 있는 SearchDataWidget 클래스를 사용한다.
2. 포함과 일치를 설정하여 검색할 수 있게 하며, 완성된 검색 조건은 함수 리스트의 형식을 띈다.
"""


class SearchDialogSignal(QObject):
    SearchButtonClicked = pyqtSignal(dict)
    BeforeButtonClicked = pyqtSignal()
    NextButtonClicked = pyqtSignal()
    FinishButtonClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class SearchDialog(QDialog, ShowingView):
    class DataType(Enum):
        ContainCheckBox = '검색\n포함'
        TitleLabel = '이름'
        DataLineEdit = '내용'
        EqualButton = '일치'
        ContainButton = '포함'

    def __init__(self, table_view: AbstractTableView):
        super().__init__()
        DataType = SearchDialog.DataType
        self.__signal_set = SearchDialogSignal(self)
        self.__table_view = table_view
        self.__is_searching = False
        self.__filter_group_list = []  # 사용하지 않는 값이지만, 저장해서 유지해야 하는 값이기에 유지함

        # 검색 Grid Layout 구성
        self.__search_widget_dict: Dict[str, Dict[DataType, QWidget]] = {}
        search_grid_layout = QGridLayout()
        #   레이아웃 상단 라벨(제목)
        createHeaderLabel = lambda text: MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True, point_size=MyDefaultWidgets.basicPointSize() + 1),
                                                                      text=text, alignment=Qt.AlignLeft | Qt.AlignVCenter)
        header_contain_cbox = QCheckBox()
        search_grid_layout.addWidget(header_contain_cbox, 0, 0)
        search_grid_layout.addWidget(createHeaderLabel(DataType.TitleLabel.value), 0, 1)
        search_grid_layout.addWidget(createHeaderLabel(DataType.DataLineEdit.value), 0, 2)
        search_grid_layout.addWidget(createHeaderLabel(DataType.EqualButton.value), 0, 3)
        search_grid_layout.addWidget(createHeaderLabel(DataType.ContainButton.value), 0, 4)
        header_contain_cbox.toggled.connect(lambda checked: [self.widget(field_name_iter, DataType.ContainCheckBox).setChecked(checked)
                                                             for field_name_iter in self.searchFieldList()])

        #   데이터
        row_iter = 1
        for field_name_iter in self.searchFieldList():
            # 포함 체크박스
            contain_cbox = QCheckBox()
            contain_cbox.toggled.connect(lambda checked, field_name=field_name_iter:
                                         self.enableDataField(field_name, checked))
            # 필드 제목 라벨
            printed_field_name = ConfigModule.TableField.fieldModel(field_name_iter).printedName()
            title_lbl = MyDefaultWidgets.basicQLabel(font=MyDefaultWidgets.basicQFont(bold=True), text=printed_field_name,
                                                     alignment=Qt.AlignLeft | Qt.AlignVCenter)
            # 데이터 위젯 (LineEditor)
            data_widget = SearchDataWidget(field_name_iter)
            # 일치/포함 라디오박스
            equal_radio = QRadioButton()
            contain_radio = QRadioButton()
            filter_group = QButtonGroup()
            filter_group.addButton(equal_radio)
            filter_group.addButton(contain_radio)
            self.__filter_group_list.append(filter_group)

            # 날짜나 시간 필드면 라인에디트 두개로 늘리도록 하기
            field_model = ConfigModule.TableField.fieldModel(field_name_iter)
            if field_model.globalOption(TableFieldOption.Global.IsTime) or field_model.globalOption(TableFieldOption.Global.IsDate):
                contain_radio.toggled.connect(lambda checked, widget=data_widget: widget.setDouble() if checked is True else None)
                equal_radio.toggled.connect(lambda checked, widget=data_widget: widget.setSingle() if checked is True else None)
            contain_radio.setChecked(True)

            # 행 레이아웃
            search_grid_layout.addWidget(contain_cbox, row_iter, 0)
            search_grid_layout.addWidget(title_lbl, row_iter, 1)
            search_grid_layout.addWidget(data_widget, row_iter, 2)
            search_grid_layout.addWidget(equal_radio, row_iter, 3)
            search_grid_layout.addWidget(contain_radio, row_iter, 4)

            # 위젯 딕셔너리에 등록
            search_widget_dict_iter: Dict[DataType, QWidget] = {}
            search_widget_dict_iter[DataType.ContainCheckBox] = contain_cbox
            search_widget_dict_iter[DataType.TitleLabel] = title_lbl
            search_widget_dict_iter[DataType.DataLineEdit] = data_widget
            search_widget_dict_iter[DataType.EqualButton] = equal_radio
            search_widget_dict_iter[DataType.ContainButton] = contain_radio
            self.__search_widget_dict[field_name_iter] = search_widget_dict_iter
            row_iter += 1

        # 모두 체크 (기본적으로 모든 필드를 검색조건에 포함시킨다)
        header_contain_cbox.setChecked(True)

        # 버튼 구성
        self.__search_button = MyDefaultWidgets.basicQPushButton(text='\n검색\n')
        self.__search_button.clicked.connect(self.__searchButtonClicked)
        self.__before_button = MyDefaultWidgets.basicQPushButton(text='이전')
        self.__before_button.clicked.connect(self.__beforeButtonClicked)
        self.__next_button = MyDefaultWidgets.basicQPushButton(text='계속')
        self.__next_button.clicked.connect(self.__nextButtonClicked)
        self.__rewrite_button = MyDefaultWidgets.basicQPushButton(text='\n다시 입력\n')
        self.__rewrite_button.clicked.connect(self.__rewriteButtonClicked)

        # 버튼 레이아웃
        vbox_button = QVBoxLayout()
        vbox_button.addWidget(self.__before_button)
        vbox_button.addWidget(self.__next_button)
        hbox = QHBoxLayout()
        hbox.addWidget(self.__search_button)
        hbox.addLayout(vbox_button)
        hbox.addWidget(self.__rewrite_button)

        # 전체 레이아웃
        vbox = QVBoxLayout()
        vbox.addLayout(search_grid_layout)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setSearching(False)
        self.setFont(MyDefaultWidgets.basicQFont())
        self.setWindowIcon(QIcon(DefaultFilePath.Icon))
        self.setWindowTitle('검색')

    """
    property
    * signalSet
    * tableView
    * isSearching
    """
    def signalSet(self) -> SearchDialogSignal:
        return self.__signal_set

    def tableView(self) -> AbstractTableView:
        return self.__table_view

    def isSearching(self) -> bool:
        return self.__is_searching

    def setSearching(self, is_searching: bool) -> None:
        self.__is_searching = is_searching
        self.__adjustEnable()

    """
    adveance property
    * searchFieldList
    * widget
    """
    def searchFieldList(self) -> List[str]:
        original_field_model_list = self.tableView().fieldModelList()
        return [field_model_iter.name() for field_model_iter in original_field_model_list
                if not field_model_iter.globalOption(TableFieldOption.Global.NoSearch)]

    def widget(self, field_name: str, data_type: DataType) -> QWidget:
        return self.__search_widget_dict[field_name][data_type]

    """
    method
    * __adjustEnable
    * enableDataField
    """
    def __adjustEnable(self) -> None:
        if self.isSearching() is False:
            data_enable, search_enable, before_enable, next_enable, rewrite_enable = True, True, False, False, False
        else:
            data_enable, search_enable, before_enable, next_enable, rewrite_enable = False, False, True, True, True
        for field_name_iter in self.searchFieldList():
            contain_button: QCheckBox = self.widget(field_name_iter, SearchDialog.DataType.ContainCheckBox)
            contain_button.setEnabled(data_enable)
            if contain_button.isChecked() or not data_enable:
                self.enableDataField(field_name_iter, data_enable)
        self.__search_button.setEnabled(search_enable)
        self.__before_button.setEnabled(before_enable)
        self.__next_button.setEnabled(next_enable)
        self.__rewrite_button.setEnabled(rewrite_enable)

    def enableDataField(self, field_name: str, enable: bool) -> None:
        self.widget(field_name, SearchDialog.DataType.DataLineEdit).setEnabled(enable)
        self.widget(field_name, SearchDialog.DataType.EqualButton).setEnabled(enable)
        self.widget(field_name, SearchDialog.DataType.ContainButton).setEnabled(enable)

    """
    slot
    * __searchButtonClicked
    * __beforeButtonClicked, __nextButtonClicked
    * __rewriteButtonClicked
    """
    @MyPyqtSlot()
    def __searchButtonClicked(self) -> None:
        self.__search_button.setEnabled(False)
        search_func_dict: Dict[str, Callable[[str], bool]] = {}
        for field_name_iter in self.searchFieldList():
            if self.widget(field_name_iter, SearchDialog.DataType.ContainCheckBox).isChecked():
                data_widget: SearchDataWidget = self.widget(field_name_iter, SearchDialog.DataType.DataLineEdit)
                text_list = data_widget.textList()
                if any(text_list):
                    func = None
                    if self.widget(field_name_iter, SearchDialog.DataType.EqualButton).isChecked():
                        func = lambda text, match_str=text_list[0]: text == match_str
                    elif self.widget(field_name_iter, SearchDialog.DataType.ContainButton).isChecked():
                        if len(text_list) > 1:
                            func = lambda text, str1=text_list[0], str2=text_list[1]: text >= str1 and text <= str2
                        else:
                            func = lambda text, match_str=text_list[0]: text.find(match_str) != -1
                    if func is None:
                        ErrorLogger.reportError('포함/일치 버튼이 제대로 체크되지 않았습니다.')
                        return
                    else:
                        search_func_dict[field_name_iter] = func

        self.__search_button.setEnabled(True)
        if search_func_dict:
            self.signalSet().SearchButtonClicked.emit(search_func_dict)
            self.setSearching(True)

    @MyPyqtSlot()
    def __beforeButtonClicked(self) -> None:
        self.__before_button.setEnabled(False)
        self.signalSet().BeforeButtonClicked.emit()
        self.__before_button.setEnabled(True)

    @MyPyqtSlot()
    def __nextButtonClicked(self) -> None:
        self.__next_button.setEnabled(False)
        self.signalSet().NextButtonClicked.emit()
        self.__next_button.setEnabled(True)

    @MyPyqtSlot()
    def __rewriteButtonClicked(self) -> None:
        self.__rewrite_button.setEnabled(False)
        self.signalSet().FinishButtonClicked.emit()
        self.__rewrite_button.setEnabled(True)
        self.setSearching(False)

    """
    event
    * showEvent, closeEvent
    * keyPressEvent
    * eventFilter
    """
    def showEvent(self, a0: QShowEvent) -> None:
        super().showEvent(a0)
        self.move(QApplication.activeWindow().pos())
        if self.isSearching():
            self.__searchButtonClicked()

    def closeEvent(self, a0: QCloseEvent) -> None:
        if self.isSearching():
            self.__rewriteButtonClicked()
        super().closeEvent(a0)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def eventFilter(self, widget: QObject, event: QEvent) -> bool:  # todo 추가 처리하기
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Down:
                tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.NoModifier)  # 탭키 효과로 넘어가게
                QApplication.postEvent(self, tab_event)
                return True
            elif event.key() == Qt.Key_Up:
                shift_tab_event = QKeyEvent(QEvent.KeyPress, Qt.Key_Backtab, Qt.NoModifier)  # 백탭키 효과로 넘어가게
                QApplication.postEvent(self, shift_tab_event)
                return True
        return super().eventFilter(widget, event)

    """
    override
    * activeView
    """
    def activeView(self) -> 'ShowingView':
        return self

