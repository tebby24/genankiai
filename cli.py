import argparse
import json
import os
import random
import subprocess

import openai
from dotenv import load_dotenv

from genankiai import Generator

load_dotenv()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="CLI tool for GenAnkiAI.")
    subparsers = parser.add_subparsers(title="Commands", dest="command")

    # Subparser for 'newdeck' command
    parser_newdeck = subparsers.add_parser("newdeck", help="Create a new deck")
    parser_newdeck.add_argument("-n", "--name", required=True, help="Name of the deck")
    parser_newdeck.add_argument(
        "-l",
        "--native-language",
        required=True,
        help="Native language of the deck's user",
    )

    # Subparser for 'generate' command
    parser_generate = subparsers.add_parser("generate", help="Generate .apkg")
    parser_generate.add_argument("name", help="Name of the deck")

    # Subparser for 'listdecks' command
    parser_listdecks = subparsers.add_parser("listdecks", help="List all decks")

    # Subparser for 'editdeck' command
    parser_editdeck = subparsers.add_parser("editdeck", help="Edit a deck")
    parser_editdeck.add_argument("name", help="Name of the deck")

    # Subparser for 'deletedeck' command
    parser_deletedeck = subparsers.add_parser("deletedeck", help="Delete a deck")
    parser_deletedeck.add_argument("name", help="Name of the deck")

    return parser.parse_args()


def get_settings():
    with open("settings.json", "r") as f:
        settings = json.load(f)
    settings["decks_directory"] = os.path.expanduser(settings["decks_directory"])
    settings["output_directory"] = os.path.expanduser(settings["output_directory"])
    return settings


def get_openai_client():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    return openai.OpenAI(api_key=openai_api_key)


def get_terms():
    """Get terms from the user by writing to a text file."""
    terms_file = "terms.txt"
    subprocess.call([os.environ.get("EDITOR", "vi"), terms_file])
    with open(terms_file, "r") as f:
        user_input = f.read().strip()
    terms = user_input.split("\n")
    return terms


def get_deck_json_path(name):
    """Get the path to the deck JSON file."""
    decks_directory = get_settings()["decks_directory"]
    deck_json_path = os.path.join(decks_directory, f"{name}.json")
    return deck_json_path


def deck_exists(name):
    deck_json_path = get_deck_json_path(name)
    return os.path.exists(deck_json_path)


def generate_deck(name):
    """Generate a deck using the specified deck JSON file."""
    if not deck_exists(name):
        print(f"Deck {name} does not exist.")
        return
    deck_json_path = get_deck_json_path(name)
    with open(deck_json_path, "r") as f:
        deck_info = json.load(f)
    openai_client = get_openai_client()
    generator = Generator(
        deck_info, openai_client, output_directory=get_settings()["output_directory"]
    )
    terms = get_terms()
    generator.generate_deck(terms)


def new_deck(name, native_language):
    """Create a new deck with a random deck_id and model_id."""
    if deck_exists(name):
        print(f"Deck {name} already exists.")
        return
    if " " in name:
        print("Deck name cannot contain spaces.")
        return
    deck_id = random.randrange(1 << 30, 1 << 31)
    model_id = random.randrange(1 << 30, 1 << 31)
    deck_info = {
        "name": name,
        "native_language": native_language,
        "deck_id": deck_id,
        "model_id": model_id,
    }
    deck_json_path = get_deck_json_path(name)
    with open(deck_json_path, "w") as f:
        json.dump(deck_info, f, indent=4)
    print(f"Created {deck_json_path}")


def list_decks():
    """List all decks in the decks directory."""
    decks_directory = get_settings()["decks_directory"]
    decks = [
        f.split(".")[0]
        for f in os.listdir(decks_directory)
        if f.split(".")[1] == "json"
    ]
    print("decks:")
    for deck in decks:
        print(f" - {deck}")


def edit_deck(name):
    """Edit the deck JSON file."""
    if not deck_exists(name):
        print(f"Deck {name} does not exist.")
        return
    deck_json_path = get_deck_json_path(name)
    subprocess.call([os.environ.get("EDITOR", "vi"), deck_json_path])


def delete_deck(name):
    """Delete the deck JSON file."""
    if not deck_exists(name):
        print(f"Deck {name} does not exist.")
        return
    deck_json_path = get_deck_json_path(name)
    print(f"Are you sure you want to delete {deck_json_path}?")
    response = input("y/n: ")
    if response == "y":
        os.remove(deck_json_path)
        print(f"Deleted {deck_json_path}")
    else:
        pass


if __name__ == "__main__":
    args = parse_arguments()
    if args.command == "newdeck":
        new_deck(args.name, args.native_language)
    elif args.command == "generate":
        generate_deck(args.name)
    elif args.command == "listdecks":
        list_decks()
    elif args.command == "editdeck":
        edit_deck(args.name)
    elif args.command == "deletedeck":
        delete_deck(args.name)
