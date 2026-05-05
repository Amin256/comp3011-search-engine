from bs4 import BeautifulSoup
from src.crawler import Crawler

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