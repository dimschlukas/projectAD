import math as m
import cmath as cm
from ctypes import *
from lib.WaveFormsSDK.dwfconstants import *
import sys
import numpy as np
import copy
import time





class AnalogDiscovery:
    def __init__(self, channel=0):
        self.dwf = cdll.dwf
        self.hdwf = c_int()
        self.channel = c_int(channel)

    def open(self):
        # check for available devices and print
        cdevices = c_int()
        self.serialnumber = create_string_buffer(64)
        self.dwf.FDwfEnum(c_int(0), byref(cdevices))
        self.dwf.FDwfEnumSN(c_int(0), self.serialnumber)
        print("Number of Devices: " + str(cdevices.value))

        self.dwf.FDwfDeviceOpen(c_int(0), byref(self.hdwf))

        if cdevices.value == 0:
            print("no device available")
            error = 'Verbindung zum Analog Discovery fehlgeschlagen.'
            return error
        if self.hdwf.value == hdwfNone.value:
            print("failed to open device")
            error = 'Analog Discovery wird von einem anderem Prozess verwendet.'
            return error

    def close(self):
        self.dwf.FDwfAnalogOutReset(self.hdwf, self.channel)
        self.dwf.FDwfDeviceCloseAll()
        print('finished')

    def create_custom_waveform(self, signal, t_sp, n_sp=2**12):
        signal = signal * 0.2 # skalierung für AD2
        self.n_sp = n_sp
        rgdSamples = (c_double * n_sp)()
        self.f_sp = 1/t_sp
        # samples to c_double
        for i in range(0, n_sp, 1):
            rgdSamples[i] = c_double(signal[i])
        print("Generating custom waveform...")
        self.dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, self.channel, AnalogOutNodeCarrier, c_bool(True))
        self.dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, self.channel, AnalogOutNodeCarrier, funcCustom)
        self.dwf.FDwfAnalogOutNodeDataSet(self.hdwf, self.channel, AnalogOutNodeCarrier, rgdSamples, c_int(self.n_sp))
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, self.channel, AnalogOutNodeCarrier, c_double(self.f_sp))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, self.channel, AnalogOutNodeCarrier, c_double(5.0))
        self.dwf.FDwfAnalogOutRunSet(self.hdwf, self.channel, c_double(t_sp))  # run for 1 periods
        self.dwf.FDwfAnalogOutWaitSet(self.hdwf, self.channel, c_double(0.0))  # wait 0.0 s
        self.dwf.FDwfAnalogOutRepeatSet(self.hdwf, self.channel, c_int(500))  # repeat x times
        # dwf.FDwfAnalogOutConfigure(hdwf, channel, c_bool(True))  # starte Signalgenerator

    def collect_data(self):
        sampling_rate = self.f_sp * self.n_sp
        print('Einlesen der Analogsignale')
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, c_double(sampling_rate))
        # print("Set range for all channels")
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(-1), c_double(10.0))
        self.dwf.FDwfAnalogInBufferSizeSet(self.hdwf, c_int(self.n_sp))

        # print("Wait after first device opening the analog in offset to stabilize")
        # time.sleep(0.5)
        print("Starting acquisition")
        self.dwf.FDwfAnalogOutConfigure(self.hdwf, self.channel, c_bool(True))  # starte Signalgenerator
        self.dwf.FDwfAnalogInConfigure(self.hdwf, c_int(1), c_int(1))

        print("waiting to finish")
        sts = c_int()
        while True:
            self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(sts))
            if sts.value == DwfStateDone.value:
                break
            time.sleep(0.1)

    def read_data(self):
        # Daten aus Oszilloskop auslesen
        rg1 = (c_double * self.n_sp)()
        self.dwf.FDwfAnalogInStatusData(self.hdwf, c_int(0), rg1, len(rg1))  # get channel 1 data
        rg2 = (c_double * self.n_sp)()
        self.dwf.FDwfAnalogInStatusData(self.hdwf, c_int(1), rg2, len(rg2))  # get channel 2 data

        self.dwf.FDwfDeviceCloseAll()

        ch1 = [0.0] * len(rg1)  # Initialisieren
        ch2 = [0.0] * len(rg2)
        for i in range(0, len(ch1)):
            ch1[i] = rg1[i]
            ch2[i] = rg2[i]

        return ch1, ch2




if __name__=='__main__':
    from lib.sinusgenerator import Sinusgen
    import matplotlib.pyplot as plt

    f = [1000,50]
    p = [0,0]
    a = [1,2]
    sinusgen = Sinusgen(f, a, p, asp=1)
    zeit, sin, subsinus = sinusgen.calc()

    # SN: 210321A29BB7
    ad = AnalogDiscovery()
    ad.open()
    ad.create_custom_waveform(sin, zeit[-1])
    ad.collect_data()
    ch1, ch2, = ad.read_data()
    ad.close()

    fig, ax1 = plt.subplots(figsize=(25 / 2.54, 25 / 5))
    ax1.set_title('A2 Signal')
    ax1.set_xlabel('Zeit [s]')
    ax1.set_ylabel('Spannung [V]')
    ax1.plot(zeit, sin, 'r-', linewidth=1, label='Signal')
    ax1.plot(zeit, ch1, 'r--', linewidth=1, label='Signal')
    ax1.plot(zeit, ch2, 'b--', linewidth=1, label='Signal')
    if len(subsinus) > 1:
        for i in range(len(subsinus)):
            ax1.plot(zeit, subsinus[i].signal, 'b-', linewidth=0.5, label='Sinus ' + str(i))
    ax1.grid(which='both', color='k', alpha=0.75, ls='-', lw=0.5)
    # plt.savefig('A1_Synthetisches_Signal.png', dpi=200)
    plt.show()