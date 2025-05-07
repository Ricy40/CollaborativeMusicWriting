

class MidiInstrument:
    def __init__(self, id, channel, program, volume, pan):
        self.id = id
        self.channel = channel
        self.program = program
        self.volume = volume
        self.pan = pan

    def __str__(self):
        return self.name