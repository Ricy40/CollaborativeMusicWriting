import platform
from pathlib import Path


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