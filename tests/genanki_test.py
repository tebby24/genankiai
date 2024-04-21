import os

import genanki

OUTPUT_DIRECTORY = "tests/output"

if __name__ == "__main__":
    model = genanki.Model(
        1908956292,
        "Test Model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
            {"name": "Sound"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Question}}",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}<br>{{Sound}}',
            }
        ],
    )

    note = genanki.Note(
        model=model,
        fields=[
            "This is a question",
            "This is an answer",
            "[sound:ding.wav]",
        ],
    )

    deck = genanki.Deck(1704973630, "Test Deck")

    deck.add_note(note)

    package = genanki.Package(deck)
    package.media_files = ["tests/data/media/ding.wav"]
    output_filepath = os.path.join(OUTPUT_DIRECTORY, "test_package.apkg")
    package.write_to_file(output_filepath)
