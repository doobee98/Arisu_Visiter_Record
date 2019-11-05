from Utility.Config.ConfigSet import *
from Utility.UI.BaseUI import *
from View.Option.AbstractOptionView import *


# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class ReadyOptionView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        ready_text = """
    - 준비중입니다 -
    * 설정 가능한 옵션 다양하게 추가
    * 검색 창에 다양한 옵션 추가
    * 기록부 전체 편집 잠금 기능 (다른 날짜의 기록부 파일은 편집 불가능하게 설정)
    * 데이터베이스 파일 연결 변경 기능
        """
        ready = QLabel(ready_text)
        vbox = QVBoxLayout()
        vbox.addWidget(ready)
        self.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+2))
        self.setLayout(vbox)

    def render(self) -> None:
        pass

    def applyOptionChanges(self) -> None:
        pass





