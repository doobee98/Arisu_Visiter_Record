from Model.Record.RecordModel import *
from Utility.Abstract.Model.MyTableModel import *
from Utility.Clock import *
from Utility.File.FilePathConfig import *


class RecordTableModelSignal(MyTableModelSignal):
    """
    RecordTableModelSignal
    MyTableModelSignal에서 이름 재정의(5종류)
    RecordModelIdChanged(index): recordModel의 고유번호가 변경되었을 때
    """
    RecordTableModelUpdated = MyTableModelSignal.TableModelUpdated  # ()
    RecordModelIdChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)


class RecordTableModel(MyTableModel):
    """
    RecordTableModel
    __record_date: 기록부의 날짜
    """
    def __init__(self, location_string: str, record_date_string: str, field_list: List[str] = RecordFieldModelConfig.getFieldList(), load: bool = True):
        super().__init__(field_list)
        self.__record_date = record_date_string
        self.__location = location_string
        directory, file_name = FilePathConfig.getRecordTablePath(location_string, record_date_string)
        self.setDirectory(directory)
        self.setFileName(file_name)
        self._setSignalSet(RecordTableModelSignal(self))
        self._setDataType(RecordModel)
        if load:
            self.load()
            self.setDirectory(directory)
            self.setFileName(file_name)

    @classmethod
    def initNull(cls) -> 'RecordTableModel':
        return RecordTableModel('', '')

    def getRecordDate(self) -> str:
        return self.__record_date

    def getLocation(self) -> str:
        return self.__location

    def generateTakeoverInfo(self, time: str, team: str, worker: str) -> Tuple[int, str]:
        # todo: time valid check
        remain_visitor_num = 0
        takeover_idx = 0
        remain_leader_name = None
        for idx_iter, data_iter in enumerate(self.getDataList()):
            arrive_time = data_iter.getProperty('들어오다시간')
            if (not arrive_time) or arrive_time < time:
                takeover_idx += 1
                if data_iter.isRemainAtTime(time):
                    if remain_leader_name is None:
                        remain_leader_name = data_iter.getProperty('성명')
                    remain_visitor_num += 1
            else:
                break
        if remain_visitor_num == 0:
            remain_visitor_text = '인수대상 없음'
        elif remain_visitor_num == 1:
            remain_visitor_text = f'{remain_leader_name} 인수인계'
        else:
            remain_visitor_text = f'{remain_leader_name} 외 {remain_visitor_num - 1}인 인수인계'
        takeover_string = f'{time} {remain_visitor_text} - {team} {worker}'
        return takeover_idx, takeover_string

    def getVisitorCountAtTime(self, time: str) -> int:
        # todo time valid check
        match_count = 0
        for data_iter in self.getDataList():
            if not data_iter.isTakeoverRecord():
                # todo model의 state 체크(inserted, finished)가 필요할까?
                arrive_time = data_iter.getProperty('들어오다시간')
                if arrive_time and arrive_time < time:
                    if data_iter.isRemainAtTime(time):
                        match_count += 1
                else:
                    break
        return match_count

    def getRecordIndexAtTime(self, time: str) -> int:
        # todo time valid check
        match_idx = 0
        for data_iter in self.getDataList():
            if not data_iter.isTakeoverRecord():
                arrive_time = data_iter.getProperty('들어오다시간')
                if (not arrive_time) or arrive_time > time:
                    break
                else:
                    match_idx += 1
        return match_idx

    def getLeaderNameAtTime(self, time: str) -> str:
        for data_iter in self.getDataList():
            if data_iter.isRemainAtTime(time):
                return data_iter.getProperty('성명')
        return None

    def getRemainNameListAtTime(self, time: str) -> Tuple[int, str]:
        remain_list = []
        for idx_iter, data_iter in enumerate(self.getDataList()):
            if data_iter.isRemainAtTime(time):
                remain_list.append((idx_iter, data_iter.getProperty('성명')))
        return remain_list

    def load(self):
        """
        load시 generated 상태의 record model은 삭제한다.
        """
        super().load()
        if self.hasFile():
            self.__deleteBasicRecords()

    def __deleteBasicRecords(self) -> None:
        delete_idx_list = []
        for idx in range(self.getDataCount()):
            if self.getData(idx).getState() == RecordModel.State.Generated:
                delete_idx_list.append(idx)
        delete_idx_list.reverse()  # 뒤에부터 지워야 idx가 그대로 유효함(앞에서부터 지우면 한칸씩 땡겨짐)
        for idx in delete_idx_list:
            self.deleteData(idx)


