from Utility.Config.ConfigModule import *
from Utility.UI.BaseUI import *
from View.Option.AbstractOptionView import *


# todo 현재는 baseUI에서 폰트 크기 변경 설정을 켜지 않았기 때문에, 숫자를 바꾸면 껐다 켜야만 확인이 가능함
class FileDirectoryOptionView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = Config.FileDirectoryOption
        self.__field_widget_dict: Dict[str, QLabel] = {field: None for field in self.__model.getFieldList()}
        self.__button_widget_list: List[Tuple[QPushButton, QLabel]] = []
        gbox = QGridLayout()

        for row_iter, field_iter in enumerate(self.__field_widget_dict.keys()):
            option_iter = self.__model.getOption(field_iter)
            field_lbl = BaseUI.basicQLabel(text=self.__model.fieldPrintText(field_iter), alignment=Qt.AlignLeft)
            gbox.addWidget(field_lbl, row_iter, 0)

            if type(option_iter) == bool:
                cbox = QCheckBox()
                cbox.setChecked(option_iter)
                gbox.addWidget(cbox, row_iter, 1)
                self.__field_widget_dict[field_iter] = cbox
            else:  # isinstance(self.getModel().getOption(field), int)
                directory_lbl = BaseUI.basicQLabel(text=str(option_iter), alignment=Qt.AlignLeft)
                directory_lbl.setFixedWidth(200)  # todo 왜 minimum가 안될까
                gbox.addWidget(directory_lbl, row_iter, 1)

                directory_button = BaseUI.basicQPushButton(text='...')
                directory_button.setFixedWidth(40)
                gbox.addWidget(directory_button, row_iter, 2)
                directory_button.clicked.connect(self.directoryButtonClicked)

                self.__field_widget_dict[field_iter] = directory_lbl
                self.__button_widget_list.append((directory_button, directory_lbl))
            gbox.setRowStretch(row_iter, 1)  # todo: row stretch? 의도는 높이를 모두 같게 하기 위해서
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(gbox))

    def render(self) -> None:
        for field_iter, widget_iter in self.__field_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                widget_iter.setChecked(bool(self.__model.getOption(field_iter)))
            elif isinstance(widget_iter, (QLineEdit, QLabel)):
                widget_iter.setText(str(self.__model.getOption(field_iter)))
            else:
                ErrorLogger.reportError('QCheckbox, QLabel 또는 QLineEdit중 한 종류여야 합니다.', AttributeError)

    def applyOptionChanges(self) -> None:
        change_dict = {}
        for field_iter, widget_iter in self.__field_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                old_value = bool(self.__model.getOption(field_iter))
                new_value = (widget_iter.checkState() == Qt.Checked)
            elif isinstance(widget_iter, (QLineEdit, QLabel)):
                old_value = str(self.__model.getOption(field_iter))
                new_value = widget_iter.text()
            else:
                ErrorLogger.reportError('QCheckbox 또는 QLineEdit, QLabel중 한 종류여야 합니다.', AttributeError)
                return
            if old_value != new_value:
                change_dict[field_iter] = new_value
        has_close = False
        if any(field_iter in self.__model.getCloseFieldList() for field_iter in change_dict.keys()):
            reply = QMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if reply == QMessageBox.No:
                self.render()
                return
            else:
                has_close = True
        self.__model.changeOptions(change_dict)
        if has_close:
            sys.exit()
        self.__model.changeOptions(change_dict)

    @MyPyqtSlot()
    def directoryButtonClicked(self) -> None:
        button: QPushButton = self.sender()
        if button:
            widget: QLabel = None
            for tuple_iter in self.__button_widget_list:
                if tuple_iter[0] == button:
                    widget = tuple_iter[1]
                    break
            if widget is None:
                ErrorLogger.reportError('FileDirectory View에 문제가 있습니다.', EOFError)
            file_dialog = QFileDialog(self, '폴더 찾기', './')
            file_dialog.setFileMode(QFileDialog.Directory)
            #file_dialog.setOption(QFileDialog.ShowDirsOnly, False)
            if file_dialog.exec_():
                if len(file_dialog.selectedFiles()) != 1:
                    ErrorLogger.reportError('파일을 하나만 선택해 주세요.')
                    return
                folder_path = file_dialog.selectedFiles()[0]
                widget.setText(self.__model.convertDirectory(folder_path))


