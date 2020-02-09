import sys

import style
from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from ui.main_ui import Ui_main_ui

# Eigene Imports
from lib.base_signals import Sinus
import matplotlib.pyplot as plt
import numpy as np

# 4k Display mit hoher DPI-Auflösung
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.ui = Ui_main_ui()
        self.ui.setupUi(self)
        self.setWindowTitle('Template minimal PyQt5')
        self.setMinimumSize(QSize(400, 200))
        self.resize(1000, 600)
        self.move(300, 300)
        # self.showMaximized()
        self.ui.bn_add.clicked.connect(self.add_sinus)

    def add_sinus(self):
        frequency = self.ui.sb_frequency.value()
        amplitude = self.ui.sb_amplitude.value()
        offset = self.ui.sb_offset.value()
        phase = self.ui.sb_phase.value()
        n = self.ui.sb_n.value()
        factor = self.ui.sb_factor.value()
        samples = self.ui.sb_samples.value()

        sinus = Sinus(f=frequency,
                       n_sp=samples,
                       amplitude=amplitude,
                       n=n,
                       phase=(phase * np.pi / 180.0),
                       offset=offset)
        self.ui.table_sinus.insertRow(0)
        self.ui.table_sinus.setItem(0, 0, QTableWidgetItem(str(frequency)))
        self.ui.table_sinus.setItem(0, 1, QTableWidgetItem(str(amplitude)))
        self.ui.table_sinus.setItem(0, 2, QTableWidgetItem(str(n)))
        self.ui.table_sinus.setItem(0, 3, QTableWidgetItem(str(phase)))
        self.plot(sinus.t, sinus.signal)

    def plot(self, y, x):
        fig, ax1 = plt.subplots(figsize=(25 / 2.54, 25 / 5))
        ax1.set_title('Sinus')
        ax1.set_xlabel('Zeit [s]')
        ax1.set_ylabel('Spannung [V]')
        ax1.plot(y, x, 'r-', label='Signal')
        # ax1.plot(zeit, dc, 'b--', linewidth=0.5, label='Sinus 1')
        # ax1.plot(zeit, sinus1.signal, 'b--', linewidth=0.5, label='Sinus 1')
        # ax1.plot(zeit, sinus2.signal, 'b--', linewidth=0.5, label='Sinus 2')
        # ax1.plot(zeit, sinus3.signal, 'b--', linewidth=0.5, label='Sinus 3')
        # ax1.plot(zeit, sinus4.signal, 'b--', linewidth=0.5, label='Sinus 4')
        ax1.grid(which='both', color='k', alpha=0.75, ls='-', lw=0.5)
        # plt.savefig('A1_Synthetisches_Signal.png', dpi=200)
        plt.show()

    def keyPressEvent(self, event):
        """Event Erfassung und Auswertung der gedrückten Tasten"""
        super().keyPressEvent(event)
        # print(event.key())
        if event.key() == Qt.Key_Q:
            self.close()

    def resizeEvent(self, *args):
        """Event bei Grösenänderung des Anzeigefensters"""
        super().resizeEvent(*args)

    def closeEvent(self, *args):
        """Event wird ausgeführt beim Beenden der GUI-Oberfläche"""
        super().closeEvent(*args)

    def on_main_started(self):
        """Aufruf der Funktion erfolgt nach vollständiger Initialisierung.
        self.send_status_msg('on main started')"""
        pass


def except_hook(cls, exception, traceback):
    """Fehlerausgabe in der Python-Konsole anstelle des Terminals."""
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    sys.excepthook = except_hook
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('assets/icon/abbts.ico'))
    style.set_style(app)
    main = Main()
    main.show()
    t = QTimer()
    t.singleShot(100, main.on_main_started)
    sys.exit(app.exec_())
