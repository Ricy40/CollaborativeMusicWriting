
from enum import Enum


def make_print(print_info):
    print = {
        "system-layout" : {
          "system-margins" : {
            "left-margin" : print_info.find('.//left-margin').text,
            "right-margin" : print_info.find('.//right-margin').text
          },
          "top-system-distance" : print_info.find('.//top-system-distance').text
        },
        "staff-layout" : {
            "number" : print_info.find('.//staff-layout').attrib['number'],
            "staff-distance" : print_info.find('.//staff-distance').text
        },
    }
    return print


class Measure:
    def __init__(self, measure_number, print):
        self.measure_number = measure_number
        self.print = make_print(print)
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def get_print(self):
        return self.print

    def get_notes(self):
        return self.notes

    def get_measure_number(self):
        return self.measure_number

    def get_time_signature(self):
        return self.time_signature

    def __str__(self):
        return f"Measure {self.measure_number} - {self.time_signature}"


def parse_clef(clef_element):
    sign = clef_element.find('sign').text
    line = int(clef_element.find('line').text) if clef_element.find('line') is not None else None

    for clef in Clef:
        if clef.sign == sign and clef.line == line:
            return clef
    raise ValueError(f"Unknown clef: sign={sign}, line={line}")


class Attributes:
    def __init__(self, attributes):
        self.divisions = attributes.find('divisions').text
        self.key = attributes.find('fifths').text
        self.staves = attributes.find('staves').text
        self.clefs = []
        for clef in attributes.findall('clef'):
            self.clefs.append(parse_clef(clef))

    def get_divisions(self):
        return self.divisions

    def get_key(self):
        return self.key

    def get_staves(self):
        return self.staves

    def get_clefs(self):
        return self.clefs

    def __str__(self):
        return f"Attributes: {self.divisions} {self.key} {self.time} {self.beat_type}"


class Clef(Enum):
    TREBLE = ("G", 2)
    BASS = ("F", 4)
    ALTO = ("C", 3)
    TENOR = ("C", 4)
    PERCUSSION = ("percussion", None)
    TAB = ("TAB", None)
    SOPRANO = ("C", 1)
    MEZZO_SOPRANO = ("C", 2)
    BARITONE = ("C", 5)

    def __init__(self, sign, line):
        self.sign = sign
        self.line = line


# nice


class Direction:
    def __init__(self, direction):
        self.direction = direction