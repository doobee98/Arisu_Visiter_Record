from typing import Type

class ShowingView:
    def activeView(self) -> Type['ShowingView']:
        raise NotImplementedError