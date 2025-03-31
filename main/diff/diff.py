from music21 import note, stream, chord, expressions
import copy

def compare_scores(score1, score2):
    differences = []

    for part1, part2 in zip(score1.parts, score2.parts):
        # Ensure both parts have the same number of measures
        measures1 = list(part1.getElementsByClass('Measure'))
        measures2 = list(part2.getElementsByClass('Measure'))

        if len(measures1) != len(measures2):
            raise ValueError("Parts have different numbers of measures!")

        # Compare each measure
        for measure1, measure2 in zip(measures1, measures2):
            measure_diff = {
                'part': part1.partName,
                'measure_number': measure1.number,
                'has_difference': False,
                'score1_measure': measure1,
                'score2_measure': measure2
            }

            # Check if notes differ
            if len(measure1.notes) != len(measure2.notes):
                measure_diff['has_difference'] = True
            else:
                for note1, note2 in zip(measure1.notes, measure2.notes):
                    if isinstance(note1, note.Note) and isinstance(note2, note.Note):
                        if note1.pitch != note2.pitch or note1.duration.quarterLength != note2.duration.quarterLength:
                            measure_diff['has_difference'] = True
                            break
                    elif isinstance(note1, chord.Chord) and isinstance(note2, chord.Chord):
                        if note1.pitches != note2.pitches or note1.duration.quarterLength != note2.duration.quarterLength:
                            measure_diff['has_difference'] = True
                            break

            # Check rests, clefs, time signatures, etc.
            if (measure1.timeSignature != measure2.timeSignature or
                    measure1.clef != measure2.clef):
                measure_diff['has_difference'] = True

            if measure_diff['has_difference']:
                differences.append(measure_diff)

    return differences

def merge_scores(score1, score2):
    merged_score = score1.clone()

    for part1, part2 in zip(merged_score.parts, score2.parts):
        for measure1, measure2 in zip(part1.getElementsByClass('Measure'), part2.getElementsByClass('Measure')):
            for n1, n2 in zip(measure1.notes, measure2.notes):
                if n1.nameWithOctave != n2.nameWithOctave or n1.duration.quarterLength != n2.duration.quarterLength:
                    n1.pitch = n2.pitch
                    n1.duration = n2.duration

    return merged_score


def add_highlighted_note(note_x):
    highlighted_note = copy.deepcopy(note_x)
    highlighted_note.expressions.append(expressions.TextExpression("color:red"))
    highlighted_note.style.color = 'red'
    return copy.deepcopy(highlighted_note)

def compare_measures(measure1, measure2):
    merged_measure = stream.Measure(number=measure1.number)

    # Ensure both measures have the same number of notes
    notes1 = list(measure1.notes)
    notes2 = list(measure2.notes)
    max_length = len(notes2)

    for i in range(max_length):

        try:
            note1, note2 = notes1[i], notes2[i]

            # Check for differences in pitch or duration
            if note1.pitch != note2.pitch or note1.duration.quarterLength != note2.duration.quarterLength:
                # Clone note1 and highlight it
                merged_measure.append(add_highlighted_note(note2))
            else:
                merged_measure.append(copy.deepcopy(note2))

        # Catch if there are fewer notes in measure1 than measure2
        except IndexError:
            merged_measure.append(add_highlighted_note(notes2[i]))



    return merged_measure


def show_differences(merged_measure):
    score = stream.Score()
    score.append(merged_measure)
    score.show()