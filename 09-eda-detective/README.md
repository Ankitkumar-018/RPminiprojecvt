# Project 9: EDA Detective

## What Is This?

An exploratory data analysis project that investigates **IPL match data** and surfaces **3 non-obvious patterns** — things that contradict common cricket assumptions — using visualisations.

EDA (Exploratory Data Analysis) is the first step in any data science project. Before building any model, you must understand your data.

---

## What Skills You Will Learn

- Loading and inspecting a real dataset with pandas
- Grouping and aggregating data (`groupby`, `value_counts`, `mean`)
- Handling missing values and cleaning data
- Creating meaningful charts with matplotlib
- Finding patterns that are surprising, not just obvious
- Communicating data insights clearly

---

## How the Analysis Works

```
Load matches.csv (IPL dataset from Kaggle)
        │
        ▼
   Inspect shape, columns, data types, null values
        │
        ▼
   ┌────────────────────────────────────────┐
   │  Pattern 1: Toss Win Rate              │
   │  Pattern 2: Team Dominance             │
   │  Pattern 3: Batting First vs Chasing   │
   └────────────────────────────────────────┘
        │
        ▼
   Generate charts (saved as PNG files)
        │
        ▼
   Print summary of non-obvious insights
```

---

## Folder Structure

```
09-eda-detective/
├── eda.py                    ← Main analysis script (all 3 patterns)
├── requirements.txt          ← pandas, matplotlib, seaborn
├── data/
│   └── matches_sample.csv    ← 40-row sample (works immediately)
├── charts/                   ← Auto-created, stores output charts
└── README.md
```

After running:
```
├── charts/
│   ├── pattern1_toss.png
│   ├── pattern2_teams.png
│   └── pattern3_batting.png
```

---

## Dataset

### Option A — Run immediately (sample data included)
The file `data/matches_sample.csv` is already included. Run the code as-is.

### Option B — Real IPL dataset (recommended for full analysis)

1. Go to: https://www.kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020
2. Download `matches.csv`
3. Place it in the `data/` folder
4. Open `eda.py` and change line 20:
   ```python
   DATA_FILE = "data/matches.csv"   # was "data/matches_sample.csv"
   ```

---

## Requirements

- Python 3.8 or higher
- pip

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 09-eda-detective
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Run the analysis

```bash
python eda.py
```

---

## Expected Output

```
============================================================
  EDA Detective — IPL Matches Analysis
  Data: data/matches_sample.csv
============================================================
Loaded 40 matches | Seasons: 2008–2021

============================================================
  PATTERN 1: Does winning the toss actually help?
============================================================
  Overall win rate after winning toss: 52.1%
  (A coin flip would give 50.0%)

  Win rate by toss decision:
    Chose to bat:   48.3%
    Chose to field: 54.2%

  INSIGHT: Winning the toss gives almost no advantage overall (~52%).
  Teams win roughly half the time regardless of toss — it's nearly random.

  Chart saved: charts/pattern1_toss.png

============================================================
  PATTERN 2: Which teams have been consistently dominant?
============================================================
  Team                                     Played   Won  Win %
  ────────────────────────────────────────────────────────────
  Chennai Super Kings                          12     8   66.7%
  Mumbai Indians                               11     7   63.6%
  Royal Challengers Bangalore                  10     5   50.0%
  ...

  INSIGHT: 2–3 teams win disproportionately across all seasons.

============================================================
  PATTERN 3: Is chasing or setting a target better?
============================================================
  Matches won batting first: 21 (52.5%)
  Matches won while chasing: 19 (47.5%)

  INSIGHT: Despite the belief that "chasing is easier in T20",
  the data shows it's roughly balanced overall.
```

---

## The 3 Non-Obvious Patterns

| # | Pattern | Common Assumption | What Data Shows |
|---|---------|-------------------|-----------------|
| 1 | Toss advantage | Winning toss = winning match | Win rate ≈ 52%, nearly random |
| 2 | Team dominance | All 10 teams compete equally | 2–3 teams win vastly more |
| 3 | Bat vs chase | Chasing is always easier in T20 | Roughly 50/50 overall — context matters |

---

## Try It Yourself — Extension Ideas

- Add Pattern 4: Which venue has the highest average score?
- Add Pattern 5: Does the Player of the Match always come from the winning team?
- Try the deliveries.csv dataset for ball-by-ball analysis
- Compare your findings across different IPL seasons (2008 vs 2020)

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `FileNotFoundError` | Wrong data file path | Check `DATA_FILE` variable at top of `eda.py` |
| `ModuleNotFoundError: pandas` | Dependencies not installed | Run `pip install -r requirements.txt` |
| Charts not showing | No display in some environments | Charts are saved to `charts/` folder — open them there |
| `KeyError: 'winner'` | Different column names in your CSV | Print `df.columns` to see actual column names |
