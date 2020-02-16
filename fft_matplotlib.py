import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure

from model.config import config
from lib.sinusgenerator import Sinusgen


class FftVisu:
    # Abgrenzung zu main_window
    def __init__(self, main_window):
        self.main_window = main_window
        self.plot = plotter()
        mpl_toolbar = NavigationToolbar2QT(self.plot.fig, self.main_window.ui.central_widget)
        main_window.ui.FftPlotToolbar.addWidget(mpl_toolbar)
        main_window.ui.FftPlot.addWidget(self.plot.fig)


class plotter:
    def __init__(self, left=75, right=10, top=40, bottom=60, wspace=0.2, hspace=10, dpi=96):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.wspace = wspace
        self.hspace = hspace
        self.dpi = dpi
        # Handling der Matplotfigure
        if config.style_dark:
            plt.style.use('dark_background')
        self.fig_base = Figure()
        self.fig_base, (self.ax1, self.ax2) = plt.subplots(2)
        self.fig_base.set_dpi(dpi)
        self.fig_base.set_figwidth(10)
        self.fig_base.set_figheight(2)
        if config.style_dark:
            self.fig_base.set_facecolor('#353535')
        else:
            self.fig_base.set_facecolor('#F0F0F0')
        self.fig = FigureCanvasQTAgg(self.fig_base)
        self.fig.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.fig.setMinimumSize(QtCore.QSize(100, 50))

        # Handling der Achsen
        # self.ax1 = self.fig_base.add_subplot(1, 1, 1)
        # self.ax2 = self.fig_base.add_subplot(1, 1, 1)
        if config.style_dark:
            self.ax1.set_facecolor('#353535')
            self.ax2.set_facecolor('#353535')
        else:
            self.ax1.set_facecolor('#F0F0F0')
            self.ax2.set_facecolor('#F0F0F0')

        # Funktionszuweisung
        self.x = None
        self.y = None
        self.fft_freq = None
        self.fft_spect = None

        # Initialisierung
        self.first_update = False
        # self.update_complete()

    def update_complete(self):
        # ToDO: Labels Farben und Ränder anpassen
        self.ax1.clear()
        self.ax2.clear()

        self.ax1.plot(self.x, self.y, color='#fc2403', lw=2, linestyle='-', label=r'Sinus')
        if config.style_dark:
            self.ax1.grid(color='white', alpha=0.25, ls=':', lw=0.5)
        else:
            self.ax1.grid(color='k', alpha=0.25, ls=':', lw=0.5)
        self.ax1.set_xlabel(r'Zeit [s]')
        self.ax1.set_ylabel(r'Spannung [V]')

        self.ax2.plot(self.fft_freq, self.fft_spect, color='#fc2403', lw=2, linestyle='-', label=r'Sinus')
        if config.style_dark:
            self.ax1.grid(color='white', alpha=0.25, ls=':', lw=0.5)
        else:
            self.ax1.grid(color='k', alpha=0.25, ls=':', lw=0.5)
        self.ax2.set_xlabel(r'Amplitude [V]')
        self.ax2.set_ylabel(r'Frequenz [Hz]')

        self.legend()

        # ymin = np.min(self.sinus.t)
        # ymax = np.max(self.sinus.t)
        # self.ax1.set_ylim(ymin, ymax)
        self.ax1.figure.canvas.draw_idle()
        self.ax1.figure.canvas.flush_events()

    def legend(self):
        legend = self.ax1.legend(loc='upper center')
        if config.style_dark:
            frame = legend.get_frame()
            frame.set_facecolor('#353535')
            frame.set_edgecolor('#707070')
            frame.set_linewidth(1)
