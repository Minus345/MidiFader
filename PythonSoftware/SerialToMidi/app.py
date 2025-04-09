import sys
from tokenize import String

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool
import serialInput
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QRadioButton, QLabel, QVBoxLayout, QWidget, \
    QButtonGroup
from PythonSoftware.SerialToMidi.multithreading import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.setWindowTitle("My App")

        self.layout = QVBoxLayout()

        self.toggle = QPushButton("Start Encoding")
        self.toggle.clicked.connect(self.the_button_was_toggled)
        self.layout.addWidget(self.toggle)

        self.button = QPushButton("Stop")
        self.button.clicked.connect(self.buttonPress)
        self.layout.addWidget(self.button)

        self.dataFromFader = QLabel("Input")
        self.layout.addWidget(self.dataFromFader)


        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()

        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")
        
    def the_button_was_toggled(self):
        self.worker = Worker(serialInput.setup())
        self.worker.signals.finished.connect(self.thread_complete)
        self.worker.signals.progress.connect(self.progress_fn)
        self.threadpool.start(self.worker)

    def buttonPress(self):
        self.worker.kill()

    #Verbindung zu Signals für das GUI
    def progress_fn(self, n):
        n = n.replace("b'","")
        n = n.replace("\\r\\n'","")
        self.dataFromFader.setText(str(n))

    def thread_complete(self):
        print("THREAD COMPLETE!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
