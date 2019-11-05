from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Setup.View.InnerView.StartView import *
from Setup.View.InnerView.ProgramPathView import *
from Setup.View.InnerView.ReadyView import *
from Setup.View.InnerView.InstallView import *
from Setup.View.InnerView.EndView import *


class SetupMainView(QMainWindow):
    def __init__(self):
        super().__init__()

        # view define
        start_1 = StartView(self)
        program_path_2 = ProgramPathView(self)
        ready_3 = ReadyView(self)
        install_4 = InstallView(self)
        end_5 = EndView(self)

        start_1.setNextView(program_path_2); program_path_2.setBeforeView(start_1)
        program_path_2.setNextView(ready_3); ready_3.setBeforeView(program_path_2)
        ready_3.setNextView(install_4); install_4.setBeforeView(ready_3)
        install_4.setNextView(end_5); end_5.setBeforeView(install_4)

        self.__stack_widget = QStackedWidget()
        self.__stack_widget.addWidget(start_1)
        self.__stack_widget.addWidget(program_path_2)
        self.__stack_widget.addWidget(ready_3)
        self.__stack_widget.addWidget(install_4)
        self.__stack_widget.addWidget(end_5)

        self.__stack_widget.currentChanged.connect(self.render)

        # 버튼
        self.next_button = QPushButton('계속', self)
        self.next_button.clicked.connect(self.nextView)
        self.before_button = QPushButton('이전', self)
        self.before_button.clicked.connect(self.beforeView)
        self.close_button = QPushButton('종료', self)
        self.close_button.clicked.connect(self.close)

        # 버튼 레이아웃
        self.button_box = QHBoxLayout()
        self.button_box.addWidget(self.before_button)
        self.button_box.addWidget(self.next_button)

        # 메인화면 레이아웃
        vbox = QVBoxLayout()
        vbox.addWidget(self.__stack_widget)
        vbox.addLayout(self.button_box)

        main_widget = QWidget()
        main_widget.setLayout(vbox)

        self.setCentralWidget(main_widget)
        self.setWindowTitle('아리수 출입자기록부 프로그램 설치')

        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        self.move(500, 500)
        self.render()

    def render(self) -> None:
        self.__stack_widget.currentWidget().render()

        idx = self.__stack_widget.currentIndex()
        self.before_button.setEnabled(idx != 0)
        if idx == self.__stack_widget.count() - 1:
            self.button_box.replaceWidget(self.next_button, self.close_button)
            self.next_button.hide()
            self.close_button.show()
        else:
            self.button_box.replaceWidget(self.close_button, self.next_button)
            self.close_button.hide()
            self.next_button.show()


    @pyqtSlot()
    def beforeView(self) -> None:
        self.__stack_widget.setCurrentIndex(self.__stack_widget.currentIndex() - 1)

    @pyqtSlot()
    def nextView(self) -> None:
        current_widget: AbstractInnerView = self.__stack_widget.currentWidget()
        if current_widget.verify():
            self.__stack_widget.setCurrentIndex(self.__stack_widget.currentIndex() + 1)  # todo 제대로 넘김체크 해야함
        else:
            self.warning(current_widget.errorMessage())

    def warning(self, text: str) -> None:
        QMessageBox.warning(self, '위험', text)






