from Setup.View.InnerView.AbstractInnerView import *


class StartView(AbstractInnerView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        content_text = ''
        content_text += '아리수 출입자기록부 프로그램 설치를 시작합니다.\n'
        content_text += '[계속]을 눌러 주세요.'
        lbl = QLabel(content_text)

        self.setCenterWidget(lbl)

    def verify(self) -> bool:
        return True
