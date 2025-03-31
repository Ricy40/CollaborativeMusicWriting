

class Instrument:
    def __init__(self, id, name, sound, ):
        self.id = id
        self.name = name
        self.sound = sound

    def __str__(self):
        return self.name