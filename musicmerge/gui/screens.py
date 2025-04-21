import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import threading

from musicmerge.gui import utils


class BaseScreen(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        """To be implemented by subclasses"""
        pass

    def show(self):
        """Display this screen"""
        self.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        """Hide this screen"""
        self.pack_forget()


class FileSelectScreen(BaseScreen):

    def __init__(self, master, controller):
        super().__init__(master, controller)
        # Auto-detect MuseScore on initialization
        self.auto_detect_musescore()

    def create_widgets(self):
        # File 1 Selection
        self.file1_var = tk.StringVar()
        ttk.Label(self, text="Score 1:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.file1_var, width=40).grid(row=0, column=1)
        ttk.Button(self, text="Browse",
                   command=lambda: self.browse_file(self.file1_var)).grid(row=0, column=2)

        # File 2 Selection
        self.file2_var = tk.StringVar()
        ttk.Label(self, text="Score 2:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.file2_var, width=40).grid(row=1, column=1)
        ttk.Button(self, text="Browse",
                   command=lambda: self.browse_file(self.file2_var)).grid(row=1, column=2)

        # Visual Indicators
        self.status_label = ttk.Label(self, text="Select both files to enable merge")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)

        # MuseScore Path Configuration
        self.musescore_var = tk.StringVar()
        ttk.Label(self, text="MuseScore Path:").grid(row=3, column=0, padx=5, pady=5)
        ttk.Entry(self, textvariable=self.musescore_var, width=40).grid(row=3, column=1)
        ttk.Button(self, text="Set Path",
                   command=self.set_musescore_path).grid(row=3, column=2)

        # Merge Button
        self.merge_btn = ttk.Button(self, text="Merge",
                                    state=tk.DISABLED,
                                    command=self.start_merge)
        self.merge_btn.grid(row=4, column=1, pady=20)

        # Track file selection
        self.file1_var.trace_add('write', self.check_files)
        self.file2_var.trace_add('write', self.check_files)

    def auto_detect_musescore(self):
        detected_path = utils.detect_musescore()
        if detected_path:
            self.musescore_var.set(detected_path)
            self.controller.set_musescore_path(detected_path)
            self.status_label.config(text=f"Auto-detected MuseScore at: {detected_path}",
                                     foreground="green")

    def browse_file(self, target_var):
        filepath = filedialog.askopenfilename(filetypes=[("MusicXML", "*.musicxml")])
        if filepath:
            target_var.set(filepath)

    def set_musescore_path(self, path):
        """Update both the entry field and verify the path"""
        self.musescore_var.set(path)
        if Path(path).exists():
            self.status_label.config(text=f"MuseScore path valid: {path}",
                                     foreground="green")
            self.controller.set_musescore_path(path)
        else:
            self.status_label.config(text=f"Warning: Path not found - {path}",
                                     foreground="orange")

    def check_files(self, *args):
        """Enable merge button only when both files are selected"""
        if self.file1_var.get() and self.file2_var.get():
            self.merge_btn.config(state=tk.NORMAL)
            self.status_label.config(text="Ready to merge!", foreground="green")
        else:
            self.merge_btn.config(state=tk.DISABLED)
            self.status_label.config(text="Select both files to enable merge", foreground="black")

    def start_merge(self):
        try:
            self.controller.load_scores(
                self.file1_var.get(),
                self.file2_var.get()
            )
            if len(self.controller.differences) > 0:
                self.controller.show_screen("MergeScreen")
            else:
                self.controller.show_screen("CompletionScreen")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files:\n{str(e)}\nScore is likely empty, invalid or corrupted.")


class MergeScreen(BaseScreen):
    def create_widgets(self):
        # Navigation Frame
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill=tk.X, pady=10)

        #ttk.Label(nav_frame, textvariable=self.current_part).pack(side=tk.LEFT, padx=10)
        #ttk.Label(nav_frame, textvariable=self.current_measure).pack(side=tk.LEFT)

        # Button Frame
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=20)

        # Action Buttons
        ttk.Button(btn_frame, text="Show Measure from Score 1",
                   command=lambda: self.show_measure_threaded('score1')).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Show Measure from Score 2",
                   command=lambda: self.show_measure_threaded('score2')).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Show Differences",
                   command=self.show_differences_threaded).grid(row=0, column=2, padx=5, pady=5)

        ttk.Button(btn_frame, text="Keep Measure from Score 1",
                   command=lambda: self.keep_measure('score1')).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Keep Measure from Score 2",
                   command=lambda: self.keep_measure('score2')).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Quit (q)",
                   command=self.quit).grid(row=1, column=2, padx=5, pady=5)

        # Status Label
        self.status_label = ttk.Label(self, text="")
        self.status_label.pack(pady=10)

        # Warning about MuseScore word
        ttk.Label(self,
                  text="Note: Buttons marked with (s1/s2/n) require MuseScore installed",
                  foreground="red").pack(side=tk.BOTTOM, pady=10)

    def show_measure(self, source):
        try:
            self.controller.show_measure(source)
            self.status_label.config(text=f"Showing {source}", foreground="blue")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")

    def show_measure_threaded(self, source):
        """Run show_measure in a separate thread"""
        def worker():
            self.show_measure(source)

        threading.Thread(target=worker, daemon=True).start()

    def show_differences(self):
        try:
            self.controller.show_differences()
            self.status_label.config(text="Showing differences", foreground="blue")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")

    def show_differences_threaded(self):
        """Run show_compared_measure in a separate thread"""
        def worker():
            self.show_differences()

        threading.Thread(target=worker, daemon=True).start()

    def keep_measure(self, source):
        self.controller.keep_measure(source)
        self.update_display()

    def quit(self):
        self.controller.quit_merge()

    def update_display(self):
        current = self.controller.get_current_diff()
        if current:
            self.current_part.set(f"Part: {current['part_name']}")
            self.current_measure.set(f"Measure: {current['measure_number']}")
        else:
            self.controller.show_screen("CompletionScreen")


class CompletionScreen(BaseScreen):
    def create_widgets(self):
        ttk.Label(self, text="Merge Completed Successfully!",
                  font=('Helvetica', 14)).pack(pady=20)

        # Output File Selection
        ttk.Label(self, text="Output File:").pack(pady=5)
        self.output_var = tk.StringVar(value="merged.musicxml")
        ttk.Entry(self, textvariable=self.output_var, width=40).pack()
        ttk.Button(self, text="Browse", command=self.browse_output).pack(pady=5)

        # Action Buttons
        ttk.Button(self, text="Save", command=self.save).pack(pady=10)
        ttk.Button(self, text="Quit", command=self.master.destroy).pack()

    def browse_output(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".musicxml",
            filetypes=[("MusicXML", "*.musicxml")]
        )
        if filepath:
            self.output_var.set(filepath)

    def save(self):
        try:
            self.controller.save_merge(self.output_var.get())
            messagebox.showinfo("Success", "File saved successfully!")
            self.master.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")


class FailureScreen(BaseScreen):
    def create_widgets(self):
        ttk.Label(self, text="Merge Failed",
                  font=('Helvetica', 14), foreground="red").pack(pady=20)

        ttk.Label(self, textvariable=self.controller.error_message).pack(pady=10)

        ttk.Button(self, text="Quit", command=self.master.destroy).pack(pady=20)