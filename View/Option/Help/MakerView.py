from Utility.Config.ConfigModule import *
from Utility.UI.BaseUI import *
from View.Option.AbstractOptionView import *


# todo 급조한 제작자 뷰
class MakerView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        maker_text = """
    암사 아리수 정수센터
    사회복무요원 (~2019.12)
    이두섭
        """
        maker_lbl = QLabel(maker_text)
        link_lbl = QLabel('\t\t<a href=\"https://github.com/doobee98\"> Github Link </a>')
        link_lbl.setTextFormat(Qt.RichText)
        link_lbl.setTextInteractionFlags(Qt.TextBrowserInteraction)
        link_lbl.setOpenExternalLinks(True)
        vbox = QVBoxLayout()
        vbox.addWidget(maker_lbl)
        vbox.addWidget(link_lbl)
        self.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize() + 2))
        self.setLayout(vbox)

    def render(self) -> None:
        pass

    def applyOptionChanges(self) -> None:
        pass





