from Utility.UI.BaseUI import *

from View.Option.TotalOptionMainView import *
from View.Option.RecordOptionMainView import *
from View.Option.DatabaseOptionMainView import *
from View.Option.ReadyOptionView import *
from Utility.ShowingView import *


class OptionDialog(QDialog, ShowingView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # todo 임시 준비중 뷰
        ready_view = ReadyOptionView()
        ready_view.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+2))

        self.__options_info_dict: Dict[str, Dict[str, AbstractOptionView]] = {
            '통합': {
                '일반': TotalOptionMainView(self)
            },
            '기록부': {
                '일반': RecordOptionMainView(self),
                '입력가이드': ready_view
           },
            '데이터베이스': {
                '일반': DatabaseOptionMainView(self),
                '입력가이드': ready_view
            }
        }
        max_tail_string = '입력가이드'

        # 옵션 head list widget
        self.__head_list_widget = QListWidget()
        self.__head_list_widget.addItems(self.getHeadList())
    
        # 옵션 tail list widget
        self.__tail_list_widget = QListWidget()

        #   tail list widget 너비 설정용 임시값
        self.__tail_list_widget.addItems([max_tail_string])
        
        # 리스트 위젯 스타일링
        self.__head_list_widget.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1))
        self.__tail_list_widget.setFont(BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1))
        self.__head_list_widget.setFixedWidth(self.__head_list_widget.sizeHintForColumn(0) + 2 * self.__head_list_widget.frameWidth())
        self.__tail_list_widget.setFixedWidth(self.__tail_list_widget.sizeHintForColumn(0) + 2 * self.__tail_list_widget.frameWidth())

        #   tail list widget 너비 설정용 임시값 초기화
        self.__tail_list_widget.takeItem(0)

        # 옵션 stacked widget
        self.__stacked_widget = QStackedWidget()
        for head_iter in self.getHeadList():
            for tail_iter in self.getTailList(head_iter):
                self.__stacked_widget.addWidget(self.getOptionView(head_iter, tail_iter))

        # 버튼 위젯
        apply_button = BaseUI.basicQPushButton(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1),
                                               text='적용')
        confirm_button = BaseUI.basicQPushButton(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1),
                                                 text='확인')
        cancel_button = BaseUI.basicQPushButton(font=BaseUI.basicQFont(point_size=BaseUI.defaultPointSize()+1),
                                                text='취소')
        apply_button.clicked.connect(self.applyButtonClicked)
        confirm_button.clicked.connect(self.confirmButtonClicked)
        cancel_button.clicked.connect(self.cancelButtonClicked)

        # 버튼 레이아웃
        button_hbox = QHBoxLayout()
        button_hbox.addStretch(2)
        button_hbox.addWidget(apply_button)
        button_hbox.addStretch(1)
        button_hbox.addWidget(confirm_button)
        button_hbox.addStretch(1)
        button_hbox.addWidget(cancel_button)
        button_hbox.addStretch(2)

        # 우측 레이아웃
        right_vbox = QVBoxLayout()
        right_vbox.addStretch(3)
        right_vbox.addWidget(self.__stacked_widget)
        right_vbox.addStretch(7)
        right_vbox.addLayout(button_hbox)
        right_vbox.addStretch(1)

        # 전 레이아웃
        hbox = QHBoxLayout()
        hbox.addWidget(self.__head_list_widget)
        hbox.addWidget(self.__tail_list_widget)
        hbox.addLayout(right_vbox)

        self.resize(700, 400)
        self.setLayout(hbox)
        self.setWindowTitle('설정')

        # 리스트 위젯 연결
        self.__head_list_widget.currentTextChanged.connect(self.__headChanged)
        self.__tail_list_widget.currentTextChanged.connect(self.__tailChanged)

        # 초기값
        self.__head_list_widget.setCurrentRow(0)

    def activeView(self) -> Type['ShowingView']:
        return self

    def getHeadList(self) -> List[str]:
        return list(self.__options_info_dict.keys())

    def getTailList(self, head: str) -> List[str]:
        return list(self.__options_info_dict[head].keys())

    def getOptionView(self, head: str, tail: str) -> AbstractOptionView:
        return self.__options_info_dict[head][tail]

    @pyqtSlot(str)
    def __headChanged(self, head: str) -> None:
        self.__tail_list_widget.blockSignals(True)
        for row_count in range(self.__tail_list_widget.count()):
            self.__tail_list_widget.takeItem(0)
        self.__tail_list_widget.blockSignals(False)
        self.__tail_list_widget.addItems(self.getTailList(head))
        self.__tail_list_widget.setCurrentRow(0)

    @pyqtSlot(str)
    def __tailChanged(self, tail: str) -> None:
        head = self.__head_list_widget.currentItem().text()
        self.__stacked_widget.setCurrentWidget(self.getOptionView(head, tail))

    @pyqtSlot()
    def applyButtonClicked(self) -> None:
        for head_iter in self.getHeadList():
            for tail_iter in self.getTailList(head_iter):
                self.getOptionView(head_iter, tail_iter).applyOptionChanges()

    @pyqtSlot()
    def confirmButtonClicked(self) -> None:
        self.applyButtonClicked()
        self.close()

    @pyqtSlot()
    def cancelButtonClicked(self) -> None:
        for head_iter in self.getHeadList():
            for tail_iter in self.getTailList(head_iter):
                self.getOptionView(head_iter, tail_iter).render()
        self.close()



