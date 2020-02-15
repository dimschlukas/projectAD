from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QMainWindow
from model.config import config


class Menu():
    def __init__(self, main):
        self.main: QMainWindow = main

        self.main_menu = QMenuBar(main)
        self.main_menu.setObjectName("mainMenu")
        main.setMenuBar(self.main_menu)

        # Datei
        self.file_menu = self.main_menu.addMenu('&Datei')
        self.exit_button = QtWidgets.QAction(QIcon('assets/icon/x-circle.svg'), '&Exit', main)
        # self.exitButton.setShortcut('Ctrl+Q')
        self.exit_button.setShortcut('q')
        self.exit_button.setStatusTip('Exit application')
        self.exit_button.triggered.connect(main.close)
        self.file_menu.addAction(self.exit_button)

        # Einstellungen
        self.settingsmenu = self.main_menu.addMenu('&Einstellungen')

        self.options_button = QAction(QIcon('assets/icon/settings.svg'), '&Optionen', main)
        self.options_button.triggered.connect(self.on_about)
        self.settingsmenu.addAction(self.options_button)

        self.load_config_button = QAction(QIcon('assets/icon/upload.svg'), '&Config Laden', main)
        self.load_config_button.triggered.connect(config.read)
        self.settingsmenu.addAction(self.load_config_button)

        self.save_config_button = QAction(QIcon('assets/icon/download.svg'), '&Config Speichern', main)
        self.save_config_button.triggered.connect(config.write)
        self.settingsmenu.addAction(self.save_config_button)


        # Hilfe
        self.helpMenu = self.main_menu.addMenu('&?')
        self.about_button = QAction(QIcon('assets/icon/help-circle.svg'), '&Information', main)
        self.about_button.triggered.connect(self.on_about)
        self.helpMenu.addAction(self.about_button)

    def on_about(self):
        QtWidgets.QMessageBox.about(self.main, 'Projekt AD',
                                    'Analog Discovery 2 ansteuerung\n'
                                    'mittels Python und QT\n'
                                    ' \n'
                                    '.\n'
                                    'Lukas Schmid')

    def context_main_menu(self, event):
        menu = QMenu(self.main)
        menu.addAction(self.about_button)
        menu.exec_(event.globalPos())
