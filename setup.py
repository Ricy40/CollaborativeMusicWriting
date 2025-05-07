from setuptools import setup, find_packages
import pathlib

setup(
    name="musicmerge",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "musicmerge-gui = musicmerge.gui.app:run_gui"
        ],
    },
    install_requires=[
        "music21",
    ],
    python_requires=">=3.11",
)