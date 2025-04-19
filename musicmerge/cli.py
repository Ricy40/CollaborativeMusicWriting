import argparse
from pathlib import Path
from music21 import converter
from .core import interactive_merge

def main():
    parser = argparse.ArgumentParser(description="Merge two MusicXML scores.")
    parser.add_argument("score1", help="First MusicXML file")
    parser.add_argument("score2", help="Second MusicXML file")
    parser.add_argument("-o", "--output", default="merged.musicxml", help="Output file")
    args = parser.parse_args()

    # Load scores
    score1 = converter.parse(args.score1)
    score2 = converter.parse(args.score2)

    # Merge and save
    merged = interactive_merge(score1, score2)
    merged.write('musicxml', args.output)
    print(f"Merged score saved to {args.output}")

if __name__ == "__main__":
    main()