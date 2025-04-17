class FaderData:
    def __init__(self, name):
        self.name = name
        self.data = None
        self.midiNote__ = int(name)

    def setMidiNote(self,x):
        self.midiNote__ = x