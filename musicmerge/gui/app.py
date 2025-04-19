import tkinter as tk

from . import utils
from .screens import FileSelectScreen, MergeScreen, CompletionScreen, FailureScreen
from music21 import converter, environment


class MusicMergeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MusicMerge")
        self.root.geometry("600x400")

        # Application state
        self.scores = {}
        self.differences = []
        self.current_diff_index = 0
        self.merged_score = None
        self.error_message = tk.StringVar()

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

    def set_musescore_path(self, path):
        env = environment.Environment()
        env['musicxmlPath'] = path

    def load_scores(self, file1, file2):
        self.scores['score1'] = converter.parse(file1)
        self.scores['score2'] = converter.parse(file2)
        self.differences = self.compare_scores()
        self.current_diff_index = 0
        self.merged_score = self.scores['score1'].clone()

    def get_current_diff(self):
        if self.current_diff_index < len(self.differences):
            return self.differences[self.current_diff_index]
        return None

    def show_measure(self, source):
        current = self.get_current_diff()
        if current:
            measure = current[f'{source}_measure']
            measure.show('musicxml')

    def show_differences(self):
        current = self.get_current_diff()
        if current:
            # Implement your show_differences logic here
            pass

    def keep_measure(self, source):
        current = self.get_current_diff()
        if current:
            # Implement your measure keeping logic here
            self.current_diff_index += 1

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