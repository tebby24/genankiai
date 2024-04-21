tebby24: @work

GitHub Copilot: Hello! How can I assist you with your programming needs today?

tebby24: @workspace please write a readme for this project

GitHub Copilot: Determining workspace structure

Deciding which workspace information to collect

Gathering workspace info

# Anki Deck Generator

This project is a Python application that generates Anki decks using OpenAI's GPT-3 model. It takes a deck JSON file and a terms TXT file as inputs and generates an Anki deck as output.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- An OpenAI API key

### Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/yourrepository.git
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

To generate an Anki deck, run the `generate_deck.py` script with the `-d` option for the deck JSON file and the `-t` option for the terms TXT file:

```sh
python src/generate_deck.py -d decks/elvis.json -t terms.txt
```
The generated Anki deck will be saved in the `output` directory.

