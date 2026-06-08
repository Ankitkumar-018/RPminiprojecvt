# Project 1: Word Frequency Analyzer — Approach & Planning

---

## Part A: Filled Example
> Read this before you start coding. This is how an experienced developer thinks through the problem.

---

### Step 1 — Understand the Problem

Before writing a single line of code, ask yourself:

**What exactly does this program need to do?**
- Read a text file from disk
- Split the text into individual words
- Count how many times each word appears
- Show the top N most frequent words

**What are the inputs and outputs?**
- Input: a `.txt` file path (from the user)
- Output: a ranked list of words with counts, printed to the terminal

**What edge cases should I think about?**
- What if the file doesn't exist?
- What if the file is empty?
- Should "The" and "the" count as the same word? (yes — lowercase everything)
- Should "hello!" and "hello" count as the same word? (yes — remove punctuation)
- Words like "the", "is", "and" will always be most frequent — do we want them? (no — filter them)

---

### Step 2 — Questions to Ask Before Writing Code

- Do I need any external library, or can I use Python's standard library?
  → `collections.Counter` does the counting. `re` does the cleaning. No pip install needed.

- What's the best data structure to count word frequency?
  → A dictionary `{word: count}`. Python's `Counter` is a dictionary that does this automatically.

- How do I make the bar chart scale correctly?
  → Find the max count first, then make every bar proportional to that max.

- How do I accept command-line arguments?
  → `sys.argv` — `sys.argv[0]` is the script name, `sys.argv[1]` is the first argument.

---

### Step 3 — Pseudo Code

```
START

  Get file path from command-line argument (default: sample_texts/chapter.txt)
  Get top_n from argument (default: 10)
  Get remove_stopwords from argument (default: True)

  OPEN the file
    READ all text into a string
  CLOSE the file

  FUNCTION clean_text(text):
    convert text to lowercase
    remove all characters that are NOT letters or spaces (using regex)
    return cleaned text

  words = split cleaned text by spaces

  IF remove_stopwords is True:
    words = [word for word in words if word NOT IN stop_words set]

  counter = Count frequency of each word in words list

  top_results = get top_n most common (word, count) pairs from counter

  PRINT header with file name, total words, unique words

  FOR each (rank, word, count) in top_results:
    calculate bar_length = (count / max_count) * 25
    bar = "#" repeated bar_length times
    PRINT rank, word, count, bar

END
```

---

### Step 4 — Think About the Order of Functions

```
main()
  └── get_word_frequencies(filepath, top_n, remove_stopwords)
        └── clean_text(text)         ← called inside
  └── display_results(results, ...)
```

Build and test bottom-up:
1. Write `clean_text()` and test it alone
2. Write the counting logic and test with a small string
3. Wire everything together in `main()`

---

### Step 5 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| File not found | `try/except FileNotFoundError` — print error and exit |
| File has special characters | Open with `encoding='utf-8'` or `'latin-1'` |
| All words are stop words | Output nothing — warn the user |
| top_n is larger than unique word count | `most_common(n)` handles this — returns whatever is available |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start coding. Submit this as part of your assignment.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Understand the Problem

**In your own words, what does this program do?**

```
Write here:


```

**What are the inputs?**

```
Write here:


```

**What are the outputs?**

```
Write here:


```

**What edge cases can you think of?**

```
Write here (at least 3):
1.
2.
3.
```

---

### Step 2 — Questions You Have Before Starting

```
Write at least 2 questions you want answered before coding:
1.
2.
3.
```

---

### Step 3 — Your Pseudo Code

```
Write your own pseudo code here (plain English steps, no actual Python):




```

---

### Step 4 — What data structure will you use to count words, and why?

```
Write here:


```

---

### Step 5 — What could go wrong? How will you handle it?

```
Risk 1:
How to handle:

Risk 2:
How to handle:
```

---

### Step 6 — After finishing, reflect

**What was the hardest part?**
```

```

**What would you do differently next time?**
```

```

**What did the AI suggest that you changed or improved?**
```

```
