from Model.Config.FilePathConfigModel import *
from Model.Config.TableFieldConfigModel import *
from Model.Config.ApplicationConfigModel import *
from Model.Config.HiddenConfigModel import *
from Model.Config.FieldFilterConfigModel import *

"""
ConfigModule
"""


class ConfigModule:
    FilePath = FilePathConfigModel().instance()
    TableField = TableFieldConfigModel(FilePath.configFilePath('TableFieldConfig'))
    Application = ApplicationConfigModel(FilePath.configFilePath('ApplicationConfig'))
    Hidden = HiddenConfigModel(FilePath.configFilePath('HiddenConfig'))
    FieldFilter = FieldFilterConfigModel(FilePath.configFilePath('FieldFilterConfig'))
