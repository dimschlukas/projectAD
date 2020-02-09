import numpy as np


class SignalBase():
    """
    Basisklasse mit den Gemeinsamkeiten der Signale.
    """

    def __init__(self, f=100,
                       n_sp = 2**12,
                       amplitude=1.0,
                       n=2.0,
                       phase=0.0,
                       offset=0.0):

        self.f = f  # Signalfrequenz
        self.n_sp = n_sp  # Anzahl Sampling Points

        self.amplitude = amplitude  # Amplitude des Signals
        self.n = n  # Anzahl Perioden in der betrachteten Zeitspanne t_sp
        self.t_sp = 1/f * n  # s Betrachtete Zeitspanne
        self.phase = phase  # Phasenverschiebung (im Bogenmass)
        self.offset = offset  # Offset des Signals

        self.sp = None  # NumPy Array der Grösse n_sp
        self.dt_sp = None  # s Zeit zwischen zwei Sampling Points
        self.t = None  # Zeitvektor
        self.wt = None  # Produkt aus Kreisfrequenz, Anzahl Perioden und Zeitvektor
        self.sampling_rate = None  # Taktrate bei der Ausgabe auf einem Signalgenerator

        self.signal = np.zeros(n_sp)  # Signalvektor

    def calc(self):
        self.sp = np.arange(0, self.n_sp, 1)  # NumPy Array der Grösse n_sp
        self.dt_sp = self.t_sp / (self.n_sp - 1)  # s Zeit zwischen zwei Sampling Points
        self.t = self.dt_sp * self.sp  # Zeitvektor
        self.wt = 2 * np.pi * self.f * self.t  # Produkt aus Kreisfrequenz, Anzahl Perioden und Zeitvektor
        self.sampling_rate = self.n_sp / self.t_sp  # Taktrate bei der Ausgabe auf einem Signalgenerator


class Sinus(SignalBase):
    def __init__(self, f=100,
                       n_sp=2**12,
                       amplitude=1.0,
                       n=2.0,
                       phase=0.0,
                       offset=0.0):

        super().__init__(f, n_sp, amplitude, n, phase, offset)
        self.calc()

    def calc(self):
        super().calc()
        self.signal = self.amplitude * np.sin(self.wt + self.phase) + self.offset


class Cosinus(SignalBase):
    def __init__(self, f=100,
                       n_sp=2**12,
                       amplitude=1.0,
                       n=2.0,
                       phase=0.0,
                       offset=0.0):

        super().__init__(f, n_sp, amplitude, n, phase, offset)
        self.calc()

    def calc(self):
        super().calc()
        self.signal = self.amplitude * np.cos(self.wt + self.phase) + self.offset


class Square(SignalBase):
    def __init__(self, f=100,
                       n_sp=2**12,
                       amplitude=1.0,
                       n=2.0,
                       phase=0.0,
                       offset=0.0):

        super().__init__(f, n_sp, amplitude, n, phase, offset)
        self.calc()

    def calc(self):
        super().calc()
        sin_sp = self.amplitude * np.sin(self.wt + self.phase)
        for i in range(0, self.n_sp, 1):
            if sin_sp[i] >= 0.0:
                self.signal[i] = self.amplitude + self.offset
            else:
                self.signal[i] = (-1) * self.amplitude + self.offset


class Triangle(SignalBase):
    def __init__(self, f=100,
                       n_sp=2**12,
                       amplitude=1.0,
                       n=2.0,
                       phase=0.0,
                       offset=0.0):

        super().__init__(f, n_sp, amplitude, n, phase, offset)
        self.calc()

    def calc(self):
        super().calc()
        sin_sp = 1 * np.sin(self.wt + self.phase)
        arcsin = np.arcsin(sin_sp) * 2 / np.pi
        self.signal = arcsin * self.amplitude + self.offset


class PWM(SignalBase):
    def __init__(self, f=100,
                       n_sp=2**12,
                       amplitude=1.0,
                       n=2.0,
                       phase=0.0,
                       offset=0.0,
                       duty_cycle=0.75):

        super().__init__(f, n_sp, amplitude, n, phase, offset)
        self.duty_cycle = duty_cycle
        self.calc()

    def calc(self):
        super().calc()
        sin_sp = 1 * np.sin(self.wt + self.phase)
        triangle_sp = 1 * np.arcsin(sin_sp) / np.pi + 0.5
        for i in range(0, self.n_sp, 1):
            if triangle_sp[i] < self.duty_cycle:
                self.signal[i] = self.amplitude + self.offset
            else:
                self.signal[i] = 0.0 + self.offset


if __name__ == '__main__':
    from plot_oop_signal import PlotSignal
    import numpy as np

    signaltest = Sinus(f=10, n=1, phase=(0*np.pi/180.0))

    plot_signal = PlotSignal(width=5, height=2, dpi=140)
    plot_signal.plot(x=signaltest.t, y=signaltest.signal)
