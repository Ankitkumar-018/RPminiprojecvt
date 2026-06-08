# Project 12: Sentiment on Real Reviews

## What Is This?

A sentiment classifier that labels product reviews (boAt, Mamaearth, Amazon India) as **Positive / Neutral / Negative** — and honestly reports **where the model is unreliable** and why.

---

## What Skills You Will Learn

- Text cleaning for real-world reviews (URLs, punctuation, mixed languages)
- Multi-class text classification (3 labels, not just binary)
- TF-IDF features + Logistic Regression
- Reading a 3×3 confusion matrix
- Understanding model failure modes: sarcasm, Hinglish, short reviews
- Communicating model limitations honestly — a critical professional skill

---

## How the Pipeline Works

```
Raw reviews CSV (review text + star rating)
        │
        ▼
   Label from rating:
   4–5 stars → positive
   3 stars   → neutral
   1–2 stars → negative
        │
        ▼
   Clean text:
   - Lowercase
   - Remove URLs, numbers, punctuation
   - Remove English stop words
        │
        ▼
   TF-IDF vectorisation (5000 features, unigrams + bigrams)
        │
        ▼
   Logistic Regression (multi-class)
        │
        ▼
   Evaluation: per-class Precision, Recall, F1
        │
        ▼
   Confusion matrix
        │
        ▼
   Report where the model fails (sarcasm, Hinglish, short reviews)
```

---

## Folder Structure

```
12-sentiment-reviews/
├── sentiment.py              ← Full pipeline + unreliability report
├── requirements.txt          ← pandas, scikit-learn, matplotlib
├── data/
│   └── reviews_sample.csv    ← 40 reviews across boAt/Mamaearth/Amazon
├── charts/                   ← Auto-created
└── README.md
```

---

## Dataset

### Option A — Run immediately (sample included)
`data/reviews_sample.csv` is included with 40 real-style reviews.

### Option B — Real datasets from Kaggle (recommended)

**boAt earphone reviews:**
https://www.kaggle.com/datasets/deepcontractor/boat-earphones-reviews

**Amazon India product reviews:**
https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews

**Steps after downloading:**
1. Place your CSV in `data/`
2. Open `sentiment.py` and update these 3 variables at the top:
   ```python
   DATA_FILE  = "data/your_file.csv"
   REVIEW_COL = "review_body"    # whatever column has the text
   RATING_COL = "star_rating"    # whatever column has the stars
   ```

---

## Requirements

- Python 3.8 or higher

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 12-sentiment-reviews
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run sentiment analysis

```bash
python sentiment.py
```

---

## Expected Output

```
============================================================
  Sentiment Analysis — Product Reviews
  Data: data/reviews_sample.csv
============================================================

Loaded 40 reviews
  Sentiment distribution:
    positive    22 (55.0%)
    negative    12 (30.0%)
    neutral      6 (15.0%)

============================================================
  Model: Logistic Regression + TF-IDF
  Overall Accuracy: 0.700
============================================================

  Per-Class Report:
               precision  recall  f1-score  support
  negative        0.75    0.75      0.75       4
  neutral         0.33    0.33      0.33       3
  positive        0.83    0.83      0.83       6

============================================================
  WHERE THE MODEL IS UNRELIABLE
============================================================

  UNRELIABLE CASE 1 — SARCASM
  "Great product. Broke in 2 days. Absolutely love it!" (1 star)
  Words: great, love → model predicts POSITIVE. Actual: NEGATIVE.

  UNRELIABLE CASE 2 — NEUTRAL/BORDERLINE REVIEWS
  3-star reviews mix praise and criticism — model picks the louder signal.

  UNRELIABLE CASE 3 — HINGLISH
  "Bahut achha product hai but quality thodi kam hai"
  Non-English words are ignored by TF-IDF → less reliable.

  UNRELIABLE CASE 4 — SHORT REVIEWS
  "Ok" → too little signal for TF-IDF → model essentially guesses.
```

---

## Understanding the 3×3 Confusion Matrix

```
              Predicted:
              Negative   Neutral   Positive
Actual:
Negative    [    TP    |   FN    |   FN    ]
Neutral     [    FP    |   TP    |   FP    ]
Positive    [    FP    |   FN    |   TP    ]

Diagonal cells = correct predictions
Off-diagonal  = errors (look here to understand mistakes)

Common pattern: Neutral is hardest to classify.
It gets confused with both positive and negative.
```

---

## Why Neutral Is the Hardest Class

Most reviews are either clearly positive (5 stars) or clearly negative (1–2 stars). Neutral reviews (3 stars) are:
- **Few in number** → less training data
- **Mixed in language** → "good but not great" confuses TF-IDF
- **Ambiguous by nature** → even humans disagree on 3-star reviews

---

## Try It Yourself — Extension Ideas

- Try VADER (rule-based sentiment scorer) as a baseline — no training needed
- Translate Hinglish reviews using `googletrans` before classifying
- Add product name as a feature — sentiment may differ by product line
- Try a pre-trained model: `transformers` library with `bert-base-uncased`
- Build a simple dashboard: input any review URL → get sentiment

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Wrong file path | Update `DATA_FILE` in `sentiment.py` |
| `KeyError: 'review'` | Column name differs | Update `REVIEW_COL` to match your CSV |
| `ValueError: stratify` | A class has only 1 sample | Add more data or remove `stratify=y` |
| All neutral predicted wrong | Too few 3-star reviews | Real datasets have more balanced distribution |
| `ModuleNotFoundError` | Missing library | `pip install -r requirements.txt` |
