import time
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com/"
POLITENESS_DELAY = 6

@dataclass
class CrawledPage:
    url: str
    title: str
    text: str

class Crawler:
    # Crawler for quotes.toscrape.com
    def __init__(self, base_url: str = BASE_URL, delay: int = POLITENESS_DELAY):
        self.base_url = base_url
        self.delay = delay
        self.visited_urls = set()

    # Fetch a page and return a BeautifulSoup object
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        try:
            print(f"Crawling: {url}")

            response = requests.get(url, timeout=10)
            response.raise_for_status()

            return BeautifulSoup(response.text, "html.parser")

        except requests.RequestException as error:
            print(f"Error fetching {url}: {error}")
            return None

    # Extract quote text, authors and tags from a page
    def extract_page_text(self, soup: BeautifulSoup) -> str:
        text_parts = []

        quotes = soup.find_all("div", class_ = "quote")

        for quote in quotes:
            quote_text = quote.find("span", class_ = "text")
            author = quote.find("small", class_ = "author")
            tags = quote.find_all("a", class_ = "tag")

            if quote_text:
                text_parts.append(quote_text.get_text(" ", strip = True))

            if author:
                text_parts.append(author.get_text(" ", strip = True))

            for tag in tags:
                text_parts.append(tag.get_text(" ", strip = True))

        return " ".join(text_parts)

    # Find the next page link
    def find_next_page(self, soup: BeautifulSoup, current_url: str) -> Optional[str]:
        next_link = soup.select_one("li.next a")

        if not next_link:
            return None

        next_href = next_link.get("href")
        return urljoin(current_url, next_href)

    # Crawl pages until there are no more pages
    def crawl(self, max_pages: Optional[int] = None) -> List[CrawledPage]:
        pages = []
        current_url = self.base_url

        while current_url and current_url not in self.visited_urls:
            if max_pages is not None and len(pages) >= max_pages:
                break

            self.visited_urls.add(current_url)

            soup = self.fetch_page(current_url)

            if soup is None:
                break

            title = soup.title.get_text(strip=True) if soup.title else "No title"
            text = self.extract_page_text(soup)

            pages.append(
                CrawledPage(
                    url=current_url,
                    title=title,
                    text=text
                )
            )

            next_url = self.find_next_page(soup, current_url)

            if next_url:
                print(f"Waiting {self.delay} seconds before next request...")
                time.sleep(self.delay)

            current_url = next_url

        return pages


if __name__ == "__main__":
    crawler = Crawler()
    crawled_pages = crawler.crawl()

    print(f"\nCrawled {len(crawled_pages)} pages.")

    for page in crawled_pages:
        print(page.url)