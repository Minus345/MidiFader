from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class FaderMenu(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, faderNumber):
        super().__init__()

        self.setWindowTitle("Settings Fader: " + str(faderNumber))
        self.setMinimumWidth(300)

        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
