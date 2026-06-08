# Project 12: Sentiment on Real Reviews — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data scientist thinks about NLP classification.

---

### Step 1 — Understand the Problem

**What exactly does this project do?**
Classify the sentiment of product reviews into 3 categories: Positive, Neutral, Negative — and honestly report where the model fails.

**How is this different from binary classification?**
- Binary: spam vs ham (2 classes)
- Multi-class: positive, neutral, negative (3 classes)
Multi-class is harder because misclassifications can go in multiple directions (positive predicted as neutral, neutral predicted as negative, etc.)

**Where does the label come from?**
Star ratings — a proxy for sentiment:
- 4–5 stars → Positive
- 3 stars → Neutral
- 1–2 stars → Negative

This is called **weak supervision** — using a related signal (ratings) to automatically label text.

---

### Step 2 — Questions to Ask Before Writing Code

- **Is the label (star rating) a perfect proxy for sentiment?**
  → No. A 3-star review can be very positive ("Good product but slightly overpriced — 3 stars"). A 5-star review can have complaints ("Loved it but delivery was terrible!"). Weak supervision introduces noise.

- **What is the biggest challenge specific to Indian product reviews?**
  → **Hinglish** — mixing Hindi and English in the same sentence. TF-IDF only sees English words — Hindi words look like garbage tokens and are ignored. This makes the model less reliable on Hinglish reviews.

- **What is sarcasm and why can't TF-IDF handle it?**
  → Sarcasm uses positive words to express negative sentiment: "Oh fantastic, broke on day 1." TF-IDF counts "fantastic" as a positive signal. It has no concept of tone or context.

- **What does a 3×3 confusion matrix show?**
  → For 3 classes, you get a 3×3 grid. The diagonal shows correct predictions. Off-diagonal shows what the model confused. You'll see that neutral is most often misclassified.

- **Why is neutral the hardest class?**
  → It has fewer examples, uses mixed vocabulary, and is inherently ambiguous — even humans sometimes disagree on whether a review is neutral or slightly positive.

---

### Step 3 — Pseudo Code

```
START

  LOAD reviews CSV
  MAP star rating to sentiment label:
    4–5 → "positive"
    3   → "neutral"
    1–2 → "negative"

  PRINT label distribution

  CLEAN TEXT (for each review):
    lowercase
    remove URLs (http://...)
    remove non-letter characters
    remove extra spaces

  VECTORIZE:
    TfidfVectorizer(max_features=5000, ngram_range=(1,2), stop_words="english")
    X = vectorizer.fit_transform(cleaned reviews)
    y = sentiment labels

  SPLIT with stratify=y:
    X_train, X_test, y_train, y_test = split 75/25

  TRAIN:
    model = LogisticRegression(multi_class="multinomial")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)

  EVALUATE:
    print classification_report(y_test, preds)   ← per-class precision/recall/F1

  PLOT:
    sentiment distribution bar chart
    3×3 confusion matrix

  REPORT unreliable cases:
    sarcasm → positive words in negative review
    neutral → model picks up only the strongest word
    Hinglish → non-English words ignored
    short reviews → too little signal

END
```

---

### Step 4 — Design the Text Cleaning Function

Before training, every review goes through this function:

```
Input:  "LOVED IT!! Battery lasts all day. http://buy.now/link 😊👍"

Step 1: lowercase         → "loved it!! battery lasts all day. http://buy.now/link 😊👍"
Step 2: remove URLs       → "loved it!! battery lasts all day.  😊👍"
Step 3: remove non-letters → "loved it battery lasts all day"
Step 4: remove extra spaces → "loved it battery lasts all day"

Output: "loved it battery lasts all day"
```

Why remove emojis? TF-IDF cannot process them — they become garbage characters. (A next-level project would convert emojis to text: 😊 → "happy".)

---

### Step 5 — Think About Where It Will Fail BEFORE Running

Before writing the model, predict the failure modes:

```
Sarcasm:
  Review: "Wow, so durable. Lasted a whole 3 days." (1 star)
  Words: wow, durable → model predicts positive
  Reality: negative

Hinglish:
  Review: "Bahut sahi hai yaar, ekdam mast product" (5 stars)
  English words: None (or very few)
  TF-IDF has no signal → model guesses

Short review:
  Review: "Okay." (3 stars)
  1 word → almost no TF-IDF signal → random prediction

Mislabeled rating:
  Review: "Love the product, hate the delivery. 2 stars." (actually mixed)
  Label: "negative" (from 2-star rating)
  But review contains positive words → model confused
```

Writing these out before running helps you explain the results honestly instead of making excuses after.

---

### Step 6 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| Neutral class has < 2 samples | Remove `stratify=y` or add more data |
| All reviews predicted as positive | Class imbalance — check distribution |
| Hindi words in vocabulary | They appear as low-frequency noise — acceptable for now |
| Perfect F1 on sample data | Overfitting on 40 rows — always evaluate on held-out test set |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Understand Weak Supervision

**What is weak supervision in this project?**

```
Write here:


```

**Can star ratings be a wrong signal for sentiment? Give an example:**

```
Write here:


```

---

### Step 2 — Class Distribution

**Check your dataset and fill in:**

```
Total reviews:
Positive reviews: ______ ( ___% )
Neutral reviews:  ______ ( ___% )
Negative reviews: ______ ( ___% )

Is the dataset balanced? What problem can imbalance cause?:
```

---

### Step 3 — Design Your Text Cleaning

**Take this real-looking review and clean it step by step:**

```
Raw review: "boAt earphones are OKAY I guess... Not bad but not great either 🎧 
             Check price at: amzn.to/xyz123"

After lowercase:
After removing URLs:
After removing non-letters:
Final cleaned text:
```

---

### Step 4 — Predict the Hard Cases

**Before running the model, predict 3 types of reviews it will struggle with:**

```
Type 1:
Example review:
Why it will fail:

Type 2:
Example review:
Why it will fail:

Type 3:
Example review:
Why it will fail:
```

---

### Step 5 — Your Pseudo Code

```
Write the pipeline steps:

Step 1 (Load + label):
Step 2 (Clean):
Step 3 (Vectorise):
Step 4 (Train):
Step 5 (Evaluate per class):
Step 6 (Report failures):
```

---

### Step 6 — After finishing, reflect

**Which class had the lowest F1 score? Why?**

```
Write here:


```

**Find one review where the model was wrong. Write it and explain why:**

```
Review:
Star rating (actual label):
Model predicted:
Why it was wrong:
```

**What would you need to handle Hinglish reviews properly?**

```
Write here:

```
