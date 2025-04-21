import platform
import subprocess
import tempfile
import threading
import copy
from pathlib import Path
from music21 import stream, note, chord


def detect_musescore():
    """Try to automatically find MuseScore installation path"""
    system = platform.system()

    # Common installation paths by OS
    common_paths = {
        'Windows': [
            r"C:\Program Files\MuseScore 4\bin\MuseScore4.exe",
            r"C:\Program Files\MuseScore 3\bin\MuseScore3.exe"
        ],
        'Darwin': [  # macOS
            "/Applications/MuseScore 4.app/Contents/MacOS/mscore",
            "/Applications/MuseScore 3.app/Contents/MacOS/mscore"
        ],
        'Linux': [
            "/usr/bin/musescore",
            "/usr/bin/mscore",
            "/usr/local/bin/musescore"
        ]
    }

    # Check if any of the common paths exist
    for path in common_paths.get(system, []):
        if Path(path).exists():
            return path

    # Additional checks for Windows registry
    if system == 'Windows':
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\MuseScore\MuseScore4") as key:
                return winreg.QueryValueEx(key, "Install_Dir")[0] + r"\bin\MuseScore4.exe"
        except:
            pass

    return None

def show_in_musescore(score_obj, musescore_path=None):
    """
    Show a music21 object in MuseScore without blocking the GUI
    """
    # Get MuseScore path from environment if not provided
    if musescore_path is None:
        from music21 import environment
        musescore_path = environment.Environment()['musicxmlPath']

    if not musescore_path or not Path(musescore_path).exists():
        raise ValueError("MuseScore path not configured correctly")

    # Create temporary file
    with tempfile.NamedTemporaryFile(suffix='.musicxml', delete=False) as tmp:
        tmp_path = tmp.name

    # Write to temp file
    score_obj.write('musicxml', tmp_path)

    # Launch MuseScore (non-blocking)
    if platform.system() == 'Darwin':  # macOS
        subprocess.Popen(['open', '-a', musescore_path, tmp_path])
    elif platform.system() == 'Windows':
        subprocess.Popen([musescore_path, tmp_path], shell=True)
    else:  # Linux
        subprocess.Popen([musescore_path, tmp_path])

    # Schedule file deletion after 30 seconds
    threading.Timer(30, lambda: Path(tmp_path).unlink(missing_ok=True)).start()

def get_compared_measure(measure1, measure2):
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
    return highlighted_measure
