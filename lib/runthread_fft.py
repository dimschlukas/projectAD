from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox
from lib.ad import AnalogDiscovery
from lib.fft import Fft
from lib.runthread_progressbar import RunThread_Progressbar


class RunThread_fft(QThread):  # http://doc.qt.io/qt-5/qthread.html
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main = parent
        self.run_progressbar_thread = RunThread_Progressbar(self, parent=self.main)

    def run(self):
        if self.main.simulation:
            fft_ch1 = Fft(self.main.zeit, self.main.signal, fenstermethode=None, interpolatemethode=None, fmax=None)
            self.main.x_ch1, self.main.y_ch1, self.main.freq_ch1, self.main.spec_ch1 = fft_ch1.calc()

            self.main.fft_matplot.plot.ch2 = False
            self.main.ui.cb_fft_ch2.setChecked(False)

            # Channel 1
            self.main.fft_matplot.plot.x_ch1 = self.main.x_ch1
            self.main.fft_matplot.plot.y_ch1 = self.main.y_ch1
            self.main.fft_matplot.plot.fft_freq_ch1 = self.main.freq_ch1
            self.main.fft_matplot.plot.fft_spect_ch1 = self.main.spec_ch1
            self.main.fft_matplot.plot.update_complete()

            self.main.ui.hs_fft_slider.setSingleStep(10)
            self.main.ui.hs_fft_slider.setMaximum(self.main.freq_ch1[-1])
            self.main.ui.hs_fft_slider.setValue(self.main.freq_ch1[-1])

        else:
            self.main.ui.bn_start_measure.setEnabled(False)
            self.ad = AnalogDiscovery()
            self.error = self.ad.open()
            self.run_progressbar_thread.start_thread()
            if self.error != None:
                print(self.error)
                QMessageBox.about(self.main, 'ERROR: Analog Discovery 2', self.error)
            else:
                self.ad.create_custom_waveform(self.main.signal, self.main.zeit[-1], self.main.samples)
                self.ad.collect_data()
                ch1, ch2, = self.ad.read_data()
                fft_ch1 = Fft(self.main.zeit, ch1, fenstermethode=None, interpolatemethode=None, fmax=None)
                fft_ch2 = Fft(self.main.zeit, ch2, fenstermethode=None, interpolatemethode=None, fmax=None)
                self.main.x_ch1, self.main.y_ch1, self.main.freq_ch1, self.main.spec_ch1 = fft_ch1.calc()
                self.main.x_ch2, self.main.y_ch2, self.main.freq_ch2, self.main.spec_ch2 = fft_ch2.calc()

                # Channel 1
                self.main.fft_matplot.plot.x_ch1 = self.main.x_ch1
                self.main.fft_matplot.plot.y_ch1 = self.main.y_ch1
                self.main.fft_matplot.plot.fft_freq_ch1 = self.main.freq_ch1
                self.main.fft_matplot.plot.fft_spect_ch1 = self.main.spec_ch1
                # Channel 2
                self.main.fft_matplot.plot.x_ch2 = self.main.x_ch2
                self.main.fft_matplot.plot.y_ch2 = self.main.y_ch2
                self.main.fft_matplot.plot.fft_freq_ch2 = self.main.freq_ch2
                self.main.fft_matplot.plot.fft_spect_ch2 = self.main.spec_ch2

                self.main.fft_matplot.plot.update_complete()

                self.main.ui.hs_fft_slider.setSingleStep(10)
                self.main.ui.hs_fft_slider.setMaximum(self.main.freq_ch2[-1])
                self.main.ui.hs_fft_slider.setValue(self.main.freq_ch2[-1])
            self.ad.close()
        self.main.menu.save_fft_csv.setEnabled(True)
        self.main.menu.save_fft_plot.setEnabled(True)
        self.main.ui.bn_start_measure.setEnabled(True)

    def start_thread(self):
        print('starting thread...')
        self.start(QThread.NormalPriority)

    def stop(self):
        print('stopping thread...')
        self.terminate()
        self.run_progressbar_thread.stop()
        self.ad.close()
        self.main.menu.save_fft_csv.setEnabled(True)
        self.main.menu.save_fft_plot.setEnabled(True)
        self.main.ui.bn_start_measure.setEnabled(True)
