import json
import os
from datetime import datetime

import genanki


class Generator:

    MEDIA_DIRECTORY = "media"
    OUTPUT_DIRECTORY = "output"

    frontside_template = """
<div class="term">{{Term}}</div>
<div>{{Term Audio}}</div>
"""
    backside_template = """
{{FrontSide}}
<hr id="answer">
<div class="definition">{{English Definition}}</div>
<div class="translation">{{Native Language Translation}}</div><br>
<div class="example">{{Example Sentence}}</div>
<div>{{Example Sentence Audio}}</div>
"""
    style = """
body {
	display: block;
	font-family: "Times New Roman"
}

.term {
	font-size: 3rem;
}

.definition {

}

.translation {

}

.example {
	font-style: italic;
}
"""

    def __init__(self, deck_info, openai_client):
        self.deck_info = deck_info
        self.openai_client = openai_client
        self.media_files = []

    def setup_directories(self):
        """Create media and output directories if it does not exist"""
        if not os.path.exists(self.MEDIA_DIRECTORY):
            os.makedirs(self.MEDIA_DIRECTORY)
        if not os.path.exists(self.OUTPUT_DIRECTORY):
            os.makedirs(self.OUTPUT_DIRECTORY)

    def generate_deck(self, terms):
        """
        generate a deck from given terms and write to the specified output path
        """
        notes = [self.get_note(term) for term in terms]
        deck = self.get_deck()
        [deck.add_note(note) for note in notes]
        package = genanki.Package(deck)
        package.media_files = self.media_files
        date = datetime.now().strftime("%Y-%m-%d")
        output_filename = self.deck_info["name"] + "_" + date + ".apkg"
        output_filepath = os.path.join(self.OUTPUT_DIRECTORY, output_filename)
        package.write_to_file(output_filepath)

    def get_model(self):
        """Generate a model for the deck"""
        model = genanki.Model(
            self.deck_info["model_id"],
            self.deck_info["name"] + " (Model)",
            fields=[
                {"name": "Term"},
                {"name": "Term Audio"},
                {"name": "English Definition"},
                {"name": "Native Language Translation"},
                {"name": "Example Sentence"},
                {"name": "Example Sentence Audio"},
            ],
            templates=[
                {
                    "name": "Card",
                    "qfmt": self.frontside_template,
                    "afmt": self.backside_template,
                }
            ],
            css=self.style,
        )
        return model

    def get_note(self, term):
        """Generate a note for the given term"""
        example_sentence = self.get_example_sentence(term)
        fields = [
            term,
            self.get_tts(term),
            self.get_english_definition(term),
            self.get_translation(self.deck_info["native_language"], term),
            example_sentence,
            self.get_tts(example_sentence),
        ]
        return genanki.Note(model=self.get_model(), fields=fields)

    def get_deck(self):
        """Generate a deck from the given terms"""
        return genanki.Deck(self.deck_info["deck_id"], self.deck_info["name"])

    def get_tts(self, string):
        """Uses OpenAI API to convert input string into speech"""
        print(f"get_tts({string})")
        filename = f"{self.to_snake_case(string)}.mp3"
        path = os.path.join("media", filename)
        response = self.openai_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=string,
        )
        response.stream_to_file(path)
        self.media_files.append(path)
        return f"[sound:{filename}]"

    def get_english_definition(self, term):
        """Uses OpenAI API to generate an English definition of input term"""
        print(f"get_english_definition({term})")
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "In this chat, you will act as a dictionary, providing simple definitions of English terms. I will provide you with a term, and you will give a simple definition and nothing else. Do not include the term in your definition.",
                },
                {"role": "user", "content": term},
            ],
        )
        return response.choices[0].message.content

    def get_translation(self, native_language, term):
        """Uses OpenAI API to generate a translation of input term"""
        print(f"get_translation({native_language}, {term})")
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"In this chat, you will act as a translator, providing translations of English terms into {native_language}. I will provide you with a term, and you will give a translation and nothing else.",
                },
                {"role": "user", "content": term},
            ],
        )
        return response.choices[0].message.content

    def get_example_sentence(self, term):
        """Uses OpenAI API to generate an example sentence using input term"""
        print(f"get_example_sentence({term})")
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "In this chat, you will act as a writer, providing example sentences using the English terms I give you. I will provide you with a term, and you will give an example sentence using that term and nothing else.",
                },
                {"role": "user", "content": term},
            ],
        )
        return response.choices[0].message.content

    def to_snake_case(self, string):
        """Convert a string to snake_case"""
        return string.lower().replace(" ", "_").replace(".", "")
