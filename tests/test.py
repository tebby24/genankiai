import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.genankiai import Generator

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def get_deck_info(deck_json):
    with open(deck_json, "r") as f:
        return json.load(f)


def get_terms(terms_file):
    with open(terms_file, "r") as f:
        return [line.strip() for line in f.readlines()]


if __name__ == "__main__":
    openai_client = OpenAI(api_key=openai_api_key)
    generator = Generator(
        get_deck_info("tests/data/decks/test_deck.json"), openai_client
    )
    generator.generate_deck(
        get_terms("tests/data/terms/test_terms.txt"), "tests/output"
    )
