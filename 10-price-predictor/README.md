# Project 10: Price Predictor

## What Is This?

A regression model that predicts **Bengaluru house prices** from features like location, size, and number of bathrooms. Reports the right evaluation metric (RMSE + R²) and identifies the single most important feature.

---

## What Skills You Will Learn

- Data cleaning — parsing messy inputs like "1200-1500 sqft" and "3 BHK"
- Feature engineering — encoding categorical variables (location)
- Training and comparing regression models (Linear Regression vs Random Forest)
- Why accuracy is the wrong metric for regression problems
- Interpreting feature importance
- Reading a scatter plot of predicted vs actual values

---

## How the Pipeline Works

```
Raw CSV (location, size, sqft, bath, price)
        │
        ▼
   Clean data
   - Parse sqft ranges (e.g., "1200-1500" → 1350)
   - Extract BHK from "3 BHK"
   - Drop extreme outliers by price-per-sqft
   - Group rare locations as "Other"
        │
        ▼
   Feature engineering
   - Encode location as numbers (LabelEncoder)
   - Features: total_sqft, bath, bhk, balcony, location_encoded
        │
        ▼
   Train/Test Split (80/20)
        │
        ├── Linear Regression → RMSE + R²
        └── Random Forest     → RMSE + R² + Feature Importance
        │
        ▼
   Charts: Predicted vs Actual | Feature Importance bar
```

---

## Folder Structure

```
10-price-predictor/
├── predictor.py              ← Full pipeline (clean → train → evaluate → explain)
├── requirements.txt          ← pandas, scikit-learn, matplotlib
├── data/
│   └── bengaluru_sample.csv  ← 40-row sample (works immediately)
├── charts/                   ← Auto-created, stores output charts
└── README.md
```

---

## Dataset

### Option A — Run immediately (sample included)
`data/bengaluru_sample.csv` is already included. Works out of the box.

### Option B — Real dataset (recommended)

1. Go to: https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data
2. Download `Bengaluru_House_Data.csv`
3. Place it in the `data/` folder
4. Open `predictor.py` and update line 20:
   ```python
   DATA_FILE = "data/Bengaluru_House_Data.csv"
   ```

---

## Requirements

- Python 3.8 or higher

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 10-price-predictor
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run the predictor

```bash
python predictor.py
```

---

## Expected Output

```
============================================================
  Price Predictor — Bengaluru House Prices
============================================================

Loaded 40 rows | Columns: [area_type, availability, location, ...]
After cleaning: 38 rows

Features used: ['total_sqft', 'bath', 'bhk', 'balcony', 'location_encoded']
Target: price (in Lakhs)

====================================================
  Model Comparison
====================================================
  Model                     RMSE (Lakhs)   R² Score
  ──────────────────────────────────────────────────
  Linear Regression               48.21      0.712
  Random Forest                   36.88      0.831

  WHY NOT ACCURACY?
  House price is a continuous number — not a category.
  RMSE tells you the average error in Lakhs (rupees × 100,000).
  R² tells you how much price variation the model explains (1.0 = perfect).

====================================================
  Most Important Features (Random Forest)
====================================================
  location_encoded       0.482  ####################
  total_sqft             0.334  ##############
  bhk                    0.098  ####
  bath                   0.071  ###
  balcony                0.015  

  TOP FEATURE: 'location_encoded'
  Same flat, 2x the price in Indiranagar vs Electronic City.
```

---

## Why RMSE and R² (Not Accuracy)

| Metric | Used For | Why Not Here |
|--------|----------|--------------|
| Accuracy | Classification (spam/not spam) | Price is a number, not a category |
| RMSE | Regression | Average error in the same units as target (Lakhs) |
| R² | Regression | How much variance is explained (0 = random, 1 = perfect) |

**Example:** RMSE of 37 Lakhs means on average the model is off by ₹37,00,000. R² of 0.83 means the model explains 83% of the variation in house prices.

---

## Try It Yourself — Extension Ideas

- Add more features: `area_type` (super built-up vs carpet), `availability`
- Try `GradientBoostingRegressor` — often beats Random Forest on tabular data
- Plot price vs location as a box plot to see which areas are most expensive
- Try predicting `price_per_sqft` instead of raw price

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Wrong file path | Update `DATA_FILE` variable in `predictor.py` |
| `ModuleNotFoundError: sklearn` | scikit-learn not installed | `pip install -r requirements.txt` |
| Very low R² score | Too few rows in sample | Use real Kaggle dataset (13,000 rows) |
| `ValueError: could not convert` | Sqft column has unexpected format | Check `parse_sqft()` function and add your format |
