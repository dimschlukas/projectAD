from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow


class Toolbar():
    def __init__(self, main):
        self.main: QMainWindow = main

        # Toolbar Exit
        self.toolbar_exit = QtWidgets.QToolBar('Exit')
        self.main.addToolBar(Qt.TopToolBarArea, self.toolbar_exit) # QtCore.Qt.LeftToolBarArea
        self.action_exit = QtWidgets.QAction(QIcon('assets/icon/exit.ico'), 'Exit', main)
        self.action_exit.setShortcut('Ctrl+Q')
        self.action_exit.triggered.connect(self.main.close)
        self.toolbar_exit.addAction(self.action_exit)
