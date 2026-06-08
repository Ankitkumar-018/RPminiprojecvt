# Project 11: Classifier with Honest Metrics

## What Is This?

A spam classifier that is **honest** about what it gets wrong. Reports Precision and Recall (not just accuracy), shows a confusion matrix, and explains one real case it gets wrong and why.

---

## What Skills You Will Learn

- Text preprocessing and TF-IDF vectorisation
- Training a Naive Bayes classifier
- Why accuracy is misleading on imbalanced datasets
- What Precision and Recall mean — and the tradeoff between them
- Reading a confusion matrix
- Analysing and explaining model errors (not just celebrating success)

---

## How the Pipeline Works

```
Raw SMS messages (ham / spam labels)
        │
        ▼
   TF-IDF vectorisation
   - Tokenise words
   - Score by term frequency × inverse document frequency
   - Convert each message to a numeric vector
        │
        ▼
   Train/Test Split (75/25 with stratification)
        │
        ├── Naive Bayes        → Accuracy, Precision, Recall, F1
        └── Logistic Regression → Accuracy, Precision, Recall, F1
        │
        ▼
   Confusion Matrix (True Positive, False Positive, etc.)
        │
        ▼
   Find and explain wrong predictions
   - False Negative: spam that slipped through
   - False Positive: ham wrongly blocked
```

---

## Folder Structure

```
11-classifier-honest-metrics/
├── classifier.py             ← Full pipeline with honest error analysis
├── requirements.txt          ← pandas, scikit-learn, matplotlib
├── data/
│   └── sms_sample.csv        ← 40 messages (works immediately)
├── charts/                   ← Auto-created
└── README.md
```

---

## Dataset

### Option A — Run immediately (sample included)
`data/sms_sample.csv` is included. Works out of the box.

### Option B — Real dataset (5,572 messages — recommended)

1. Go to: https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset
2. Download `spam.csv`
3. Place it in the `data/` folder
4. Open `classifier.py` and update line 20:
   ```python
   DATA_FILE = "data/spam.csv"
   ```

---

## Requirements

- Python 3.8 or higher

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 11-classifier-honest-metrics
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run the classifier

```bash
python classifier.py
```

---

## Expected Output

```
Loaded 40 messages
  Ham (not spam): 26 (65.0%)
  Spam:           14 (35.0%)

=================================================================
  Model                   Accuracy  Precision   Recall       F1
=================================================================
  Naive Bayes                0.900      0.875    0.875    0.875
  Logistic Regression        0.900      0.889    0.889    0.889
=================================================================

  WHY ACCURACY IS MISLEADING HERE
  Dataset is imbalanced: ~87% ham, ~13% spam.
  A model predicting EVERY message as ham gets:
    Accuracy = 87%  ← looks great!
    Recall   = 0%   ← catches ZERO spam (useless)

  For spam detection:
  PRECISION = Of flagged spam, how many actually are?
    Low precision → legitimate emails go to spam folder (annoying)
  RECALL = Of all real spam, how many were caught?
    Low recall → spam slips into inbox (dangerous)

  FALSE NEGATIVE EXAMPLE (spam that got through):
  Message: "Congratulations! You are selected for our survey..."
  Why model missed it: Avoids obvious spam trigger words.

  FALSE POSITIVE EXAMPLE (ham marked as spam):
  Message: "You won the debate last night! Amazing performance."
  Why model was wrong: Contains "won" — common in spam — but used legitimately.
```

---

## Precision vs Recall — The Core Tradeoff

```
              Predicted Ham    Predicted Spam
Actual Ham  [ True Negative  |  False Positive ]  ← ham wrongly blocked
Actual Spam [ False Negative |  True Positive  ]  ← spam caught

Precision = TP / (TP + FP)   →  of spam flags, how many are real?
Recall    = TP / (TP + FN)   →  of all real spam, how much caught?

Tradeoff:
  High Precision → fewer false alarms, but some spam gets through
  High Recall    → catches more spam, but blocks some legitimate messages
```

---

## Try It Yourself — Extension Ideas

- Try `LinearSVC` — often the best for text classification
- Add word count, message length as extra features
- Plot the most common words in spam vs ham as a word cloud
- Try classifying using only the subject line (first 10 words)
- Evaluate on 10-fold cross-validation instead of a single split

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Wrong file path | Update `DATA_FILE` in `classifier.py` |
| `KeyError: 'v1'` | Column names differ in your file | Update `REVIEW_COL` to match your CSV's column name |
| All F1 = 0 | Too few spam examples in sample | Use real 5572-row Kaggle dataset |
| `ValueError: stratify` | One class has < 2 samples | Use sample data with more rows or remove `stratify=y` |
