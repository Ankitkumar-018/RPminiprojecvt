import time
import sys
from trie import Trie


def load_trie(filepath):
    trie = Trie()
    start = time.perf_counter()
    trie.load_from_file(filepath)
    elapsed = (time.perf_counter() - start) * 1000
    print(f"Loaded {trie.total_words} entries in {elapsed:.2f} ms")
    return trie


def benchmark(trie, prefix, runs=1000):
    start = time.perf_counter()
    for _ in range(runs):
        trie.search(prefix, limit=10)
    elapsed = (time.perf_counter() - start) * 1000
    avg = elapsed / runs
    return avg


def interactive_mode(trie):
    print("\nType a prefix to search (press Ctrl+C to exit):\n")
    while True:
        try:
            prefix = input("Search > ").strip()
            if not prefix:
                continue

            start = time.perf_counter()
            results = trie.search(prefix, limit=10)
            elapsed = (time.perf_counter() - start) * 1000

            if results:
                print(f"\n  Suggestions for '{prefix}':")
                for i, r in enumerate(results, 1):
                    print(f"    {i}. {r}")
                print(f"\n  [{len(results)} results in {elapsed:.3f} ms]\n")
            else:
                print(f"  No matches found for '{prefix}'\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


def demo_mode(trie):
    test_prefixes = ["M", "Ban", "Hyd", "Del", "Ko", "Ja", "Ra", "Vi", "Na", "Ch"]
    print("\n--- DEMO: Autocomplete Results ---\n")
    for prefix in test_prefixes:
        results = trie.search(prefix, limit=5)
        avg_ms = benchmark(trie, prefix, runs=500)
        print(f"  Prefix '{prefix}' -> {results}")
        print(f"           Avg search time over 500 runs: {avg_ms:.4f} ms")
        print()


def main():
    filepath = "data/indian_cities.txt"
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]

    trie = load_trie(filepath)

    mode = sys.argv[2] if len(sys.argv) >= 3 else "interactive"

    if mode == "demo":
        demo_mode(trie)
    else:
        interactive_mode(trie)


if __name__ == "__main__":
    main()
