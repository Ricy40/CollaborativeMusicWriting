

class TimeSignature:
    def __init__(self, beats, beat_type):
        self.beats = beats
        self.beat_type = beat_type

    def __str__(self):
        return f"{self.beats}/{self.beat_type}"
