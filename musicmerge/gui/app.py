import tkinter as tk
import copy
from tkinter import ttk

from . import utils
from .screens import FileSelectScreen, MergeScreen, CompletionScreen, FailureScreen
from music21 import converter, environment

from .utils import update_measure_in_score
from ..core import compare_scores, show_differences, show_highlighted_score


class MusicMergeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MusicMerge")
        self.root.geometry("600x400")

        # Application state
        self.score1 = None
        self.score2 = None

        self.differences = []
        self.current_part_index = 0
        self.current_measure_set = []
        self.current_measure_index = 0
        self.current_overall_index = 1

        self.merged_score = None
        self.error_message = tk.StringVar()

        self.style = ttk.Style()

        # Configure screens
        self.screens = {}
        self._setup_screens()
        self.show_screen("FileSelectScreen")

        # Musescore installtion
        self.musescore_path = None
        self._check_musescore()

    def _setup_screens(self):
        container = tk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        for ScreenClass in [FileSelectScreen, MergeScreen, CompletionScreen, FailureScreen]:
            screen = ScreenClass(container, self)
            self.screens[ScreenClass.__name__] = screen

    def show_screen(self, screen_name):
        for screen in self.screens.values():
            screen.hide()
        self.screens[screen_name].show()

    def get_current_part(self):
        if self.current_part_index < len(self.differences):
            return f"{self.differences[self.current_part_index]['part_id'] if self.differences else None}, {self.differences[self.current_part_index]['part_name'] if self.differences else None}"
        return "No part selected"

    def get_current_measure(self):
        if self.current_measure_set:
            return f"Measure {self.current_measure_set[self.current_measure_index]['measure_number']}"
        return "No measure selected"

    def get_total_differences(self):
        total = 0
        for part in self.differences:
            total += len(part['differences'])
        return total

    def get_current_diff_overall_number(self):
        return self.current_overall_index

    def set_musescore_path(self, path):
        env = environment.Environment()
        env['musicxmlPath'] = path

    def load_scores(self, file1, file2):
        self.score1 = converter.parse(file1)
        self.score2 = converter.parse(file2)
        self.differences = self.compare_scores()

        self.current_part_index = 0
        self.current_measure_set = (self.differences[self.current_part_index]['differences'] if self.differences else "")
        self.current_measure_index = 0

        self.merged_score = copy.deepcopy(self.score1)

    def get_current_diff(self):
        if self.current_part_index < len(self.differences):
            if self.current_measure_index < len(self.current_measure_set):
                return self.current_measure_set[self.current_measure_index]
        return None

    def compare_scores(self):
        return compare_scores(self.score1, self.score2)

    def show_measure(self, source):
        current = self.get_current_diff()
        if current:
            measure = current[f'{source}_measure']
            measure.show('musicxml')

    def show_score(self, source):
        score = self.score1
        if score:
            to_show = show_highlighted_score(score, self.differences)
            to_show.show('musicxml')

    def show_differences(self):
        current = self.get_current_diff()
        if current:
            compared_measure = show_differences(current['score2_measure'], current['score1_measure'])
            compared_measure.show('musicxml')

    def move_to_next_measure(self):
        if self.current_measure_index + 1 < len(self.current_measure_set):
            self.current_measure_index += 1
            self.current_overall_index += 1
        elif self.current_part_index + 1 < len(self.differences):
            self.current_part_index += 1
            self.current_measure_set = (self.differences[self.current_part_index]['differences'] if self.differences else "")
            self.current_measure_index = 0
            self.current_overall_index += 1
        else:
            self.show_screen("CompletionScreen")

    def keep_measure(self):
        current = self.get_current_diff()
        new_measure = current['score2_measure']
        part_id = self.differences[self.current_part_index]['part_id']
        measure_id = current['measure_number']
        update_measure_in_score(self.merged_score, part_id, measure_id, new_measure)

    def quit_merge(self):
        self.show_screen("CompletionScreen")

    def save_merge(self, output_path):
        if self.merged_score:
            self.merged_score.write('musicxml', output_path)

    def _check_musescore(self):
        """Check for MuseScore at startup"""
        detected_path = utils.detect_musescore()
        if detected_path:
            self.set_musescore_path(detected_path)

def run_gui():
    root = tk.Tk()
    app = MusicMergeApp(root)
    root.mainloop()