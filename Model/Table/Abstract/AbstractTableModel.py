from Model.AbstractSerializeModel import *
from Model.Table.Field.TableFieldModel import *
from Model.Table.Abstract.AbstractTableItemModel import *
from typing import overload

"""
AbstractTableModel(AbstractSerializeModel)
AbstractTableItemModel을 관리하는 테이블
1. 해당 테이블에서 관리할 아이템의 FieldList를 가짐(TableFieldModel이 아닌, Name(str)으로 관리함)
2. 아이템의 변화(FieldDataChanged)를 수신하고 변환하여 index를 포함한 시그널을 발생시킴(Changed, Inserted, Removed) 
3. 아이템 접근 메소드를 제공함
"""


class AbstractTableModelSignal(QObject):
    ItemChanged = pyqtSignal(int)
    ItemInserted = pyqtSignal(int)
    ItemRemoved = pyqtSignal(int)

    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class AbstractTableModel(AbstractSerializeModel):
    def __init__(self, file_path: str, parent: QObject = None):
        self.__auto_save = True
        self.__item_list: List[AbstractTableItemModel] = []
        super().__init__(parent)
        self._setSignalSet(AbstractTableModelSignal(self))
        self.setFilePath(file_path)

        if self.hasFile():
            self.load()
        else:
            self.save()

    """
    property
    * itemList
    * autoSave
    """
    def itemList(self) -> List[AbstractTableItemModel]:
        return self.__item_list

    def _setItemList(self, item_list: List[AbstractTableItemModel]) -> None:
        self.__item_list = item_list

    def autoSave(self) -> bool:
        return self.__auto_save

    def setAutoSave(self, enable: bool) -> None:
        self.__auto_save = enable

    """
    advanced property
    * fieldNameList
    * item
    * itemCount
    """
    def fieldNameList(self) -> List[str]:
        raise NotImplementedError

    def item(self, index: int) -> AbstractTableItemModel:
        return self.itemList()[index]

    def itemCount(self) -> int:
        return len(self.itemList())

    """
    method
    * _createItem
    * _connectItem
    * addItem, insertItem, removeItem
    * findItems
    """
    def _createItem(self, field_data_dict: Dict[str, str]) -> AbstractTableItemModel:
        raise NotImplementedError
    
    def _connectItem(self, item: AbstractTableItemModel) -> None:
        if item.parent() != self:
            item.setParent(self)
            item.adjustField()
        item.signalSet().FieldDataChanged.connect(self._itemFieldDataChanged)

    @overload
    def addItem(self, item: AbstractTableItemModel) -> None:
        pass

    @overload
    def addItem(self, field_data_dict: Dict[str, str]) -> None:
        pass

    def addItem(self, args) -> None:
        self.insertItem(self.itemCount(), args)

    @overload
    def insertItem(self, index: int, item: AbstractTableItemModel) -> None:
        pass

    @overload
    def insertItem(self, index: int, field_data_dict: Dict[str, str]) -> None:
        pass

    def insertItem(self, index: int, args) -> None:
        item = None
        if isinstance(args, AbstractTableItemModel):
            item = args
        elif isinstance(args, dict):
            item = self._createItem(args)
        if item:
            self.__item_list.insert(index, item)
            self._connectItem(item)
            self.update()
            self.signalSet().ItemInserted.emit(index)
        else:
            raise AttributeError

    def removeItem(self, index: int) -> None:
        del self.__item_list[index]
        self.update()
        self.signalSet().ItemRemoved.emit(index)

    def findItems(self, field_data_dict: Dict[str, str]) -> List[AbstractTableItemModel]:
        # field_data_dict의 조건에 일치하는 데이터를 검색한다.
        match_data_list = []
        for item in self.itemList():
            if all([item.fieldData(field) == data for field, data in field_data_dict.items()]):
                match_data_list.append(item)
        return match_data_list

    """
    slot
    * itemFieldDataChanged
    """
    @MyPyqtSlot()
    def _itemFieldDataChanged(self):
        idx = self.itemList().index(self.sender().parent())
        if idx is not None:
            self.update()
            self.signalSet().ItemChanged.emit(idx)
            return

    """
    override
    * signalSet
    * save
    * load
    """
    def signalSet(self) -> AbstractTableModelSignal:
        return super().signalSet()

    def save(self) -> None:
        if self.autoSave():
            super().save()

    def load(self) -> None:
        super().load()
        for item_iter in self.itemList():
            self._connectItem(item_iter)
