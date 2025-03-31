import argparse
from music21 import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="The name of the person you want to greet")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")


