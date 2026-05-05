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