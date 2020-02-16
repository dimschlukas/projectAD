import csv

import numpy as np


class CsvReadWrite():
    """
    ToDo: Allgmeingültiger ausprogrammieren.
    Die Umsetzung zeigt das Konzept ohne Anspruch auf Vollständigkeit
    """

    def __init__(self, url_read='', url_write='', delimiter_read=',', delimiter_write=','):
        self.url_read = url_read
        self.url_write = url_write
        self.delimiter_read = delimiter_read
        self.delimiter_write = delimiter_write
        self.header = None
        self.data = None
        self.data_np = None

    def read(self, header_included=True, convert_to_numpy=True, transpose=True):
        f = open(self.url_read, 'r')
        reader = csv.reader(f, delimiter=self.delimiter_read)
        self.header = []
        self.data = []
        line_count = 1
        for row in reader:
            row_list = []
            for col in row:
                if (line_count == 1) and header_included:
                    self.header.append(col)
                else:
                    row_list.append(float(col))
            if line_count > 1:
                self.data.append(row_list)
            line_count += 1
        f.close()

        if convert_to_numpy:
            self.data_np = np.array(self.data)
            if transpose:
                self.data_np = self.data_np.transpose()

    def write(self, header_included=True):
        csv.register_dialect('my_dialect',
                             delimiter=self.delimiter_write,
                             quoting=csv.QUOTE_NONE,
                             skipinitialspace=True,
                             lineterminator='\n')

        f = open(self.url_write, 'w')
        writer = csv.writer(f, dialect='my_dialect')

        if header_included:
            # Header 1. Zeile
            row = [self.header[i]
                   for i in range(0, np.shape(self.header)[0], 1)]
            writer.writerow(row)

        for i in range(0, np.shape(self.data_np)[1]):
            row = ['{:1.3f}'.format(self.data_np[n, i])
                   for n in range(0, np.shape(self.data_np)[0], 1)]
            writer.writerow(row)

        f.close()

    def print_data_info(self):
        print('---------------------------------')
        print('Anzahl Spalten:', len(self.data))
        print('Anzahl Zeilen:', len(self.data[0]))
        print('---------------------------------')
        print('header', self.header)
        print('---------------------------------')


if __name__ == '__main__':
    csv_rw = CsvReadWrite('Loggerdaten_Demo_1.csv', 'Loggerdaten_Demo_1_write_Uebung_2.csv')
    csv_rw.read()
    csv_rw.print_data_info()
    csv_rw.write()
