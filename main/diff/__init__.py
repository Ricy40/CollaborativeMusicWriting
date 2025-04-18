from diff import compare_scores, merge_scores, compare_measures, show_differences
from music21 import converter
from music21 import environment
import copy

# To Do:
#
# Account for scores with different parts
# Create a new score that is populated with merged parts and measures
#
#j

env = environment.Environment()
env['musicxmlPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'  # Update path
env['musescoreDirectPNGPath'] = r'C:\Program Files\MuseScore 4\bin\MuseScore4.exe'

def version_control(score1, score2, output_file):

    differences = compare_scores(score1, score2)

    if differences:
        print(f"{len(differences)} Differences found:")
        new_score = copy.deepcopy(score1)
        new_score.parts
        for measure in score1.parts[0].getElementsByClass('Measure'):
            for difference in differences:
                if measure.measureNumber == difference['measure_number']:
                    managing_difference = True
                    print(f"""Difference:\nPart: {difference['part']}\nMeasure: {difference['measure_number']}""")

                    while managing_difference:
                        sel = input("""type:
                        's1' to show the first score's measure
                        's2' to show the second score's measure
                        'n' to highlight the difference in notes from the first score to the second score
                        "c1" to choose to keep the first score's measure
                        "c2" to choose to keep the second score's measure
                        'q' to quit""")

                        sel = sel.lower()

                        if sel == "s2":
                            difference['score1_measure'].show()
                        elif sel == "s2":
                            difference['score2_measure'].show()
                        elif sel == "n":
                            merged_measure = compare_measures(difference['score1_measure'], difference['score2_measure'])
                            show_differences(merged_measure)
                        elif sel == "c1":
                            score1.remove(difference['score1_measure'])
                            score1.insert(difference['measure_number'], difference['score2_measure'])
                            managing_difference = False


                        merged_measure = compare_measures(difference['score1_measure'], difference['score2_measure'])
                        show_differences(merged_measure)
                        input("Press Enter to continue...")




        # merged_score = merge_scores(score1, score2)
        # merged_score.write('musicxml', output_file)
        # print(f"Merged score saved to {output_file}")
    else:
        print("No differences found.")



file1 = "../testfiles/testscore.musicxml"
file2 = "../testfiles/testscore2.musicxml"

score1 = converter.parse(file1)
score2 = converter.parse(file2)

version_control(score1, score2, "output.musicxml")