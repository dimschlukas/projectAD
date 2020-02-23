import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QAction, QMenu, QMainWindow, QFileDialog, QTableWidgetItem
from model.config import config
from lib.csv_read_write import CsvReadWrite
from lib.ad import AnalogDiscovery

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
        self.save_fft_plot.setEnabled(False)
        self.save_fft_csv = QAction(QIcon(''), '&CSV speichern', main)
        self.save_fft_csv.triggered.connect(self.save_fft_csv_function)
        self.fft_menu.addAction(self.save_fft_csv)
        self.save_fft_csv.setEnabled(False)


        # Einstellungen
        self.settingsmenu = self.main_menu.addMenu('&Einstellungen')

        self.simulation_button = QAction(QIcon(''), '&Simulations Modus', main, checkable=True)
        self.simulation_button.triggered.connect(self.simulation)
        self.settingsmenu.addAction(self.simulation_button)

        # Hilfe
        self.helpMenu = self.main_menu.addMenu('&?')

        self.about_button = QAction(QIcon('assets/icon/help-circle.svg'), '&Information', main)
        self.about_button.triggered.connect(self.on_about)
        self.helpMenu.addAction(self.about_button)

        self.credits_button = QAction('&Credits', main)
        self.credits_button.triggered.connect(self.credits)
        self.helpMenu.addAction(self.credits_button)

    def on_about(self):
        ad = AnalogDiscovery()
        error = ad.open()
        ad.close()
        if error:
            QtWidgets.QMessageBox.about(self.main, 'Projekt AD',
                                        'Analog Discovery 2 ansteuerung\n'
                                        'mittels Python und QT\n'
                                        ' \n'
                                        'Kein Analog Discovery verbunden.\n'
                                        '\n by Lukas Schmid')
        else:
            sn = ad.serialnumber
            QtWidgets.QMessageBox.about(self.main, 'Projekt AD',
                                        'Analog Discovery 2 ansteuerung\n'
                                        'mittels Python und QT\n'
                                        ' \n'
                                        'Analog Discovery verbunden: '+str(sn.value)+'\n'
                                        '\n by Lukas Schmid')

    def simulation(self):
        if self.simulation_button.isChecked():
            self.main.simulation = True
            self.main.ui.progressBar.setFormat('SIMULATION')
            self.main.ui.progressBar.setTextVisible(True)
        else:
            self.main.simulation = False
            self.main.ui.progressBar.setTextVisible(False)

    def load_config(self):
        self.ui.table_sinus.clearContents()
        for i in range(self.ui.table_sinus.rowCount()):
            self.ui.table_sinus.removeRow(i)
        self.ui.table_sinus.removeRow(0)
        config.read()
        for i in range(config.row_count):
            self.ui.table_sinus.insertRow(i)
            self.ui.table_sinus.setItem(i, 0, QTableWidgetItem(str(config.frequencies[i])))
            self.ui.table_sinus.setItem(i, 1, QTableWidgetItem(str(config.amplitudes[i])))
            self.ui.table_sinus.setItem(i, 2, QTableWidgetItem(str(config.phases[i])))
        self.ui.le_offset.setText(str(config.offset))
        self.ui.sb_abs.setValue(int(config.periods))
        self.ui.le_factor.setText(str(config.factor))
        self.ui.le_samples.setText(str(config.samples))
        self.main.adjust_samples()
        QtWidgets.QMessageBox.about(self.main, 'Config', 'Config erfolgreich geladen')

    def save_config(self):
        config.row_count = self.ui.table_sinus.rowCount()
        if config.row_count > 0:
            f = []
            a = []
            p = []
            for i in range(config.row_count):
                f.append(float(self.ui.table_sinus.item(i, 0).text()))
                a.append(float(self.ui.table_sinus.item(i, 1).text()))
                p.append(float(self.ui.table_sinus.item(i, 2).text()))
            config.frequencies = f
            config.amplitudes = a
            config.phases = p
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
        filename = QFileDialog.getExistingDirectory(self.main, 'Speichere FFT CSV')
        if filename == '':
            return
        c = CsvReadWrite(url_write=filename + '/FFT_Zeitsignal.csv')
        c.header = ['Zeit [s]', 'Spannung [V]']
        x = self.main.fft_matplot.plot.x
        y = self.main.fft_matplot.plot.y
        data = x, y
        c.data_np = np.array(data)
        c.write(header_included=True)

        c = CsvReadWrite(url_write=filename + '/FFT_Frequenzspektren.csv')
        c.header = ['Frequenz [Hz]', 'Amplitude [V]']
        freq = self.main.fft_matplot.plot.fft_freq
        spect = self.main.fft_matplot.plot.fft_spect
        data = freq, spect
        c.data_np = np.array(data)
        c.write(header_included=True)
        QtWidgets.QMessageBox.about(self.main, 'CSV gespeichert',
                                    'FFT_Zeitsignal.csv und FFT_Frequenzspektren.csv wurde unter folgendem ordner abgelegt:\n \n "' + filename + '"')

    def credits(self):
        QtWidgets.QMessageBox.about(self.main, 'Credits',
                                    'Icon By Maxim Kulikov from Noun Project')

    def context_main_menu(self, event):
        menu = QMenu(self.main)
        menu.addAction(self.about_button)
        menu.addAction(self.simulation_button)
        menu.addAction(self.load_config_button)
        menu.addAction(self.save_config_button)
        menu.addAction(self.save_fft_plot)
        menu.addAction(self.save_fft_csv)
        menu.addAction(self.load_config_button)
        menu.addAction(self.save_config_button)
        menu.exec_(event.globalPos())
