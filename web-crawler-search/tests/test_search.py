from src.search import SearchEngine

def sample_index():
    return {
        "good": {
            "page1": {"frequency": 2, "positions": [0, 4]},
            "page2": {"frequency": 1, "positions": [3]},
        },
        "friends": {
            "page1": {"frequency": 1, "positions": [1]},
            "page3": {"frequency": 5, "positions": [2, 5, 8, 10, 12]},
        },
        "love": {
            "page2": {"frequency": 4, "positions": [1, 2, 3, 4]},
        },
    }

def test_print_existing_word():
    search_engine = SearchEngine(sample_index())
    result = search_engine.print_word("good")
    assert "page1" in result
    assert "page2" in result

def test_print_nonexistent_word():
    search_engine = SearchEngine(sample_index())
    result = search_engine.print_word("unknown")
    assert result == "No results found for 'unknown'."

def test_find_single_word():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("love")
    assert len(results) == 1
    assert results[0]["url"] == "page2"
    assert results[0]["score"] > 0

def test_find_multi_word_query_requires_all_terms():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("good friends")
    assert len(results) == 1
    assert results[0]["url"] == "page1"

def test_find_empty_query():
    search_engine = SearchEngine(sample_index())
    result = search_engine.find("")
    assert result == "Please provide a search query."

def test_find_nonexistent_word():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("notreal")
    assert results == []
    
def test_search_case_insensitive():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("LOVE")
    assert len(results) == 1
    assert results[0]["url"] == "page2"

def test_partial_word_not_matched():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("lov")
    assert results == []

def test_ranking_order():
    index = {
        "love": {
            "page1": {"frequency": 1, "positions": [1]},
            "page2": {"frequency": 5, "positions": [1, 2, 3, 4, 5]}
        }
    }

    search_engine = SearchEngine(index)
    results = search_engine.find("love")
    assert results[0]["url"] == "page2"
    
def test_find_multi_word_no_common_page():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("friends love")
    assert results == []

def test_print_empty_word():
    search_engine = SearchEngine(sample_index())
    result = search_engine.print_word("")
    assert result == "Please provide a word to print."

def test_find_query_with_extra_spaces():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("   love   ")
    assert len(results) == 1
    assert results[0]["url"] == "page2"
    
def test_find_empty_index():
    search_engine = SearchEngine({})
    results = search_engine.find("love")
    assert results == []

def test_print_empty_index():
    search_engine = SearchEngine({})
    result = search_engine.print_word("love")
    assert result == "No results found for 'love'."

def test_find_repeated_query_terms():
    search_engine = SearchEngine(sample_index())
    results = search_engine.find("love love")
    assert len(results) == 1
    assert results[0]["url"] == "page2"

def test_get_all_pages():
    search_engine = SearchEngine(sample_index())
    pages = search_engine.get_all_pages()
    assert "page1" in pages
    assert "page2" in pages
    assert "page3" in pages


def test_calculate_idf_known_word():
    search_engine = SearchEngine(sample_index())
    idf = search_engine.calculate_idf("love")
    assert idf > 0


def test_calculate_idf_unknown_word():
    search_engine = SearchEngine(sample_index())
    idf = search_engine.calculate_idf("unknown")
    assert idf == 0