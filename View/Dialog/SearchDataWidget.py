from Utility.MyPyqt.MyDefaultWidgets import *
from Model.Table.Field.TableFieldModel import *


class SearchDataWidget(QWidget):
    def __init__(self, field_name: str, parent: QWidget = None):
        super().__init__(parent)
        self.__field_name = field_name
        self.__has_single_widget = True
        hbox = QHBoxLayout()
        hbox.addWidget(self.protoLineEdit())
        self.setLayout(hbox)
        self.setMinimumWidth(300)

    """
    property
    * fieldName
    * hasSingleWidget
    """
    def fieldName(self) -> str:
        return self.__field_name

    def setFieldName(self, field_name: str) -> None:
        self.__field_name = field_name

    def hasSingleWidget(self) -> bool:
        return self.__has_single_widget

    """
    advanced property
    * protoLineEdit
    * textList
    * __firstLineEdit, __secondLineEdit
    """
    def protoLineEdit(self) -> MyLineEdit:
        le = MyDefaultWidgets.basicQLineEdit()
        le.installFilterFunctions(ConfigModule.FieldFilter.filterFunctionList(self.fieldName()))
        if ConfigModule.TableField.fieldModel(self.fieldName()).globalOption(TableFieldOption.Global.IsTime):
            le.setTimeMask()
        elif ConfigModule.TableField.fieldModel(self.fieldName()).globalOption(TableFieldOption.Global.IsDate):
            le.setDateMask()
        return le

    def textList(self) -> List[str]:
        if self.hasSingleWidget():
            return [self.__firstLineEdit().text()]
        else:
            return [self.__firstLineEdit().text(), self.__secondLineEdit().text()]

    def __firstLineEdit(self) -> MyLineEdit:
        return self.layout().itemAt(0).widget()

    def __secondLineEdit(self) -> MyLineEdit:
        return self.layout().itemAt(2).widget() if not self.hasSingleWidget() else None

    """
    method
    * setSingle, setDouble
    """
    def setSingle(self) -> None:
        self.__has_single_widget = True
        if self.layout().count() > 1:
            self.layout().takeAt(2).widget().close()  # todo close 외에 다른 방법이 있는지는 모르겠음. 혹시 버퍼가 쌓이고 있는건 아닌지?
            self.layout().takeAt(1).widget().close()

    def setDouble(self) -> None:
        self.__has_single_widget = False
        self.layout().addWidget(MyDefaultWidgets.basicQLabel(text=' ~ '))
        self.layout().addWidget(self.protoLineEdit())
        QWidget.setTabOrder(self.__firstLineEdit(), self.__secondLineEdit())
        if ConfigModule.TableField.fieldModel(self.fieldName()).globalOption(TableFieldOption.Global.IsTime):
            self.__firstLineEdit().setText('00:00')
            self.__secondLineEdit().setText('24:00')
        elif ConfigModule.TableField.fieldModel(self.fieldName()).globalOption(TableFieldOption.Global.IsDate):
            self.__firstLineEdit().setText('0000-01-01')
            self.__secondLineEdit().setText('9999-12-31')

