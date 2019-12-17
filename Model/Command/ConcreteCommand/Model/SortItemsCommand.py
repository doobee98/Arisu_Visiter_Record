from Model.Command.AbstractCommand import *
from Model.Table.Database.DatabaseTableModel import *

"""
SortItemsCommand
주어진 필드 이름을 기준으로 정렬함.
기본은 오름차순, 오름차순 상태에서 다시 정렬시 내림차순
내림차순 상태에서 다시 정렬시 기본 정렬인 (고유번호, 오름차순)으로 정렬함.
"""


class SortItemsCommand(AbstractCommand):
    def __init__(self, table_model: DatabaseTableModel, field_name: str):
        super().__init__()
        self.__table_model = table_model
        self.__field_name = field_name
        self.__original_id_idx_dict = None

    def execute(self) -> bool:
        if super().execute():
            StatusBarManager.setMessage('데이터 정렬중')
            # undo를 위해 원래 순서를 저장. 아이템마다 독립적인 ID를 기준으로 기존 순서를 저장한다.
            self.__original_id_idx_dict = {item.fieldData(TableFieldOption.Necessary.ID): index
                                           for index, item in enumerate(self.__table_model.itemList())}
            if self.__table_model.sortFieldName() == self.__field_name:
                if self.__table_model.sortOrder():
                    self.__table_model.sortItems(self.__field_name, False)
                else:
                    self.__table_model.sortItems(TableFieldOption.Necessary.ID, True)
            else:
                self.__table_model.sortItems(self.__field_name, True)
            return True
        else:
            return False

    def undo(self) -> bool:
        if super().undo():
            StatusBarManager.setMessage('데이터 정렬 취소중')
            self.__table_model.sortItems(lambda item: self.__original_id_idx_dict[item.fieldData(TableFieldOption.Necessary.ID)])
            return True
        else:
            return False
