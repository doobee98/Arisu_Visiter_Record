from Model.AbstractSerializeModel import *

"""
TableFieldModel
테이블 모델에서 사용하는 필드의 규격을 정하는 클래스.
옵션 타입은 전역적으로 사용하는 옵션, 기록부와 데이터베이스 각각에서만 사용하는 옵션으로 분류된다.
"""


class TableFieldOption:
    class Global(Flag):
        null = 0
        NameChangeable = auto()     # 이 필드의 이름이 변경 가능한가
        Removable = auto()          # 이 필드가 삭제 가능한가
        Uneditable = auto()         # 이 필드의 값을 사용자가 직접 변경하는 것이 불가능한가
        Share = auto()              # Record와 Database가 서로 공유하는 필드인가
        Key = auto()                # Share 필드 중 검색 키로 활용되는 필드인가
        IsTime = auto()             # Time 필드인가
        IsDate = auto()             # Date 필드인가
        NoModelData = auto()        # 사전에 약속된 모델 데이터 필드가 아닌 사용자 필드인가
        NoSearch = auto()           # 검색하지 않는 필드인가
        @classmethod
        def default(cls) -> 'TableFieldOption.Global':
            return cls.NameChangeable | cls.Removable
        @classmethod
        def changableOptionList(cls) -> List['TableFieldOption.Global']:
            return [cls.Share, cls.IsTime, cls.IsDate]

    class Record(Flag):
        null = 0
        Active = auto()         # 기록부에서 활성화된 필드인가
        Hidden = auto()         # 기록부 뷰에서 숨겨져있는가
        DefaultUnable = auto()  # Generated 상태에서 편집하거나 선택할 수 있는가 -> ItemViewOption에서 Dotted로 표현됨
        Group = auto()          # 그룹으로 취급되는 필드인가 (+ 버튼을 눌렀을 때 복사될 필드 여부)
        ShareOn = auto()        # Global.Share가 True라면, Database에서 이 필드의 데이터를 가져갈 수 있는가
        Bold = auto()           # Bold체인가
        WidthUp = auto()        # 가로 사이즈를 두 배로 늘림
        WidthDown = auto()      # 가로 사이즈를 최소로 줄임
        Completer = auto()      # 자동완성을 사용하는 필드인가
        @classmethod
        def default(cls) -> 'TableFieldOption.Record':
            return cls.Active
        @classmethod
        def changableOptionList(cls) -> List['TableFieldOption.Record']:
            return [cls.Active, cls.Hidden, cls.Group, cls.ShareOn, cls.Bold, cls.WidthDown, cls.WidthUp, cls.Completer]

    class Database(Flag):
        null = 0
        Active = auto()         # 데이터베이스에서 활성화된 필드인가
        Hidden = auto()         # 데이터베이스 뷰에서 숨겨져있는가
        ShareOn = auto()        # Global.Share가 True라면, Record에서 이 필드의 데이터를 가져갈 수 있는가
        Bold = auto()           # Bold체인가
        WidthUp = auto()        # 가로 사이즈를 두 배로 늘림
        WidthDown = auto()      # 가로 사이즈를 최소로 줄임
        AutoComplete = auto()   # 프로그램에 의해 자동으로 채워지는 필드
        @classmethod
        def default(cls) -> 'TableFieldOption.Database':
            return cls.Active
        @classmethod
        def changableOptionList(cls) -> List['TableFieldOption.Database']:
            return [cls.Active, cls.Hidden, cls.ShareOn, cls.Bold, cls.WidthDown, cls.WidthUp]

    class Necessary:
        ID = '고유번호'
        RECORD_ID = '출입증\n번호'
        NAME = '성명'
        BIRTHDAY = '생년월일'
        CAR_NUMBER = '차량번호'
        COMPANY = '소속'
        PURPOSE = '방문목적'
        IN_TIME = '들어오다\n시간'
        IN_WORKER = '들어오다\n근무자'
        OUT_TIME = '\0나가다\0\n시간'
        OUT_WORKER = '\0나가다\0\n근무자'
        TAKEOVER = '인수인계'
        DATE_FIRST = '최초 출입날짜'
        DATE_RECENT = '최근 출입날짜'
        Button_Plus = '추가'
        Button_Edit_Remove = '편집/삭제'


class TableFieldModel(AbstractSerializeModel):
    def __init__(self, name: str):
        super().__init__()
        self.__name: str = name
        self.__global_flags: TableFieldOption.Global = TableFieldOption.Global.default()
        self.__record_flags: TableFieldOption.Record = TableFieldOption.Record.default()
        self.__database_flags: TableFieldOption.Database = TableFieldOption.Database.default()

    """
    property
    * name
    * globalFlags, recordFlags, databaseFlags
    """
    def name(self) -> str:
        return self.__name

    def setName(self, name: str) -> None:
        self.__name = name

    def globalFlags(self) -> TableFieldOption.Global:
        return self.__global_flags

    def setGlobalFlags(self, flags: TableFieldOption.Global) -> None:
        self.__global_flags = flags

    def recordFlags(self) -> TableFieldOption.Record:
        return self.__record_flags

    def setRecordFlags(self, flags: TableFieldOption.Record) -> None:
        self.__record_flags = flags

    def databaseFlags(self) -> TableFieldOption.Database:
        return self.__database_flags

    def setDatabaseFlags(self, flags: TableFieldOption.Database) -> None:
        self.__database_flags = flags

    """
    advanced property
    * printedName
    * globalOption, recordOption, databaseOption
    """
    def printedName(self) -> str:
        return self.name().replace('\n', ' ').replace('\0', '')

    def globalOption(self, option: TableFieldOption.Global) -> bool:
        return bool(self.__global_flags & option)

    def setGlobalOption(self, option: TableFieldOption.Global, option_value: bool) -> None:
        self.setGlobalFlags(self.globalFlags() | option if option_value else self.globalFlags() & ~option)

    def recordOption(self, option: TableFieldOption.Record) -> bool:
        return bool(self.__record_flags & option)

    def setRecordOption(self, option: TableFieldOption.Record, option_value: bool) -> None:
        self.setRecordFlags(self.recordFlags() | option if option_value else self.recordFlags() & ~option)

    def databaseOption(self, option: TableFieldOption.Database) -> bool:
        return bool(self.__database_flags & option)

    def setDatabaseOption(self, option: TableFieldOption.Database, option_value: bool) -> None:
        self.setDatabaseFlags(self.databaseFlags() | option if option_value else self.databaseFlags() & ~option)

    """
    override
    * initNull
    """
    @classmethod
    def initNull(cls) -> 'TableFieldModel':
        return TableFieldModel('')
