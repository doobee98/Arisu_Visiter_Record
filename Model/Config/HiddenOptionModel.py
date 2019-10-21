from Utility.File.FilePathConfig import *
from Model.Config.AbstractOptionModel import *


class HiddenOptionModel(AbstractOptionModel):
    def __init__(self):
        directory, file_name = FilePathConfig.getConfigPath('HiddenConfig')
        field_list = ['save_team', 'save_worker', 'window_geometry']
        super().__init__(file_name, field_list)
        self.setDirectory(directory)

        default_dict = {
            'save_team': None,
            'save_worker': '근무자',
            'window_geometry': (0, 0)
        }
        self._setDefaultOptions(MyModel(default_dict))

        if self.hasFile():
            self.load()
            for field_iter in default_dict.keys():
                if not self._getOptionList().hasField(field_iter):
                    self._getOptionList()._setProperty(field_iter, default_dict[field_iter])
        else:
            self._setOptionList(self.getDefaultOptions())
            self.update()

    def team(self) -> str:
        return self._getOptionList().getProperty('save_team')

    def setTeam(self, team: str) -> None:
        self._getOptionList().changeProperty('save_team', team)

    def worker(self) -> str:
        return self._getOptionList().getProperty('save_worker')

    def setWorker(self, worker: str) -> None:
        self._getOptionList().changeProperty('save_worker', worker)

    def windowGeometry(self) -> Tuple[int, int]:
        return self._getOptionList().getProperty('window_geometry')

    def setWindowGeometry(self, geometry: Tuple[int, int]) -> None:
        self._getOptionList().changeProperty('window_geometry', geometry)







