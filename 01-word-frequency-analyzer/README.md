# Project 1: Word Frequency Analyzer

## What Is This?

A Python program that reads any text file and tells you which words appear most often, with a visual bar chart in the terminal.

Great for analysing book chapters, news articles, or your own essays.

---

## What Skills You Will Learn

- Reading and processing files in Python
- Cleaning text with regular expressions (`re` module)
- Using `collections.Counter` to count efficiently
- Filtering stop words (common words like "the", "is", "and")
- Accepting command-line arguments with `sys.argv`
- Displaying data visually in the terminal

---

## How the Program Works

```
Text file (chapter.txt)
        │
        ▼
   Read entire file into a string
        │
        ▼
   Clean text — lowercase + remove punctuation (regex)
        │
        ▼
   Split into individual words
        │
        ▼
   Filter out stop words ("the", "is", "and", ...)
        │
        ▼
   Count word frequency using Counter
        │
        ▼
   Pick top N words
        │
        ▼
   Display as ranked table with bar chart
```

---

## Folder Structure

```
01-word-frequency-analyzer/
├── analyzer.py              ← Main program (all logic here)
├── sample_texts/
│   └── chapter.txt          ← Sample text (classic literature + quotes)
└── README.md
```

---

## Requirements

- Python 3.7 or higher
- No external libraries needed — uses only the Python standard library

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 01-word-frequency-analyzer
```

### Step 2 — Run with the included sample text

```bash
python analyzer.py
```

### Step 3 — Run with your own text file

```bash
python analyzer.py path/to/your_file.txt
```

### Step 4 — Change how many top words to show (default is 10)

```bash
python analyzer.py sample_texts/chapter.txt 20
```

### Step 5 — Include stop words (show "the", "is", "and" etc.)

```bash
python analyzer.py sample_texts/chapter.txt 10 false
```

---

## Expected Output

```
==================================================
  Word Frequency Analysis
  File: sample_texts/chapter.txt
==================================================
  Total words (after filtering): 153
  Unique words:                  114
  Showing top 10 most frequent words:
--------------------------------------------------
  Rank   Word                 Count      Bar
--------------------------------------------------
  1      time                 7          #########################
  2      read                 4          ##############
  3      mind                 4          ##############
  4      before               3          ##########
  5      learning             3          ##########
  6      end                  3          ##########
  7      man                  3          ##########
  8      life                 3          ##########
  9      times                2          #######
  10     worst                2          #######
==================================================
```

---

## How the Code Works

### Cleaning text with regex

```python
import re

def clean_text(text):
    text = text.lower()                    # "Hello World" → "hello world"
    text = re.sub(r"[^a-z\s]", "", text)  # remove punctuation and numbers
    return text
```

`re.sub(r"[^a-z\s]", "", text)` keeps only lowercase letters and spaces — everything else (commas, periods, digits) is removed.

### Counting words

```python
from collections import Counter

words = cleaned.split()
counter = Counter(words)
top_10 = counter.most_common(10)
# → [("time", 7), ("read", 4), ("mind", 4), ...]
```

`Counter` is a dictionary that automatically counts how many times each item appears in a list.

### Drawing the bar chart

```python
max_count = results[0][1]   # highest count (first result)
bar_length = int((count / max_count) * 25)
bar = "#" * bar_length      # e.g., "#########################"
```

The bar length is proportional to the word's count relative to the most frequent word.

---

## Try It Yourself — Extension Ideas

- Paste any news article into a `.txt` file and analyse it
- Add words to the `STOP_WORDS` set in `analyzer.py` to ignore more common words
- Analyse two different files and compare which words differ
- Export results to a CSV file using Python's `csv` module

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Wrong file path | Check the spelling and path — run from inside the project folder |
| `UnicodeDecodeError` | File has special characters | Add `encoding='latin-1'` to the `open()` call in `analyzer.py` |
| Empty output | All words filtered as stop words | Run with third argument `false` to include stop words |
| `python: command not found` | Python not installed or wrong command | Try `python3 analyzer.py` instead |
