from Utility.Abstract.View.Button.ButtonFactory import *
from Utility.Config.ConfigModule import *
from typing import Optional



class MyItemView(QObject):
    class Option(IntFlag):
        # ColorOption
        White = auto()
        WhiteGray = auto()
        LightGray = auto()
        Gray = auto()
        DarkGray = auto()
        Black = auto()
        Dotted = auto()
        LightBlue = auto()
        Red = auto()
        _ColorSet = White | LightGray | Gray | DarkGray | Black | Dotted | LightBlue | Red  # SoloType

        # EditOption
        Uneditable = auto()
        _Unable = auto()
        Unable = Uneditable | _Unable  # Unable은 Uneditable도 포함하도록 함
        _EditSet = Uneditable | _Unable

        # FontOption
        BoldStyle = auto()
        AlignCenterStyle = auto()
        _FontStyleSet = BoldStyle | AlignCenterStyle

        # SpanOption
        SpanOwner = auto()
        _Spanned = auto()
        Spanned = _Spanned | Unable

        Default = White | AlignCenterStyle

        def __or__(self, other):
            if self & MyItemView.Option._ColorSet and other & MyItemView.Option._ColorSet:
                remove_color = self & ~MyItemView.Option._ColorSet
                return remove_color | other
            return super().__or__(other)

        def color(self):
            if self & MyItemView.Option._ColorSet:
                color_dict : Dict[MyItemView.Option, Union[Qt.GlobalColor, QBrush]]= {
                    MyItemView.Option.White: Qt.white,
                    MyItemView.Option.LightGray: Qt.lightGray,
                    MyItemView.Option.Gray: Qt.gray,
                    MyItemView.Option.DarkGray: Qt.darkGray,
                    MyItemView.Option.Black: Qt.black,
                    MyItemView.Option.Dotted: QBrush(Qt.Dense4Pattern),
                    MyItemView.Option.LightBlue: QColor(0xFFE13C),  #99ffff
                    MyItemView.Option.Red: Qt.red
                }
                return color_dict[self & MyItemView.Option._ColorSet]
            else:
                ErrorLogger.reportError('No Color Config.')
                raise AttributeError


    def __init__(self, parent: 'MyTableView',
                 *, options: Option = Option.Default, buttons: Optional[List[MyButtonInput]] = None):
        super().__init__(parent)
        self.__option: MyItemView.Option = options
        self.__buttons: Optional[List[MyButtonInput]] = buttons

    """
    property
    * tableView
    * option
    * buttons
    """

    def tableView(self) -> 'MyTableView':
        if not self.parent():
            ErrorLogger.reportError('ItemView has no parent', AttributeError)
        return self.parent()

    def option(self) -> Option:
        return self.__option

    def setOption(self, option: Option):
        self.__option = option

    def buttons(self) -> Optional[List[MyButtonInput]]:
        return self.__buttons

    def setButtons(self, buttons: Optional[List[MyButtonInput]]) -> None:
        self.__buttons = buttons

    def render(self, item: QTableWidgetItem) -> None:
        option, buttons = self.option(), self.buttons()
        table = self.tableView()
        if option & MyItemView.Option._Spanned:
            pass  # return
        if option & MyItemView.Option.SpanOwner:
            pass

        item.setBackground(option.color())

        item_flag = item.flags()
        if option & MyItemView.Option.Uneditable:
            item_flag &= ~Qt.ItemIsEditable
        else:
            item_flag |= Qt.ItemIsEditable
        if option & MyItemView.Option._Unable:
            item_flag &= ~Qt.ItemIsEnabled
        else:
            item_flag |= Qt.ItemIsEnabled
        item.setFlags(item_flag)

        item_font = item.font()
        is_bold = bool(option & MyItemView.Option.BoldStyle)
        item_font.setBold(is_bold)
        item_font.setPointSize(Config.TotalOption.baseFontSize())  #TODO FONTSIZE
        item.setFont(item_font)

        if option & MyItemView.Option.AlignCenterStyle:
            item.setTextAlignment(Qt.AlignCenter)
        else:
            item.setTextAlignment(Qt.AlignLeft)

        if buttons is not None:  # isinstance(widget, MyButtonWidget) and
            # create button widget
            button_widget = table.buttonFactory().createButtonWidget(buttons)
            if table.cellWidget(item.row(), item.column()):
                table.removeCellWidget(item.row(), item.column())
            table.setCellWidget(item.row(), item.column(), button_widget)
            # todo: 버튼 옵션 정리할것.


