from Model.AbstractSerializeModel import *
from Model.Table.Field.TableFieldModel import *

"""
AbstractTableItemModel(AbstractSerializeModel)
AbstractTableModel에 들어갈 데이터 리스트의 인터페이스이다.
1. field(str) - data(str)의 1대 1 딕셔너리를 통해 데이터를 관리한다.
2. data가 변경될 시 변경된 field 정보를 담은 시그널을 발생시킨다.
3. 필드 정보는 부모 AbstractTableModel의 필드와 일치시킨다(adjustField)
"""


class AbstractTableItemModelSignal(QObject):
    FieldDataChanged = pyqtSignal(list)

    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class AbstractTableItemModel(AbstractSerializeModel):
    DefaultValue = ''

    def __init__(self, field_data_dict: Dict[str, str], parent: QObject):
        super().__init__(parent)
        self._setSignalSet(AbstractTableItemModelSignal(self))
        self.__field_data_dict: Dict[str, str] = field_data_dict
        self.adjustField()

    """
    property
    * fieldDataDictionary
    """
    def fieldDataDictionary(self) -> Dict[str, str]:
        return self.__field_data_dict.copy()

    """
    advanced property
    * index
    * fieldNameList
    * fieldData  (setFieldData, setFieldDatum)
    """
    def index(self) -> int:
        return self.parent().itemList().index(self)

    def fieldNameList(self) -> List[str]:
        return list(self.fieldDataDictionary().keys())

    def fieldData(self, field_name: str) -> str:
        return self.fieldDataDictionary()[field_name]

    def setFieldData(self, field_name: str, data: str) -> None:
        if field_name not in self.fieldNameList():
            raise KeyError
        if self.__field_data_dict[field_name] == data:
            return
        self.__field_data_dict[field_name] = data
        self.signalSet().FieldDataChanged.emit([field_name])

    def setFieldDatum(self, field_data_dict: Dict[str, str]) -> None:
        # 여러 field의 데이터가 한번에 변하면, 시그널의 과도한 발생을 막기 위해 한번에 시그널을 발생시킨다.
        changed_list = []
        self.blockSignals(True)
        for field_name_iter, data_iter in field_data_dict.items():
            if self.fieldData(field_name_iter) != data_iter:
                changed_list.append(field_name_iter)
                self.setFieldData(field_name_iter, data_iter)
        self.blockSignals(False)
        if changed_list:
            self.signalSet().FieldDataChanged.emit(changed_list)

    """
    method
    * hasFieldData
    * addField, removeField  
    * adjustField
    """
    def hasFieldData(self, field: str) -> bool:
        return self.fieldData(field) != AbstractTableItemModel.DefaultValue

    def addField(self, field_name: str) -> None:
        self.__field_data_dict[field_name] = AbstractTableItemModel.DefaultValue

    def removeField(self, field_name: str) -> None:
        del self.__field_data_dict[field_name]

    def adjustField(self) -> None:
        # parent(tableModel)의 fieldNameList와 불일치하는 부분을 맞춰줌
        if self.parent():
            for field_name_iter in self.parent().fieldNameList():
                if field_name_iter not in self.fieldDataDictionary():
                    self.addField(field_name_iter)

    """
    override
    * signalSet
    * load
    """
    def signalSet(self) -> AbstractTableItemModelSignal:
        return super().signalSet()

    def load(self) -> None:
        super().load()
        self.adjustField()





