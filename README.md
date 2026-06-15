# Mini Projects — Student Edition

Sixteen standalone projects covering Python fundamentals, data structures, SQL, AI/LLM development, and data science. Each project is self-contained with its own README, APPROACH.md, code, and sample data.

---

## Projects Overview

| # | Project | Key Skill | Time Estimate |
|---|---------|-----------|---------------|
| 1 | [Word Frequency Analyzer](01-word-frequency-analyzer/) | Python + File Handling | 1–2 hours |
| 2 | [Instant Autocomplete](02-instant-autocomplete/) | Data Structures (Trie) | 2–3 hours |
| 3 | [Streaming Service DB](03-streaming-service-db/) | SQL + Schema Design | 2–3 hours |
| 4 | [AI Pair-Programmed Endpoint](04-ai-pair-programmed-endpoint/) | REST API + AI Tools | 3–4 hours |
| 5 | [Structured Output Workflow](05-structured-output-workflow/) | Claude API + JSON schemas | 2–3 hours |
| 6 | [Mini-RAG](06-mini-rag/) | Retrieval-Augmented Generation | 3–4 hours |
| 7 | [Single-Tool Agent](07-single-tool-agent/) | Tool Use / Function Calling | 2–3 hours |
| 8 | [Agent with Memory & Guardrails](08-agent-memory-guardrails/) | Agent Design + Safety | 3–4 hours |
| 9 | [EDA Detective](09-eda-detective/) | Exploratory Data Analysis | 2–3 hours |
| 10 | [Price Predictor](10-price-predictor/) | Regression + Feature Engineering | 3–4 hours |
| 11 | [Classifier with Honest Metrics](11-classifier-honest-metrics/) | Classification + Evaluation | 3–4 hours |
| 12 | [Sentiment on Real Reviews](12-sentiment-reviews/) | NLP + Multi-class Classification | 3–4 hours |
| 13 | [Clean the Mess](13-clean-the-mess/) | Data Cleaning + Audit Trail | 2–3 hours |
| 14 | [One Question, Five Charts](14-one-question-five-charts/) | Data Visualisation | 2–3 hours |
| 15 | [Will It Be Late?](15-will-it-be-late/) | Binary Classification | 3–4 hours |
| 16 | [Insight Memo](16-insight-memo/) | Data Storytelling + Reporting | 3–4 hours |

---

## Python Fundamentals (Projects 1–4)

### Project 1: Word Frequency Analyzer

**What it does:** Reads any text file and reports the most common words with a visual bar chart.

**What you learn:** File I/O, regex, `collections.Counter`, command-line arguments

```bash
cd 01-word-frequency-analyzer
python analyzer.py
```

> Full details: [01-word-frequency-analyzer/README.md](01-word-frequency-analyzer/README.md)

---

### Project 2: Instant Autocomplete

**What it does:** Type a prefix (e.g. "Ban") and instantly get matching Indian cities — stays fast on 10,000+ entries.

**What you learn:** Trie data structure, why it beats linear search, performance benchmarking

```bash
cd 02-instant-autocomplete
python autocomplete.py
```

> Full details: [02-instant-autocomplete/README.md](02-instant-autocomplete/README.md)

---

### Project 3: Streaming Service Database

**What it does:** Full database design for a Hotstar/Netflix-style app with 12 SQL queries including a recommendation engine.

**What you learn:** Schema design, foreign keys, JOIN, GROUP BY, subqueries, recommendation logic

```bash
cd 03-streaming-service-db
python run_queries.py
```

> Full details: [03-streaming-service-db/README.md](03-streaming-service-db/README.md)

---

### Project 4: AI Pair-Programmed REST API

**What it does:** A Task Manager API with 6 endpoints, 25+ tests, and a log documenting where AI helped and where it was wrong.

**What you learn:** REST API design, Flask, pytest, critically reviewing AI-generated code

```bash
cd 04-ai-pair-programmed-endpoint
pip install -r requirements.txt
python app.py
```

> Full details: [04-ai-pair-programmed-endpoint/README.md](04-ai-pair-programmed-endpoint/README.md)

---

## AI / LLM Projects (Projects 5–8)

> **Note:** Projects 5–8 require an Anthropic API key. Set it as: `export ANTHROPIC_API_KEY=sk-ant-...`

### Project 5: Structured Output Workflow

**What it does:** Sends messy unstructured text (recipes, job postings) to Claude and gets back clean JSON.

**What you learn:** Prompt engineering for structured output, JSON schema injection, retry logic, stripping markdown fences

```bash
cd 05-structured-output-workflow
pip install -r requirements.txt
python pipeline.py sample_inputs/recipes.txt
```

> Full details: [05-structured-output-workflow/README.md](05-structured-output-workflow/README.md)

---

### Project 6: Mini-RAG

**What it does:** Answers questions about your own documents using TF-IDF retrieval + Claude. No hallucinations — if the answer isn't in the docs, it says so.

**What you learn:** Document chunking, TF-IDF, cosine similarity, anti-hallucination prompts

```bash
cd 06-mini-rag
pip install -r requirements.txt
python rag.py
```

> Full details: [06-mini-rag/README.md](06-mini-rag/README.md)

---

### Project 7: Single-Tool Agent

**What it does:** Claude calls a calculator and unit converter tool — a working implementation of the tool use pattern.

**What you learn:** Tool schemas, agent loop (`stop_reason`), safe `eval()`, function calling

```bash
cd 07-single-tool-agent
pip install -r requirements.txt
python agent.py
```

> Full details: [07-single-tool-agent/README.md](07-single-tool-agent/README.md)

---

### Project 8: Agent with Memory and Guardrails

**What it does:** Three versions of the same agent — no memory, with memory, and with safety guardrails. Shows exactly what changes between each.

**What you learn:** Conversation history management, hard pre-filters, soft topic restriction via system prompt

```bash
cd 08-agent-memory-guardrails
pip install -r requirements.txt
python agent_with_guardrails.py
```

> Full details: [08-agent-memory-guardrails/README.md](08-agent-memory-guardrails/README.md)

---

## Data Science Projects (Projects 9–12)

> **Note:** Projects 9–12 work with included sample datasets. For full results, download the Kaggle datasets linked in each README.

### Project 9: EDA Detective — IPL

**What it does:** Explores IPL match data to answer 3 detective questions: Does toss matter? Which teams dominate? Is batting first or chasing better?

**What you learn:** Pandas EDA, matplotlib subplots, asking questions of data

```bash
cd 09-eda-detective
pip install -r requirements.txt
python eda.py
```

> Full details: [09-eda-detective/README.md](09-eda-detective/README.md)

---

### Project 10: House Price Predictor

**What it does:** Predicts Bengaluru house prices using location, size, and BHK. Handles messy real-world data: "1200-1500 sqft", "3 BHK", missing values.

**What you learn:** Feature engineering, outlier removal, LinearRegression vs RandomForest, R² interpretation

```bash
cd 10-price-predictor
pip install -r requirements.txt
python predictor.py
```

> Full details: [10-price-predictor/README.md](10-price-predictor/README.md)

---

### Project 11: Spam Classifier with Honest Metrics

**What it does:** Builds a spam classifier and shows you *all* the metrics — not just accuracy. Includes which messages it got wrong and why.

**What you learn:** TF-IDF, Naive Bayes, Logistic Regression, precision/recall/F1, confusion matrix

```bash
cd 11-classifier-honest-metrics
pip install -r requirements.txt
python classifier.py
```

> Full details: [11-classifier-honest-metrics/README.md](11-classifier-honest-metrics/README.md)

---

### Project 12: Sentiment on Real Reviews

**What it does:** Classifies product reviews as positive/neutral/negative. Honestly reports where it fails: sarcasm, Hinglish, short reviews.

**What you learn:** Weak supervision, multi-class classification, handling Indian-language data

```bash
cd 12-sentiment-reviews
pip install -r requirements.txt
python sentiment.py
```

> Full details: [12-sentiment-reviews/README.md](12-sentiment-reviews/README.md)

---

## Data Science Projects — Advanced (Projects 13–16)

### Project 13: Clean the Mess

**What it does:** Takes a deliberately messy employee dataset (duplicate rows, mixed date formats, currency symbols, impossible ages) and produces a clean version. Every decision is documented in `cleaning_log.md`.

**What you learn:** Pandas data cleaning, date parsing, salary normalisation, missing value strategy, audit trails

```bash
cd 13-clean-the-mess
pip install -r requirements.txt
python clean.py
```

**Key output:** `data/clean_employees.csv` + `cleaning_log.md`

> Full details: [13-clean-the-mess/README.md](13-clean-the-mess/README.md)

---

### Project 14: One Question, Five Charts

**What it does:** Answers one question — "Which category drives the most revenue?" — using 5 different chart types (bar, line, pie, stacked bar, heatmap). Shows when each chart works best.

**What you learn:** Matplotlib visualisation, when to use each chart type, `pd.Categorical` for ordering, stacked bar mechanics

```bash
cd 14-one-question-five-charts
pip install -r requirements.txt
python charts.py
```

**Key output:** 5 chart images in `charts/`

> Full details: [14-one-question-five-charts/README.md](14-one-question-five-charts/README.md)

---

### Project 15: Will It Be Late?

**What it does:** Predicts whether a delivery will arrive late (before it ships) using route, carrier, season, and weight. Explains which orders the model got wrong and why.

**What you learn:** Binary classification, feature engineering (`delay_buffer`), Recall vs Accuracy, confusion matrix interpretation, Random Forest feature importance

```bash
cd 15-will-it-be-late
pip install -r requirements.txt
python predictor.py
```

**Key output:** Feature importance chart, confusion matrix, prediction for a new order

> Full details: [15-will-it-be-late/README.md](15-will-it-be-late/README.md)

---

### Project 16: Insight Memo

**What it does:** Reads an e-commerce orders CSV and auto-generates a structured business memo in markdown — with revenue analysis, return rates, delivery performance, customer geography, and data-driven recommendations.

**What you learn:** Pandas aggregation, datetime arithmetic, Pearson correlation, separating analysis from report writing, generating markdown from Python

```bash
cd 16-insight-memo
pip install -r requirements.txt
python memo.py
```

**Key output:** `insight_memo.md` + 2 summary charts

> Full details: [16-insight-memo/README.md](16-insight-memo/README.md)

---

## Requirements by Project Group

| Group | Python | Extra Packages |
|-------|--------|---------------|
| Projects 1–3 | 3.7+ | None (stdlib only) |
| Project 4 | 3.7+ | `flask`, `pytest` |
| Projects 5–8 | 3.9+ | `anthropic` + API key |
| Projects 9–12 | 3.9+ | `pandas`, `scikit-learn`, `matplotlib` |
| Projects 13–16 | 3.9+ | `pandas`, `scikit-learn`, `matplotlib` |

---

## Folder Structure

```
Project/
├── README.md                              ← You are here
├── 01-word-frequency-analyzer/
├── 02-instant-autocomplete/
├── 03-streaming-service-db/
├── 04-ai-pair-programmed-endpoint/
├── 05-structured-output-workflow/
├── 06-mini-rag/
├── 07-single-tool-agent/
├── 08-agent-memory-guardrails/
├── 09-eda-detective/
├── 10-price-predictor/
├── 11-classifier-honest-metrics/
├── 12-sentiment-reviews/
├── 13-clean-the-mess/
├── 14-one-question-five-charts/
├── 15-will-it-be-late/
└── 16-insight-memo/
```

Each project folder contains:
```
project-name/
├── README.md        ← Setup, expected output, code explanation
├── APPROACH.md      ← Part A (filled pseudo-code) + Part B (blank student template)
├── requirements.txt ← pip dependencies
├── *.py             ← Main script(s)
└── data/            ← Sample dataset (included)
```

---

## Tips for Students

1. **Read APPROACH.md first** — fill in Part B before writing code
2. **Run the program as-is** before making changes — confirm it works
3. **Break things on purpose** — change inputs, try edge cases
4. **Read cleaning_log.md / ai_collaboration_log.md** — these document real decisions and mistakes, which is where the real learning is
5. **For Projects 9–16:** Download the full Kaggle datasets — the 40–70 row samples show you the pattern; the full data shows you the challenge
