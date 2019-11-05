from Setup.View.InnerView.AbstractInnerView import *


class EndView(AbstractInnerView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        content_text = ''
        content_text += '설치가 종료되었습니다.\n'
        content_text += '[종료]를 눌러 주세요.'
        lbl = QLabel(content_text)

        self.setCenterWidget(lbl)

    def verify(self) -> bool:
        return True
