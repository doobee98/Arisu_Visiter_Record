from typing import Optional, Type
from datetime import datetime
from Utility.CryptListModule import *
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Utility.TableInterface.Model.MyModel import *
from Utility.File.FileNameConfig import *
import os

# 레코드 번호를 가지는, 더블 링크드 리스트 형태로 바꾸기
# 이는 데이터의 삭제와 삽입이 잦은 것을 보완하기 위함
# 추가해야할 데이터 필드: head, tail 객체(인덱스) -> 순서가 실제 데이터 연관과 관련이 없기 때문이다.


class MyTableModelSignal(QObject):
    """
    MyTableModelSignal
    TableModelUpdated(): 사용하지 않음
    ModelAppended(): 새로운 model이 최후방에 추가되었을 때 방출
    ModelInserted(index): 새로운 model이 중간에 삽입되었을 때 방출(index)
    ModelDeleted(index): model이 삭제되었을 때
    ModelChanged(index): model의 데이터가 변경되었을 때
    """
    ModelUpdated = pyqtSignal(int)
    TableModelUpdated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)


class MyTableModel(QObject):
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
        self.__signal_set: Type[MyTableModelSignal] = MyTableModelSignal()
        self.__file_name: str = None
        self.__field_list: List[str] = field_list
        self.__data_type: type = MyModel
        self.__data_list: List[Type[MyModel]] = []

    def getSignalSet(self) -> Type[MyTableModelSignal]:
        return self.__signal_set

    def _setSignalSet(self, signal: Type[MyTableModelSignal]) -> None:
        self.__signal_set = signal

    def getFieldList(self) -> List[str]:
        return self.__field_list.copy()

    def _setFieldList(self, field_list: List[str]) -> None:
        self.__field_list = field_list

    def getFileName(self) -> str:
        return self.__file_name

    def _setFileName(self, file_name: str) -> None:
        self.__file_name = file_name

    def getDataType(self) -> type:
        return self.__data_type

    def _setDataType(self, data_type: type) -> None:
        self.__data_type = data_type

    def getDataList(self) -> List[Type[MyModel]]:
        return self.__data_list

    def getData(self, idx: int) -> Type[MyModel]:
        self._checkValidIndex(idx)
        return self.getDataList()[idx]

    def _setData(self, idx: int, data: Type[MyModel]) -> None:
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

    def getDataIndex(self, data: Type[MyModel]) -> int:
        for idx_iter, data_iter in enumerate(self.getDataList()):
            if data == data_iter:
                return idx_iter
        return None

    def addData(self, data: Type[MyModel]) -> None:
        self._setData(self.getDataCount(), data)
        self.update()

    def insertData(self, idx: int, data: Type[MyModel]) -> None:
        self._setData(idx, data)
        self.update()

    def deleteData(self, idx: int) -> Type[MyModel]:
        deleted_data = self.getData(idx)
        del self.__data_list[idx]
        self.update()
        return deleted_data

    def findData(self, property_dict: Dict[str, Union[str, bool]]) -> List[Type[MyModel]]:
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

    def isFileExist(self) -> bool:
        return self.getFileName() and os.path.isfile(self.getFileName())

    def _checkValidIndex(self, idx: int) -> None:
        """
        유효한 인덱스인지 확인하고 유효하지 않다면 에러를 발생시킴
        """
        if idx < 0 or idx >= self.getDataCount():
            ErrorLogger.reportError(f'Index Error: you try to find index {idx}, '
                                   f'but Table has only {self.getDataCount()} datum.')

    def _checkValidData(self, data: Type[MyModel]) -> None:
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
                ErrorLogger.reportError(f'Unexpected field: {field}')

    @pyqtSlot()
    def dataChanged(self) -> None:
        idx = self.getDataIndex(self.sender().parent())
        if idx is None:
            ErrorLogger.reportError('Why this data is connected to table model?')
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

    def save(self) -> None:
        cipher_list = CryptListModule.encrypt(self.getDataList())
        with open(self.getFileName(), 'wb') as f:
            for cipher_text in cipher_list:
                f.write(cipher_text + b'\n')

    def _load(self) -> None:
        if self.isFileExist():
            with open(self.getFileName(), 'rb') as f:
                cipher_list = f.readlines()
                object_list = CryptListModule.decrypt(cipher_list, self.getDataType())

                for record in object_list:
                    self._setData(self.getDataCount(), record)
                self.update()  # 이전에 켰을때와 뭔가 바뀐게 있다면 저장하기위해서 로드 하자마자 저장함
        else:
            ErrorLogger.reportError(f'Cannot find file {self.getFileName()}.')

    def blockSignals(self, b: bool) -> bool:
        self.getSignalSet().blockSignals(b)
        return super().blockSignals(b)