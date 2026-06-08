# Project 10: Price Predictor — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data scientist thinks before training a model.

---

### Step 1 — Understand the Problem

**What exactly does this project do?**
Predict house prices (a continuous number) from features like location, size, and bathrooms. This is a **regression** problem — not classification.

**What is the target variable?**
`price` — in Lakhs (Indian rupees × 100,000)

**What are the input features?**
- `location` — categorical (neighbourhood name)
- `total_sqft` — numeric, but stored as messy strings ("1200-1500")
- `bath` — integer
- `bhk` — extracted from "3 BHK"
- `balcony` — integer

---

### Step 2 — Questions to Ask Before Writing Code

- **Why not use accuracy for regression?**
  → Accuracy measures correct class predictions. Price is a real number — there's no "correct" class. A prediction of ₹85L for a ₹90L house is "wrong" by accuracy but actually quite good. RMSE and R² measure how close you are.

- **What is RMSE?**
  → Root Mean Squared Error = `sqrt(mean((actual - predicted)²))`. Same unit as the target (Lakhs). An RMSE of 30 means your average prediction is off by ₹30 Lakhs.

- **What is R²?**
  → R-squared = how much of the variation in price the model explains. R² = 1.0 is perfect. R² = 0 means the model is no better than always predicting the mean price.

- **How do I handle location? It's text, not a number.**
  → LabelEncoder assigns a unique integer to each location (e.g., Whitefield=42, Indiranagar=21). The model learns which numbers correlate with higher prices.

- **Why is feature importance useful?**
  → It tells you which input variable most influences the prediction. In real estate, knowing that location matters more than size (or vice versa) is a business insight, not just a technical result.

---

### Step 3 — Pseudo Code

```
START

  LOAD bengaluru_sample.csv

  FUNCTION parse_sqft(value):
    IF value contains "-":
      return average of the two numbers
    ELSE:
      return float(value)

  FUNCTION extract_bhk(size_string):
    return int of first word in "3 BHK" → 3

  CLEAN DATA:
    df["total_sqft"] = parse_sqft for each row
    df["bhk"] = extract_bhk for each row
    drop rows with null in key columns
    compute price_per_sqft = price × 100000 / total_sqft
    remove rows where price_per_sqft > mean + 3×std (outliers)
    group rare locations into "Other" (keep top 20 only)

  FEATURE ENGINEERING:
    location_encoded = LabelEncoder().fit_transform(location column)
    features = [total_sqft, bath, bhk, balcony, location_encoded]
    X = df[features]
    y = df["price"]

  SPLIT:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

  FOR model in [LinearRegression, RandomForestRegressor]:
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    RMSE = sqrt(mean_squared_error(y_test, preds))
    R²   = r2_score(y_test, preds)
    PRINT model name, RMSE, R²

  FEATURE IMPORTANCE:
    importance = rf_model.feature_importances_
    PRINT features sorted by importance
    PLOT horizontal bar chart

  PLOT predicted vs actual scatter plot (both models)

END
```

---

### Step 4 — Think About Feature Engineering First

The messiest part of this project is cleaning the data — not training the model. Think through each column:

```
total_sqft:
  "1056"      → fine, just convert to float
  "1200-1500" → take average: 1350
  "34.46Sq. Meter" → convert units (rare, can drop)

size:
  "2 BHK"     → extract "2"
  "2 Bedroom" → extract "2"
  NaN         → drop row

location:
  430 unique values in real data
  Problem: rare locations have very few houses → model can't learn from them
  Solution: group all locations with < 10 houses as "Other"
```

---

### Step 5 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| Sqft contains letters ("Sq. Meter") | Catch with `try/except` in `parse_sqft()` |
| Outlier: 1 BHK priced at ₹500 Crore | Remove by price_per_sqft filter |
| Location has 400+ unique values | Group rare ones as "Other" |
| R² is negative | Model is worse than mean prediction → check for data leakage or scaling issues |
| Small sample → low R² | Expected with 40 rows; use real Kaggle data |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Understanding the Problem

**Is this classification or regression? How do you know?**

```
Write here:


```

**What is the target variable (what are you predicting)?**

```
Write here:

```

**What features will you use and why?**

```
Feature 1: ________ because:
Feature 2: ________ because:
Feature 3: ________ because:
```

---

### Step 2 — Data Cleaning Plan

**For each problematic column, write how you will fix it:**

```
total_sqft issue: "1200-1500" (a range, not a number)
Fix:

size issue: "3 BHK" (text, not a number)
Fix:

location issue: 400+ unique text values
Fix:
```

---

### Step 3 — Why Not Accuracy?

**Explain in your own words why accuracy is the wrong metric for this problem:**

```
Write here:


```

**What does RMSE measure? Give an example using house prices:**

```
Write here:


```

---

### Step 4 — Your Pseudo Code

```
Write the main pipeline steps:

Step 1 (Load):
Step 2 (Clean):
Step 3 (Features):
Step 4 (Train):
Step 5 (Evaluate):
Step 6 (Explain):
```

---

### Step 5 — After finishing, reflect

**What was the most important feature? Does this make real-world sense?**

```
Write here:

```

**What is the RMSE of your model? What does that mean in rupees?**

```
RMSE = _____ Lakhs = ₹ _____________
Interpretation:

```

**What could you add to improve the model?**

```
Write here:

```
