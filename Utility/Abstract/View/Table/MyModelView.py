from Utility.Abstract.View.Table.MyItemViewFactory import *
from Utility.Abstract.View.Button.ButtonFactory import *


class MyModelView(QObject):
    def __init__(self, parent: 'MyTableView'):
        super().__init__(parent)

        self.__column_options: Dict[int, MyItemView.Option] = {}
        self.__column_buttons: Dict[int, Tuple[MyButtonInput]] = {}

    """
    property
    * tableView
    * columnOptions
    * columnButtons
    """

    def tableView(self) -> 'MyTableView':
        if not self.parent():
            ErrorLogger.reportError('ModelView has no parent', AttributeError)
        return self.parent()

    def columnOption(self, column: int) -> MyItemView.Option:
        if self.__column_options.get(column):
            return self.__column_options[column]
        else:
            return MyItemView.Option.Default  # Todo default 처리가 맞는가? 에러?

    def setColumnOption(self, column: int, options: MyItemView.Option) -> None:
        self.__column_options[column] = options

    def columnButtons(self, column: int) -> List[MyButtonInput]:
        if self.__column_buttons.get(column):
            return self.__column_buttons[column].copy()
        else:
            return None  # Todo default 처리가 맞는가? 에러?

    def setColumnButtons(self, column: int, buttons: List[MyButtonInput]):
        self.__column_buttons[column] = buttons

    """
    rendering
    """

    def render(self, items: List[QTableWidgetItem], model: MyModel = None):
        """
        render MyModel to tablewidgetitems
        """
        if items:
            if model:
                self._renderText(items, model)
            #self._renderButton(items)
            self._renderStyle(items)

    def _renderText(self, items: List[QTableWidgetItem], model: MyModel):
        if items and model:
            table = self.tableView()
            for model_field in table.modelFieldList():
                field_column = table.fieldColumn(model_field)
                items[field_column].setText(str(model.getProperty(model_field)))

            """
            1. field list를 테이블로부터 가져옴
            2. field col을 얻음
            3. model에서 field property를 가져옴
            4. property를 items[col]에 배치함
            """

    def _renderStyle(self, items: List[QTableWidgetItem]):  # need to call after _renderButton
        if items:
            table = self.tableView()
            item_factory = table.itemViewFactory()

            for col_iter, item_iter in enumerate(items):
                option_iter = self.columnOption(col_iter)
                button_iter = self.columnButtons(col_iter)

                if option_iter & MyItemView.Option.SpanOwner:
                    row, col_span = items[0].row(), 1
                    for spanned_col_iter in range(col_iter + 1, len(items)):
                        if self.columnOption(spanned_col_iter) & MyItemView.Option._Spanned:
                            col_span += 1
                        else:
                            break
                    table.setSpan(row, col_iter, 1, col_span)

                # rendering item style to item type
                item_factory.optionView(option_iter, button_iter).render(item_iter)

                # # set button state
                # for button_type_iter in ButtonFactory.ButtonType:
                #     if button_type_iter in button_list_iter:
                #         button_widget = table.cellWidget(item_iter.row(), item_iter.column())
                #         btn = ButtonFactory.getButtonFromWidget(button_widget, button_type_iter)
                #         btn.setEnabled(self.buttonEnableState(button_type_iter))
                #         btn.setHidden(self.buttonHiddenState(button_type_iter))


            """
            여긴 abstract class이므로 아주 기초적인 것만 배치
            즉, 반드시 행해져야 할 것들만 둠 (폰트 크기, 중앙정렬 등? 이건 생성할 때 해야할까)
            
            이 함수에서 설정해야 할 값
            1. bold 처리
            2. 배경 색, 글자 색
            3. editable, enable 변수 정리
            4. 버튼 상태
            """

