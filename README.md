# COMP3011 Search Engine Tool

A Python command-line search engine tool built for the COMP3011 Web Services and Web Data coursework 2.

The application crawls `quotes.toscrape.com`, builds an inverted index from the crawled pages, saves the index to the file system and allows users to search for pages containing specific words or query phrases.

## Features

- Crawls the quote listing pages from `quotes.toscrape.com`
- Respects a 6-second politeness window between requests
- Extracts quote text, authors and tags
- Builds an inverted index storing:
  - word frequency
  - word positions
  - page URLs
- Supports case-insensitive search
- Supports multi-word conjunctive queries
- Supports:
  - `build`
  - `load`
  - `print <word>`
  - `find <query>`
- Uses TF-IDF style ranking for search results
- Includes automated testing using pytest
- Includes coverage reporting using pytest-cov

## Project Structure

```text
web-crawler-search/
│
├── src/
│   ├── __init__.py
│   ├── crawler.py
│   ├── indexer.py
│   ├── search.py
│   ├── utils.py
│   └── main.py
│
├── tests/
│   ├── test_crawler.py
│   ├── test_indexer.py
│   └── test_search.py
│
├── data/
│   └── index.json
│
├── requirements.txt
├── pytest.ini
├── .coveragerc
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Amin256/comp3011-search-engine.git
cd comp3011-search-engine/web-crawler-search
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Search Tool

Run the command-line application using:

```bash
python -m src.main
```

You will see:

```text
COMP3011 Search Engine Tool
Type 'help' to see available commands.
>
```

---

## Commands

### build

Crawls the website, builds the inverted index, and saves it to `data/index.json`.

```text
> build
```

---

### load

Loads the saved index from `data/index.json`.

```text
> load
```

---

### print

Prints the inverted index entry for a word.

```text
> print love
```

Example output:

```text
{
  "https://quotes.toscrape.com/page/2/": {
    "frequency": 8,
    "positions": [219, 286, 419, 468, 513, 522, 540, 541]
  }
}
```

---

### find

Searches for pages containing a query term or terms.

```text
> find indifference
```

Multi-word query:

```text
> find good friends
```

The search uses conjunctive query processing, meaning that pages must contain all query terms to be returned.

Results are ranked using TF-IDF style scoring.

---

## Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

The automated tests cover:

- crawler parsing
- mocked successful and failed network requests
- tokenisation
- inverted index creation
- frequency and position storage
- save/load functionality
- single-word search
- multi-word search
- case-insensitive search
- TF-IDF ranking
- edge cases such as empty queries and missing words

The project achieves approximately 91% line coverage across the main source modules.

---

## Design Decisions

The project is split into separate modules to keep responsibilities clear.

- `crawler.py`
  - handles web crawling and HTML parsing
- `indexer.py`
  - builds and stores the inverted index
- `search.py`
  - handles query processing and ranking
- `utils.py`
  - contains shared tokenisation logic
- `main.py`
  - provides the command-line interface

The inverted index maps words to the pages in which they appear. Each posting stores:

- page URL
- frequency
- positions

TF-IDF style scoring was added to improve result ranking beyond simple word matching. This means pages are ranked using both term frequency and inverse document frequency.

---

## Generative AI Declaration

OpenAI ChatGPT was used as a development support tool during this project.

It was used to:

- debug implementation issues
- improve testing coverage
- explore TF-IDF ranking
- suggest edge-case tests

For example, AI helped suggest tests for empty queries, repeated words, mocked failed network requests and TF-IDF ranking checks.

All AI-generated suggestions were reviewed, tested and adapted manually before inclusion in the final implementation. The final project reflects my own understanding of crawling, tokenisation, inverted indexing, query processing, ranking, testing and software design.