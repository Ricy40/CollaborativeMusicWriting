from diff import compare_scores, merge_scores, compare_measures, show_differences, update_measure
from music21 import converter
from music21 import environment
import copy

# To Do:
#
# Account for scores with different parts
# Create a new score that is populated with merged parts and measures
#
#

env = environment.Environment()
env['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'  # Update path
env['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'

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
                    show_differences(measure_diff['score1_measure'], measure_diff['score2_measure'])
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


def version_control(score1, score2, output_file):
    """
    Save the merged score to a file.
    """
    merged_score = interactive_merge(score1, score2)
    merged_score.write('musicxml', fp=output_file)
    print(f"Merged score saved as {output_file}")


file3 = "../testfiles/testscore.musicxml"
file4 = "../testfiles/testscore2.musicxml"
file1 = "C:/Users/ricar/Documents/University/CM3203/main/testfiles/testscore.musicxml"
file2 = "C:/Users/ricar/Documents/University/CM3203/main/testfiles/testscore2.musicxml"
#output_file = "output.musicxml"

score3 = converter.parse(file3)
score4 = converter.parse(file4)
print("okay")
score1 = converter.parse(file1)
score2 = converter.parse(file2)

#version_control(score1, score2, output_file)


