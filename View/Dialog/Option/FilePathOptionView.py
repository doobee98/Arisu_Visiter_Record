from View.Dialog.Option.AbstractOptionView import *
from Utility.Module.ConfigModule import *
from Utility.MyPyqt.MyMessageBox import *

"""
FilePathOptionView(AbstractOptionView)
"""# todo 좀더 이쁘게


class FilePathOptionView(AbstractOptionView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__model = ConfigModule.FilePath
        self.__file_type_widget_dict: Dict[FileType, QLabel] = {file_enum_iter: None for file_enum_iter in FileType}
        gbox = QGridLayout()

        for row_iter, file_enum_iter in enumerate(FileType):
            field_lbl = MyDefaultWidgets.basicQLabel(text=file_enum_iter.value, alignment=Qt.AlignLeft)
            gbox.addWidget(field_lbl, row_iter, 0)

            file_path_iter = self.__model.filePathDirectory(file_enum_iter)
            if type(file_path_iter) == bool:
                cbox = QCheckBox()
                cbox.setChecked(file_path_iter)
                gbox.addWidget(cbox, row_iter, 1)
                self.__file_type_widget_dict[file_enum_iter] = cbox
            else:  # isinstance(self.getModel().getOption(field), int)
                directory_le = MyDefaultWidgets.basicQLineEdit(text=str(file_path_iter), alignment=Qt.AlignLeft)
                directory_le.setFixedWidth(400)  # todo 왜 minimum가 안될까
                directory_le.setReadOnly(True)
                gbox.addWidget(directory_le, row_iter, 1)

                def buttonSlot(widget: MyLineEdit) -> None:
                    find_path = self.execFileFinderView()
                    if find_path:
                        widget.setText(find_path.replace('/', '\\'))
                    else:
                        return

                directory_button = MyDefaultWidgets.basicQPushButton(text='...')
                directory_button.setFixedWidth(40)
                gbox.addWidget(directory_button, row_iter, 2)
                directory_button.clicked.connect(lambda checked, widget=directory_le: buttonSlot(widget))
                self.__file_type_widget_dict[file_enum_iter] = directory_le
            gbox.setRowStretch(row_iter, 1)  # todo: row stretch? 의도는 높이를 모두 같게 하기 위해서
        self.setLayout(AbstractOptionView.getCenterWrapperLayout(gbox))

    def myRender(self) -> None:
        for file_type_enum_iter, widget_iter in self.__file_type_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                widget_iter.setChecked(bool(self.__model.filePathDirectory(file_type_enum_iter)))
            elif isinstance(widget_iter, (QLineEdit, QLabel)):
                widget_iter.setText(str(self.__model.filePathDirectory(file_type_enum_iter)))
            else:
                ErrorLogger.reportError('QLabel, QCheckbox 또는 QLineEdit중 한 종류여야 합니다.')
                raise AttributeError

    def applyOptionChanges(self) -> None:
        change_dict = {}
        for file_type_enum_iter, widget_iter in self.__file_type_widget_dict.items():
            if isinstance(widget_iter, QCheckBox):
                old_value = bool(self.__model.filePathDirectory(file_type_enum_iter))
                new_value = (widget_iter.checkState() == Qt.Checked)
            elif isinstance(widget_iter, (QLineEdit, QLabel)):
                old_value = str(self.__model.filePathDirectory(file_type_enum_iter))
                new_value = widget_iter.text()
            else:
                ErrorLogger.reportError('QLabel, QCheckbox 또는 QLineEdit중 한 종류여야 합니다.', AttributeError)
                return
            if old_value != new_value:
                change_dict[file_type_enum_iter] = new_value
        has_close = False
        if any(option_enum_iter.value in self.__model.closeOptionNameList() for option_enum_iter in change_dict.keys()):
            reply = MyMessageBox.question(self, '종료', '변경할 옵션 중에서 재시작이 필요한 옵션이 있습니다.\n종료하시겠습니까?')
            if reply == MyMessageBox.Yes:
                has_close = True
            else:
                self.myRender()
                return
        for file_type_enum_iter, data_iter in change_dict.items():
            self.__model.setFilePathDirectory(file_type_enum_iter, data_iter)
        if has_close:
            sys.exit()

    def execFileFinderView(self) -> str:
        file_dialog = QFileDialog(self, '폴더 찾기', DefaultFilePath.DATA)
        file_dialog.setFileMode(QFileDialog.Directory)
        if file_dialog.exec_():
            if len(file_dialog.selectedFiles()) != 1:
                ErrorLogger.reportError('파일을 하나만 선택해 주세요.')
                return None
            folder_path = file_dialog.selectedFiles()[0]
            return folder_path
        return None



