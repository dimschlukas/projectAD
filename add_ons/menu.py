import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QMainWindow, QFileDialog
from model.config import config
from lib.csv_read_write import CsvReadWrite

class Menu():
    def __init__(self, main, ui):
        self.main: QMainWindow = main
        self.ui = ui

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

        self.load_config_button = QAction(QIcon('assets/icon/upload.svg'), 'Config &Laden', main)
        self.load_config_button.triggered.connect(self.load_config)
        self.file_menu.addAction(self.load_config_button)

        self.save_config_button = QAction(QIcon('assets/icon/download.svg'), 'Config &Speichern', main)
        self.save_config_button.triggered.connect(self.save_config)
        self.file_menu.addAction(self.save_config_button)

        # Messung
        self.measurement_menu = self.main_menu.addMenu('&Messung')
        self.fft_menu = self.measurement_menu.addMenu('&FFT')

        self.save_fft_plot = QAction(QIcon(''), '&Plot speichern', main)
        self.save_fft_plot.triggered.connect(self.save_fft_plot_function)
        self.fft_menu.addAction(self.save_fft_plot)
        self.save_fft_csv = QAction(QIcon(''), '&CSV speichern', main)
        self.save_fft_csv.triggered.connect(self.save_fft_csv_function)
        self.fft_menu.addAction(self.save_fft_csv)




        # Einstellungen
        self.settingsmenu = self.main_menu.addMenu('&Einstellungen')

        self.options_button = QAction(QIcon('assets/icon/settings.svg'), '&Optionen', main)
        self.options_button.triggered.connect(self.on_about)
        self.settingsmenu.addAction(self.options_button)

        # Hilfe
        self.helpMenu = self.main_menu.addMenu('&?')

        self.about_button = QAction(QIcon('assets/icon/help-circle.svg'), '&Information', main)
        self.about_button.triggered.connect(self.on_about)
        self.helpMenu.addAction(self.about_button)

        self.credits_button = QAction('&Credits', main)
        self.credits_button.triggered.connect(self.credits)
        self.helpMenu.addAction(self.credits_button)


    def on_about(self):
        QtWidgets.QMessageBox.about(self.main, 'Projekt AD',
                                    'Analog Discovery 2 ansteuerung\n'
                                    'mittels Python und QT\n'
                                    ' \n'
                                    '.\n'
                                    'Lukas Schmid')

    def load_config(self):
        config.read()
        self.ui.le_offset.setText(str(config.offset))
        self.ui.sb_abs.setValue(int(config.periods))
        self.ui.le_factor.setText(str(config.factor))
        self.ui.le_samples.setText(str(config.samples))
        self.main.adjust_samples()
        QtWidgets.QMessageBox.about(self.main, 'Config',
                                    'Config erfolgreich geladen')

    def save_config(self):
        if self.ui.table_sinus.rowCount() > 0:
            config.frequency = float(self.ui.table_sinus.item(0, 0).text())
            config.amplitude = float(self.ui.table_sinus.item(0, 1).text())
            config.phase = float(self.ui.table_sinus.item(0, 2).text())
        else:
            config.frequency = 1.0
            config.amplitude = 1.0
            config.phase = 0.0
        config.offset = float(self.ui.le_offset.text())
        config.periods = self.ui.sb_abs.value()
        config.factor = float(self.ui.le_factor.text())
        config.samples = int(self.ui.le_samples.text())
        config.write()
        QtWidgets.QMessageBox.about(self.main, 'Config',
                                    'Config erfolgreich gespeichert')

    def save_fft_plot_function(self):
        filename = QFileDialog.getSaveFileName(self.main, 'Speichere FFT Plot', 'FFT_Plot.png', 'PNG (*.png)')
        if filename[0] == '':
            return
        self.main.fft_matplot.plot.fig_base.savefig(filename[0])

    def save_fft_csv_function(self):
        filename = QFileDialog.getSaveFileName(self.main, 'Speichere FFT CSV', 'FFT_data.txt', 'TXT (*.txt);;CSV (*.csv)')
        if filename[0] == '':
            return
        c = CsvReadWrite(url_write=filename[0])
        c.header = ['t [s]', 'y [V]', 'f [Hz]', 'A [V]']
        x = self.main.fft_matplot.plot.x
        y = self.main.fft_matplot.plot.y
        freq = self.main.fft_matplot.plot.fft_freq
        spect = self.main.fft_matplot.plot.fft_spect
        for i in range(int(len(x)/2)):
            freq = np.append(freq, '')
            spect = np.append(spect, '')
        data = x, y, freq, spect
        c.data_np = np.array(data)
        c.write(header_included=True)

    def credits(self):
        QtWidgets.QMessageBox.about(self.main, 'Credits',
                                    'Icon By Maxim Kulikov from Noun Project')

    def context_main_menu(self, event):
        menu = QMenu(self.main)
        menu.addAction(self.about_button)
        menu.exec_(event.globalPos())
