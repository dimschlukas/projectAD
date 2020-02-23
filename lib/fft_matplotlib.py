import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from model.config import config


class FftVisu:
    # Abgrenzung zu main_window
    def __init__(self, main_window):
        self.main_window = main_window
        self.plot = plotter()
        mpl_toolbar = NavigationToolbar2QT(self.plot.fig, self.main_window.ui.central_widget)
        main_window.ui.FftPlotToolbar.addWidget(mpl_toolbar)
        main_window.ui.FftPlot.addWidget(self.plot.fig)


class plotter:
    def __init__(self, left=75, right=20, top=10, bottom=50, wspace=0.2, hspace=0.3, dpi=96):
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
        self.fig_base.set_figwidth(17)
        self.fig_base.set_figheight(8)
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
        self.x_ch1 = []
        self.y_ch1 = []
        self.fft_freq_ch1 = []
        self.fft_spect_ch1 = []
        self.x_ch2 = []
        self.y_ch2 = []
        self.fft_freq_ch2 = []
        self.fft_spect_ch2 = []


        self.ch1 = True
        self.ch2 = True
        self.xmax = None

        # Initialisierung
        self.first_update = False

    def update_complete(self):
        # ToDO: Labels Farben und Ränder anpassen
        self.ax1.clear()
        self.ax2.clear()

        if self.ch1:
            self.ax1.plot(self.x_ch1, self.y_ch1, color='#1bb2e0', lw=2, linestyle='-', label=r'Channel 1')
            self.ax2.plot(self.fft_freq_ch1, self.fft_spect_ch1, color='#1bb2e0', lw=2, linestyle='-', label=r'Channel 1')
        if self.ch2:
            self.ax1.plot(self.x_ch2, self.y_ch2, color='#fc2403', lw=2, linestyle='-', label=r'Channel 2')
            self.ax2.plot(self.fft_freq_ch2, self.fft_spect_ch2, color='#fc2403', lw=2, linestyle='-', label=r'Channel 2')


        if config.style_dark:
            self.ax1.grid(color='white', alpha=0.25, ls=':', lw=0.5)
            self.ax2.grid(color='white', alpha=0.25, ls=':', lw=0.5)
        else:
            self.ax1.grid(color='k', alpha=0.25, ls=':', lw=0.5)
            self.ax2.grid(color='k', alpha=0.25, ls=':', lw=0.5)

        self.ax1.set_xlabel(r'Zeit [s]')
        self.ax1.set_ylabel(r'Spannung [V]')
        self.ax2.set_xlabel(r'Amplitude [V]')
        self.ax2.set_ylabel(r'Frequenz [Hz]')

        if self.ch1 or self.ch2:
            self.legend()

        self.ax2.set_xlim(0, self.xmax)
        self.ax1.figure.canvas.draw_idle()
        self.ax1.figure.canvas.flush_events()
        self.ax2.figure.canvas.draw_idle()
        self.ax2.figure.canvas.flush_events()

    def subplots_adjust(self):
        # Handling der Plotränder => Verknüpfung mit resizeEvent (main_window) nicht vergessen
        # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
        width, height = self.fig.get_width_height()
        self.fig_base.subplots_adjust(left=self.left / width,
                                      right=1.0 - self.right / width,
                                      bottom=self.bottom / height,
                                      top=1.0 - self.top / height,
                                      wspace=self.wspace,
                                      hspace=self.hspace)

    def legend(self):
        legend = self.ax1.legend(loc='upper center')
        if config.style_dark:
            frame = legend.get_frame()
            frame.set_facecolor('#353535')
            frame.set_edgecolor('#707070')
            frame.set_linewidth(1)
