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

def update_measure_in_score(target_score, part_id, measure_number, new_measure):
    """
    Replace a specific measure in the target score
    Args:
        target_score: The score being modified (music21.stream.Score)
        part_id: ID of the part to update (str)
        measure_number: Measure number to replace (int)
        new_measure: The measure to insert (music21.stream.Measure)
    """
    for part in target_score.parts:
        if part.id == part_id:
            for measure in part.getElementsByClass('Measure'):
                if measure.number == measure_number:
                    # Clone the measure to avoid reference issues
                    new_measure_copy = copy.deepcopy(new_measure)
                    new_measure_copy.number = measure_number  # Preserve measure number

                    part.replace(measure, new_measure_copy, recurse=True)
                    return True
    return False