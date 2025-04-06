import sys
import time
import traceback

from PyQt6.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThreadPool

import serialInput

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QRadioButton, QLabel, QVBoxLayout, QWidget

from PythonSoftware.SerialToMidi.multithreading import Worker


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.layout = QVBoxLayout()

        self.toggle = QRadioButton("Start Encoding")
        self.toggle.setCheckable(True)
        self.toggle.clicked.connect(self.the_button_was_toggled)
        self.layout.addWidget(self.toggle)

        self.dataFromFader = QLabel("Input")
        self.layout.addWidget(self.dataFromFader)

        self.button = QPushButton()
        self.layout.addWidget(self.button)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.show()

        self.threadpool = QThreadPool()
        thread_count = self.threadpool.maxThreadCount()
        print(f"Multithreading with maximum {thread_count} threads")

    # wenn der button gedrückt wird
    def the_button_was_toggled(self, checked):
        print("Checked?", checked)
        running = True

        if checked:
            ser = serialInput.setup()
            # Pass the function to execute
            worker = Worker(self.running_function, ser,running)  # Any other args, kwargs are passed to the run function
            worker.signals.finished.connect(self.thread_complete)
            worker.signals.progress.connect(self.progress_fn)
            # Execute
            self.threadpool.start(worker)
        else:
            running = False
            self.dataFromFader.setText("---")

    #Die Funktion die aufgeführt wird
    def running_function(self, ser,running, progress_callback):
        while running:
            time.sleep(1)
            print(running)
            line = str(serialInput.getLine(ser))
            progress_callback.emit(line)

    #Verbindung zu Signals für das GUI
    def progress_fn(self, n):
        self.dataFromFader.setText(str(n))

    def thread_complete(self):
        print("THREAD COMPLETE!")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
