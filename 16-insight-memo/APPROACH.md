# Project 16: Insight Memo — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data analyst thinks about building a report.

---

### Step 1 — Understand the Problem

**What is an "insight memo"?**
A business memo that translates raw data into readable findings and recommendations. It's not just tables of numbers — it explains what the numbers mean and what to do about them.

**Who is the audience?**
A business manager who doesn't write code. They need:
- Key numbers at the top (executive summary)
- Findings in plain English ("Electronics is 56% of revenue")
- A recommendation with evidence ("Fix Electronics returns — 14% return rate")

**What makes this different from just printing `df.describe()`?**
`df.describe()` gives you raw statistics. A memo gives you business language:

```
Raw output:            df["delivery_days"].mean() = 5.6
Memo finding:          "Orders average 5.6 days for delivery. Orders taking >5 days
                        have significantly lower satisfaction scores."
```

---

### Step 2 — Questions to Ask Before Writing Code

- **What 5 things does every business want to know about their orders?**
  → Revenue (how much), Returns (what came back), Customers (who's buying), Delivery (how fast), Ratings (are they happy)

- **How do you compute delivery time from the CSV?**
  → `(delivery_date - order_date).dt.days` — subtract two datetime columns.

- **What is "correlation" and what does it tell you here?**
  → Pearson correlation between delivery_days and rating. If it's -0.4, faster delivery = higher rating. If it's 0.0, they're unrelated.

- **How do you make the memo update automatically when you change the dataset?**
  → Use f-strings with computed values: `f"{rev['top_category']} contributes {rev['top_cat_share']:.1f}% of revenue"` — the numbers come from actual analysis, not hardcoded.

- **What makes a good recommendation?**
  → A good recommendation has: a priority (HIGH/MEDIUM/LOW), an action ("Investigate Electronics returns"), and evidence ("14.3% return rate — highest category").

---

### Step 3 — Pseudo Code

```
START

  LOAD CSV (parse_dates=["order_date","delivery_date"])
  ENGINEER:
    delivery_days = delivery_date - order_date (in days)
    month = order_date.to_period("M")

  ── ANALYSIS MODULE ──

  analyse_revenue():
    total = df["order_value"].sum()
    avg   = df["order_value"].mean()
    by_category = groupby("category")["order_value"].sum()
    by_month    = groupby("month")["order_value"].sum()
    best_month  = by_month.idxmax()
    mom_change  = (month[-1] - month[-2]) / month[-2] * 100
    RETURN all values as dict

  analyse_returns():
    return_rate = (returned == "Yes").sum() / total * 100
    by_category = groupby("category").apply(return_rate_per_cat)
    returned_avg_rating  = df[returned=="Yes"]["rating"].mean()
    normal_avg_rating    = df[returned=="No"]["rating"].mean()
    RETURN dict

  analyse_customers():
    repeat = customer_id value_counts where count > 1
    by_state = groupby("state")["order_value"].sum().head(5)
    by_city  = groupby("city")["order_value"].sum().head(5)
    RETURN dict

  analyse_delivery():
    avg_days = delivery_days.mean()
    late_count = (delivery_days > 5).sum()
    corr = rating.corr(delivery_days)
    RETURN dict

  analyse_ratings():
    avg = rating.mean()
    by_category = groupby("category")["rating"].mean()
    lowest_cat = by_category.idxmin()
    RETURN dict

  ── CHART MODULE ──
    Chart 1: Revenue by category (bar) + monthly trend (line) — side by side
    Chart 2: Return rate by category (barh) + rating by category (bar) — side by side

  ── MEMO WRITING MODULE ──
    write_memo(all dicts):
      FOR each section (Revenue, Returns, Customers, Delivery, Satisfaction):
        WRITE heading
        WRITE table of key numbers
        WRITE "Finding:" — plain English sentence using computed values
      WRITE Recommendations table (built from actual worst-performing values)
    SAVE as insight_memo.md

END
```

---

### Step 4 — Design Principle: Separate Analysis from Writing

The most important design decision in this project is keeping analysis and writing apart:

```
BAD approach (mixed):
  def analyse_and_write():
      total = df["order_value"].sum()
      f.write(f"Total revenue: ₹{total:,.0f}")
      by_cat = df.groupby("category")["order_value"].sum()
      f.write(f"Top category: {by_cat.idxmax()}")

GOOD approach (separated):
  def analyse_revenue(df):
      ...
      return {"total_revenue": total, "top_category": top_cat, ...}

  def write_memo(rev, ret, ...):
      lines.append(f"Total Revenue: ₹{rev['total_revenue']:,.0f}")
      lines.append(f"Top Category: {rev['top_category']}")
```

With separation:
- You can reuse `analyse_revenue()` for multiple output formats (markdown, HTML, PDF)
- You can test analysis functions independently
- The writing module reads naturally as a template

---

### Step 5 — What Could Go Wrong?

| Risk | How to Handle |
|------|---------------|
| Order date not parsed as datetime | Use `parse_dates=["order_date", "delivery_date"]` in read_csv |
| Month ordering wrong | Use `dt.to_period("M")` — periods sort correctly |
| Division by zero in return rate | Check `if len(df) > 0` before dividing |
| Only 1 month in dataset | Guard `if len(by_month) >= 2` before computing MoM change |
| Correlation is NaN | Happens if all values in a column are the same — handle with `if pd.notna(corr)` |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — What Are the 5 Key Questions?

**For your chosen dataset, what are the 5 most important things a business would want to know?**

```
Question 1 (Revenue/Volume):

Question 2 (Quality/Returns):

Question 3 (Customers/Users):

Question 4 (Performance/Speed):

Question 5 (Satisfaction):
```

---

### Step 2 — Design the analyse_*() Functions

**For each question, what calculation will you do?**

```
analyse_revenue():
  What I calculate:
  What I return (dict keys):

analyse_returns():
  What I calculate:
  What I return (dict keys):

analyse_customers():
  What I calculate:
  What I return (dict keys):
```

---

### Step 3 — Write One Finding

**Pick one number from your analysis and write the "Finding:" sentence in plain English:**

```
Raw number:

Plain English finding:
(e.g. "Electronics contributes X% of total revenue, more than all other categories combined.")
```

---

### Step 4 — Write One Recommendation

**A good recommendation has a priority, an action, and evidence. Fill in:**

```
Priority:  HIGH / MEDIUM / LOW
Action:    (what should the business do?)
Evidence:  (what number supports this?)
```

---

### Step 5 — Your Pseudo Code

```
Step 1 (Load + engineer features):
Step 2 (analyse_revenue):
Step 3 (analyse_returns):
Step 4 (analyse_customers):
Step 5 (analyse_delivery):
Step 6 (analyse_ratings):
Step 7 (generate_charts):
Step 8 (write_memo):
```

---

### Step 6 — After Finishing, Reflect

**Read your generated `insight_memo.md`. Would a business manager understand it?**

```
Yes / No — reason:
```

**What's the most surprising finding in your data?**

```
Finding:
Why it's surprising:
```

**If you had to email this memo to your CEO, what would the subject line be?**

```
Subject:
```
