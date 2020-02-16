import sys
import time

from PyQt5.QtCore import QSize, QTimer, Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem

import add_ons.style
from add_ons.menu import Menu
from add_ons.statusbar import Statusbar
from add_ons.toolbar import Toolbar
from ui.main_ui import Ui_main_ui

# Eigene Imports
from model.config import config
from signalgen_matplotlib import SignalgenVisu
from fft_matplotlib import FftVisu
import numpy as np
from lib.sinusgenerator import Sinusgen
from lib.ad import AnalogDiscovery
from lib.fft import Fft


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
        self.setWindowTitle('Template PyQt5')
        self.setMinimumSize(QSize(400, 200))
        self.resize(2000, 1200)
        self.move(300, 300)
        # self.showMaximized()

        self.menu = Menu(self)
        self.toolbar = Toolbar(self)
        self.statusbar = Statusbar(self)

        # Defaultwerte laden
        self.ui.le_offset.setText(str(config.offset))
        self.ui.sb_abs.setValue(int(config.periods))
        self.ui.le_factor.setText(str(config.factor))
        self.ui.le_samples.setText(str(config.samples))

        # Funktionszuordnung
        self.ui.bn_add.clicked.connect(self.add_sinus)
        self.ui.bn_delete.clicked.connect(self.delete_sinus)
        self.ui.bn_delete_all.clicked.connect(self.delete_all_sinus)
        self.ui.bn_calc_sinus.clicked.connect(self.generate_sinus)
        self.ui.cb_subsinus_visible.clicked.connect(self.view_subsinus)
        self.ui.le_samples.editingFinished.connect(self.adjust_samples)
        self.ui.bn_start_measure.clicked.connect(self.start_measure)
        self.ui.bn_cancle_measure.clicked.connect(self.stop_measure)

        self.signalgen_matplot = SignalgenVisu(self)
        self.fft_matplot = FftVisu(self)


    def start_measure(self):
        # run thread
        run_thread = RunThread_fft(self.zeit, self.signal, self.fft_matplot, parent=self)
        run_thread.start_thread()
        run_thread = RunThread_Progressbar(self.zeit, self.ui, parent=self)
        run_thread.start_thread()




    def stop_measure(self):
        self.run_thread.stop()

    def adjust_samples(self):
        # Runde auf die nächste Zweierpotenz auf
        num = float(self.ui.le_samples.text())
        if np.log2(num).is_integer() == False:
            next = 2 ** (int(np.log2(num))+1)
            self.ui.le_samples.setText(str(next))

    def view_subsinus(self):
        if self.ui.cb_subsinus_visible.isChecked() == True:
            self.signalgen_matplot.plot.subsinus_visible = True
            self.signalgen_matplot.plot.update_complete()
        else:
            self.signalgen_matplot.plot.subsinus_visible = False
            self.signalgen_matplot.plot.update_complete()

    def generate_sinus(self):
        if self.ui.table_sinus.rowCount() > 0:
            f = []
            a = []
            p = []
            for i in range(self.ui.table_sinus.rowCount()):
                f.append(float(self.ui.table_sinus.item(i, 0).text()))
                a.append(float(self.ui.table_sinus.item(i, 1).text()))
                p.append(float(self.ui.table_sinus.item(i, 2).text()))
            offset = float(self.ui.le_offset.text())
            asp = self.ui.sb_abs.value()
            factor = float(self.ui.le_factor.text())
            samples = int(self.ui.le_samples.text())

            sinusgen = Sinusgen(frequencies=f, amplitudes=a, phases=p, n_sp=samples, asp=asp, offset=offset, factor=factor)
            self.zeit, self.signal, self.subsinus = sinusgen.calc()

            self.signalgen_matplot.plot.zeit = self.zeit
            self.signalgen_matplot.plot.signal = self.signal
            self.signalgen_matplot.plot.subsinus = self.subsinus
            self.signalgen_matplot.plot.update_complete()
        else:
            print('Kein Sinus zum erzeugen')

    def add_sinus(self):
        # ToDO: get values from config file for default sinus
        frequency = config.frequency
        amplitude = config.amplitude
        phase = config.phase
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

    def keyPressEvent(self, event):
        """Event Erfassung und Auswertung der gedrückten Tasten"""
        super().keyPressEvent(event)
        # print(event.key())
        if event.key() == Qt.Key_Q:
            self.close()

    def contextMenuEvent(self, event):
        """Event Kontextmenu (rechte Maustaste) mit Weiterleitung and die"""
        # Klasse MainMenu
        super().contextMenuEvent(event)
        try:
            self.menu.context_main_menu(event)
        except Exception as e:
            print('contextMenuEvent:', e)

    def resizeEvent(self, *args):
        """Event bei Grösenänderung des Anzeigefensters"""
        super().resizeEvent(*args)

    def closeEvent(self, *args):
        """Event wird ausgeführt beim Beenden der GUI-Oberfläche"""
        super().closeEvent(*args)

    def on_main_started(self):
        """Aufruf der Funktion erfolgt nach vollständiger Initialisierung."""
        pass


class RunThread_fft(QThread):  # http://doc.qt.io/qt-5/qthread.html
    signal_counter = pyqtSignal(int)  # define new Signal

    def __init__(self, zeit, signal, fft_matplot, parent=None):
        super().__init__(parent)
        self.zeit = zeit
        self.signal = signal
        self.fft_matplot = fft_matplot
        # self.fft_matplot = FftVisu(main_window)

    def run(self):
        ad = AnalogDiscovery()
        ad.open()
        ad.create_custom_waveform(self.signal, self.zeit[-1])
        ad.collect_data()
        ch1, ch2, = ad.read_data()
        ad.close()

        fft = Fft(self.zeit, ch2, fenstermethode=None, interpolatemethode='linear', fmax=200)
        x, y, freq, spec = fft.calc()

        self.fft_matplot.plot.x = x
        self.fft_matplot.plot.y = y
        self.fft_matplot.plot.fft_freq = freq
        self.fft_matplot.plot.fft_spect = spec
        self.fft_matplot.plot.update_complete()

    def start_thread(self):
        print('starting thread...')
        self.start(QThread.NormalPriority)

    def stop(self):
        print('stopping thread...')
        self.terminate()

class RunThread_Progressbar(QThread):  # http://doc.qt.io/qt-5/qthread.html
    signal_counter = pyqtSignal(int)  # define new Signal

    def __init__(self, zeit, ui, parent=None):
        super().__init__(parent)
        self.zeit = zeit
        self.ui = ui

    def run(self):
        self.ui.progressBar.setTextVisible(False)
        for i in range(0, 101, 1):
            time.sleep(self.zeit[-1]/100)
            self.ui.progressBar.setValue(i)
        self.ui.progressBar.setTextVisible(True)

    def start_thread(self):
        print('starting thread...')
        self.start(QThread.NormalPriority)

    def stop(self):
        print('stopping thread...')
        self.terminate()

def except_hook(cls, exception, traceback):
    """Fehlerausgabe in der Python-Konsole anstelle des Terminals."""
    sys.__excepthook__(cls, exception, traceback)

def except_hook(cls, exception, traceback):
    """Fehlerausgabe in der Python-Konsole anstelle des Terminals."""
    sys.__excepthook__(cls, exception, traceback)



if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icon/abbts.ico'))
    add_ons.style.set_style(app)
    main = Main()
    main.show()
    t = QTimer()
    t.singleShot(100, main.on_main_started)
    sys.exit(app.exec_())
