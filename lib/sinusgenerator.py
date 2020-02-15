from lib.base_signals import Sinus
import numpy as np

class Sinusgen:
    def __init__(self, frequencies, amplitudes, phases, n_sp=2**12, asp=4.0, offset=0.0, factor=1.0):
        self.frequencies = frequencies  # Array of frequencies
        self.amplitudes = amplitudes  # Array of amplitudes
        self.phases = phases # Array of Phases
        self.n_sp = n_sp
        self.asp = asp
        self.offset = offset
        self.factor = factor


    def calc(self):
        self.n = []
        for i in range(len(self.frequencies)):
            self.n.append(self.frequencies[i] / np.amin(self.frequencies) * self.asp)
        sinus = []
        for i in range(len(self.frequencies)):
            sinus.append(Sinus(f=self.frequencies[i],
                       n_sp=self.n_sp,
                       amplitude=self.amplitudes[i],
                       n=self.n[i],
                       phase=(self.phases[i] * np.pi / 180.0),
                       offset=self.offset))
        signal = np.zeros(self.n_sp)
        for i in range(len(sinus)):
            signal = signal + sinus[i].signal
        signal = self.factor * signal
        time = sinus[0].t

        return time, signal, sinus


if __name__=='__main__':
    import matplotlib.pyplot as plt
    f = [50,200,500,1000]
    p = [0,0,0,0]
    a = [325,70,40,25]

    # f = np.flip(f)
    # p = np.flip(p)
    # a = np.flip(a)


    sinusgen = Sinusgen(f,a,p)
    zeit, signal, subsinus = sinusgen.calc()

    fig, ax1 = plt.subplots(figsize=(25 / 2.54, 25 / 5))
    ax1.set_title('A2 Signal')
    ax1.set_xlabel('Zeit [s]')
    ax1.set_ylabel('Spannung [V]')
    ax1.plot(zeit, signal, 'r-', linewidth=1, label='Signal')
    if len(subsinus) > 1:
        for i in range(len(subsinus)):
            ax1.plot(zeit, subsinus[i].signal, 'b--', linewidth=0.5, label='Sinus ' + str(i))
    ax1.grid(which='both', color='k', alpha=0.75, ls='-', lw=0.5)
    # plt.savefig('A1_Synthetisches_Signal.png', dpi=200)
    plt.show()