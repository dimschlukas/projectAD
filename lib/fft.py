import numpy as np
from scipy import interpolate
from scipy import signal
from scipy.fftpack import fft
import matplotlib.pyplot as plt
from lib.csv_read_write import CsvReadWrite

class Fft:
    def __init__(self, __x, __y, fenstermethode=None, interpolatemethode=None, fmax=None):
        self.__x = __x
        self.__y = __y
        self.fenstermethode = fenstermethode
        self.interpolatemethode = interpolatemethode
        self.__fmax = fmax


    def calc(self):
        if self.interpolatemethode != None:
            self.x_neu, self.y_interpoliert, self.anzahl_neue_stellen = self.stuetzstellen_anpassung(self.__x, self.__y, self.interpolatemethode)
        else:
            self.x_neu = self.__x
            self.y_interpoliert = self.__y
            self.anzahl_neue_stellen = len(self.__x)
        self.delta_zeit = self.x_neu[1] - self.x_neu[0]
        self.phase = self.x_neu[0] - self.x_neu[-1]
        if self.fenstermethode != None:
            self.y_windowed = self.fensterfunktion(self.y_interpoliert, self.fenstermethode)
        else:
            self.y_windowed = self.y_interpoliert
        self.fft_freq, self.fft_spect = self.frequenzspektrum(self.y_windowed, self.delta_zeit, self.anzahl_neue_stellen, self.__fmax)

        return self.x_neu, self.y_windowed, self.fft_freq, self.fft_spect


    def stuetzstellen_anpassung(self, x, y, methode='linear'):
        anzahl_neue_stellen = 2**np.ceil(np.log2(len(y)))
        f = interpolate.interp1d(x, y, kind=methode, )
        x_neu = np.linspace(x[0], x[-1], anzahl_neue_stellen)
        y_interpoliert = f(x_neu)

        return x_neu, y_interpoliert, anzahl_neue_stellen


    def fensterfunktion(self, y_interpoliert, methode=None):
        offset = np.average(y_interpoliert)
        y_offset = np.subtract(y_interpoliert, offset)

        if methode == 'hamming':
            fenster = np.hamming(len(y_offset))
        elif methode == 'hanning':
            fenster = np.hanning(len(y_offset))
        elif methode == 'blackman':
            fenster = np.blackman(len(y_offset))
        elif methode == 'tukey':
            fenster = signal.tukey(len(y_offset))
        else:
            print('Ungültiges Fenster')
            fenster = None

        y_fenst = np.multiply(y_offset, fenster)
        y_windowed = np.add(y_fenst, offset)

        return y_windowed


    def frequenzspektrum(self, y_windowed, delta_zeit, anzahl_neue_stellen, fmax=None):
        fft_spect_total = np.abs(fft(y_windowed)) * 2 / anzahl_neue_stellen
        fft_spect_total[0] = fft_spect_total[0] / 2

        fft_freq_total = np.linspace(0, 1 / delta_zeit, anzahl_neue_stellen)

        if fmax is not None:
            frequenz = (1/delta_zeit)/2
            __fmax = ((self.anzahl_neue_stellen / 2)*fmax)/frequenz


            if __fmax > (self.anzahl_neue_stellen / 2):
                print('Eingegebene Frequenz zu hoch')
                __fmax = self.anzahl_neue_stellen /2
            fft_freq = fft_freq_total[0:int(np.ceil(__fmax))]
            fft_spect = fft_spect_total[0:int(np.ceil(__fmax))]
        else:
            __fmax = self.anzahl_neue_stellen / 2
            for i in range(int(__fmax)):
                if fft_spect_total[i] > 0.01:
                    latest = i
            if latest == None:
                print('Amplituden < 0.01')
                fft_freq = fft_freq_total[0:int(np.ceil(__fmax))]
                fft_spect = fft_spect_total[0:int(np.ceil(__fmax))]
            else:
                fft_freq = fft_freq_total[0:latest+latest+10]
                fft_spect = fft_spect_total[0:latest+latest+10]

        return fft_freq, fft_spect


    def plot(self):
        fig, (ax1, ax2) = plt.subplots(2)
        ax1.set_title('Signal')
        ax1.set_xlabel('Zeit')
        ax1.set_ylabel('Signal')
        ax1.plot(self.__x, self.__y, 'b', label='Zeitsignal Original')
        if self.fenstermethode != None:
            ax1.plot(self.x_neu, self.y_windowed, 'r', label='tukey Zeitsignal vorkonditioniert')
        ax1.legend()
        ax1.grid(which='both', color='k', alpha=0.75, ls='-', lw=0.5)

        ax2.set_title('Frequenzspektrum')
        ax2.set_xlabel('Frequenz')
        ax2.set_ylabel('Amplitude')
        ax2.plot(self.fft_freq, self.fft_spect, 'r.--', label='Frequenzspektrum')
        ax2.legend()
        ax2.grid(which='both', color='k', alpha=0.75, ls='-', lw=0.5)

        plt.subplots_adjust(hspace=0.5)
        plt.savefig('plot.png', dpi=200)
        plt.show()


    def csv_export(self):
        c = CsvReadWrite(url_write='Ausgabe.csv')
        c.header = ['t [s]', 'y (resampled)', 'y (windowed)', 'f [Hz]', 'Amplitude']
        data = self.x_neu, self.y_interpoliert, self.y_windowed, self.fft_freq, self.fft_spect
        print(len(data[0]))
        print(len(data[1]))
        print(len(data[2]))
        print(len(data[3]))
        print(len(data[4]))
        # c.data_np = np.array(data)
        # c.data_np[0] = self.x_neu
        # c.data[1] = self.y_interpoliert
        # c.data[2] = self.y_windowed
        # c.data[3] = self.fft_freq
        # c.data[4] = self.fft_spect
        # c.write(header_included=True)


if __name__=='__main__':
    from lib.sinusgenerator import Sinusgen
    from lib.ad import AnalogDiscovery

    f = [1000, 50]
    p = [0, 0]
    a = [1, 2]
    sinusgen = Sinusgen(f, a, p, asp=1)
    zeit, sin, subsinus = sinusgen.calc()

    # SN: 210321A29BB7
    ad = AnalogDiscovery()
    ad.open()
    ad.create_custom_waveform(sin, zeit[-1])
    ad.collect_data()
    ch1, ch2, = ad.read_data()
    ad.close()

    test = Fft(zeit, ch2, fenstermethode=None, interpolatemethode='linear', fmax=200)
    test.calc()
    test.plot()
    # test.csv_export()

