
from Utility.File.FileNameConfig import *
from Model.Config.AbstractOptionModel import *

# todo: fieldview config와 fieldmodel config를 어떻게 할지, 그룹을 어떻게 할지
class HiddenOptionModel(AbstractOptionModel):
    def __init__(self):
        file_name = FileNameConfig.getConfigName('HiddenConfig')
        field_list = ['save_team', 'save_worker']
        super().__init__(file_name, field_list)
        if self.isFileExist():
            self._load()
        else:
            proto = MyModel({
                'save_team': None,
                'save_worker': '근무자'
            })
            self._setOptionList(proto)
            self.update()

    def team(self) -> str:
        return self._getOptionList().getProperty('save_team')

    def setTeam(self, team: str) -> None:
        self._getOptionList().changeProperty('save_team', team)

    def worker(self) -> str:
        return self._getOptionList().getProperty('save_worker')

    def setWorker(self, worker: str) -> None:
        self._getOptionList().changeProperty('save_worker', worker)






