# Project 14: One Question, Five Charts — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data analyst thinks about visualisation.

---

### Step 1 — Understand the Problem

**Why five charts for one question?**
Every chart type is designed to answer a different question. If you always use bar charts, you miss trends. If you only use line charts, you miss proportions. By building all 5 for the same dataset, you train yourself to pick the right tool automatically.

**The one question:**
> "Which product category drives the most revenue?"

This question can be answered in 5 ways:
- "Which category has the biggest number?" → Bar chart
- "Which category has led every month?" → Line chart
- "What percentage of total revenue is each category?" → Pie chart
- "How do categories combine inside each month?" → Stacked bar
- "Which category + region combination is biggest?" → Heatmap

---

### Step 2 — Questions to Ask Before Writing Code

- **What does the data look like?**
  → 3 categories × 4 regions × 6 months = 72 rows. Each row has a sales number.

- **What aggregation does each chart need?**
  → Bar: `groupby("category").sum()`
  → Line: `groupby(["month", "category"]).sum()` (monthly, per category)
  → Pie: same as bar
  → Stacked: same as line, but `unstack()` to make it a 2D table
  → Heatmap: `groupby(["region", "category"]).sum()` then `unstack()`

- **Why does month ordering matter?**
  → Alphabetical order is wrong: Apr, Feb, Jan, Jun, Mar, May. You need Jan → Jun. Use `pd.Categorical` with an explicit order.

- **When is a chart a bad choice?**
  → Pie charts are bad when you have more than 5 slices (too hard to compare)
  → Line charts are bad for non-time data (doesn't imply sequence)
  → Bar charts are bad when showing proportions (use pie/stacked instead)

---

### Step 3 — Pseudo Code

```
START

  LOAD CSV
    month → convert to Categorical with fixed order [Jan...Jun]

  DEFINE COLORS = {"Electronics": blue, "Clothing": orange, "Food": green}

  ── CHART 1: Bar ──
    totals = groupby("category")["sales"].sum()
    sort descending
    bar chart: categories on x, totals on y
    annotate each bar with ₹ amount
    save → chart1_bar.png
    PRINT insight

  ── CHART 2: Line ──
    monthly = groupby(["month","category"])["sales"].sum()
    FOR each category:
      PLOT line with markers
    save → chart2_line.png
    PRINT insight

  ── CHART 3: Pie ──
    totals = groupby("category")["sales"].sum()
    pie(totals, autopct="%1.1f%%")
    save → chart3_pie.png
    PRINT insight

  ── CHART 4: Stacked Bar ──
    monthly_2d = groupby(["month","category"]).sum().unstack("category")
    bottom = zeros series
    FOR each category:
      bar(month, values, bottom=bottom)
      bottom += values    ← shift up for next segment
    save → chart4_stacked_bar.png
    PRINT insight

  ── CHART 5: Heatmap ──
    pivot = groupby(["region","category"]).sum().unstack()
    imshow(pivot.values, cmap="YlOrRd")
    annotate each cell with its value
    save → chart5_heatmap.png
    PRINT insight

  PRINT summary: chart type → when to use

END
```

---

### Step 4 — Think Through the Stacked Bar Trick

The key to a stacked bar chart is the `bottom` parameter:

```
Month: Jan
  Food segment:        bar from 0 to 138,000
  Clothing segment:    bar from 138,000 to 394,000   (bottom=138,000)
  Electronics segment: bar from 394,000 to 814,000   (bottom=394,000)
```

After drawing each category, the `bottom` shifts up by that category's height. If you forget to do this, all bars start at 0 and overlap.

```python
bottom = 0
for cat in ["Food", "Clothing", "Electronics"]:
    ax.bar(months, monthly[cat], bottom=bottom, label=cat)
    bottom = bottom + monthly[cat]   # critical line!
```

---

### Step 5 — What Could Go Wrong?

| Risk | How to Handle |
|------|---------------|
| Month order is wrong (alphabetical) | Use `pd.Categorical` with explicit order |
| Colors don't match across charts | Define COLORS dict once, use everywhere |
| Values in different scales make comparison hard | Convert to same unit (₹ Thousands or Millions) |
| Heatmap text unreadable on dark cells | Check value and switch text color: black if low, white if high |
| Pie chart with too many slices | Bad chart — do not use pie for > 5 categories |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Choose Your Question

**What business question will your 5 charts answer?**

```
My question: 
```

**What dataset will you use? (columns it has)**

```
Dataset:
Columns:
```

---

### Step 2 — Plan Each Chart

For each chart, write what aggregation you'll need:

```
Chart 1 (Bar):
  groupby:
  what's on x-axis:
  what's on y-axis:

Chart 2 (Line):
  groupby:
  what creates separate lines:
  x-axis (time column):

Chart 3 (Pie):
  groupby:
  what determines slice size:

Chart 4 (Stacked Bar):
  groupby:
  what creates the segments (stacks):
  x-axis groups:

Chart 5 (Heatmap):
  groupby:
  rows of heatmap:
  columns of heatmap:
```

---

### Step 3 — The Stacked Bar Trick

**Explain in your own words: why do you need the `bottom` variable?**

```
Answer:


```

**What happens if you forget to update `bottom += values`?**

```
Answer:


```

---

### Step 4 — Your Pseudo Code

```
Write steps here:

Step 1 (Load + prepare data):
Step 2 (Chart 1 — Bar):
Step 3 (Chart 2 — Line):
Step 4 (Chart 3 — Pie):
Step 5 (Chart 4 — Stacked Bar):
Step 6 (Chart 5 — Heatmap):
```

---

### Step 5 — After Finishing, Reflect

**Which chart was most useful for answering your question? Why?**

```
Answer:


```

**Which chart was the LEAST useful? Why?**

```
Answer:


```

**Give a business scenario where a pie chart is the WRONG choice:**

```
Scenario:
Why it's wrong:
Better chart to use:
```
