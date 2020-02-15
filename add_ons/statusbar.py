from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QStatusBar, QLabel, QPushButton, QMainWindow


class Statusbar():
    def __init__(self, main):
        self.main: QMainWindow = main

        self.statusbar = QStatusBar(main)
        self.statusbar.setEnabled(True)
        self.statusbar.setCursor(QCursor(Qt.ArrowCursor))
        self.statusbar.setAutoFillBackground(True)
        main.setStatusBar(self.statusbar)
        main.statusBar().showMessage('')

        # optionale Integration von Widgets in der Statusbar
        # self.label = QLabel()
        # self.label.setText('')
        #
        # self.btn_exit = QPushButton()
        # self.btn_exit.setIcon(QIcon('assets/icon/exit.ico'))
        # self.btn_exit.clicked.connect(self.main.close)
        #
        # self.statusbar.addWidget(self.label, stretch=1.0)  # fake spacer
        # self.statusbar.addWidget(self.btn_exit)
        # self.label.show()
        # self.btn_exit.show()
        # self.statusbar.show()

    def status_message(self, value):
        self.main.statusBar().showMessage(value)
