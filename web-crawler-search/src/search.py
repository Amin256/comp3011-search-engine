import math

class SearchEngine:
    # Search engine that uses an inverted index
    def __init__(self, index = None):
        if index is not None:
            self.index = index
        else:
            self.index = {}

    # Set or update the active index
    def set_index(self, index):
        self.index = index

    # Get all page URLs stored in the index
    def get_all_pages(self):
        pages = set()

        for postings in self.index.values():
            pages.update(postings.keys())

        return pages

    # Print inverted index entry for a word
    def print_word(self, word):
        word = word.lower().strip()

        if not word:
            return "Please provide a word to print."

        if word not in self.index:
            return f"No results found for '{word}'."

        return self.index[word]

    # Calculate IDF score
    def calculate_idf(self, word):
        total_pages = len(self.get_all_pages())

        if total_pages == 0 or word not in self.index:
            return 0

        pages_containing_word = len(self.index[word])

        return math.log((total_pages + 1) / (pages_containing_word + 1)) + 1

    # Find pages containing all query terms and rank using TF-IDF
    def find(self, query):
        query = query.lower().strip()

        if not query:
            return "Please provide a search query."

        terms = query.split()

        for term in terms:
            if term not in self.index:
                return []

        matching_pages = set(self.index[terms[0]].keys())

        for term in terms[1:]:
            matching_pages = matching_pages.intersection(
                set(self.index[term].keys())
            )

        ranked_results = []

        for page in matching_pages:
            score = 0

            for term in terms:
                term_frequency = self.index[term][page]["frequency"]
                inverse_document_frequency = self.calculate_idf(term)
                score += term_frequency * inverse_document_frequency

            ranked_results.append({
                "url": page,
                "score": round(score, 4)
            })

        ranked_results.sort(key = lambda result: result["score"], reverse = True)

        return ranked_results