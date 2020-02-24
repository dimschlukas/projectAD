import sys
import numpy as np

from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox

import add_ons.style
from add_ons.menu import Menu
from add_ons.statusbar import Statusbar
from add_ons.toolbar import Toolbar
from ui.main_ui import Ui_main_ui

# Eigene Imports
from model.config import config
from lib.signalgen_matplotlib import SignalgenVisu
from lib.fft_matplotlib import FftVisu
from lib.sinusgenerator import Sinusgen
from lib.runthread_fft import RunThread_fft


# 4k Display mit hoher DPI-Auflösung
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)


class Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_main_ui()
        self.ui.setupUi(self)
        self.setWindowTitle('ProjectAD by Lukas Schmid')
        self.setMinimumSize(QSize(1400, 800))
        self.resize(1600, 1400)
        self.move(300, 300)
        # self.showMaximized()

        self.menu = Menu(self, self.ui)
        self.toolbar = Toolbar(self)
        self.statusbar = Statusbar(self)

        # Defaultwerte laden
        for i in range(self.ui.table_sinus.rowCount()):
            self.ui.table_sinus.removeRow(i)
        self.ui.table_sinus.removeRow(0)
        for i in range(config.row_count):
            self.ui.table_sinus.insertRow(i)
            self.ui.table_sinus.setItem(i, 0, QTableWidgetItem(str(config.frequencies[i])))
            self.ui.table_sinus.setItem(i, 1, QTableWidgetItem(str(config.amplitudes[i])))
            self.ui.table_sinus.setItem(i, 2, QTableWidgetItem(str(config.phases[i])))
        self.ui.le_offset.setText(str(config.offset))
        self.ui.sb_abs.setValue(int(config.periods))
        self.ui.le_factor.setText(str(config.factor))
        self.ui.le_samples.setText(str(config.samples))
        self.adjust_samples()

        # Funktionszuordnung
        self.ui.bn_add.clicked.connect(self.add_sinus)
        self.ui.bn_delete.clicked.connect(self.delete_sinus)
        self.ui.bn_delete_all.clicked.connect(self.delete_all_sinus)
        self.ui.bn_calc_sinus.clicked.connect(self.generate_sinus)
        self.ui.cb_subsinus_visible.clicked.connect(self.view_subsinus)
        self.ui.le_samples.editingFinished.connect(self.adjust_samples)
        self.ui.bn_start_measure.clicked.connect(self.start_measure)
        self.ui.bn_cancle_measure.clicked.connect(self.stop_measure)
        self.ui.hs_fft_slider.valueChanged.connect(self.fft_slider)
        self.ui.cb_fft_ch1.clicked.connect(self.view_ch1)
        self.ui.cb_fft_ch2.clicked.connect(self.view_ch2)

        # Plots
        self.signalgen_matplot = SignalgenVisu(self)
        self.fft_matplot = FftVisu(self)

        self.simulation = False

        # Thread
        self.run_fft_thread = RunThread_fft(parent=self)

    def start_measure(self):
        self.run_fft_thread.start_thread()

    def stop_measure(self):
        self.run_fft_thread.stop()

    def adjust_samples(self):
        # Runde auf die nächste Zweierpotenz auf
        num = float(self.ui.le_samples.text())
        if np.log2(num).is_integer() == False:
            next = 2 ** (int(np.log2(num))+1)
            self.ui.le_samples.setText(str(next))

    def fft_slider(self):
        self.fft_matplot.plot.xmax = self.ui.hs_fft_slider.value()
        self.fft_matplot.plot.update_complete()


    def view_subsinus(self):
        if self.ui.cb_subsinus_visible.isChecked() == True:
            self.signalgen_matplot.plot.subsinus_visible = True
            self.signalgen_matplot.plot.update_complete()
        else:
            self.signalgen_matplot.plot.subsinus_visible = False
            self.signalgen_matplot.plot.update_complete()

    def view_ch1(self):
        if self.ui.cb_fft_ch1.isChecked() == True:
            self.fft_matplot.plot.ch1 = True
            self.fft_matplot.plot.update_complete()
        else:
            self.fft_matplot.plot.ch1 = False
            self.fft_matplot.plot.update_complete()

    def view_ch2(self):
        if self.ui.cb_fft_ch2.isChecked() == True:
            self.fft_matplot.plot.ch2 = True
            self.fft_matplot.plot.update_complete()
        else:
            self.fft_matplot.plot.ch2 = False
            self.fft_matplot.plot.update_complete()

    def add_sinus(self):
        frequency = config.default_frequency
        amplitude = config.default_amplitude
        phase = config.default_phase
        row_count = self.ui.table_sinus.rowCount()
        self.ui.table_sinus.insertRow(row_count)
        self.ui.table_sinus.setItem(row_count, 0, QTableWidgetItem(str(frequency)))
        self.ui.table_sinus.setItem(row_count, 1, QTableWidgetItem(str(amplitude)))
        self.ui.table_sinus.setItem(row_count, 2, QTableWidgetItem(str(phase)))

    def delete_sinus(self):
        self.ui.table_sinus.removeRow(self.ui.table_sinus.currentRow())

    def delete_all_sinus(self):
        self.ui.table_sinus.clearContents()
        for i in range(self.ui.table_sinus.rowCount()):
            self.ui.table_sinus.removeRow(i)
        self.ui.table_sinus.removeRow(0)

    def generate_sinus(self):
        if self.ui.table_sinus.rowCount() > 0:
            self.f = []
            self.a = []
            self.p = []
            for i in range(self.ui.table_sinus.rowCount()):
                self.f.append(float(self.ui.table_sinus.item(i, 0).text()))
                self.a.append(float(self.ui.table_sinus.item(i, 1).text()))
                self.p.append(float(self.ui.table_sinus.item(i, 2).text()))
            self.offset = float(self.ui.le_offset.text())
            self.asp = self.ui.sb_abs.value()
            self.factor = float(self.ui.le_factor.text())
            self.samples = int(self.ui.le_samples.text())

            sinusgen = Sinusgen(frequencies=self.f,
                                amplitudes=self.a,
                                phases=self.p,
                                n_sp=self.samples,
                                asp=self.asp,
                                offset=0.0,
                                factor=self.factor)
            self.zeit, self.signal, self.subsinus = sinusgen.calc()
            self.signal = self.signal + self.offset

            self.signalgen_matplot.plot.zeit = self.zeit
            self.signalgen_matplot.plot.signal = self.signal
            self.signalgen_matplot.plot.subsinus = self.subsinus
            self.signalgen_matplot.plot.update_complete()
        else:
            QMessageBox.about(self, 'ERROR: Sinus generieren', 'Es befinden sich keine Sinus Signale in der Liste.')
            print('Kein Sinus zum erzeugen')

    def keyPressEvent(self, event):
        """Event Erfassung und Auswertung der gedrückten Tasten"""
        super().keyPressEvent(event)
        # print(event.key())
        if event.key() == Qt.Key_Q:
            self.close()

    def resizeEvent(self, *args):
        """Event bei Grösenänderung des Anzeigefensters"""
        super().resizeEvent(*args)
        self.signalgen_matplot.plot.subplots_adjust()
        self.fft_matplot.plot.subplots_adjust()

    def closeEvent(self, *args):
        """Event wird ausgeführt beim Beenden der GUI-Oberfläche"""
        super().closeEvent(*args)

    def on_main_started(self):
        """Aufruf der Funktion erfolgt nach vollständiger Initialisierung."""

    def contextMenuEvent(self, event):
        """Event Kontextmenu (rechte Maustaste) mit Weiterleitung and die"""
        # Klasse MainMenu
        super().contextMenuEvent(event)
        try:
            self.menu.context_main_menu(event)
        except Exception as e:
            print('contextMenuEvent:', e)





def except_hook(cls, exception, traceback):
    """Fehlerausgabe in der Python-Konsole anstelle des Terminals."""
    sys.__excepthook__(cls, exception, traceback)

def except_hook(cls, exception, traceback):
    """Fehlerausgabe in der Python-Konsole anstelle des Terminals."""
    sys.__excepthook__(cls, exception, traceback)



if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icon/icon.png'))
    add_ons.style.set_style(app)
    main = Main()
    main.show()
    t = QTimer()
    t.singleShot(100, main.on_main_started)
    sys.exit(app.exec_())
