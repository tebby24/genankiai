# Anki Deck Generator

This project is a Python application that generates Anki decks using OpenAI's GPT-3 model. It takes a deck JSON file and a terms TXT file as inputs and generates an Anki deck as output.

## Getting Started

### Prerequisites

-   Python 3.8 or higher
-   An OpenAI API key

### Installation

1. Clone the repository:

```sh
git clone https://github.com/tebby24/genankiai.git
```

2. Install the required Python packages:

```sh
pip install -r requirements.txt
```

3. Set up your OpenAI API key in a `.env`

```sh
echo "OPENAI_API_KEY=yourapikey" > .env
```

### Usage

Create a deck json based of the following example. Generate unique id's for the `deck_id` and `model_id` by using `import random; random.randrange(1 << 30, 1 << 31)`

```json
{
    "name": "DeckName",
    "deck_id": 0123456789,
    "model_id": 0123456789,
    "native_language": "Chinese"
}
```

Create a txt file that contains terms you wish to generate cards for (one term per line)

```txt
term 1
term 2
term 3
```

To generate an Anki deck, run the `generate_deck.py` script with the `-d` option for the deck JSON file and the `-t` option for the terms TXT file:

```sh
python src/generate_deck.py -d path/to/deck.json -t path/to/terms.txt
```

The generated Anki deck will be saved in the `output` directory.
