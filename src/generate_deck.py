import argparse
import json
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from genankiai import Generator

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Process deck JSON and terms TXT files."
    )
    parser.add_argument(
        "-d", "--deck", required=True, help="Path to the deck JSON file."
    )
    parser.add_argument(
        "-t", "--terms", required=True, help="Path to the terms TXT file."
    )
    return parser.parse_args()


def get_deck_info(deck_json):
    with open(deck_json, "r") as f:
        return json.load(f)


def get_terms(terms_file):
    with open(terms_file, "r") as f:
        return f.readlines()


if __name__ == "__main__":
    args = parse_arguments()
    deck_info = get_deck_info(args.deck)
    terms = get_terms(args.terms)
    openai_client = OpenAI(api_key=openai_api_key)
    generator = Generator(deck_info, openai_client)

    generator.generate_deck(
        terms,
    )
