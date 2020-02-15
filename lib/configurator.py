import configparser

class Configurator:
    def __init__(self, filename='config.ini'):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def initialize_config(self):
        self.config['GUI-DEFAULTS'] = {'Dark_mode': 'True'}
        self.config['SINUSGEN-DEFAULTS'] = {'offset': '1.00',
                                       'periods': '1',
                                       'factor': '1.00',
                                       'samples': '4096',
                                       'frequency': '1.00',
                                       'amplitude': '1.00',
                                       'phase': '0.00'}

        with open(self.filename, 'w') as file:
            self.config.write(file)

    def load(self):
        self.config.read(self.filename)
        self.dark_mode = self.config['GUI-DEFAULTS']['dark_mode']
        self.offset = self.config['SINUSGEN-DEFAULTS']['offset']
        self.periods = self.config['SINUSGEN-DEFAULTS']['periods']
        self.factor = self.config['SINUSGEN-DEFAULTS']['factor']
        self.samples = self.config['SINUSGEN-DEFAULTS']['samples']
        self.frequency = self.config['SINUSGEN-DEFAULTS']['frequency']
        self.amplitude = self.config['SINUSGEN-DEFAULTS']['amplitude']
        self.phase = self.config['SINUSGEN-DEFAULTS']['phase']

    def save(self):
        self.config['SINUSGEN-DEFAULTS']['offset'] = self.offset
        self.config['SINUSGEN-DEFAULTS']['periods'] = self.periods
        self.config['SINUSGEN-DEFAULTS']['factor'] = self.factor
        self.config['SINUSGEN-DEFAULTS']['samples'] = self.samples
        self.config['SINUSGEN-DEFAULTS']['frequency'] = self.frequency
        self.config['SINUSGEN-DEFAULTS']['amplitude'] = self.amplitude
        self.config['SINUSGEN-DEFAULTS']['phase'] = self.phase


if __name__=='__main__':
    config = Configurator('config.ini')
    # config.initialize_config()
    config.load()
    print(config.dark_mode)