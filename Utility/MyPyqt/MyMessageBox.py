from Utility.MyPyqt.ShowingView import *
from PyQt5.QtWidgets import QMessageBox, QWidget
from typing import Union

"""
MyMessageBox
QMessageBox를 규격화하여 간편하게 쓰기 위해 만든 편의 클래스
"""

# todo
"""
1. Alert 시스템?
2. 상속 전 클래스랑 다른 인자? -> information 따위를 myInformation으로 바꿔야 할까
"""
class MyMessageBox(QMessageBox, ShowingView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    """
    method
    * information
    * question
    * warning
    * critical
    * __createMessageBox
    """
    @classmethod
    def information(cls, parent: QWidget, title: str, text: str) -> 'QMessageBox.StandardButton':
        msg = MyMessageBox.__createMessageBox(title, text, QMessageBox.Yes, QMessageBox.Yes, parent)
        msg.setIcon(QMessageBox.Information)
        reply = msg.exec_()
        return reply

    @classmethod
    def question(cls, parent: QWidget, title: str, text: str) -> 'QMessageBox.StandardButton':
        msg = MyMessageBox.__createMessageBox(title, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.No, parent)
        msg.setIcon(QMessageBox.Question)
        reply = msg.exec_()
        return reply

    @classmethod
    def warning(cls, parent: QWidget, title: str, text: str) -> 'QMessageBox.StandardButton':
        msg = MyMessageBox.__createMessageBox(title, text, QMessageBox.Yes, QMessageBox.Yes, parent)
        msg.setIcon(QMessageBox.Warning)
        reply = msg.exec_()
        return reply

    @classmethod
    def critical(cls, parent: QWidget, title: str, text: str) -> 'QMessageBox.StandardButton':
        msg = MyMessageBox.__createMessageBox(title, text, QMessageBox.Yes, QMessageBox.Yes, parent)
        msg.setIcon(QMessageBox.Critical)
        reply = msg.exec_()
        return reply

    @classmethod
    def __createMessageBox(cls, title: str, text: str,
                           standard_buttons: Union[QMessageBox.StandardButtons, QMessageBox.StandardButton],
                           default_button: QMessageBox.StandardButton, parent: QWidget) -> 'MyMessageBox':
        msg = MyMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStandardButtons(standard_buttons)
        msg.setDefaultButton(default_button)
        return msg

    """
    override
    * activeView
    """
    def activeView(self) -> 'ShowingView':
        return self