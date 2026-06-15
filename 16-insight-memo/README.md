# Project 16: Insight Memo

Build a script that reads an e-commerce orders CSV and automatically generates a structured business memo — with numbers, tables, charts, and recommendations — as a markdown file.

**Skills practiced:** Pandas aggregation, data storytelling, translating numbers into business language, auto-generating reports.

---

## What This Project Does

```
ecommerce_sample.csv
(70 orders: Jan–Mar 2024, electronics/clothing/food/books)
        │
        ▼
┌────────────────────────────────────────────────────┐
│                    memo.py                         │
│                                                    │
│  Analyses 5 dimensions:                            │
│    1. Revenue — total, by category, by month       │
│    2. Returns — rate, by category, impact          │
│    3. Customers — repeat buyers, geography         │
│    4. Delivery — speed, delays, rating correlation │
│    5. Satisfaction — ratings, low-rated orders     │
│                                                    │
│  Generates:                                        │
│    - 2 summary charts (PNG)                        │
│    - insight_memo.md (complete business memo)      │
└────────────────────────────────────────────────────┘
        │
        ▼
insight_memo.md
charts/memo_revenue.png
charts/memo_quality.png
```

---

## The Key Lesson: Numbers Aren't Insights

Anyone can print `df.describe()`. The skill is turning raw statistics into business language:

| Raw Number | Insight |
|------------|---------|
| Electronics return_rate = 14.3% | "High-value Electronics returns have the most financial impact — one returned laptop costs as much as 10 returned books." |
| rating_days_corr = -0.41 | "Longer delivery times correlate with lower ratings. Orders taking >5 days have significantly worse satisfaction scores." |
| C012 has 5 orders | "One customer placed 5 orders worth ₹31,300. Repeat customers are a high-value segment worth a loyalty programme." |

The `write_memo()` function translates every number into a sentence like this.

---

## Setup — Step by Step

**Step 1: Go to the project folder**
```bash
cd 16-insight-memo
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
python memo.py
```

**Step 5: Read the memo**
```bash
# Open in any markdown viewer, or:
cat insight_memo.md
```

---

## Expected Output (Terminal)

```
=======================================================
  Insight Memo Generator
  Dataset: data/ecommerce_sample.csv
=======================================================

───────────────────────────────────────────────────────
  Analysing...
───────────────────────────────────────────────────────
  Orders: 70
  Period: 2024-01-05 to 2024-03-24

───────────────────────────────────────────────────────
  Key Numbers
───────────────────────────────────────────────────────
  Total revenue:     ₹6,52,480
  Top category:      Electronics (56.2% of revenue)
  Return rate:       10.0%
  Avg rating:        4.14/5.0
  Avg delivery:      5.6 days
  Repeat customers:  4 of 66

───────────────────────────────────────────────────────
  Generating Charts
───────────────────────────────────────────────────────
  charts/memo_revenue.png
  charts/memo_quality.png

───────────────────────────────────────────────────────
  Writing Memo
───────────────────────────────────────────────────────
  Memo written: insight_memo.md

=======================================================
  Done. Open insight_memo.md to read the memo.
=======================================================
```

---

## The Generated Memo Structure

`insight_memo.md` contains 7 sections:

```
# Insight Memo — E-Commerce Performance

Executive Summary (3 sentences of key numbers)

1. Revenue (table + finding)
2. Returns (return rate by category + finding)
3. Customers & Geography (repeat buyers + top cities)
4. Delivery Performance (speed + rating correlation)
5. Customer Satisfaction (ratings by category)
6. Recommendations (priority table with evidence)
7. Data Notes (dataset info)
```

---

## How the Code Works

### 1. Separate Analysis from Writing

Each analysis function returns a dictionary of computed values:

```python
rev = analyse_revenue(df)    # → {"total_revenue": ..., "top_category": ..., ...}
ret = analyse_returns(df)    # → {"return_rate": ..., "returns_by_category": ..., ...}
```

Then `write_memo()` takes all these dictionaries and assembles the document. This separation means you can change the writing style without touching the analysis — or reuse analysis results for different report formats.

### 2. Feature Engineering for Delivery

```python
df["delivery_days"] = (df["delivery_date"] - df["order_date"]).dt.days
```

Pandas can subtract two datetime columns directly. The `.dt.days` extracts the number of days as an integer. This lets you compute delivery speed, find late orders, and correlate with ratings.

### 3. Correlation as a Finding

```python
corr = df["rating"].corr(df["delivery_days"])
```

This single line computes the Pearson correlation between delivery time and customer rating. A value of -0.4 means "longer deliveries tend to get lower ratings." In the memo, this becomes an actionable insight.

### 4. Dynamic Recommendations

```python
top_return_cat = ret["returns_by_category"].idxmax()
top_return_rate = ret["returns_by_category"].max()
recs = [
    ("HIGH", f"Investigate {top_return_cat} return causes",
     f"{top_return_rate:.1f}% return rate — highest of all categories"),
```

Recommendations are built from actual numbers, not hardcoded text. If you run this script on a different dataset where Clothing has the highest return rate, the memo will say "Investigate Clothing return causes" — automatically.

### 5. Period-Aware Summary

```python
df["month"] = df["order_date"].dt.to_period("M").astype(str)
by_month = df.groupby("month")["order_value"].sum()
```

`dt.to_period("M")` converts a date to its month period ("2024-01", "2024-02"). Grouping by this gives monthly totals. The memo can then say "February was the best month, up 12% vs January."

---

## Real Dataset (Optional — Kaggle)

**Olist Brazilian E-Commerce (100,000 orders)**
```
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
```
Download `olist_orders_dataset.csv` and `olist_order_items_dataset.csv`, join them, rename columns to match (`order_value`, `order_date`, `delivery_date`), and run `memo.py`. The memo will scale automatically to millions of rows.

---

## What You Learn

| Skill | Where It Appears |
|-------|-----------------|
| Datetime arithmetic | `(delivery_date - order_date).dt.days` |
| Period groupby | `dt.to_period("M")` |
| Pearson correlation | `df["rating"].corr(df["delivery_days"])` |
| Dynamic text generation | f-strings with computed values |
| Separating analysis from reporting | `analyse_*()` vs `write_memo()` |
| Writing markdown from Python | `f.writelines(lines)` |

---

## Student Challenge

1. Add a **Section 8: Discount Analysis** — do orders with higher discounts return more often? Are they rated differently?
2. Make the memo output as **HTML** instead of markdown (hint: replace `#` headers with `<h1>` tags and `|` tables with `<table>` tags).
3. Add a **flag** in the executive summary: "⚠ Warning: Electronics return rate is above 10% — this needs immediate investigation."
4. Download the Kaggle dataset and run the script. Does the structure of `insight_memo.md` still make sense at 100,000 rows? What would you change?
