from music21 import converter, stream, note, chord, expressions
import copy

from music21.musicxml.testPrimitive import articulations01


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
                        if calculate_difference(n1, n2) >= 0:
                            has_diff = True
                            break
                    elif (isinstance(n1, chord.Chord)) and (isinstance(n2, chord.Chord)):
                        if n1.pitches != n2.pitches or n1.duration != n2.duration:
                            has_diff = True
                            break
                    else:
                        # Handle cases where one is a Note and the other is a Chord
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

    if len(measure1.notesAndRests) != len(measure2.notesAndRests):
        for n in measure1.notesAndRests:
            nc = copy.deepcopy(n)
            nc.style.color = '#ff0000'  # Highlight in red
            highlighted_measure.insert(n.offset, nc)
        return highlighted_measure

    # Compare notes/chords
    for n1, n2 in zip(measure1.notesAndRests, measure2.notesAndRests):
        # Case 1: Both are Notes/Chords and differ
        if ((isinstance(n1, (note.Note, chord.Chord)) and
             isinstance(n2, (note.Note, chord.Chord)))):

            diff_met = calculate_difference(n1, n2)

            colored_note = copy.deepcopy(n1)
            if diff_met >= 0.8: # Major -> Red
                colored_note.style.color = '#ff0000'
            elif diff_met >= 0.3: # Moderate -> Reddish Orange
                colored_note.style.color = '#ff5500'
            elif diff_met >= 0.1: # Minor -> Orange
                colored_note.style.color = '#ffbb00'
            highlighted_measure.insert(n1.offset, colored_note)

        # Case 2: Rest or no difference -> copy as-is
        else:
            highlighted_measure.insert(n1.offset, copy.deepcopy(n1))

    # Display in MuseScore
    return highlighted_measure


def calculate_difference(note1, note2):
    weights = {
        'pitch': 0.8,  # Most musically significant
        'duration': 0.5,
        'articulation': 0.2,
        'stem_direction': 0.1  # Least disruptive
    }

    differences = {
        'pitch': 0 if note1.pitch == note2.pitch else 1,
        'duration': abs(note1.duration.quarterLength - note2.duration.quarterLength),
        'articulation': 0 if note1.articulations == note2.articulations else 1,
        'stem_direction': 0 if note1.stemDirection == note2.stemDirection else 1
    }

    # Normalize duration difference to [0,1]
    differences['duration'] = min(differences['duration'] / 4.0, 1.0)
    to_return = sum(weights[feat] * differences[feat] for feat in weights)
    return to_return

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

def show_highlighted_score(score, differences):
    """
    Display the score with highlighted differences.
    """
    highlighted_score = copy.deepcopy(score)
    for part in highlighted_score.parts:
        for measure in part.getElementsByClass('Measure'):
            for diff in differences:
                if part.id == diff['part_id']:
                    for measure_diff in diff['differences']:
                        if measure.number == measure_diff['measure_number']:
                            print("\n measure number: " + str(measure_diff['measure_number']))
                            print(measure, measure_diff['score2_measure'], measure_diff['score1_measure'])
                            highlighted_measure = show_differences(measure_diff['score2_measure'], measure_diff['score1_measure'])
                            print(highlighted_measure)
                            part.replace(measure, highlighted_measure)

    return highlighted_score

def interactive_merge(score1, score2):
    """
    Interactively merge two scores, letting the user choose which measures to keep.
    Returns:
        The merged score (initially a copy of score1, updated with user choices).
    """

    # Step 1: Detect differences
    differences = compare_scores(score1, score2)
    if not differences:
        print("No differences found. Scores are identical.")
        return copy.deepcopy(score1)

    # Step 2: Initialize new_score as a copy of score1
    new_score = copy.deepcopy(score1)
    print("New score created as a copy of score1.")

    # Step 3: Iterate through parts with differences
    for part_diff in differences:
        part_name = part_diff['part_name']
        print(f"\nChecking part: {part_name}")

        # Step 4: Iterate through differing measures in this part
        for measure_diff in part_diff['differences']:
            measure_number = measure_diff['measure_number']
            print(f"\nMeasure {measure_number}: Differences detected.")

            while True:
                # Prompt user for action
                user_input = input(
                    "Options:\n"
                    "  s1 - Show measure from score1\n"
                    "  s2 - Show measure from score2\n"
                    "  n  - Show differences (highlighted in red)\n"
                    "  c1 - Keep measure from score1\n"
                    "  c2 - Keep measure from score2\n"
                    "  q  - Quit merging\n"
                    "Choose an option: "
                ).strip().lower()

                # Handle user input
                if user_input == 's1':
                    measure_diff['score1_measure'].show('musicxml')
                elif user_input == 's2':
                    measure_diff['score2_measure'].show('musicxml')
                elif user_input == 'n':
                    measure = show_differences(measure_diff['score1_measure'], measure_diff['score2_measure'])
                    measure.show()
                elif user_input == 'c1':
                    print(f"Keeping measure {measure_number} from score1.")
                    break
                elif user_input == 'c2':
                    print(f"Keeping measure {measure_number} from score2.")
                    update_measure(new_score, part_name, measure_number, measure_diff['score2_measure'])
                    break
                elif user_input == 'q':
                    print("Quitting merge early.")
                    return new_score
                else:
                    print("Invalid option. Try again.")

    print("\nMerge complete!")
    return new_score

def merge_export(merged_score, output_file):
    """
    Save the merged score to a file.
    """
    merged_score.write('musicxml', fp=output_file)
    print(f"Merged score saved as {output_file}")