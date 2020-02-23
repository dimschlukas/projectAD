#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from configparser import ConfigParser


class Config():
    def __init__(self, file_path=None):
        if file_path is None:
            absolute_path = (os.path.dirname(os.path.abspath(__file__))).replace('\\', '/')
            self._file_path = absolute_path + '/config.ini'
        else:
            self._file_path = file_path

        self._config = ConfigParser()

        # [gui_defaults]
        self.style_dark = False

        # [sinusgen_defaults]
        self.offset = 1.00
        self.periods = 1
        self.factor = 1.00
        self.samples = 4096
        self.default_frequency = 1.00
        self.default_amplitude = 1.00
        self.default_phase = 0.00

        # [sinus]
        self.frequencies = 1.00
        self.amplitudes = 1.00
        self.phases = 0.00

        self.row_count = 0
        self._callback_functions_update = []

        self.read()

    def read(self):
        try:
            f = open(self._file_path, 'r')
            self._config.read_file(f)
            f.close()

            # [gui_defaults]
            self.style_dark = self._config.getboolean('gui_defaults', 'dark')

            # [sinusgen_defaults]
            self.offset = self._config.getfloat('sinusgen_defaults', 'offset')
            self.periods = self._config.getint('sinusgen_defaults', 'periods')
            self.factor = self._config.getfloat('sinusgen_defaults', 'factor')
            self.samples = self._config.getint('sinusgen_defaults', 'samples')
            self.default_frequency = self._config.getfloat('sinusgen_defaults', 'frequency')
            self.default_amplitude = self._config.getfloat('sinusgen_defaults', 'amplitude')
            self.default_phase = self._config.getfloat('sinusgen_defaults', 'phase')

            # [sinus]
            self.frequencies = []
            self.amplitudes = []
            self.phases = []
            self.row_count = len(self._config.options('sinus'))
            for i in range(self.row_count):
                data = self._config.get('sinus', str(i))
                data = data.split(',')
                self.frequencies.append(float(data[0]))
                self.amplitudes.append(float(data[1]))
                self.phases.append(float(data[2]))

        except Exception as e:
            print('Error _config read:', str(e))

        finally:
            f.close()
            return self.offset

    def write(self):
        try:
            f = open(self._file_path, 'w')

            # [gui_defaults]
            self._config.set('gui_defaults', 'dark', Config.bool_to_string(self.style_dark))

            # [sinusgen_defaults]
            # bei Configfiles lauten die boolschen Ausdrücke true und false (kleingeschrieben)
            # siehe www.pyformat.info für die Interpretation des Formatbefehles
            self._config.set('sinusgen_defaults', 'offset', '{:f}'.format(self.offset))
            self._config.set('sinusgen_defaults', 'periods', '{:d}'.format(self.periods))
            self._config.set('sinusgen_defaults', 'factor', '{:f}'.format(self.factor))
            self._config.set('sinusgen_defaults', 'samples', '{:d}'.format(self.samples))
            self._config.set('sinusgen_defaults', 'default_frequency', '{:f}'.format(self.default_frequency))
            self._config.set('sinusgen_defaults', 'default_amplitude', '{:f}'.format(self.default_amplitude))
            self._config.set('sinusgen_defaults', 'default_phase', '{:f}'.format(self.default_phase))

            # [sinus]
            self._config.remove_section('sinus')
            self._config.add_section('sinus')
            for i in range(self.row_count):
                self._config.set('sinus', str(i), '{:f},{:f},{:f}'.format(self.frequencies[i], self.amplitudes[i], self.phases[i]))

            self._config.write(f)

        except Exception as e:
            print('Error _config write:', str(e))

        finally:
            f.close()

    def callback_update(self):
        # print('config callback_update')
        for i in range(0, len(self._callback_functions_update), 1):
            self._callback_functions_update[i]()

    def register_callback_update(self, callback_function):
        # print('register_callback_update')
        self._callback_functions_update.append(callback_function)

    @staticmethod
    def bool_to_string(value):
        if value:
            string = 'true'
        else:
            string = 'false'
        return string


if __name__ == '__main__':
    config = Config()
    config.read()

    print('[gui_defaults]')
    print('dark =', config.style_dark)

    config.write()
