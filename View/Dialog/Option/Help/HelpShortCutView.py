from Utility.Module.ConfigModule import *
from Utility.MyPyqt.MyDefaultWidgets import *
from View.Dialog.Option.AbstractOptionView import *


# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class HelpShortCutView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        help_text = """
    - 통합 -
    * Ctrl + X: 잘라내기
    * Ctrl + C: 복사, Ctrl + V: 붙여넣기
    * Ctrl + F: 검색
    * Ctrl + Z: 실행 취소, Ctrl + Y: 다시 실행
    
    - 기록부 -
    * Ctrl + A: 들어오다, Ctrl + D: 나가다
    * Ctrl + Q: 작성 행 스크롤
        """
        help_lbl = QLabel(help_text)
        vbox = QVBoxLayout()
        vbox.addWidget(help_lbl)
        self.setFont(MyDefaultWidgets.basicQFont(point_size=MyDefaultWidgets.basicPointSize()+2))
        self.setLayout(vbox)

    def myRender(self) -> None:
        pass

    def applyOptionChanges(self) -> None:
        pass





