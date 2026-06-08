# Project 2: Instant Autocomplete

## What Is This?

A type-ahead suggestion system — like the search bar on Google or Swiggy — built using a **Trie** data structure. You type a prefix and it instantly returns all matching entries.

Works on 10,000+ entries and still responds in under **1 millisecond** per query.

---

## What Skills You Will Learn

- Trie data structure — how to build one from scratch (`TrieNode` + `Trie` class)
- Why Tries beat linear search for prefix lookups
- Reading data from files and building an in-memory index
- Measuring performance with `time.perf_counter()`
- Building an interactive terminal program

---

## How the System Works

```
Load cities from file (indian_cities.txt)
        │
        ▼
   Insert each city into the Trie
   (one character per node, letter by letter)
        │
        ▼
   User types a prefix  e.g., "Ban"
        │
        ▼
   Walk Trie: root → b → a → n
        │
        ▼
   Collect all words under that node
   (depth-first traversal)
        │
        ▼
   Return top matches + time taken
```

---

## Folder Structure

```
02-instant-autocomplete/
├── trie.py              ← Trie data structure (TrieNode + Trie class)
├── autocomplete.py      ← Main program (interactive + demo mode)
├── data/
│   └── indian_cities.txt   ← 189 Indian cities dataset
└── README.md
```

---

## Requirements

- Python 3.7 or higher
- No external libraries needed — pure Python

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 02-instant-autocomplete
```

### Step 2 — Run in interactive mode (live search)

```bash
python autocomplete.py
```

### Step 3 — Run in demo mode (preset searches with timing benchmarks)

```bash
python autocomplete.py data/indian_cities.txt demo
```

### Step 4 — Use your own dataset

Create a `.txt` file with one word per line, then run:

```bash
python autocomplete.py data/my_words.txt
```

---

## Expected Output — Interactive Mode

```
Loaded 189 entries in 0.69 ms

Type a prefix to search (press Ctrl+C to exit):

Search > Ban
  Suggestions for 'Ban':
    1. Bangalore
    2. Baranagar
    3. Bathinda

  [3 results in 0.031 ms]

Search > Ko
  Suggestions for 'Ko':
    1. Kolkata
    2. Kolhapur
    3. Kollam
    4. Kota
    5. Kochi

  [5 results in 0.046 ms]
```

---

## Expected Output — Demo Mode

```
Loaded 189 entries in 0.69 ms

--- DEMO: Autocomplete Results ---

  Prefix 'M' -> ['Mumbai', 'Muzaffarnagar', 'Muzaffarpur', 'Meerut', 'Madurai']
           Avg search time over 500 runs: 0.0087 ms

  Prefix 'Ban' -> ['Bangalore']
           Avg search time over 500 runs: 0.0014 ms

  Prefix 'Del' -> ['Delhi']
           Avg search time over 500 runs: 0.0008 ms
```

---

## How the Trie Works

### Inserting words

```
Insert "Mumbai", "Mysore", "Meerut":

root
└── m
    ├── u → m → b → a → i  [END: "Mumbai"]
    ├── y → s → o → r → e  [END: "Mysore"]
    └── e → e → r → u → t  [END: "Meerut"]
```

### Searching by prefix

```python
def search(self, prefix, limit=10):
    node = self.root
    for char in prefix.lower():
        if char not in node.children:
            return []          # prefix not found → no results
        node = node.children[char]
    results = []
    self._collect_words(node, results, limit)   # collect everything below
    return results
```

Search prefix `"my"` → walk to root → m → y → collect everything below → `["Mysore"]`

### Why Trie is faster than a list

| Approach | Steps to search "Ban" in 10,000 words |
|----------|---------------------------------------|
| Linear scan (`for word in list`) | Up to 10,000 comparisons |
| Trie | Exactly 3 steps (one per character) then collect |

---

## Key Design Decisions Explained

### Why store `full_word` on the end node?

Cities like `"Pimpri-Chinchwad"` have hyphens and mixed case. We insert the lowercased version letter-by-letter (for matching), but store the **original casing** on the terminal node so the display is correct.

```python
node.is_end = True
node.full_word = word   # preserves "Mumbai" not "mumbai"
```

---

## Try It Yourself — Extension Ideas

- Add Bollywood movie titles as a dataset (one title per line)
- Add a frequency/popularity score so more popular cities appear first
- Try building a simple web autocomplete with Flask + JavaScript
- Add fuzzy matching to handle typos (e.g., "Bangalre" → "Bangalore")

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Wrong path to data file | Use `data/indian_cities.txt` exactly as shown |
| `ModuleNotFoundError: trie` | Running from the wrong folder | Make sure you are inside `02-instant-autocomplete/` |
| No suggestions showing | Prefix case mismatch | Trie is case-insensitive — try typing with capital first letter |
| `python: command not found` | Python not in PATH | Try `python3 autocomplete.py` |
