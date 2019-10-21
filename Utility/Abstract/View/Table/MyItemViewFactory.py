from Utility.Abstract.View.Table.MyItemView import *
from Utility.Abstract.View.Button.ButtonFactory import *


class MyItemViewFactory(QObject):
    OptionsKeyType = Tuple[MyItemView.Option, Optional[Tuple[MyButtonInput]]]

    def __init__(self, parent: 'MyTableView'):
        super().__init__(parent)
        self.__view_dict: Dict[MyItemViewFactory.OptionsKeyType, MyItemView] = {}

    """
    property
    * tableView
    * viewDictionary
    """

    def tableView(self) -> 'MyTableView':
        if not self.parent():
            ErrorLogger.reportError('ItemViewFactory has no parent', AttributeError)
        return self.parent()

    def _viewDictionary(self) -> Dict[OptionsKeyType, MyItemView]:
        return self.__view_dict

    """
    method
    * createView(options)
    * optionView(options)
    """

    def _generateOptionsKey(self, options: MyItemView.Option,
                            buttons: Optional[List[MyButtonInput]]) -> OptionsKeyType:
        buttons_key = buttons if not buttons else tuple(buttons)
        return (options, buttons_key)

    def _createView(self, options: MyItemView.Option, buttons: Optional[List[MyButtonInput]]) -> MyItemView:
        new_view = MyItemView(self.tableView(), options=options, buttons=buttons)
        self._viewDictionary()[self._generateOptionsKey(options, buttons)] = new_view
        return new_view

    def optionView(self, options: MyItemView.Option, buttons: Optional[List[MyButtonInput]]) -> MyItemView:
        key = self._generateOptionsKey(options, buttons)
        if self._viewDictionary().get(key):
            return self._viewDictionary()[key]
        else:
            return self._createView(options, buttons)
