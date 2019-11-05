from Setup.View.InnerView.AbstractInnerView import *


class ReadyView(AbstractInnerView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        content_text = ''
        content_text += f'-------- 경로에 아리수 출입자기록부 프로그램을 설치합니다.\n\n'
        content_text += f'* 바탕화면에 ArisuRecord 프로그램 바로가기가 생성됩니다.\n'
        content_text += f'* 바탕화면에 기록부 폴더 바로가기가 생성됩니다.\n'
        content_text += f'* 설치 후 rcd 확장자 파일의 연결프로그램을 설정해주시기 바랍니다.\n'
        self.lbl = QLabel(content_text)

        self.setCenterWidget(self.lbl)

    def render(self) -> None:
        install_path = self.beforeView().installPath()

        content_text = ''
        content_text += f'{install_path} 경로에 아리수 출입자기록부 프로그램을 설치합니다.\n\n'
        content_text += f'* 바탕화면에 ArisuRecord 프로그램 바로가기가 생성됩니다.\n'
        content_text += f'* 바탕화면에 기록부 폴더 바로가기가 생성됩니다.\n'
        content_text += f'* 설치 후 rcd 확장자 파일의 연결프로그램을 설정해주시기 바랍니다.\n'
        self.lbl.setText(content_text)

    def verify(self) -> bool:
        return True
