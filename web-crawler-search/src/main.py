from crawler import Crawler
from indexer import Indexer

def main():
    crawler = Crawler()
    pages = crawler.crawl(max_pages = 2)

    indexer = Indexer()
    indexer.build_index(pages)
    indexer.save_index()

    result = indexer.print_word("love")
    print(result)

if __name__ == "__main__":
    main()