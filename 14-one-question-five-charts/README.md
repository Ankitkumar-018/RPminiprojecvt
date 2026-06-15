# Project 14: One Question, Five Charts

Answer a single business question — "Which category drives the most revenue?" — using 5 different chart types. Learn when each chart reveals something the others miss.

**Skills practiced:** Matplotlib visualisation, pandas groupby, choosing the right chart for the right question.

---

## What This Project Does

```
sales_sample.csv
(72 rows: 3 categories × 4 regions × 6 months)
        │
        ▼
┌────────────────────────────────────────────┐
│               charts.py                    │
│                                            │
│  The Question:                             │
│  "Which category drives most revenue?"     │
│                                            │
│  Chart 1: Bar     → total comparison       │
│  Chart 2: Line    → trend over time        │
│  Chart 3: Pie     → proportion / share     │
│  Chart 4: Stacked → composition within     │
│  Chart 5: Heatmap → two-dimension pattern  │
└────────────────────────────────────────────┘
        │
        ▼
charts/chart1_bar.png
charts/chart2_line.png
charts/chart3_pie.png
charts/chart4_stacked_bar.png
charts/chart5_heatmap.png
```

---

## The Key Lesson

Every chart answers a slightly different version of the question:

| Chart | What It Answers |
|-------|----------------|
| Bar chart | Which category has the highest total? |
| Line chart | Which category leads **every month**? |
| Pie chart | What **percentage** of revenue does each category hold? |
| Stacked bar | How does the category breakdown change **month to month**? |
| Heatmap | Which category performs best in which **region**? |

The bar chart tells you "Electronics wins." The heatmap tells you "Electronics × North is the single biggest combination." Same question — very different insights.

---

## Setup — Step by Step

**Step 1: Go to the project folder**
```bash
cd 14-one-question-five-charts
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
python charts.py
```

---

## Expected Output

```
============================================================
  One Question, Five Charts
  Question: Which product category drives the most revenue?
============================================================
Loaded 72 rows × 6 columns
Categories: ['Clothing', 'Electronics', 'Food']
Months: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
Total sales: ₹9,498,000

  Generating charts...

  Chart 1: Bar Chart
  When to use: Comparing totals across categories — best for 'which is biggest'
  What you see: Electronics (₹4.29M) clearly leads. Simple, direct, no ambiguity.

  Chart 2: Line Chart
  When to use: Showing how values change over time — best for trends
  What you see: All 3 categories are growing. Electronics maintains its lead.

  Chart 3: Pie Chart
  When to use: Showing proportions that add to 100%
  What you see: Electronics is 45.2% of all revenue.

  Chart 4: Stacked Bar Chart
  When to use: Showing composition within each group
  What you see: Total monthly revenue grows AND Electronics takes largest chunk.

  Chart 5: Heatmap
  When to use: Showing two-dimensional patterns
  What you see: Electronics × North is highest revenue combination.

============================================================
  SUMMARY: Which Chart for Which Purpose?
============================================================
  Bar chart          → Compare totals — which is biggest?
  Line chart         → Show trends — how does it change over time?
  Pie chart          → Show proportions — what % is each?
  Stacked bar        → Show composition — what's inside each bar?
  Heatmap            → Show two dimensions — which combo stands out?

  ANSWER TO THE QUESTION:
  Electronics (₹4.29M) drives the most revenue.
  Electronics is 45.2% of total sales.
```

---

## How the Code Works

### 1. Load with Categorical Month Order

```python
df["month"] = pd.Categorical(df["month"],
                categories=["Jan","Feb","Mar","Apr","May","Jun"],
                ordered=True)
```

Without this, matplotlib would sort months alphabetically: Apr, Feb, Jan... Using `pd.Categorical` tells pandas these have a specific order.

### 2. Bar Chart — groupby + sort

```python
totals = df.groupby("category")["sales"].sum().sort_values(ascending=False)
ax.bar(totals.index, totals.values / 1_000_000, color=[COLORS[c] for c in totals.index])
```

`groupby("category")["sales"].sum()` — for each category, sum all sales rows. The color list maps category names to specific hex colours defined in `COLORS`.

### 3. Line Chart — groupby two columns

```python
monthly = df.groupby(["month", "category"])["sales"].sum().reset_index()
for cat in COLORS:
    subset = monthly[monthly["category"] == cat]
    ax.plot(subset["month"], subset["sales"] / 1000, marker="o", label=cat)
```

Group by both month AND category. Then plot each category as a separate line.

### 4. Stacked Bar — unstack + cumulative bottom

```python
monthly = df.groupby(["month", "category"])["sales"].sum().unstack("category")
bottom = pd.Series([0] * len(monthly), index=monthly.index)

for cat in ["Electronics", "Clothing", "Food"]:
    ax.bar(monthly.index, monthly[cat], bottom=bottom)
    bottom = bottom + monthly[cat]   # next bar starts where this one ends
```

The `bottom` parameter tells matplotlib where each bar segment starts. After each category, the bottom shifts up.

### 5. Heatmap — pivot table + imshow

```python
pivot = df.groupby(["region", "category"])["sales"].sum().unstack("category")
ax.imshow(pivot.values, cmap="YlOrRd")
```

`unstack()` converts the category level into columns, creating a 2D matrix. `imshow()` treats that matrix as pixel colours — higher values get darker colours.

---

## Real Dataset (Optional — Kaggle)

This project uses a synthetic 72-row dataset. For a more interesting challenge:

**Superstore Sales (9,994 rows)**
```
https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
```
Download `Sample - Superstore.csv`, rename columns to match (`category`, `sales`, `region`, etc.) and run the same code.

---

## What You Learn

| Skill | Where It Appears |
|-------|-----------------|
| `groupby` with aggregation | `df.groupby("category")["sales"].sum()` |
| Groupby multiple columns | `groupby(["month", "category"])` |
| Unstack for pivot tables | `.unstack("category")` |
| Categorical ordering | `pd.Categorical(..., ordered=True)` |
| Bar, line, pie, stacked, heatmap | Each chart function |
| Annotating bars with text | `ax.text(bar.get_x(), bar.get_height(), ...)` |
| Color dictionaries | `COLORS = {"Electronics": "#2196F3", ...}` |

---

## Student Challenge

1. Add a 6th chart: a scatter plot of `units` vs `profit` coloured by category. Does higher units sold always mean more profit?
2. Change the question to "Which region generates the most revenue?" and recreate all 5 charts for that question.
3. Answer: When is a pie chart a **bad** choice? (Hint: try making one with 8 categories.)
4. Download the Kaggle Superstore dataset and run this analysis on real data. What changes?
