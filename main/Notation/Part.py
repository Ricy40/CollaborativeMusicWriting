

class Part:
    def __init__(self, id, name, abbreviation, time_signature, key_signature, midi_device, midi_instrument):
        self.id = id
        self.name = name
        self.abbreviation = abbreviation
        self.midi_device = midi_device
        self.midi_instrument = midi_instrument
        self.measures = []

    def add_bar(self, bar):
        self.measures.append(bar)

    def get_measures(self):
        return self.measures

    def __str__(self):
        return f'Part: {self.name} Voice: {self.voice} staff: {len(self.staff)}'