

class Note:
    def __init__(self, pitch, duration, accidental, articulation, dynamics):
        self.pitch = pitch
        self.duration = duration
        self.accidental = accidental
        self.articulation = articulation
        self.dynamics = dynamics

    def get_pitch(self):
        return self.pitch

    def get_duration(self):
        return self.duration

    def get_accidental(self):
        return self.accidental

    def get_articulation(self):
        return self.articulation

    def get_dynamics(self):
        return self.dynamics

    def __str__(self):
        return f"Note: {self.pitch} ({self.duration}, {self.accidental}, {self.articulation}, {self.dynamics})"

# ordinary linear merge
#