from typing import Dict, Union, Tuple, Type
from enum import Enum, auto, IntFlag
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Utility.Log.ErrorLogger import *
from Utility.Log.ExecuteLogger import *
from Utility.CryptModule import *
from Utility.MyPyqtSlot import *
import pickle, os


class _AbstractModelSerial(list):
    def __init__(self):
        super().__init__()


class AbstractModel(QObject):
    AttrType = Union[bool, int, str, 'AbstractModel', Dict['AttrType', 'AttrType'], List['AttrType'], Tuple['AttrType']]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__signal_set: QObject = None
        self.__directory: str = ''
        self.__file_name: str = ''
    """
    init
    * initNull - serialize시 생성자의 통일을 위한 메소드
    """
    @classmethod
    def initNull(cls) -> 'AbstractModel':
        raise NotImplementedError  # 상속 처리

    """
    property
    * attrList (객체의 attribute name list: str)
    * signalSet
    * directory
    * fileName
    """
    def __attrList(self) -> List[str]:
        attr_list = list(self.__dict__.keys())
        if '_AbstractModel__signal_set' in attr_list:
            attr_list.remove('_AbstractModel__signal_set')  # signalSet은 QObject여서 pickle 불가능, 따라서 제외
            attr_list.remove('_AbstractModel__directory')
            attr_list.remove('_AbstractModel__file_name')
            return attr_list
        else:
            ErrorLogger.reportError('내부 오류: SignalSet이 정의되지 않았습니다.', AttributeError)

    def getSignalSet(self) -> QObject:
        return self.__signal_set

    def _setSignalSet(self, signal_set: QObject):
        self.__signal_set = signal_set

    def directory(self) -> str:
        return self.__directory

    def setDirectory(self, directory: str) -> None:
        self.__directory = directory

    def fileName(self) -> str:
        return self.__file_name

    def setFileName(self, file_name) -> None:
        self.__file_name = file_name

    """
    method
    * filePath (directory + fileName)
    * hasFile
    * serialize, deserialize (instance attribute serialize)
    * serializeAttr, deserializeAttr (class method, recursive method)
    * save, load, update
    """

    def filePath(self) -> str:
        directory, file_name = self.directory(), self.fileName()
        if file_name == '':
            return None  # todo 에러처리
        elif directory == '':
            return file_name
        else:
            return directory + '\\' + file_name

    def hasFile(self) -> bool:
        return self.filePath() is not None and os.path.isfile(self.filePath())

    def _serialize(self) -> str:
        try:
            return pickle.dumps(self.__class__._serializeAttr(self))
        except Exception as e:
            ErrorLogger.reportError(f'{self.fileName()} 파일 직렬화 실패.', AttributeError)

    def _deserialize(self, obj_str: str) -> None:
        try:
            load_data: _AbstractModelSerial = pickle.loads(obj_str)
            load_data_type, load_attr_list = load_data
            if load_data_type != self.__class__:
                raise AttributeError
            for attr_name_iter, attr_value_iter in load_attr_list:
                if attr_name_iter in self.__attrList():
                    setattr(self, attr_name_iter, self.__class__._deserializeAttr(attr_value_iter))
                else:
                    ErrorLogger.reportError(f'속성값 오류 - {attr_name_iter} / {attr_value_iter}.', AttributeError)
        except Exception as e:
            ErrorLogger.reportError(f'{self.fileName()} 파일 직렬화 해제 실패: ', e)

    @classmethod
    def _serializeAttr(cls, attr: AttrType) -> AttrType:
        if isinstance(attr, AbstractModel):
            attr_serial = _AbstractModelSerial()
            attr_str_list = []
            for attr_name_iter in attr.__attrList():
                attr_tuple = (attr_name_iter, cls._serializeAttr(getattr(attr, attr_name_iter)))
                attr_str_list.append(attr_tuple)
            attr_serial.append(attr.__class__)
            attr_serial.append(attr_str_list)
            return attr_serial
        elif isinstance(attr, dict):
            return dict(map(cls._serializeAttr, attr.items()))
        elif isinstance(attr, (list, tuple)):
            attr_type = attr.__class__
            return attr_type(map(cls._serializeAttr, attr))
        else:
            return attr

    @classmethod
    def _deserializeAttr(cls, attr: AttrType) -> AttrType:
        if isinstance(attr, _AbstractModelSerial):
            attr_type: Type[AbstractModel] = attr[0]
            attr_list: List[Tuple[str, cls.AttrType]] = attr[1]
            new_model = attr_type.initNull()
            for attr_name_iter, attr_value_iter in attr_list:
                if attr_name_iter in new_model.__attrList():
                    setattr(new_model, attr_name_iter, cls._deserializeAttr(attr_value_iter))
                else:
                    ErrorLogger.reportError(f'속성값 오류 - {attr_name_iter} / {attr_value_iter}.', AttributeError)
            return new_model
        elif isinstance(attr, dict):
            return dict(map(cls._deserializeAttr, attr.items()))
        elif isinstance(attr, (tuple, list)):
            attr_type: Type[Union[Tuple, List]] = attr.__class__
            return attr_type(map(cls._deserializeAttr, attr))
        else:
            return attr

    def save(self) -> None:
        try:
            if self.filePath() is not None:
                with open(self.filePath(), 'wb') as f:
                    f.write(CryptModule.encrypt(self._serialize()))
        except Exception as e:
            error_string = f'{self.filePath()} 파일 저장 실패'
            if self.directory():
                error_string += f'\n{self.directory()} 폴더가 존재하는지 확인해 보세요.'
            ErrorLogger.reportError(f'{self.filePath()} 파일 저장 실패', e)

    def load(self) -> None:
        try:
            if self.hasFile():
                with open(self.filePath(), 'rb') as f:
                    cipher_list = f.readlines()
                    self._deserialize(CryptModule.decrypt(cipher_list[0]))
                    self.update()  # 이전에 켰을때와 뭔가 바뀐게 있다면 저장하기위해서 로드 하자마자 저장함
        except Exception as e:
            error_string = f'{self.filePath()} 파일 로딩 실패'
            if self.directory():
                error_string += f'\n{self.directory()} 폴더가 존재하는지 확인해 보세요.'
            ErrorLogger.reportError(f'{self.filePath()} 파일 로딩 실패', e)

    def update(self) -> None:
        self.save()

    """
    override
    * blockSignals
    """
    def blockSignals(self, b: bool) -> bool:
        self.getSignalSet().blockSignals(b)
        return super().blockSignals(b)

