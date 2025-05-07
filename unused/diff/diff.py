from music21 import note, stream, chord, expressions
import copy

def compare_scores(score1, score2):
    """
        Compare two scores and return differences organized by part.
        Returns:

        List of dictionaries, where each dict represents a part and its differing measures.
        Format: [
            {
                'part_id': str,       # Part ID (e.g., "P1")
                'part_name': str,     # Part name (e.g., "Piano")
                'differences': [      # List of differing measures
                    {
                        'measure_number': int,
                        'score1_measure': music21.stream.Measure,
                        'score2_measure': music21.stream.Measure
                    },
                    ...
                ]
            },
            ...
        ]
    """

    differences = []

    for part1, part2 in zip(score1.parts, score2.parts):
        part_diff = {
            'part_id': part1.id,
            'part_name': part1.partName,
            'differences': []
        }

        # Ensure both parts have the same number of measures
        measures1 = list(part1.getElementsByClass('Measure'))
        measures2 = list(part2.getElementsByClass('Measure'))

        if len(measures1) != len(measures2):
            raise ValueError("Parts have different numbers of measures!")

        # Compare each measure
        for measure1, measure2 in zip(measures1, measures2):
            # Check for differences in notes/chords
            has_diff = False
            if len(measure1.notes) != len(measure2.notes):
                has_diff = True
            else:
                for n1, n2 in zip(measure1.notes, measure2.notes):
                    if (isinstance(n1, note.Note)) and (isinstance(n2, note.Note)):
                        if n1.pitch != n2.pitch or n1.duration != n2.duration:
                            has_diff = True
                            break
                    elif (isinstance(n1, chord.Chord)) and (isinstance(n2, chord.Chord)):
                        if n1.pitches != n2.pitches or n1.duration != n2.duration:
                            has_diff = True
                            break

            # Check other elements (time signatures, clefs, etc.)
            if (measure1.timeSignature != measure2.timeSignature or
                measure1.clef != measure2.clef):
                has_diff = True

            if has_diff:
                part_diff['differences'].append({
                    'measure_number': measure1.number,
                    'score1_measure': measure1,
                    'score2_measure': measure2
                })

        # Only add parts with differences
        if part_diff['differences']:
            differences.append(part_diff)

    return differences

def merge_scores(score1, score2):
    merged_score = copy.deepcopy(score1)

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


def show_differences(measure1, measure2):
    """
    Show a measure with differing notes/chords highlighted in red.
    Works for both Notes and Chords.
    """
    # Create a new measure to hold the highlighted version
    highlighted_measure = stream.Measure(number=measure1.number)

    # Copy all elements (clefs, time signatures, etc.) from measure1
    for elem in measure1.elements:
        if not isinstance(elem, (note.Note, chord.Chord, note.Rest)):
            highlighted_measure.insert(elem.offset, copy.deepcopy(elem))

    # Compare notes/chords
    for n1, n2 in zip(measure1.notesAndRests, measure2.notesAndRests):
        # Case 1: Both are Notes/Chords and differ
        if ((isinstance(n1, (note.Note, chord.Chord)) and
             isinstance(n2, (note.Note, chord.Chord))) and
                (n1.pitches != n2.pitches or n1.duration != n2.duration)):

            # Create a colored version
            colored_note = copy.deepcopy(n1)
            colored_note.style.color = 'red'
            highlighted_measure.insert(n1.offset, colored_note)

        # Case 2: Rest or no difference -> copy as-is
        else:
            highlighted_measure.insert(n1.offset, copy.deepcopy(n1))

    # Display in MuseScore
    highlighted_measure.show('musicxml')

def update_measure(target_score, part_name, measure_number, new_measure):
    """
    Replace a measure in `target_score` with `new_measure`.
    """
    for part in target_score.parts:
        if part.partName == part_name:
            for m in part.getElementsByClass('Measure'):
                if m.number == measure_number:
                    part.replace(m, new_measure, recurse=True)
                    break
            break


def show_diff_old(merged_measure):
    """
        Show a measure with differing notes/chords highlighted in red.
    """
    score = stream.Score()
    score.append(merged_measure)
    score.show()