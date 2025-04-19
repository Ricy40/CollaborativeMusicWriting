from platform import python_revision

from setuptools import setup, find_packages

setup(
    name="musicmerge",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "musicmerge = musicmerge.cli:main",
            "musicmerge-gui = musicmerge.gui.app:run_gui"
        ],
    },
    install_requires=[
        "music21",
    ],
    python_requires=">=3.7",
)