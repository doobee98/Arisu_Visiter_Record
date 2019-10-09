from Utility.TableInterface.View.MyModelView import *
from typing import Optional
from Utility.TableInterface.View.Button.ButtonFactory import *


class MyModelViewFactory(QObject):
    OptionsKeyType = Tuple[Tuple[MyItemView.Option], Tuple[Optional[Tuple[MyButtonInput]]]]

    def __init__(self, parent: Type['MyTableView.MyTableView']):
        super().__init__(parent)
        self.__view_dict: Dict[MyModelViewFactory.OptionsKeyType, MyModelView] = {}


    """
    property
    * tableView
    * viewDictionary
    * buttonsDictionary
    """

    def tableView(self) -> Type['MyTableView']:
        if not self.parent():
            ErrorLogger.reportError('ModelView has no parent')
            return None
        return self.parent()

    def _viewDictionary(self) -> Dict[OptionsKeyType, MyModelView]:
        return self.__view_dict

    """
    method
    * optionView(optionDictionary)
    """
    def _generateOptionsKey(self, option_list: List[MyItemView.Option],
                            buttons_list: List[Optional[List[MyButtonInput]]]) -> OptionsKeyType:
        buttons_key_list = [tuple(buttons_iter) if buttons_iter else None for buttons_iter in buttons_list]
        return (tuple(option_list), tuple(buttons_key_list))

    def _createView(self, option_list: List[MyItemView.Option], button_list: List[Optional[List[MyButtonInput]]]) -> MyModelView:
        new_view = MyModelView(self.tableView())
        for col_iter, option_iter in enumerate(option_list):
            new_view.setColumnOption(col_iter, option_iter)
        for col_iter, buttons_iter in enumerate(button_list):
            new_view.setColumnButtons(col_iter, buttons_iter)
        self._viewDictionary()[self._generateOptionsKey(option_list, button_list)] = new_view
        return new_view

    def optionView(self, option_list: List[MyItemView.Option], button_list: List[Optional[List[MyButtonInput]]]) -> MyModelView:
        options_key = self._generateOptionsKey(option_list, button_list)
        if self._viewDictionary().get(options_key):
            return self._viewDictionary()[options_key]
        else:
            return self._createView(option_list, button_list)