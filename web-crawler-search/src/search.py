from collections import defaultdict

class SearchEngine:
    # Search engine that uses inverted index
    def __init__(self, index = None):
        if index is not None:
            self.index = index
        else:
            self.index = {}

    # Set or update the active index
    def set_index(self, index):
        self.index = index

    # Print the inverted index entry for a word
    def print_word(self, word):
        word = word.lower().strip()

        if not word:
            return "Please provide a word to print."

        if word not in self.index:
            return f"No results found for '{word}'."

        return self.index[word]

    # Find pages containing all query terms
    def find(self, query):
        query = query.lower().strip()

        if not query:
            return "Please provide a search query."

        terms = query.split()

        # Check if every query term exists in the index
        for term in terms:
            if term not in self.index:
                return []

        # Start with pages for the first term
        matching_pages = set(self.index[terms[0]].keys())

        # Intersect with pages for the remaining terms
        for term in terms[1:]:
            matching_pages = matching_pages.intersection(
                set(self.index[term].keys())
            )

        # Rank by total frequency of query terms
        ranked_results = []

        for page in matching_pages:
            score = 0

            for term in terms:
                score += self.index[term][page]["frequency"]

            ranked_results.append({
                "url": page,
                "score": score
            })

        ranked_results.sort(key = lambda result: result["score"], reverse = True)

        return ranked_results