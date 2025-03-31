

class Chord:
    def __init__(self, notes):
        self.notes = notes

    def get_notes(self):
        return self.notes

    def __str__(self):
        return f"Chord: {self.notes}"