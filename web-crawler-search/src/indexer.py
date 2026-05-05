import json
import re
from collections import defaultdict
from pathlib import Path

INDEX_FILE = "data/index.json"

# Convert text into lowercase word tokens
def tokenize(text):
    text = text.lower()
    return re.findall(r"[a-z0-9]+", text)

class Indexer:
    # Creates and stores an inverted index
    def __init__(self):
        self.index = defaultdict(dict)

    # Add one crawled page to the inverted index
    def add_page(self, page):
        tokens = tokenize(page.text)

        for position, word in enumerate(tokens):
            if page.url not in self.index[word]:
                self.index[word][page.url] = {
                    "frequency": 0,
                    "positions": []
                }

            self.index[word][page.url]["frequency"] += 1
            self.index[word][page.url]["positions"].append(position)

    # Build index from all crawled pages
    def build_index(self, pages):
        for page in pages:
            self.add_page(page)

        return self.index

    # Save index to file system
    def save_index(self, file_path = INDEX_FILE):
        Path("data").mkdir(exist_ok = True)

        with open(file_path, "w", encoding = "utf-8") as file:
            json.dump(self.index, file, indent = 4)

        print(f"Index saved to {file_path}")

    # Load index from file system
    def load_index(self, file_path = INDEX_FILE):
        with open(file_path, "r", encoding = "utf-8") as file:
            self.index = json.load(file)

        print(f"Index loaded from {file_path}")
        return self.index

    # Print inverted index for one word
    def print_word(self, word):
        word = word.lower()

        if word not in self.index:
            print(f"No index entry found for '{word}'")
            return None

        return self.index[word]