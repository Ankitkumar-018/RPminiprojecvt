# Project 15: Will It Be Late? — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how an ML engineer frames a classification problem.

---

### Step 1 — Understand the Problem

**What kind of ML problem is this?**
Binary classification — the output is one of two classes: **Late (1)** or **On Time (0)**.

**Where does the label come from?**
We engineer it:
```
is_late = 1  if  actual_delivery_days > promised_delivery_days
is_late = 0  otherwise
```
This is sometimes called "derived labelling" — the raw data doesn't have a "late" column, but we can compute it from two columns that are present.

**Why is this classification and not regression?**
We could predict the number of delay days (regression). But the business question is binary: "Will it be late?" Binary classification is often more actionable than regression — the answer drives a yes/no decision (warn customer or not).

---

### Step 2 — Questions to Ask Before Writing Code

- **What features predict whether an order is late?**
  → Distance (longer = more risk), weight, carrier reliability, season (Monsoon = bad), warehouse delays, whether the promise was tight.

- **What is a "tight promise"?**
  → If distance is 1415 km and the promise is 4 days, that's barely possible. We engineer a `delay_buffer` feature to capture this.

- **Does class balance matter?**
  → Yes. If 70% of orders are late, a model that always predicts "late" gets 70% accuracy without learning anything. Check the class distribution first.

- **What mistake is more costly — predicting late when it's on time, or predicting on time when it's late?**
  → False Negatives (said "on time" but it was late) are worse. The customer wasn't warned. So optimise for **Recall**, not just Accuracy.

---

### Step 3 — Pseudo Code

```
START

  LOAD CSV
  ENGINEER features:
    is_late = (actual_delivery_days > promised_delivery_days).astype(int)
    delay_buffer = promised_delivery_days - (distance_km / 300)
    is_fragile = (fragile == "Yes").astype(int)

  PRINT class distribution (how many late vs on-time)

  ENCODE categoricals:
    FOR each col in [category, carrier, season, payment_mode, city_cols]:
      LabelEncoder().fit_transform(col)

  DEFINE feature_cols = numeric + encoded_categorical columns
  X = df[feature_cols]
  y = df["is_late"]

  SPLIT with stratify=y:
    X_train, X_test (75 / 25 split)

  TRAIN model 1: LogisticRegression(max_iter=1000)
  TRAIN model 2: RandomForestClassifier(n_estimators=100)

  FOR each model:
    preds = model.predict(X_test)
    PRINT accuracy, precision, recall, F1

  PRINT classification_report (per-class breakdown)

  PLOT feature importance bar chart (horizontal)
  PLOT confusion matrix

  FIND false negatives (predicted On Time, actually Late)
    PRINT which orders were missed and why

  PREDICT a new order:
    Build feature dict for a new order
    PRINT prediction + probability

END
```

---

### Step 4 — Feature Engineering: delay_buffer

The `delay_buffer_days` feature is the most important engineering decision in this project.

```
Formula: delay_buffer = promised_days - (distance / 300)

Example:
  Order: Mumbai → Delhi, 1415 km, promised in 4 days
  Average truck speed: ~300 km/day
  Minimum days needed: 1415 / 300 ≈ 4.7 days
  Buffer: 4 - 4.7 = -0.7 days   ← NEGATIVE — physically impossible!

  Another order: Mumbai → Pune, 148 km, promised in 3 days
  Minimum days: 148 / 300 ≈ 0.5 days
  Buffer: 3 - 0.5 = 2.5 days    ← comfortable, low risk
```

A negative buffer almost always predicts lateness. This single engineered feature may matter more than the raw distance or promised_days individually.

---

### Step 5 — Why Recall > Accuracy

| Metric | Formula | What It Catches |
|--------|---------|----------------|
| Accuracy | (TP + TN) / Total | Overall correctness |
| Precision | TP / (TP + FP) | Reliability of "late" predictions |
| Recall | TP / (TP + FN) | How many actual late orders did we find? |

**For this project, prioritise Recall.**

If Recall = 60%, you're missing 40% of orders that will actually be late. Those customers get no warning. If Recall = 90%, you catch 9 out of 10 late orders proactively.

Low Recall = unhappy customers who were surprised by delays.
Low Precision = extra apology emails that weren't needed (annoying but recoverable).

---

### Step 6 — What Could Go Wrong?

| Risk | How to Handle |
|------|---------------|
| Class imbalance (60% late) | Use `stratify=y` in train_test_split |
| Carrier not seen in new order at prediction time | Use `try/except` around LabelEncoder.transform |
| Model has 100% accuracy on small dataset | Almost certainly overfitting — need more data |
| delay_buffer is always negative for 2-day promises | Add a flag: `too_tight = delay_buffer < 0` |
| Random Forest slow on many features | Reduce `n_estimators=50` for faster demo |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Understand the Label

**How do we know if an order was late?**

```
Formula:
is_late = __________ if actual_delivery_days _____ promised_delivery_days
```

**Is this classification or regression? Why?**

```
Answer:


```

---

### Step 2 — Design the delay_buffer Feature

**Why is a 4-day promise for a 1415 km delivery risky?**

```
Calculation:
  Minimum days at 300 km/day = ______
  Promised days = ______
  Buffer = ______

  Conclusion:


```

**What value of delay_buffer would make you confident the order will be on time?**

```
Answer:
```

---

### Step 3 — Class Balance Check

**Before training, what do you check first?**

```
What you check:
Why it matters:
What to do if 90% of orders are "Late":
```

---

### Step 4 — Precision vs Recall

**Fill in the confusion matrix cells:**

```
              Predicted: On Time  |  Predicted: Late
Actual: On Time     ___           |      ___
Actual: Late        ___           |      ___

TN = ___, FP = ___, FN = ___, TP = ___
```

**Which is worse for a delivery company — a False Negative or a False Positive? Why?**

```
Answer:


```

---

### Step 5 — Your Pseudo Code

```
Step 1 (Load + engineer features):
Step 2 (Encode categoricals):
Step 3 (Split with stratify):
Step 4 (Train models):
Step 5 (Evaluate with classification_report):
Step 6 (Plot feature importance):
Step 7 (Find false negatives):
Step 8 (Predict a new order):
```

---

### Step 6 — After Finishing, Reflect

**What are the top 3 features that predict lateness?**

```
1.
2.
3.
Why do you think these matter most?
```

**Find one false negative in your results. What was special about that order?**

```
Order ID:
Route:
Carrier:
Why the model missed it:
```

**If you had to pick ONE change to reduce late deliveries, what would it be?**

```
Answer (based on feature importance):
```
