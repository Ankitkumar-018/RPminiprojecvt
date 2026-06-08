# Project 11: Classifier with Honest Metrics — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data scientist thinks about classification honestly.

---

### Step 1 — Understand the Problem

**What exactly does this project do?**
Classify SMS messages as spam or ham (not spam) — and report the metrics that actually matter, not just accuracy.

**Why is accuracy not enough?**
The dataset has ~87% ham, ~13% spam. A model that classifies EVERYTHING as ham achieves 87% accuracy while being completely useless — it catches zero spam. This is the **class imbalance problem**.

**What is the right question to ask?**
Not "how often is my model right overall?" but:
- "Of all spam it flagged, how much was actually spam?" → Precision
- "Of all real spam in the dataset, how much did it catch?" → Recall

---

### Step 2 — Questions to Ask Before Writing Code

- **What is TF-IDF and why use it?**
  → Converts text to numbers. Each message becomes a vector where each element represents how important a word is in that message vs the entire dataset. Spam messages have distinctive vocabulary (free, winner, claim, txt).

- **Why Naive Bayes for text?**
  → It assumes words are independent (naïve) but works surprisingly well for text. Fast, interpretable, and effective with little data. A good baseline to beat.

- **What is the confusion matrix?**
  → A 2×2 table showing all 4 possible outcomes:
    - True Positive: spam correctly caught
    - True Negative: ham correctly allowed through
    - False Positive: ham wrongly blocked (annoying)
    - False Negative: spam that slipped through (dangerous)

- **Which error is worse — False Positive or False Negative?**
  → Depends on context. For spam: False Negative (spam slips through) is dangerous. For medical diagnosis (cancer): False Negative (missed cancer) is much more dangerous than False Positive.

- **What is the F1 Score?**
  → Harmonic mean of Precision and Recall. Useful when you need to balance both.
  → `F1 = 2 × (Precision × Recall) / (Precision + Recall)`

---

### Step 3 — Pseudo Code

```
START

  LOAD spam.csv
  IF columns are v1, v2: rename to label, message
  label_num = 1 if label == "spam" else 0
  PRINT class distribution

  VECTORIZE:
    vectorizer = TfidfVectorizer(max_features=3000, ngram_range=(1,2))
    X = vectorizer.fit_transform(messages)
    y = label_num

  SPLIT with stratify=y (keeps same spam ratio in train and test):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

  FOR model in [NaiveBayes, LogisticRegression]:
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    COMPUTE accuracy, precision, recall, f1
    PRINT results

  EXPLAIN why accuracy misleads on imbalanced data

  PLOT confusion matrix for best model

  FIND wrong predictions:
    false_negatives = spam predicted as ham
    false_positives = ham predicted as spam
  PRINT one example of each with explanation

END
```

---

### Step 4 — Understand TF-IDF Before Coding

```
Term Frequency (TF) = how often a word appears in ONE message
  "Win a free prize now free!" → TF("free") = 2/6 = 0.33

Inverse Document Frequency (IDF) = how rare the word is across ALL messages
  "free" appears in 500/5572 messages → IDF = log(5572/500) = 2.41

TF-IDF = TF × IDF = 0.33 × 2.41 = 0.80

Common words like "the", "is" appear in ALL messages → very low IDF → low score
Spam words like "winner", "claim", "prize" are rare overall → high IDF → high score
```

This is why TF-IDF is powerful for spam detection — it naturally boosts distinctive spam words.

---

### Step 5 — Think About the Errors BEFORE Running

Before training, think: what kinds of messages would be hard to classify?

```
Hard for the model:
  1. Legitimate promotional messages: "Your Swiggy order is confirmed! Track here."
     Contains: order, track, confirm → sounds like spam to the model

  2. Casual spam written to sound normal: "Hi, saw your profile. Interested?"
     No obvious spam words → model misses it

  3. Context-dependent messages: "You've won the team quiz!"
     "Won" is a spam signal, but here it's legitimate

These are the cases you will explain in Step 6 of your code.
```

---

### Step 6 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| Class imbalance → always predicts majority | Check class distribution at start |
| Precision = 0 | Model never predicts spam → check threshold |
| Recall = 1.0, Precision = 0.1 | Model marks everything as spam → unusable |
| `stratify` fails | A class has < 2 samples → use larger dataset |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Understand the Class Imbalance

**What is the class distribution in the SMS dataset?**

```
Ham messages:  ______ ( ___% )
Spam messages: ______ ( ___% )
```

**If a model always predicts "ham", what accuracy does it get?**

```
Answer:
```

**Is that a good model? Why or why not?**

```
Write here:


```

---

### Step 2 — Explain the Metrics in Your Own Words

```
Precision (for spam class):


Recall (for spam class):


F1 Score:


Which error is worse for a spam filter — False Positive or False Negative? Why?:
```

---

### Step 3 — Draw the Confusion Matrix

After running the model, fill in this table:

```
                  Predicted Ham   Predicted Spam
Actual Ham     [               |               ]
Actual Spam    [               |               ]

Number of False Negatives (spam that slipped through): ____
Number of False Positives (ham wrongly blocked):        ____
```

---

### Step 4 — Your Pseudo Code

```
Write the main pipeline:

Step 1 (Load + label):
Step 2 (Vectorise):
Step 3 (Split):
Step 4 (Train):
Step 5 (Evaluate):
Step 6 (Explain errors):
```

---

### Step 5 — Find a Wrong Prediction

**Find one False Negative (spam the model missed). Write the message:**

```
Message:
Why did the model miss it?:
```

**Find one False Positive (ham the model blocked). Write the message:**

```
Message:
Why did the model get confused?:
```

---

### Step 6 — After finishing, reflect

**What metric would you optimise for a medical diagnosis model (cancer/not cancer)?**

```
Write here (and explain why):

```

**What does `ngram_range=(1,2)` do in TF-IDF?**

```
Write here:

```
