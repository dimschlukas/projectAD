import time

from PyQt5.QtCore import QThread

class RunThread_Progressbar(QThread):  # http://doc.qt.io/qt-5/qthread.html

    def __init__(self, fft_thread, parent=None):
        super().__init__(parent)
        self.main = parent
        self.fft_thread = fft_thread
        # self.zeit = zeit
        # self.ui = ui
        # self.error = error

    def run(self):
        if self.fft_thread.error != None:
            self.main.ui.progressBar.setFormat('ERROR')
            self.main.ui.progressBar.setTextVisible(True)
        else:
            self.main.ui.progressBar.setTextVisible(False)
            for i in range(0, 101, 1):
                time.sleep(self.main.zeit[-1]/100)
                self.main.ui.progressBar.setValue(i)
                self.main.ui.progressBar.setFormat('Done')
            self.main.ui.progressBar.setTextVisible(True)

    def start_thread(self):
        print('starting thread...')
        self.start(QThread.NormalPriority)

    def stop(self):
        print('stopping thread...')
        self.terminate()
        self.main.ui.progressBar.setFormat('Stopped')
        self.main.ui.progressBar.setTextVisible(True)