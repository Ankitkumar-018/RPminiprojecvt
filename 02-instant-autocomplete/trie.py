class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.full_word = None


class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.total_words = 0

    def insert(self, word):
        node = self.root
        for char in word.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.full_word = word  # preserve original casing
        self.total_words += 1

    def _collect_words(self, node, results, limit):
        if len(results) >= limit:
            return
        if node.is_end:
            results.append(node.full_word)
        for child in node.children.values():
            if len(results) >= limit:
                return
            self._collect_words(child, results, limit)

    def search(self, prefix, limit=10):
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
        results = []
        self._collect_words(node, results, limit)
        return results

    def load_from_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip()
                if word:
                    self.insert(word)
