# Project 15: Will It Be Late?

Build a binary classifier that predicts whether a delivery will be late — before it ships. Learn the full classification pipeline and understand why some misclassifications matter more than others.

**Skills practiced:** Binary classification, feature engineering, confusion matrix interpretation, class imbalance awareness, scikit-learn `RandomForestClassifier`.

---

## What This Project Does

```
deliveries_sample.csv
(60 orders with route, carrier, season, weight, fragile flag)
        │
        ▼
┌────────────────────────────────────────────────────┐
│                  predictor.py                      │
│                                                    │
│  1. Engineer features                              │
│     is_late = actual > promised                    │
│     delay_buffer = promised - (distance / 300)     │
│                                                    │
│  2. Encode categoricals (LabelEncoder)             │
│  3. Train Logistic Regression + Random Forest      │
│  4. Evaluate: Accuracy, Precision, Recall, F1      │
│  5. Plot: Feature importance + Confusion matrix    │
│  6. Explain: Which orders got it wrong and WHY?    │
│  7. Demo: Predict a brand-new order                │
└────────────────────────────────────────────────────┘
        │
        ▼
charts/feature_importance.png
charts/confusion_matrix.png
```

---

## The Business Problem

An e-commerce company wants to predict, at the time of order placement, whether the delivery will arrive later than promised. If the model catches a likely-late order early, the company can:
- Proactively message the customer ("We're monitoring your order closely")
- Assign a faster carrier
- Offer a pre-emptive discount before the customer complains

---

## Setup — Step by Step

**Step 1: Go to the project folder**
```bash
cd 15-will-it-be-late
```

**Step 2: Create a virtual environment**
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run**
```bash
python predictor.py
```

---

## Expected Output

```
============================================================
  DATA OVERVIEW
============================================================
  Rows: 60  |  Columns: 13
  Late deliveries: 38 (63.3%)
  On-time deliveries: 22 (36.7%)

============================================================
  MODEL COMPARISON
============================================================
  Model                  Accuracy Precision   Recall       F1
  ------------------------------------------------------------
  Logistic Regression      73.3%     81.8%    75.0%    78.3%
  Random Forest            80.0%     87.5%    87.5%    87.5%

============================================================
  CLASSIFICATION REPORT — Random Forest
============================================================
              precision    recall  f1-score   support

     On Time       0.67      0.67      0.67         6
        Late       0.87      0.87      0.87        15

============================================================
  TRY IT — Predict a New Order
============================================================
  Order details:
    Route:     Mumbai → Delhi (1415 km)
    Category:  Electronics (fragile)
    Carrier:   Delhivery
    Season:    Monsoon
    Promised:  4 days (very tight for this distance)

  Prediction: ⚠ WILL BE LATE
  Probability of being late: 82%
```

---

## How the Code Works

### 1. Creating the Target Variable

```python
df["is_late"] = (df["actual_delivery_days"] > df["promised_delivery_days"]).astype(int)
```

The raw data has `actual_delivery_days` and `promised_delivery_days`. If actual > promised, the delivery was late (1). Otherwise, on time (0). This converts a regression problem into a classification problem.

### 2. Feature Engineering — delay_buffer

```python
df["delay_buffer_days"] = df["promised_delivery_days"] - (df["distance_km"] / 300)
```

A delivery promised in 4 days for a 1415 km route has a buffer of `4 - 4.7 = -0.7` days — a physically tight promise. This engineered feature captures whether the delivery commitment was realistic. A negative buffer almost always means it will be late.

### 3. Encoding Categorical Variables

```python
le = LabelEncoder()
df_encoded[col + "_enc"] = le.fit_transform(df[col])
```

Machine learning models need numbers. `LabelEncoder` converts "BlueDart" → 0, "Delhivery" → 1, etc. The `encoders` dict stores each encoder so you can use the same mapping when predicting new orders.

### 4. The Confusion Matrix — Why It Matters More Than Accuracy

```
              Predicted On Time  |  Predicted Late
Actual On Time       TN          |      FP
Actual Late          FN          |      TP
```

**False Negatives (FN) are the dangerous ones:** The model said "on time" but the order arrived late. The customer wasn't warned, wasn't compensated early, and will be angry.

**False Positives (FP) are costly but recoverable:** The model said "late" but the order arrived on time. You sent an unnecessary apology — awkward but not damaging.

This is why **Recall** matters more than Accuracy in delivery delay prediction.

### 5. Feature Importance — What Actually Drives Delays?

```python
importances = pd.Series(rf_model.feature_importances_, index=feature_cols)
```

Random Forest assigns an importance score to each feature based on how much it reduces prediction error. The top predictors in this dataset are typically:
- `warehouse_to_pickup_hrs` — pre-shipment delays cascade
- `delay_buffer_days` — tight promises are broken more often
- `distance_km` — longer routes have more points of failure
- `season` — Monsoon causes road closures and flood delays

---

## Key Concepts Explained

### Why Not Just Use Distance?

Longer distance = more likely to be late, but it's not the whole story. A 2150 km route promised in 7 days might arrive on time. A 700 km route promised in 2 days might arrive late. The **delay_buffer** captures this interaction.

### Why Is Recall More Important Than Precision Here?

- **Precision**: Of all orders predicted late, how many were actually late?
- **Recall**: Of all orders that were actually late, how many did we catch?

For a delivery business, missing a late order (low recall) = unhappy customer. Predicting unnecessary lateness (low precision) = unnecessary apology emails. Missing late orders is worse.

---

## Real Dataset (Optional — Kaggle)

**E-Commerce Shipping Dataset (10,999 rows)**
```
https://www.kaggle.com/datasets/prachi13/customer-churn-dataset
```

Download and look for the `Reached.on.Time_Y.N` column as your target variable.

---

## What You Learn

| Skill | Where It Appears |
|-------|-----------------|
| Binary classification | `is_late = actual > promised` |
| Feature engineering | `delay_buffer_days` calculation |
| Label encoding | `LabelEncoder` for categorical columns |
| Random Forest | `RandomForestClassifier` |
| Confusion matrix | `confusion_matrix()` + visual |
| Feature importance | `rf_model.feature_importances_` |
| Precision vs Recall | Business context interpretation |

---

## Student Challenge

1. The model uses `promised_delivery_days` as a feature — is that fair? Should you remove it? What happens to accuracy if you do?
2. Change the model to predict **how many days late** (a regression problem instead of classification). Which approach is more useful for a business?
3. Add a new feature: `is_long_route = distance_km > 1500`. Does this improve the F1 score?
4. Download the Kaggle dataset and find which carrier has the worst late-delivery rate. Does the model agree?
