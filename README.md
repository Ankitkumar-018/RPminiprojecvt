# Mini Projects — Student Edition

Four standalone projects covering Python fundamentals, data structures, SQL, and AI-assisted development. Each project is self-contained with its own README, code, and sample data.

---

## Projects Overview

| # | Project | Key Skill | Time Estimate |
|---|---------|-----------|---------------|
| 1 | [Word Frequency Analyzer](01-word-frequency-analyzer/) | Python + File Handling | 1–2 hours |
| 2 | [Instant Autocomplete](02-instant-autocomplete/) | Data Structures (Trie) | 2–3 hours |
| 3 | [Streaming Service DB](03-streaming-service-db/) | SQL + Schema Design | 2–3 hours |
| 4 | [AI Pair-Programmed Endpoint](04-ai-pair-programmed-endpoint/) | REST API + AI Tools | 3–4 hours |

---

## Project 1: Word Frequency Analyzer

**What it does:** Reads any text file and reports the most common words with a visual bar chart.

**What you learn:** File I/O, regex, `collections.Counter`, command-line arguments

**Run it:**
```bash
cd 01-word-frequency-analyzer
python analyzer.py
```

**Sample output:**
```
  Rank   Word                 Count      Bar
  1      time                 7          #########################
  2      read                 5          ##################
  3      life                 4          ##############
```

> Full details: [01-word-frequency-analyzer/README.md](01-word-frequency-analyzer/README.md)

---

## Project 2: Instant Autocomplete

**What it does:** Type a prefix (e.g. "Ban") and instantly get matching Indian cities — stays fast on 10,000+ entries.

**What you learn:** Trie data structure, why it beats linear search, performance benchmarking

**Run it:**
```bash
cd 02-instant-autocomplete
python autocomplete.py
```

**Sample output:**
```
Search > Ban
  Suggestions for 'Ban':
    1. Bangalore
    2. Baranagar
    3. Bathinda
  [3 results in 0.031 ms]
```

> Full details: [02-instant-autocomplete/README.md](02-instant-autocomplete/README.md)

---

## Project 3: Streaming Service Database

**What it does:** Full database design for a Hotstar/Netflix-style app with 12 SQL queries — including a recommendation engine.

**What you learn:** Schema design, foreign keys, JOIN, GROUP BY, subqueries, recommendation logic

**Run it:**
```bash
cd 03-streaming-service-db
python run_queries.py
```

**Includes:** 10 users, 15 Indian movies/series, watch history, ratings, watchlists

> Full details: [03-streaming-service-db/README.md](03-streaming-service-db/README.md)

---

## Project 4: AI Pair-Programmed REST API

**What it does:** A Task Manager API with 6 endpoints, 25+ tests, and a log documenting where AI helped and where it was wrong.

**What you learn:** REST API design, Flask, pytest, critically reviewing AI-generated code

**Run it:**
```bash
cd 04-ai-pair-programmed-endpoint
pip install -r requirements.txt
python app.py
```

**Then test:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Study Flask", "priority": "high"}'
```

> Full details: [04-ai-pair-programmed-endpoint/README.md](04-ai-pair-programmed-endpoint/README.md)

---

## Requirements

- **Python 3.7+** — required for all projects
- **SQLite3** — built into Python, required for Project 3
- **Flask + pytest** — required for Project 4 only (`pip install -r requirements.txt`)

---

## Folder Structure

```
Project/
├── README.md                            ← You are here
├── 01-word-frequency-analyzer/
│   ├── analyzer.py
│   ├── sample_texts/chapter.txt
│   └── README.md
├── 02-instant-autocomplete/
│   ├── trie.py
│   ├── autocomplete.py
│   ├── data/indian_cities.txt
│   └── README.md
├── 03-streaming-service-db/
│   ├── schema.sql
│   ├── seed_data.sql
│   ├── queries.sql
│   ├── run_queries.py
│   └── README.md
└── 04-ai-pair-programmed-endpoint/
    ├── app.py
    ├── requirements.txt
    ├── ai_collaboration_log.md
    ├── tests/test_tasks.py
    └── README.md
```

---

## Tips for Students

1. **Read the README first** before touching any code
2. **Run the program as-is** before making changes — confirm it works
3. **Break things on purpose** — change inputs, try edge cases
4. **Extend the project** — each README has "Try It Yourself" ideas
5. **For Project 4:** Read `ai_collaboration_log.md` — understanding *where* AI goes wrong is the most valuable skill
