from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QHBoxLayout


class FaderMenu(QWidget):
    def __init__(self, faderNumber, mainWindow):
        super().__init__()

        self.faderNumber = faderNumber
        self.mainWindow = mainWindow

        self.setWindowTitle("Settings Fader: " + str(faderNumber))
        self.setMinimumWidth(300)
        self.setMinimumHeight(150)

        self.midiNoteUserInput = mainWindow.faderList[self.faderNumber].midiNote

        layout = QVBoxLayout()

        self.l1 = QLabel("Select Midi Note")
        layout.addWidget(self.l1)

        self.selectMidiNote = QSpinBox()
        self.selectMidiNote.setValue(self.midiNoteUserInput)
        self.selectMidiNote.setMinimum(0)
        self.selectMidiNote.setMaximum(127)
        self.selectMidiNote.valueChanged.connect(self.selectMidiNoteChanged)
        layout.addWidget(self.selectMidiNote)

        layout2 = QHBoxLayout()

        self.applyButton = QPushButton("Apply")
        self.applyButton.clicked.connect(self.applyButtonClicked)
        layout2.addWidget(self.applyButton)

        self.saveButton = QPushButton("Save")
        self.saveButton.clicked.connect(self.saveButtonClicked)
        layout2.addWidget(self.saveButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.closeButtonClicked)
        layout2.addWidget(self.closeButton)

        self.controlElements = QWidget()
        self.controlElements.setLayout(layout2)

        layout.addWidget(self.controlElements)

        self.setLayout(layout)

    def selectMidiNoteChanged(self, i):
        self.midiNoteUserInput = i

    def applyButtonClicked(self):
        self.saveSettings()
        self.close()

    def saveButtonClicked(self):
        self.saveSettings()

    def closeButtonClicked(self):
        self.close()

    def saveSettings(self):
        print(self.midiNoteUserInput)
        self.mainWindow.faderList[self.faderNumber].midiNote = self.midiNoteUserInput
