import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.genankiai import Generator

if __name__ == "__main__":
    generator = Generator("tests/data/decks/testdeck.json")
