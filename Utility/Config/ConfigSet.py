from Utility.File.BasicFileTable import *
from Model.Config.TotalOptionModel import *
from Model.Config.HiddenOptionModel import *
from Model.Config.RecordOptionModel import *
from Model.Config.DatabaseOptionModel import *
from Model.Config.FileDirectoryOptionModel import *
from Model.Config.FilterOptionModel import *


class Config:
    FileDirectoryOption = FileDirectoryOptionModel()
    TotalOption = TotalOptionModel()
    HiddenOption = HiddenOptionModel()
    RecordOption = RecordOptionModel()
    DatabaseOption = DatabaseOptionModel()
    FilterOption = FilterOptionModel()
