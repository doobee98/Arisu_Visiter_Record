from Model.Config.AbstractConfigModel import *
from Model.Table.Field.TableFieldModel import *
from Utility.Info.DefaultFilePath import *

"""
TableFieldConfigModel(AbstractConfigModel)
AbstractTableModel에서 사용하는 TableFieldModel에 대한 설정값을 관리함.
1. 기록부, 데이터베이스의 모델과 뷰가 생성될 때, 이 클래스에서 사용할 필드의 정보를 취득함

* AbstractConfigModel의 Field를 사용하지 않고, 자체적인 field_midel_list를 사용함
"""


class TableFieldConfigModel(AbstractConfigModel):
    OptionType = Dict[str, AbstractSerializeModel.AttrType]

    def __init__(self, file_path: str):
        self.__field_model_list: List[TableFieldModel] = []
        super().__init__(file_path)

    """
    property
    * fieldModelList
    """
    def fieldModelList(self) -> List[TableFieldModel]:
        return self.__field_model_list

    """
    advanced property
    * fieldModel
    * databaseFieldModelList, recordFieldModelList
    """
    def fieldModel(self, field_name: str) -> TableFieldModel:
        for field_iter in self.fieldModelList():
            if field_iter.name() == field_name:
                return field_iter
        return None

    def databaseFieldModelList(self) -> List[TableFieldModel]:
        return [field_model_iter for field_model_iter in self.fieldModelList()
                if field_model_iter.databaseOption(TableFieldOption.Database.Active)]

    def recordFieldModelList(self) -> List[TableFieldModel]:
        return [field_model_iter for field_model_iter in self.fieldModelList()
                if field_model_iter.recordOption(TableFieldOption.Record.Active)]

    """
    method
    * addField, removeField, changeFieldName
    """
    def addField(self, field: TableFieldModel) -> None:
        if any([field_model_iter.name() == field.name() for field_model_iter in self.fieldModelList()]):
            raise KeyError  # 중복
        self.__field_model_list.append(field)
        self.update()

    def removeField(self, field_name: str) -> None:
        if any([field_model_iter.name() == field_name for field_model_iter in self.fieldModelList()]):
            self.__field_model_list.remove(self.fieldModel(field_name))
            self.update()

    def changeFieldName(self, old_name: str, new_name: str) -> None:
        if any([field_model_iter.name() == old_name for field_model_iter in self.fieldModelList()]):
            if not any([field_model_iter.name() == new_name for field_model_iter in self.fieldModelList()]):
                self.fieldModel(old_name).setName(new_name)
                self.update()

    """
    override
    * initNull
    * setDefault
    """
    @classmethod
    def initNull(cls) -> 'TableFieldConfigModel':
        return TableFieldConfigModel('')

    def setDefault(self) -> None:
        # TableFieldModel 모듈의 FieldOption을 보면서 참조할 것
        G, D, R = TableFieldOption.Global, TableFieldOption.Database, TableFieldOption.Record
        default_dict: Dict[str, Dict[Type[Union[G, D, R]], Union[G, D, R]]] = {
            TableFieldOption.Necessary.Button_Plus: {
                G: G.Uneditable | G.NoModelData | G.NoSearch,
                D: D.null,
                R: R.Active | R.WidthDown
            },
            TableFieldOption.Necessary.RECORD_ID: {
                G: G.null,
                D: D.null,
                R: R.Active | R.Group | R.Bold | R.WidthDown
            },
            TableFieldOption.Necessary.NAME: {
                G: G.Share | G.Key,
                D: D.Active | D.ShareOn | D.WidthUp,
                R: R.Active | R.ShareOn | R.Completer
            },
            TableFieldOption.Necessary.BIRTHDAY: {
                G: G.Share | G.Key,
                D: D.Active | D.ShareOn,
                R: R.Active | R.ShareOn
            },
            TableFieldOption.Necessary.CAR_NUMBER: {
                G: G.Share,
                D: D.Active | D.ShareOn | D.WidthUp,
                R: R.Active | R.Group | R.ShareOn | R.WidthUp | R.Completer
            },
            TableFieldOption.Necessary.COMPANY: {
                G: G.Share,
                D: D.Active | D.ShareOn | D.WidthUp,
                R: R.Active | R.Group | R.ShareOn | R.WidthUp | R.Completer
            },
            TableFieldOption.Necessary.PURPOSE: {
                G: G.Share,
                D: D.Active | D.ShareOn | D.WidthUp,
                R: R.Active | R.Group | R.ShareOn | R.WidthUp | R.Completer
            },
            '반출입\n물품명': {
                G: G.Removable | G.NameChangeable,
                D: D.null,
                R: R.Active
            },
            '반입/반출량': {
                G: G.Removable | G.NameChangeable,
                D: D.null,
                R: R.Active
            },
            '비고': {
                # Record에서 Database 방향으로만 비고 내용이 이동함
                G: G.Removable | G.NameChangeable | G.Share,
                D: D.Active | D.WidthUp,
                R: R.Active | R.ShareOn | R.WidthUp
            },
            TableFieldOption.Necessary.IN_TIME: {
                G: G.IsTime,
                D: D.WidthDown,
                R: R.Active | R.DefaultUnable | R.WidthDown
            },
            TableFieldOption.Necessary.IN_WORKER: {
                G: G.null,
                D: D.WidthDown,
                R: R.Active | R.DefaultUnable | R.WidthDown
            },
            TableFieldOption.Necessary.OUT_TIME: {
                G: G.IsTime,
                D: D.WidthDown,
                R: R.Active | R.DefaultUnable | R.WidthDown
            },
            TableFieldOption.Necessary.OUT_WORKER: {
                G: G.null,
                D: D.WidthDown,
                R: R.Active | R.DefaultUnable | R.WidthDown
            },
            TableFieldOption.Necessary.TAKEOVER: {
                G: G.NoSearch,
                D: D.null,
                R: R.Active | R.Hidden
            },
            TableFieldOption.Necessary.DATE_FIRST: {
                G: G.Uneditable | G.IsDate,
                D: D.Active | D.WidthUp | D.AutoComplete,
                R: R.null
            },
            TableFieldOption.Necessary.DATE_RECENT: {
                G: G.Uneditable | G.IsDate,
                D: D.Active | D.WidthUp | D.AutoComplete,
                R: R.null
            },
            TableFieldOption.Necessary.ID: {
                G: G.Share | G.Uneditable,
                D: D.Active | D.ShareOn | D.AutoComplete,
                R: R.Active | R.ShareOn | R.DefaultUnable
            },
            TableFieldOption.Necessary.Button_Edit_Remove: {
                G: G.Uneditable | G.NoModelData | G.NoSearch,
                D: D.Active | D.WidthDown,
                R: R.Active | R.WidthDown
            }
        }

        self.setBlockUpdate(True)
        for option_name_iter in default_dict.keys():
            field_model_iter = TableFieldModel(option_name_iter)
            field_model_iter.setGlobalFlags(default_dict[option_name_iter][G])
            field_model_iter.setDatabaseFlags(default_dict[option_name_iter][D])
            field_model_iter.setRecordFlags(default_dict[option_name_iter][R])
            self.addField(field_model_iter)
        self.setBlockUpdate(False)
        self.save()
