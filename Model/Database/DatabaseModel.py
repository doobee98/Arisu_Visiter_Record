from Utility.Abstract.Model.MyTableModel import *
from Model.Database.VisitorModel import *
from Utility.Config.DatabaseFieldModelConfig import *
from Utility.Clock import *
from Utility.Config.ConfigModule import *

class DatabaseModelSignal(MyTableModelSignal):
    """
    DatabaseModelSignal
    MyTableModelSignal에서 이름 재정의(5종류)
    """
    DatabaseModelUpdated = MyTableModelSignal.TableModelUpdated  # (), 사용하지 않음
    #DatabaseSorted = MyTableModelSignal.TableSorted

    def __init__(self, parent=None):
        super().__init__(parent)


class DatabaseModel(MyTableModel):
    """
    DatabaseModel
    __id_initial_alphabet: __generateVisitorId 참조
    __id_number_width: __generateVisitorId 참조
    """
    def __init__(self, location_string: str, field_list: List[str] = DatabaseFieldModelConfig.getFieldList(), load: bool= True):
        super().__init__(field_list)

        self.__location = location_string
        self._setSignalSet(DatabaseModelSignal(self))
        directory, file_name = FilePathConfig.getDatabasePath(location_string)
        self.setDirectory(directory)
        self.setFileName(file_name)
        self._setDataType(VisitorModel)
        self.__id_initial_alphabet = 'A'
        self.__id_number_width = 8
        self.__auto_save = True
        if load:
            self.load()
            self.setDirectory(directory)
            self.setFileName(file_name)

    @classmethod
    def initNull(cls) -> 'DatabaseModel':
        return DatabaseModel('')

    def getLocation(self) -> str:
        return self.__location

    def setAutoSave(self, enable: bool) -> None:
        self.__auto_save = enable

    def addData(self, data: VisitorModel):
        """
        새로운 데이터를 추가할 때, auto-generate field를 형식에 맞게 추가함
        """
        change_dict = {}
        if not data.getProperty('고유번호'):
            change_dict['고유번호'] = self.__generateVisitorID()
        if not data.getProperty('최초출입날짜'):
            change_dict['최초출입날짜'] = Clock.getDate().toString('yyyy-MM-dd')
        if not data.getProperty('최근출입날짜'):
            change_dict['최근출입날짜'] = Clock.getDate().toString('yyyy-MM-dd')
        data.changeProperties(change_dict)
        super().addData(data)

    def __generateVisitorID(self) -> str:
        """
        database에 새로 데이터를 추가할 때, 기존에 있던 데이터와 중복되지 않는 id를 만들어줌
            고유번호 문자열 형식: id_initial_alphabet + 숫자 8자리
            __id_initial_alphabet: 고유번호 앞에 붙는 영어 문자
            __id_number_width: 고유번호 숫자 부분의 자리수
        :return: generated visitor id
        """
        
        # 고유번호 숫자를 고유번호 문자열로 바꾸어주는 지역함수
        getIDString = lambda n: self.__id_initial_alphabet + f'{n:0>{self.__id_number_width}}'
        # 기존 데이터 고유번호 리스트
        visitor_id_list = [visitor.getProperty('고유번호') for visitor in self.getDataList()]

        target_num = 1  # 고유번호는 1부터 시작함
        while True:
            id_str = getIDString(target_num)
            if id_str not in visitor_id_list:
                return id_str
            else:
                target_num += 1

    def save(self) -> None:
        if self.__auto_save:
            super().save()

    def load(self):
        """
        load시 save_deadline을 지난 데이터는 삭제한다
        """
        super().load()
        if self.hasFile():
            self.__deleteOldData()

    def __deleteOldData(self) -> None:
        save_deadline = Config.DatabaseOption.saveDeadLine()
        today = Clock.getDateTime().toPyDateTime()
        delete_idx_list = []
        for idx in range(self.getDataCount()):
            recent_date = datetime.strptime(self.getData(idx).getProperty('최근출입날짜'), '%Y-%m-%d')
            diff_days = (today - recent_date).days
            if diff_days > save_deadline:
                delete_idx_list.append(idx)
        if delete_idx_list:
            question_string = f'출입한 지 {save_deadline}일이 지난 데이터 {len(delete_idx_list)} 건이 검색되었습니다.\n'
            question_string += '삭제하시겠습니까?'
            reply = QMessageBox.question(QApplication.activeWindow(), '삭제', question_string,
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                return
            else:
                delete_idx_list.reverse()  # 뒤에부터 지워야 idx가 그대로 유효함(앞에서부터 지우면 한칸씩 땡겨짐)
                for idx in delete_idx_list:
                    self.deleteData(idx)

