

class Clef:
    def __init__(self, sign, line):
        self.sign = sign
        self.line = line

    def __str__(self):
        return f'Clef: {self.sign} on line {self.line}'