from src.indexer import Indexer
from src.crawler import CrawledPage
from src.utils import tokenise

def test_tokenise_lowercase_and_punctuation():
    text = "Good friends, GOOD times!"
    tokens = tokenise(text)
    assert tokens == ["good", "friends", "good", "times"]

def test_indexer_stores_frequency_and_positions():
    page = CrawledPage(
        url = "https://example.com",
        title = "Example",
        text = "good friends good"
    )

    indexer = Indexer()
    index = indexer.build_index([page])

    assert "good" in index
    assert index["good"]["https://example.com"]["frequency"] == 2
    assert index["good"]["https://example.com"]["positions"] == [0, 2]

    assert "friends" in index
    assert index["friends"]["https://example.com"]["frequency"] == 1
    assert index["friends"]["https://example.com"]["positions"] == [1]
    
def test_indexer_empty_page():
    page = CrawledPage(url = "test", title = "empty", text = "")
    indexer = Indexer()
    index = indexer.build_index([page])
    assert index == {}

def test_repeated_word_positions():
    page = CrawledPage(url = "test", title = "test", text = "hello hello hello")
    indexer = Indexer()
    index = indexer.build_index([page])
    assert index["hello"]["test"]["frequency"] == 3
    assert index["hello"]["test"]["positions"] == [0, 1, 2]

def test_indexer_multiple_pages_same_word():
    page1 = CrawledPage(url = "page1", title = "Page 1", text = "love")
    page2 = CrawledPage(url = "page2", title = "Page 2", text = "love love")
    indexer = Indexer()
    index = indexer.build_index([page1, page2])
    assert index["love"]["page1"]["frequency"] == 1
    assert index["love"]["page2"]["frequency"] == 2
    
def test_tokenise_keeps_numbers():
    tokens = tokenise("Quote number 123 is here")

    assert "123" in tokens

def test_tokenise_removes_punctuation():
    tokens = tokenise("Hello!!! Are you there???")

    assert tokens == ["hello", "are", "you", "there"]

def test_indexer_case_insensitive():
    page = CrawledPage(url = "page1", title = "Page 1", text = "Love love LOVE")

    indexer = Indexer()
    index = indexer.build_index([page])

    assert index["love"]["page1"]["frequency"] == 3

def test_save_and_load_index(tmp_path):
    page = CrawledPage(url = "page1", title = "Page 1", text = "love wisdom")
    file_path = tmp_path / "test_index.json"

    indexer = Indexer()
    indexer.build_index([page])
    indexer.save_index(file_path)

    new_indexer = Indexer()
    loaded_index = new_indexer.load_index(file_path)

    assert "love" in loaded_index
    assert "wisdom" in loaded_index
    assert loaded_index["love"]["page1"]["frequency"] == 1