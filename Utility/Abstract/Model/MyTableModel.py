from Utility.CryptModule import *
from Utility.Abstract.Model.MyModel import *
import os

# 레코드 번호를 가지는, 더블 링크드 리스트 형태로 바꾸기
# 이는 데이터의 삭제와 삽입이 잦은 것을 보완하기 위함
# 추가해야할 데이터 필드: head, tail 객체(인덱스) -> 순서가 실제 데이터 연관과 관련이 없기 때문이다.


class MyTableModelSignal(QObject):
    """
    MyTableModelSignal
    ModelUpdated(int): 업데이트된 모델의 index와 함께 발생함 
    TableModelUpdated(): 사용하지 않음
    """
    ModelUpdated = pyqtSignal(int)
    TableModelUpdated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class MyTableModel(AbstractModel):
    """
    MyTableModel
    __signal_set
    __file_name: 암호화되어 저장된 파일 이름, 파일로 저장하지 않으면 None
    __field_list: data의 필드 리스트
    __data_type: data의 타입. 다루는 데이터가 MyModel을 상속한다면 호출한다.
    __data_list: data 리스트
    """
    def __init__(self, field_list: List[str]):
        super().__init__()
        self._setSignalSet(MyTableModelSignal(self))
        self.__field_list: List[str] = field_list
        self.__data_type: Type[MyModel] = MyModel
        self.__data_list: List[MyModel] = []

    def getSignalSet(self) -> MyTableModelSignal:
        return super().getSignalSet()

    def getFieldList(self) -> List[str]:
        return self.__field_list.copy()

    def _setFieldList(self, field_list: List[str]) -> None:
        self.__field_list = field_list
    
    # todo addDataComamand에서 사용하는데 대체 방법이 있을까
    def getDataType(self) -> Type[MyModel]:
        return self.__data_type

    def _setDataType(self, data_type: Type[MyModel]) -> None:
        self.__data_type = data_type

    def getDataList(self) -> List[MyModel]:
        return self.__data_list

    def getData(self, idx: int) -> MyModel:
        self._checkValidIndex(idx)
        return self.getDataList()[idx]

    def _setData(self, idx: int, data: MyModel) -> None:
        """
        인자로 받은 model을 table에 추가시킴.
        * 만일 table에서 요구하는 field가 없다면 default string으로 생성하여 채워넣음. (이 과정에서 protect method 사용)
        """
        if idx != self.getDataCount():
            self._checkValidIndex(idx)
        self._checkValidData(data)
        for field in self.getFieldList():
            if data.getProperties().get(field) is None:
                data._setProperty(field, MyModel.DefaultString)
        self.__data_list.insert(idx, data)
        data.getSignalSet().Updated.connect(self.dataChanged)
        self.getSignalSet().ModelUpdated.emit(idx)

    def getDataCount(self) -> int:
        """
        :return: table model이 관리하는 data 갯수
        """
        return len(self.getDataList())

    # todo 꼭필요? 방법 다른거 없을까?
    def getDataIndex(self, data: MyModel) -> int:
        for idx_iter, data_iter in enumerate(self.getDataList()):
            if data == data_iter:
                return idx_iter
        return None

    def addData(self, data: MyModel) -> None:
        self.insertData(self.getDataCount(), data)

    def insertData(self, idx: int, data: MyModel) -> None:
        self._setData(idx, data)
        self.update()

    def deleteData(self, idx: int) -> MyModel:
        deleted_data = self.getData(idx)
        del self.__data_list[idx]
        self.update()
        return deleted_data

    def findData(self, property_dict: Dict[str, AbstractModel.AttrType]) -> List[MyModel]:
        """
        주어진 field-property 조합에 매칭되는 데이터 리스트를 반환함
        :param property_dict: empty List면 에러 발생
        :return: List, empty List - None Matching
        """
        match_data_list = []
        for data in self.getDataList():
            if all([data.getProperty(field) == property for field, property in property_dict.items()]):
                match_data_list.append(data)
        return match_data_list

    def sortData(self, field: str, ascending: bool = True) -> None:
        self.__data_list.sort(key=lambda data: data.getProperty(field), reverse=not ascending)
        self.update()

    def unsortData(self, original_id_idx_dict: Dict[str, int]) -> None:
        self.__data_list.sort(key=lambda data: original_id_idx_dict[data.getProperty('고유번호')], reverse=False)
        self.update()

    def _checkValidIndex(self, idx: int) -> None:
        """
        유효한 인덱스인지 확인하고 유효하지 않다면 에러를 발생시킴
        """
        if idx < 0 or idx >= self.getDataCount():
            ErrorLogger.reportError(f'Index Error: you try to find index {idx}, '
                                   f'but Table has only {self.getDataCount()} datum.', IndexError)

    def _checkValidData(self, data: MyModel) -> None:
        """
         # 유효한 데이터인지 확인하고 유효하지 않다면 에러를 발생시킴
        """
        """
        필드 개수 체크를 진행하지 않음
        if len(__data_dict.keys()) != len(self.__field_list):
            pass  # throw error: field의 개수가 일치하지 않음
        """
        for field in data.getProperties().keys():
            if field not in self.getFieldList():
                ErrorLogger.reportError(f'Unexpected field: {field}', AttributeError)

    @MyPyqtSlot()
    def dataChanged(self) -> None:
        idx = self.getDataIndex(self.sender().parent())
        if idx is None:
            ErrorLogger.reportError('데이터와 데이터 테이블의 잘못된 연결입니다.', EOFError)
        else:
            self.getSignalSet().ModelUpdated.emit(idx)
            self.update()
            return
        # for idx, data in enumerate(self.getDataList()):
        #     if data == self.sender().parent():
        #         self.getSignalSet().ModelUpdated.emit(idx)
        #         self.update()
        #         return
        # ErrorLogger.reportError('Why this data is connected to table model?')

    def update(self) -> None:
        self.getSignalSet().TableModelUpdated.emit()
        self.save()

    def _deserialize(self, obj_str: str) -> None:
        super()._deserialize(obj_str)
        for data_iter in self.getDataList():
            data_iter.getSignalSet().Updated.connect(self.dataChanged)