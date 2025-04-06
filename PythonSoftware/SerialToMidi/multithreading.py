import sys
import time
import traceback

from PyQt6.QtCore import (
    QObject,
    QRunnable,
    QThreadPool,
    QTimer,
    pyqtSignal,
    pyqtSlot,
)
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from PythonSoftware.SerialToMidi import serialInput


class WorkerSignals(QObject):
    """Signals from a running worker thread.

    finished
        No data

    progress

    """

    finished = pyqtSignal()
    progress = pyqtSignal(object)

class Worker(QRunnable):
    """Worker thread.

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread.
                     Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    """

    def __init__(self, ser):
        super().__init__()
        self.ser = ser
        self.signals = WorkerSignals()
        self.is_killed = False

    @pyqtSlot()
    def run(self):
         while True:
            #time.sleep(1)
            line = str(serialInput.getLine(self.ser))
            self.signals.progress.emit(line)

            if self.is_killed:
                serialInput.killSerial(self.ser)
                break

     #self.signals.finished.emit()

    def kill(self):
        print("killed")
        self.is_killed = True