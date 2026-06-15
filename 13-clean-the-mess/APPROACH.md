# Project 13: Clean the Mess — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a data engineer thinks about cleaning a dataset.

---

### Step 1 — Understand the Problem

**What does data cleaning actually mean?**
Raw data from the real world is almost never analysis-ready. It has:
- Inconsistencies ("Male" / "M" / "male" all meaning the same thing)
- Format variations ("₹85000" / "75K" / "90000 INR")
- Errors (age = 250, salary = -5000)
- Missing values (some fields are blank or "N/A")
- Duplicates (the same row entered twice)

Data cleaning means fixing all of these — **and documenting every decision**.

**Why document decisions?**
Because cleaning involves judgment. If you set a salary to NaN because it was negative, someone else reading your data needs to know why it's blank. The `cleaning_log.md` file is your audit trail.

---

### Step 2 — Questions to Ask Before Writing Code

- **What format are the dates in?**
  → Look at the raw CSV first. Count how many different date formats exist. List them all.

- **What makes a salary value "impossible"?**
  → Negative salary is definitely wrong. What about ₹500? Could be a typo for ₹50,000. You decide the threshold and write it down.

- **Should I impute (guess) missing values or leave them as NaN?**
  → It depends on the column. Performance rating: fill with department median (reasonable estimate). Age: don't impute — you could add 10 years to someone's age by accident. Document the rule.

- **What counts as a duplicate?**
  → Exact row duplicates are obvious. But what about E015 and E023 (same person, different employee ID)? This is harder — usually you'd need business context.

---

### Step 3 — Pseudo Code

```
START

  LOAD CSV with dtype=str   ← don't let pandas guess types

  PRINT snapshot:
    shape (rows × columns)
    null count per column

  ── STEP 1: Fix column names ──
    strip whitespace, lowercase, replace spaces with underscores

  ── STEP 2: Remove duplicates ──
    df.drop_duplicates()
    LOG how many were removed

  ── STEP 3: Clean name column ──
    strip leading/trailing whitespace
    apply Title Case
    LOG count of changes

  ── STEP 4: Standardise gender ──
    map {"male": "Male", "m": "Male", "female": "Female", "f": "Female"}
    LOG how many were remapped
    any unmapped → NaN + log warning

  ── STEP 5: Standardise department ──
    strip + Title Case
    fix "Hr" → "HR"
    LOG count of changes

  ── STEP 6: Parse salary ──
    define parse_salary(val):
      remove ₹, commas, spaces
      remove "INR" suffix
      if ends with K: multiply by 1000
      try convert to float
    apply to all rows
    flag negative → NaN + LOG
    flag < 10000 → NaN + LOG (likely entry error)
    LOG salary parsing

  ── STEP 7: Fix impossible ages ──
    convert to numeric (errors="coerce" → NaN for "N/A")
    flag age < 18 OR age > 70 → NaN + LOG

  ── STEP 8: Parse dates ──
    strip ordinal suffixes: "22nd" → "22" using regex
    try each format: ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y"]
    standardise to: "%Y-%m-%d"
    LOG parsing

  ── STEP 9: Handle missing values ──
    performance_rating → fill with department median + LOG
    experience_years → fill with 0 + LOG
    age → leave as NaN + LOG (too risky to impute)
    salary → leave as NaN + LOG (too risky to impute)

  ── STEP 10: Fix data types ──
    cast numeric columns to float
    cast joining_date to datetime
    LOG type casting

  SAVE clean CSV
  WRITE cleaning_log.md (table of all LOG entries)

  PRINT final summary:
    rows before / after
    duplicates removed
    remaining nulls

END
```

---

### Step 4 — Thinking Through the Hard Cases

**Salary: "₹65,000" appears as "₹65" in one row**

This is because someone split across a comma that the CSV treated as a field separator. The value loaded as "₹65" — which after parsing becomes 65. Is 65 a valid salary? No. Your `too_low` threshold catches it:

```
IF salary < 10000 THEN salary = NaN
```

You've lost the original value (it was probably ₹65,000) so you log it for manual review.

**Age: "N/A" in the raw file**

When you do `pd.to_numeric(df["age"], errors="coerce")`, the string "N/A" can't be converted and becomes NaN. Then your impossible-age check (`age < 18`) won't trigger because NaN comparisons return False. So "N/A" rows end up with NaN age automatically — correct behaviour.

**Date: "22nd June 2020"**

Python's `strptime` format `%d %B %Y` would match "22 June 2020" but fails on "22nd June 2020" because of the "nd" suffix. Solution: strip ordinal suffixes first with regex:

```python
val = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", val)
# "22nd June 2020" → "22 June 2020"
```

---

### Step 5 — What Could Go Wrong?

| Risk | How to Handle |
|------|---------------|
| CSV has commas in text fields | Load with `quotechar='"'` (default); check raw file first |
| Department median is NaN (all NaN in that dept) | `.median()` returns NaN — check and handle |
| Ordinal regex breaks a number like "23rd" | Test regex on all date strings before running |
| Date format "07-03-2017" — DD-MM or MM-DD? | Decide a rule (we use DD-MM) and document it |
| "₹1,10,000" — Indian comma format | Stripping all commas gives 110000 — correct |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE writing any code.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — Look at the Raw Data

Open `data/messy_employees.csv` in a spreadsheet or text editor. List every problem you find:

```
Issue 1:
Issue 2:
Issue 3:
Issue 4:
Issue 5:
Issue 6:
Issue 7:
Issue 8:
Issue 9:
Issue 10:
```

---

### Step 2 — Salary: All the Formats

Look at the salary column. List every format you see:

```
Format 1:  e.g. ₹85000
Format 2:
Format 3:
Format 4:
Format 5:

How would you convert all of them to a plain number?
Write the steps:



```

---

### Step 3 — Date Parsing Plan

List all the date formats in the joining_date column:

```
Format 1:
Format 2:
Format 3:
Format 4:

One of the dates has "22nd" — what problem does this cause?
Answer:

How would you fix it before parsing?
Answer:
```

---

### Step 4 — Missing Value Strategy

For each column with missing values, decide what to do:

```
Column: age
Decision (impute / leave as NaN):
Reason:

Column: performance_rating
Decision (impute / leave as NaN):
Reason:
What value would you impute?

Column: experience_years
Decision (impute / leave as NaN):
Reason:
What value would you impute?
```

---

### Step 5 — Your Pseudo Code

```
Write the steps here:

Step 1 (Load):
Step 2 (Duplicates):
Step 3 (Names):
Step 4 (Gender):
Step 5 (Department):
Step 6 (Salary):
Step 7 (Age):
Step 8 (Dates):
Step 9 (Missing values):
Step 10 (Types):
```

---

### Step 6 — After Finishing, Reflect

**Open `cleaning_log.md`. How many cleaning decisions were made?**
```
Answer:
```

**Which decision do you disagree with? Why?**
```
Decision I'd change:
My alternative approach:
Reason:
```

**What does E004's salary issue teach you about collecting data from humans?**
```
Answer:
```
