# Project 9: EDA Detective — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data analyst thinks before opening any dataset.

---

### Step 1 — Understand the Problem

**What does EDA mean?**
Exploratory Data Analysis — understanding a dataset by looking at its shape, distributions, relationships, and anomalies before building any model.

**What is the goal here?**
Not just describe the data — find 3 things that are surprising. Patterns that contradict common sense or popular belief. That's what "detective" means.

**Questions to ask about IPL data before touching code:**
- How many matches are in the dataset? How many seasons?
- What columns exist? What do they mean?
- Are there missing values? For which columns?
- What does a "win" look like in the data? (`win_by_runs` > 0 or `win_by_wickets` > 0?)

---

### Step 2 — Questions to Ask Before Writing Code

- **What counts as a non-obvious pattern?**
  → Something the data shows that contradicts what fans or commentators usually assume. Example: "Toss matters a lot" — does the data agree?

- **How do I find patterns?**
  → Group + aggregate. `groupby("toss_decision")["result"].value_counts()` shows patterns broken down by decision. Always start with groupby.

- **How do I know if a pattern is statistically meaningful?**
  → At minimum, it should hold across many seasons (not just one fluke year). With real data (800+ matches), a 5%+ gap is meaningful.

- **Which visualisation type for which pattern?**
  → Comparisons → bar chart
  → Proportions → pie chart or stacked bar
  → Trends over time → line chart
  → Distribution → histogram or box plot

---

### Step 3 — Pseudo Code

```
START

  LOAD matches.csv into a DataFrame

  PRINT basic info:
    - shape (rows × columns)
    - column names
    - null value counts
    - unique seasons

  PATTERN 1 — Toss advantage:
    toss_won_match = (toss_winner == winner)
    win_rate = mean(toss_won_match) × 100
    PRINT win_rate
    GROUP BY toss_decision → win rate per decision
    PLOT bar chart comparing win rates

  PATTERN 2 — Team dominance:
    FOR each team:
      played = count rows where team1==team OR team2==team
      won    = count rows where winner==team
      win_pct = won / played × 100
    SORT by win_pct descending
    PRINT top 10 teams
    PLOT horizontal bar chart

  PATTERN 3 — Bat vs Chase:
    bat_first_wins  = rows where win_by_runs > 0
    chase_wins      = rows where win_by_wickets > 0
    COMPUTE percentages
    PRINT summary
    PLOT pie chart + bar chart of margins

  SAVE all charts as PNG files

END
```

---

### Step 4 — Think About the Data Before Running

Before running any code, look at the CSV file in a text editor:

```
id, season, city, date, team1, team2, toss_winner, toss_decision,
result, winner, win_by_runs, win_by_wickets, player_of_match, venue

What does result = "normal" mean? (as opposed to "D/L" — rain affected)
What does win_by_runs = 0 mean? (the team chased — wickets column has the info)
What does winner = NaN mean? (match abandoned or tied)
```

Always inspect 5–10 rows manually before writing code.

---

### Step 5 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| `winner` column has NaN (abandoned) | Filter with `df[df['winner'].notna()]` |
| Rain-affected matches skew results | Filter `df[df['result'] == 'normal']` |
| Team names changed (Deccan Chargers → Sunrisers) | Either unify or note the discrepancy |
| Small sample shows extreme patterns | Note that small sample = less reliable |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — First Look at the Dataset

**Open the CSV and answer these questions:**

```
How many rows (matches)?:
How many columns?:
List 5 columns and what they mean:
  1.
  2.
  3.
  4.
  5.
Are there null values? In which columns?:
```

---

### Step 2 — Brainstorm 3 Non-Obvious Patterns

Before looking at the data, write 3 things you want to investigate that challenge a common belief:

```
Hypothesis 1 (common belief to test):
Why it might be wrong:

Hypothesis 2 (common belief to test):
Why it might be wrong:

Hypothesis 3 (common belief to test):
Why it might be wrong:
```

---

### Step 3 — Your Pseudo Code for Pattern 1

```
Pattern I will investigate:

Pseudo code:




Which chart type will you use and why?:
```

---

### Step 4 — What groupby + aggregation will you use?

```
Pattern 1: df.groupby("___")["___"].____ ()
Pattern 2: df.groupby("___")["___"].____ ()
Pattern 3: df.groupby("___")["___"].____ ()
```

---

### Step 5 — After finishing, reflect

**Which pattern surprised you the most? Why?**
```

```

**Did any pattern CONFIRM the common belief instead of contradicting it?**
```

```

**What additional data would make your analysis stronger?**
```

```
