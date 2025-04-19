import tkinter as tk
from tkinter import filedialog, messagebox
from music21 import converter
from .core import compare_scores, show_differences, update_measure


class MusicMergeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MusicMerge")

        # Widgets
        tk.Button(root, text="Load Score 1", command=self.load_score1).pack()
        tk.Button(root, text="Load Score 2", command=self.load_score2).pack()
        tk.Button(root, text="Merge", command=self.merge).pack()

        # State
        self.score1 = None
        self.score2 = None

    def load_score1(self):
        path = filedialog.askopenfilename(filetypes=[("MusicXML", "*.musicxml")])
        if path:
            self.score1 = converter.parse(path)

    def load_score2(self):
        path = filedialog.askopenfilename(filetypes=[("MusicXML", "*.musicxml")])
        if path:
            self.score2 = converter.parse(path)

    def merge(self):
        if not self.score1 or not self.score2:
            messagebox.showerror("Error", "Load both scores first!")
            return

        # Implement GUI-based merging here
        # (e.g., show a list of differences and let the user choose)
        messagebox.showinfo("Info", "Merge logic would run here.")


def run_gui():
    root = tk.Tk()
    app = MusicMergeApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui()