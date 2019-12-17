from Model.Table.Abstract.AbstractTableModel import *
from Model.Table.Database.VisitorModel import *
from Utility.Module.ConfigModule import *
from Utility.Module.ClockModule import *

"""
DatabaseTableModel(AbstractTableModel)
1. location을 키로 하여 구분됨
"""


class DatabaseTableModelSignal(AbstractTableModelSignal):
    SortInfoChanged = pyqtSignal()
    def __init__(self, parent: QObject = None):
        super().__init__(parent)


class DatabaseTableModel(AbstractTableModel):
    def __init__(self, location: str):
        file_path = ConfigModule.FilePath.databaseTableFilePath(location)
        self.__location = location
        self.__id_alphabet = 'A'
        self.__id_number_width = 8
        self.__sort_info: List[Union[Optional[str], bool]] = [None, True]
        super().__init__(file_path)
        self._setSignalSet(DatabaseTableModelSignal(self))
        self.signalSet().ItemInserted.connect(lambda: self._setSortInfo(None, True))
        self.signalSet().ItemChanged.connect(lambda: self._setSortInfo(None, True))

    """
    property
    * location
    """
    def location(self) -> str:
        return self.__location

    """
    advanced property
    * fieldNameList
    * sortFieldName
    * sortOrder 
    * _setSortInfo
    """
    def fieldNameList(self) -> List[str]:
        return [field_iter.name() for field_iter in ConfigModule.TableField.databaseFieldModelList()
                if not field_iter.globalOption(TableFieldOption.Global.NoModelData)]

    def sortFieldName(self) -> Optional[str]:
        return self.__sort_info[0]

    def sortOrder(self) -> bool:
        return self.__sort_info[1]

    def _setSortInfo(self, sort_field_name: Optional[str], upper: bool) -> None:
        self.__sort_info = [sort_field_name, upper]
        self.signalSet().SortInfoChanged.emit()

    """
    method
    * addItem (override)
    * sortItems
    * __generateNewId
    """
    @overload
    def addItem(self, item: VisitorModel) -> None:
        pass

    @overload
    def addItem(self, field_data_dict: Dict[str, str]) -> None:
        pass

    def addItem(self, args) -> None:
        item = None
        if isinstance(args, VisitorModel):
            item = args
        elif isinstance(args, dict):
            item = self._createItem(args)
        if item:
            if not item.hasFieldData(TableFieldOption.Necessary.ID):
                item.setFieldData(TableFieldOption.Necessary.ID, self.__generateNewId())
            if not item.hasFieldData(TableFieldOption.Necessary.DATE_FIRST):
                item.setFieldData(TableFieldOption.Necessary.DATE_FIRST, ClockModule.date().toString('yyyy-MM-dd'))
            if not item.hasFieldData(TableFieldOption.Necessary.DATE_RECENT):
                item.setFieldData(TableFieldOption.Necessary.DATE_RECENT, ClockModule.date().toString('yyyy-MM-dd'))
            super().addItem(item)
        else:
            raise AttributeError

    @overload
    def sortItems(self, sort_func: Callable[[VisitorModel], bool]) -> None:
        pass

    @overload
    def sortItems(self, sort_field: Optional[str], sort_upper: bool) -> None:
        pass

    def sortItems(self, *args) -> None:
        if len(args) == 1:
            [sort_func] = args
            self.itemList().sort(key=lambda item: sort_func(item))
            self.update()
            self._setSortInfo(None, True)
        elif len(args) == 2:
            [sort_field, sort_upper] = args
            self.itemList().sort(key=lambda item: item.fieldData(sort_field), reverse=not sort_upper)
            self.update()
            self._setSortInfo(sort_field, sort_upper)
        else:
            ErrorLogger.reportError('잘못된 인자 전달입니다.\n' + str(args), AttributeError)

    def __generateNewId(self) -> str:
        """
        database에 새로 데이터를 추가할 때, 기존에 있던 데이터와 중복되지 않는 id를 만들어줌
            고유번호 문자열 형식: id_initial_alphabet + 숫자 8자리
            __id_initial_alphabet: 고유번호 앞에 붙는 영어 문자
            __id_number_width: 고유번호 숫자 부분의 자리수
        """

        # 고유번호 숫자를 고유번호 문자열로 바꾸어주는 지역함수
        getIDString = lambda n: self.__id_alphabet + f'{n:0>{self.__id_number_width}}'
        # 기존 데이터 고유번호 리스트
        visitor_id_list = [visitor.fieldData(TableFieldOption.Necessary.ID) for visitor in self.itemList()]

        target_num = 1  # 고유번호는 1부터 시작함
        while True:
            id_str = getIDString(target_num)
            if id_str not in visitor_id_list:
                return id_str
            else:
                target_num += 1

    """
    override
    * initNull
    * _createItem
    * load
    """
    @classmethod
    def initNull(cls) -> 'DatabaseTableModel':
        return DatabaseTableModel('')

    def _createItem(self, field_data_dict: Dict[str, str]) -> VisitorModel:
        return VisitorModel(field_data_dict, self)

    def load(self) -> None:
        super().load()
        # deadline check
        if QApplication.instance():
            save_deadline = ConfigModule.Application.saveDeadline()
            today = ClockModule.datetime().toPyDateTime()
            delete_idx_list = []
            for idx in range(self.itemCount()):
                recent_date = datetime.strptime(self.item(idx).fieldData(TableFieldOption.Necessary.DATE_RECENT), '%Y-%m-%d')
                diff_days = (today - recent_date).days
                if diff_days > save_deadline:
                    delete_idx_list.append(idx)
            if delete_idx_list:
                question_string = f'출입한 지 {save_deadline}일이 지난 데이터 {len(delete_idx_list)} 건이 검색되었습니다.\n'
                question_string += '삭제하시겠습니까?'
                reply = MyMessageBox.question(QApplication.activeWindow(), '삭제', question_string)
                if reply == MyMessageBox.Yes:
                    delete_idx_list.reverse()  # 뒤에부터 지워야 idx가 그대로 유효함(앞에서부터 지우면 한칸씩 땡겨짐)
                    for idx in delete_idx_list:
                        self.removeItem(idx)
                else:
                    return

    """
    return type override
    """
    def signalSet(self) -> DatabaseTableModelSignal:
        return super().signalSet()

    def itemList(self) -> List[VisitorModel]:
        return super().itemList()

    def item(self, index: int) -> VisitorModel:
        return super().item(index)

    def findItems(self, field_data_dict: Dict[str, str]) -> List[VisitorModel]:
        return super().findItems(field_data_dict)

