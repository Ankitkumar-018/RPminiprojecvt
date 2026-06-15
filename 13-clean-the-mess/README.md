# Project 13: Clean the Mess

Take a deliberately messy employee dataset and produce a clean, analysis-ready version — with every cleaning decision documented and justified.

**Skills practiced:** Pandas data cleaning, handling mixed formats, missing value strategy, generating automated reports.

---

## What This Project Does

```
messy_employees.csv
  (30 rows, 10 issues)
        │
        ▼
┌────────────────────────────────────────┐
│           clean.py                     │
│                                        │
│  1. Load everything as strings         │
│  2. Remove exact duplicates            │
│  3. Standardise names (Title Case)     │
│  4. Standardise gender (M/F → Male)    │
│  5. Standardise department casing      │
│  6. Parse salary (₹ / K / INR formats) │
│  7. Fix impossible ages                │
│  8. Parse 4 different date formats     │
│  9. Fill missing values (strategy-driven)│
│ 10. Cast final data types              │
└────────────────────────────────────────┘
        │
        ▼
clean_employees.csv  +  cleaning_log.md
```

---

## Messy Issues Built Into the Dataset

| Issue | Example |
|-------|---------|
| Duplicate rows | E001 (Arjun Sharma) appears twice |
| Inconsistent gender | "Male", "M", "male", "FEMALE", "F" |
| Inconsistent department casing | "Engineering", "engineering", "hr" |
| Salary with currency symbols | "₹85000", "90000 INR", "75K", "₹1,10,000" |
| Negative salary | E013: salary = -5000 |
| Mixed date formats | "2021-03-15", "15/04/2019", "22nd June 2020", "07-03-2017" |
| Impossible age values | E008: age = 250, E028: age = 999 |
| Missing values | age, experience_years, performance_rating |
| Extra whitespace in names | "  Anita Desai  " |
| Mixed name casing | "RAHUL VERMA", "priya mehta" |

---

## Setup — Step by Step

**Step 1: Clone or download the project**
```bash
cd 13-clean-the-mess
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

**Step 4: Run the cleaning script**
```bash
python clean.py
```

---

## Expected Output

```
============================================================
  Clean the Mess — Employee Dataset
  Input:  data/messy_employees.csv
  Output: data/clean_employees.csv
============================================================

============================================================
  RAW DATA SNAPSHOT
============================================================
  Shape: 30 rows × 10 columns
  Null counts:
    age                      1 nulls
    performance_rating       1 nulls
    experience_years         1 nulls

============================================================
  STEP 2: Duplicates
============================================================
  [2 row(s)] Exact duplicate rows found
           → Dropped 2 duplicate rows (kept first occurrence)
           e.g. E023 (Deepak Tiwari) and E001 (Arjun Sharma) were duplicated

...

============================================================
  FINAL SUMMARY
============================================================
  Rows before cleaning: 30
  Rows after cleaning:  28
  Duplicates removed:   2
  Remaining nulls:      4 (see cleaning_log.md)

  Clean file saved:  data/clean_employees.csv
  Cleaning log:      cleaning_log.md
```

Two files are generated:
- `data/clean_employees.csv` — the clean dataset, ready for analysis
- `cleaning_log.md` — a full table of every decision made and why

---

## How the Code Works

### 1. Load as Strings First

```python
df = pd.read_csv(filepath, dtype=str)
```

Loading with `dtype=str` prevents pandas from guessing types and converting `"₹85000"` to NaN or corrupting date strings. You always decide when to convert.

### 2. Salary Parsing — Handling Every Format

```python
def parse_salary(val):
    val = val.replace("₹", "").replace(",", "").replace(" ", "").upper()
    if val.endswith("INR"):
        val = val[:-3]
    if val.endswith("K"):
        return float(val[:-1]) * 1000   # "75K" → 75000
    return float(val)
```

This handles all 5 salary formats in one function. After parsing, impossible values (negative, below ₹10,000) are set to `NaN` with a log entry explaining why.

### 3. Date Parsing — Try All Formats

```python
formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y"]

def parse_date(val):
    val = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", val)   # strip ordinals
    for fmt in formats:
        try:
            return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return pd.NaT
```

The key trick: strip ordinal suffixes (`22nd → 22`, `25th → 25`) with a regex, then try every known format.

### 4. Missing Value Strategy

Different columns need different strategies:

| Column | Strategy | Reason |
|--------|----------|--------|
| `performance_rating` | Fill with department median | Similar roles have similar ratings |
| `experience_years` | Fill with 0 | Missing often means "new joinee" |
| `age` | Leave as NaN | Cannot safely impute — flag for HR |
| `salary` | Leave as NaN | Cannot safely impute — flag for HR |

The cleaning log documents every decision so others can audit or override it.

### 5. Everything Gets Logged

```python
log("Salary had mixed formats: ₹85000 / 90000 INR / 75K",
    "Stripped currency symbols, commas, 'INR'. Converted 'K' × 1000",
    "all rows",
    "'75K' → 75000 | '₹85,000' → 85000")
```

The `log()` function records every decision as a row in `cleaning_log.md`, so this script doubles as a data audit trail.

---

## Real Dataset (Optional — Kaggle)

This project includes a synthetic 30-row dataset to practice on. For a real-world challenge:

**IBM HR Analytics (14,999 rows)**
```
https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
```
Download `WA_Fn-UseC_-HR-Employee-Attrition.csv`, place in `data/`, and adapt column names in `clean.py`.

---

## What You Learn

| Skill | Where It Appears |
|-------|-----------------|
| Loading CSV safely | `pd.read_csv(..., dtype=str)` |
| Deduplication | `df.drop_duplicates()` |
| Regex for text cleaning | `re.sub(r"(\d+)(st\|nd\|rd\|th)", r"\1", val)` |
| Salary format normalisation | `parse_salary()` |
| Multi-format date parsing | `parse_date()` with format loop |
| Missing value strategies | `fillna(median)` vs leave as NaN |
| Automated audit trail | `log()` → `cleaning_log.md` |

---

## Student Challenge

After running the script, open `cleaning_log.md` and answer:

1. Which column had the most issues?
2. For `E004`, the salary was set to NaN. Do you agree with that decision? Why?
3. Try adding a new cleaning step: flag employees where `experience_years > age - 18` (impossible — they can't have more experience than working years possible).
4. Download the Kaggle dataset and adapt the script. What new issues do you find?
