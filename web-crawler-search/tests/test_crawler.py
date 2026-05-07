from bs4 import BeautifulSoup
from src.crawler import Crawler
from unittest.mock import Mock, patch
import requests

def test_extract_page_text_from_quote_html():
    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“Test quote.”</span>
                <small class="author">Test Author</small>
                <a class="tag">testing</a>
            </div>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    crawler = Crawler(delay = 0)
    text = crawler.extract_page_text(soup)
    assert "Test quote" in text
    assert "Test Author" in text
    assert "testing" in text

def test_find_next_page():
    html = """
    <html>
        <body>
            <li class="next">
                <a href="/page/2/">Next</a>
            </li>
        </body>
    </html>
    """
    soup = BeautifulSoup(html, "html.parser")
    crawler = Crawler(delay = 0)
    next_url = crawler.find_next_page(soup, "https://quotes.toscrape.com/")
    assert next_url == "https://quotes.toscrape.com/page/2/"

def test_find_next_page_returns_none_when_missing():
    html = "<html><body><p>No next page</p></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    crawler = Crawler(delay = 0)
    next_url = crawler.find_next_page(soup, "https://quotes.toscrape.com/")
    assert next_url is None

def test_extract_page_text_multiple_quotes():
    html = """
    <html>
        <body>
            <div class="quote">
                <span class="text">“First quote.”</span>
                <small class="author">Author One</small>
                <a class="tag">life</a>
            </div>
            <div class="quote">
                <span class="text">“Second quote.”</span>
                <small class="author">Author Two</small>
                <a class="tag">wisdom</a>
            </div>
        </body>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    crawler = Crawler(delay=0)
    text = crawler.extract_page_text(soup)

    assert "First quote" in text
    assert "Author One" in text
    assert "life" in text
    assert "Second quote" in text
    assert "Author Two" in text
    assert "wisdom" in text

def test_extract_page_text_empty_page():
    html = "<html><body><p>No quotes here</p></body></html>"

    soup = BeautifulSoup(html, "html.parser")
    crawler = Crawler(delay=0)
    text = crawler.extract_page_text(soup)

    assert text == ""

@patch("src.crawler.requests.get")
def test_fetch_page_success(mock_get):
    mock_response = Mock()
    mock_response.text = "<html><title>Test Page</title></html>"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    crawler = Crawler(delay=0)
    soup = crawler.fetch_page("https://quotes.toscrape.com/")

    assert soup.title.text == "Test Page"

@patch("src.crawler.requests.get")
def test_fetch_page_failure_returns_none(mock_get):
    mock_get.side_effect = requests.RequestException("Network error")

    crawler = Crawler(delay=0)
    soup = crawler.fetch_page("https://quotes.toscrape.com/")

    assert soup is None
    
@patch("src.crawler.time.sleep")
@patch.object(Crawler, "fetch_page")
def test_crawl_collects_multiple_pages(mock_fetch_page, mock_sleep):
    page1_html = """
    <html>
        <title>Page 1</title>
        <body>
            <div class="quote">
                <span class="text">“First quote.”</span>
                <small class="author">Author One</small>
            </div>
            <li class="next"><a href="/page/2/">Next</a></li>
        </body>
    </html>
    """

    page2_html = """
    <html>
        <title>Page 2</title>
        <body>
            <div class="quote">
                <span class="text">“Second quote.”</span>
                <small class="author">Author Two</small>
            </div>
        </body>
    </html>
    """

    mock_fetch_page.side_effect = [
        BeautifulSoup(page1_html, "html.parser"),
        BeautifulSoup(page2_html, "html.parser")
    ]

    crawler = Crawler(delay=0)
    pages = crawler.crawl()

    assert len(pages) == 2
    assert pages[0].url == "https://quotes.toscrape.com/"
    assert pages[1].url == "https://quotes.toscrape.com/page/2/"
    assert "First quote" in pages[0].text
    assert "Second quote" in pages[1].text