import json
import random
from pathlib import Path

WORDS_FILE = Path("words.json")
WORDS: list[str]

with WORDS_FILE.open("r") as f:
    WORDS = json.load(f)


def generate_passphrase(passphrase_words: list[str], num_words: int = 3) -> str:
    """Generate a passphrase from a list of words."""
    return " ".join(x.capitalize() for x in random.sample(passphrase_words, num_words))