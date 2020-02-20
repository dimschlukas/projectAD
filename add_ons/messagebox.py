from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QMainWindow
from model.config import config


class MessageBox:
    def __init__(self, main):
        self.main: QMainWindow = main

    def test(self, info):
        QtWidgets.QMessageBox.about(self.main, 'test test test')
