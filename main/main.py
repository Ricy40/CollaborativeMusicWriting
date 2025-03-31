from music21 import converter


# Parse the MusicXML files
score1 = 'testfiles/testscore.musicxml'
score2 = 'testfiles/testscore2.musicxml'

import xml.etree.ElementTree as ET

def parse_musicxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

class Note:
    def __init__(self, pitch, duration, voice):
        self.pitch = pitch
        self.duration = duration
        self.voice = voice


class Measure:
    def __init__(self, number):
        self.number = number
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)


class Part:
    def __init__(self, id):
        self.id = id
        self.measures = []

    def add_measure(self, measure):
        self.measures.append(measure)


def parse_musicxml_to_objects(file_path):
    root = parse_musicxml(file_path)
    part = Part(root.find('.//part').attrib['id'])

    for measure in root.findall('.//measure'):
        measure_obj = Measure(measure.attrib['number'])

        for note in measure.findall('.//note'):
            pitch = note.find('pitch')
            if pitch is not None:
                step = pitch.find('step').text
                octave = pitch.find('octave').text
                pitch_str = f"{step}{octave}"
            else:
                pitch_str = None  # Handle rests or other cases

            duration = note.find('duration').text
            voice = note.find('voice').text if note.find('voice') is not None else '1'

            note_obj = Note(pitch_str, duration, voice)
            measure_obj.add_note(note_obj)

        part.add_measure(measure_obj)

    return part

def compare_parts(part1, part2):
    differences = []

    for measure1, measure2 in zip(part1.measures, part2.measures):
        if measure1.number != measure2.number:
            differences.append(f"Measure number mismatch: {measure1.number} vs {measure2.number}")
            continue

        for note1, note2 in zip(measure1.notes, measure2.notes):
            if note1.pitch != note2.pitch or note1.duration != note2.duration or note1.voice != note2.voice:
                differences.append(
                    f"Difference in measure {measure1.number}: {note1.pitch}/{note1.duration}/{note1.voice} vs {note2.pitch}/{note2.duration}/{note2.voice}")

    return differences


# Example usage
part1 = parse_musicxml_to_objects(score1)
part2 = parse_musicxml_to_objects(score2)
differences = compare_parts(part1, part2)
for diff in differences:
    print(diff)