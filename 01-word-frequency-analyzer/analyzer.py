import re
import sys
from collections import Counter

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "be", "was", "are", "were",
    "that", "this", "not", "we", "all", "he", "she", "they", "have", "has",
    "had", "do", "did", "will", "would", "could", "should", "what", "who",
    "which", "when", "where", "how", "no", "as", "if", "i", "you", "his",
    "her", "its", "our", "their", "there", "than", "more", "so", "over",
    "us", "him", "me", "my", "your", "its", "does", "been", "being", "each"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


def get_word_frequencies(filepath, top_n=10, remove_stopwords=True):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    cleaned = clean_text(text)
    words = cleaned.split()

    if remove_stopwords:
        words = [w for w in words if w not in STOP_WORDS and len(w) > 2]

    counter = Counter(words)
    return counter.most_common(top_n), len(words), len(counter)


def display_results(results, total_words, unique_words, filepath, top_n):
    print("\n" + "=" * 50)
    print(f"  Word Frequency Analysis")
    print(f"  File: {filepath}")
    print("=" * 50)
    print(f"  Total words (after filtering): {total_words}")
    print(f"  Unique words:                  {unique_words}")
    print(f"  Showing top {top_n} most frequent words:")
    print("-" * 50)
    print(f"  {'Rank':<6} {'Word':<20} {'Count':<10} {'Bar'}")
    print("-" * 50)

    max_count = results[0][1] if results else 1
    for rank, (word, count) in enumerate(results, 1):
        bar_length = int((count / max_count) * 25)
        bar = "#" * bar_length
        print(f"  {rank:<6} {word:<20} {count:<10} {bar}")

    print("=" * 50 + "\n")


def main():
    # Default values
    filepath = "sample_texts/chapter.txt"
    top_n = 10
    remove_stopwords = True

    # Allow command-line arguments
    args = sys.argv[1:]
    if len(args) >= 1:
        filepath = args[0]
    if len(args) >= 2:
        top_n = int(args[1])
    if len(args) >= 3:
        remove_stopwords = args[2].lower() != "false"

    results, total_words, unique_words = get_word_frequencies(
        filepath, top_n, remove_stopwords
    )
    display_results(results, total_words, unique_words, filepath, top_n)


if __name__ == "__main__":
    main()
