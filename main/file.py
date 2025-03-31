
import xml.etree.ElementTree as ET
from music21 import *
from main.Notation.Measure import Measure
from main.Notation.Note import Note
from main.Notation.Part import Part
from main.Notation.Score import Score
from main.Notation.Instrument import Instrument
from main.Notation.MidiInstrument import MidiInstrument

# Parse the MusicXML files
score1 = 'testfiles/testscore.musicxml'
score2 = 'testfiles/testscore2.musicxml'

def parse_musicxml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root

def parse_musicxml_to_objects(file_path):
    root = parse_musicxml(file_path)

    score = Score()

    part_list = root.find('.//part-list')
    for score_part in part_list.findall('.//score-part'):
        part_id = score_part.attrib['id']
        part_name = score_part.find('part-name').text
        part_abbreviation = score_part.find('part-abbreviation').text
        ins = score_part.find('score-instrument')
        instrument = Instrument(
            ins.attrib['id'],
            ins.find('instrument-name').text,
            ins.find('instrument-sound').text)
        mid_ins = score_part.find('midi-instrument')
        midi_instrument = MidiInstrument(
            mid_ins.attrib['id'],
            mid_ins.find('midi-channel').text,
            mid_ins.find('midi-program').text,
            mid_ins.find('volume').text,
            mid_ins.find('pan').text)
        score.add_part(Part(part_id, part_name, part_abbreviation, instrument, midi_instrument))

    for score_part in root.findall('.//part'):
        part = score.get_part_by_id(score_part.attrib['id'])
        for measure in score_part.findall('.//measure'):



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

    return score