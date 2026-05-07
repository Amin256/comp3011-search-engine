from src.crawler import Crawler
from src.indexer import Indexer
from src.search import SearchEngine

def show_help():
    print("\nAvailable commands:")
    print("build: Crawl website and build index")
    print("load: Load index from file")
    print("print <word>: Print inverted index for a word")
    print("find <query>: Find pages containing query terms")
    print("help: Show available commands")
    print("exit: Exit the search tool\n")

def main():
    indexer = Indexer()
    search_engine = SearchEngine()

    print("COMP3011 Search Engine Tool")
    print("Type 'help' to see available commands.")

    while True:
        command = input("> ").strip()

        if not command:
            print("Please enter a command.")
            continue

        parts = command.split(maxsplit = 1)
        action = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if action == "build":
            crawler = Crawler()
            pages = crawler.crawl()

            index = indexer.build_index(pages)
            indexer.save_index()

            search_engine.set_index(index)

            print(f"Build complete. Indexed {len(pages)} pages.")

        elif action == "load":
            index = indexer.load_index()
            search_engine.set_index(index)

            print("Index loaded and ready for searching.")

        elif action == "print":
            result = search_engine.print_word(argument)
            print(result)

        elif action == "find":
            results = search_engine.find(argument)

            if isinstance(results, str):
                print(results)

            elif not results:
                print("No matching pages found.")

            else:
                print("Matching pages:")
                for result in results:
                    print(f"- {result['url']} (score: {result['score']})")

        elif action == "help":
            show_help()

        elif action == "exit":
            print("Exiting search tool.")
            break

        else:
            print("Unknown command. Type 'help' to see available commands.")

if __name__ == "__main__":
    main()