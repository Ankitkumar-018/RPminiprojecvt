# Project 2: Instant Autocomplete — Approach & Planning

---

## Part A: Filled Example
> Read this before you start coding. This is how an experienced developer thinks through the problem.

---

### Step 1 — Understand the Problem

**What exactly does this program need to do?**
- Load a list of city names from a file
- Accept a prefix typed by the user (e.g., "Ban")
- Return all cities that start with that prefix — instantly

**What are the inputs and outputs?**
- Input: a prefix string typed by the user
- Output: a list of matching city names + time taken

**What does "instant" mean?**
- The constraint says it must work on 10,000+ entries
- A simple loop through the list would work for 100 entries but gets slow at 10,000+
- We need a smarter data structure

---

### Step 2 — Questions to Ask Before Writing Code

- **Why not just use a list and loop through it?**
  → For 10,000 words, every search loops through all 10,000. For prefix "B", you check every word. A Trie goes directly to the "B" branch — much faster.

- **What is a Trie?**
  → A tree where each node is one character. To insert "Mumbai", you create nodes: M → u → m → b → a → i. To search "Mu", you walk M → u and collect everything below.

- **What do I store at each node?**
  → Its children (a dictionary of characters), a flag `is_end` to mark complete words, and `full_word` to preserve the original casing.

- **How do I collect all words under a prefix node?**
  → Depth-first traversal: visit a node, if `is_end` add to results, then recurse into all children.

---

### Step 3 — Pseudo Code

```
START

  DEFINE TrieNode:
    children = empty dictionary
    is_end = False
    full_word = None

  DEFINE Trie:

    FUNCTION insert(word):
      node = root
      FOR each character in word.lowercase():
        IF character not in node.children:
          create new TrieNode at node.children[character]
        move node = node.children[character]
      mark node.is_end = True
      store node.full_word = word   ← original casing

    FUNCTION search(prefix, limit=10):
      node = root
      FOR each character in prefix.lowercase():
        IF character not in node.children:
          RETURN []    ← prefix doesn't exist
        move node = node.children[character]
      results = []
      collect_words(node, results, limit)
      RETURN results

    FUNCTION collect_words(node, results, limit):
      IF results are full: RETURN
      IF node.is_end: add node.full_word to results
      FOR each child in node.children:
        collect_words(child, results, limit)

  LOAD cities from file
  INSERT each city into Trie

  LOOP:
    prefix = get input from user
    start_time = now()
    results = trie.search(prefix)
    elapsed = now() - start_time
    PRINT results and elapsed time

END
```

---

### Step 4 — Think About the Structure

```
trie.py
  ├── class TrieNode     ← one node in the tree
  └── class Trie
        ├── insert()     ← build the tree
        ├── search()     ← find prefix, then collect
        └── _collect_words()  ← recursive helper

autocomplete.py
  ├── load_trie()        ← reads file, builds trie
  ├── benchmark()        ← measures average search time
  ├── interactive_mode() ← live user input
  └── demo_mode()        ← automated test with timing
```

Split into two files: data structure logic in `trie.py`, application logic in `autocomplete.py`.

---

### Step 5 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| City not found (prefix has no match) | `search()` returns `[]` — display "no results" |
| User types uppercase, city stored lowercase | Always lowercase the prefix before searching |
| File is empty | `total_words` will be 0 — print a warning |
| Limit is larger than results | `_collect_words` stops when results are full, not when limit hit |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start coding.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Understand the Problem

**In your own words, what does this program do?**

```
Write here:


```

**What does "instant" mean in the context of this project?**

```
Write here:


```

**Why is a simple list + loop not good enough here?**

```
Write here:


```

---

### Step 2 — Questions You Have Before Starting

```
Write at least 2 questions:
1.
2.
3.
```

---

### Step 3 — Draw the Trie

Draw the Trie after inserting: "Delhi", "Dehradun", "Bengaluru"

```
Draw here (use text art like the example in the README):


root
└── ...
```

---

### Step 4 — Your Pseudo Code

```
Write pseudo code for the search() function only:




```

---

### Step 5 — What is the time complexity of Trie search vs linear search?

```
Linear search (loop through list): O( ? )
Trie search: O( ? )
Explain in your own words:


```

---

### Step 6 — After finishing, reflect

**What was the hardest part to implement?**
```

```

**What happens if you type a full city name as the prefix? Does it still work?**
```

```

**What would you add if you had more time?**
```

```
