import matplotlib.pyplot as plt
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from model.config import config


class SignalgenVisu:
    # Abgrenzung zu main_window
    def __init__(self, main_window):
        self.main_window = main_window
        self.plot = plotter()
        main_window.ui.SinusSignalPlot.addWidget(self.plot.fig)


class plotter:
    def __init__(self, left=75, right=10, top=10, bottom=50, wspace=0.2, hspace=0.2, dpi=96):
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
        self.fig_base.set_dpi(dpi)
        self.fig_base.set_figwidth(9)
        self.fig_base.set_figheight(2.9)
        if config.style_dark:
            self.fig_base.set_facecolor('#343434')
        else:
            self.fig_base.set_facecolor('#EDEDED')
        self.fig = FigureCanvasQTAgg(self.fig_base)
        self.fig.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.fig.setMinimumSize(QtCore.QSize(100, 50))

        # Handling der Achsen
        self.ax1 = self.fig_base.add_subplot(1, 1, 1)
        if config.style_dark:
            self.ax1.set_facecolor('#343434')
        else:
            self.ax1.set_facecolor('#EDEDED')

        # Funktionszuweisung
        self.zeit = None
        self.signal = None
        self.subsinus = None

        # Initialisierung
        self.subsinus_visible = False
        self.first_update = True

    def update_complete(self):
        self.ax1.clear()

        self.ax1.plot(self.zeit, self.signal, color='#fc2403', lw=2, linestyle='-', label=r'Furierreihe')
        if len(self.subsinus) > 1 and self.subsinus_visible:
            for i in range(len(self.subsinus)):
                self.ax1.plot(self.zeit, self.subsinus[i].signal, color='#1bb2e0', lw=1, linestyle='--', label='Sinus ' + str(i))
        if config.style_dark:
            self.ax1.grid(color='white', alpha=0.25, ls=':', lw=0.5)
        else:
            self.ax1.grid(color='k', alpha=0.25, ls=':', lw=0.5)
        self.ax1.set_xlabel(r'Zeit [s]')
        self.ax1.set_ylabel(r'Spannung [V]')
        self.legend()
        # ymin = np.min(self.sinus.t)
        # ymax = np.max(self.sinus.t)
        # self.ax1.set_ylim(ymin, ymax)
        self.ax1.figure.canvas.draw_idle()
        self.ax1.figure.canvas.flush_events()
        self.subplots_adjust()

    def subplots_adjust(self):
        # Handling der Plotränder => Verknüpfung mit resizeEvent (main_window) nicht vergessen
        # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
        width, height = self.fig.get_width_height()
        self.fig_base.subplots_adjust(left= self.left / width,
                                      right=1.0 - self.right / width,
                                      bottom=self.bottom / height,
                                      top=1.0 - self.top / height,
                                      wspace=self.wspace,
                                      hspace=self.hspace)

    def legend(self):
        legend = self.ax1.legend(loc='upper center')
        if config.style_dark:
            frame = legend.get_frame()
            frame.set_facecolor('#343434')
            frame.set_edgecolor('#707070')
            frame.set_linewidth(1)
