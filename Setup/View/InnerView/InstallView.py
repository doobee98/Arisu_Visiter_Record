from Setup.View.InnerView.AbstractInnerView import *
import zipfile
import os
from win32com.client import Dispatch
from Utility.File.BasicFileTable import *


class InstallView(AbstractInnerView):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.lbl = QLabel('\n\n\n')

        self.setCenterWidget(self.lbl)

    def install(self):
        install_path = self.beforeView().beforeView().installPath()
        data_path = BasicFileTable.DATA
        content_text = ''
        try:
            exe_zip_ref = zipfile.ZipFile('ArisuRecord.zip', 'r')
            exe_zip_ref.extractall(install_path)
            exe_zip_ref.close()
            content_text += 'Program: ' + install_path + '\n'
            if not os.path.isdir(data_path):
                data_zip_ref = zipfile.ZipFile('ArisuRecordData.zip', 'r')
                data_zip_ref.extractall(data_path)
                data_zip_ref.close()
                content_text += '   Data: ' + data_path + '\n'
            content_text += 'Success'
        except Exception as e:
            content_text += install_path + '\n'
            content_text += str(e) + '\n'
            content_text += 'Failed'
        self.lbl.setText(content_text)

        desktop_path = os.path.expanduser("~\\Desktop")
        shell = Dispatch('WScript.Shell')

        exe_path = os.path.join(desktop_path, "아리수 출입자기록부 프로그램.lnk")
        exe_target = os.path.join(install_path, 'exec\\ArisuRecord.exe')
        exe_wDir = os.path.join(install_path, 'exec')
        exe_icon = os.path.join(install_path, 'exec\\ArisuRecord.exe')

        shortcut_exe = shell.CreateShortCut(exe_path)
        shortcut_exe.TargetPath = exe_target
        shortcut_exe.WorkingDirectory = exe_wDir
        shortcut_exe.IconLocation = exe_icon
        shortcut_exe.save()

        record_folder_path = os.path.join(desktop_path, "기록부.lnk")
        record_folder_target = BasicFileTable.Record
        # record_folder_wDir = BasicFileTable.Record
        # record_folder_icon = BasicFileTable.Record

        shortcut_record_folder = shell.CreateShortCut(record_folder_path)
        shortcut_record_folder.TargetPath = record_folder_target
        # shortcut_record_folder.WorkingDirectory = record_folder_wDir
        # shortcut_record_folder.IconLocation = record_folder_icon
        shortcut_record_folder.save()

    def render(self) -> None:
        self.lbl.setText('Installing...')
        self.install()

    def verify(self) -> bool:
        return True
