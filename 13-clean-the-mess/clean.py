"""
Clean the Mess — Employee Dataset Cleaning
Takes a deliberately messy CSV and produces a clean, analysis-ready version.
Every cleaning decision is logged with a reason.

Dataset: data/messy_employees.csv (included — synthetic messy data)

Real dataset ideas from Kaggle:
  - HR Analytics Employee Attrition: https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset
  - Indian Job Market:               https://www.kaggle.com/datasets/PromptCloudHQ/jobs-on-naukricom
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime

INPUT_FILE  = "data/messy_employees.csv"
OUTPUT_FILE = "data/clean_employees.csv"
LOG_FILE    = "cleaning_log.md"

log_entries = []   # accumulate all decisions


def log(issue, action, rows_affected, example=""):
    """Record every cleaning decision with context."""
    entry = {
        "issue": issue,
        "action": action,
        "rows_affected": rows_affected,
        "example": example,
    }
    log_entries.append(entry)
    affected = f"{rows_affected} row(s)" if isinstance(rows_affected, int) else rows_affected
    print(f"  [{affected}] {issue}")
    print(f"           → {action}")
    if example:
        print(f"           e.g. {example}")


def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


# ── Step 1: Load ──────────────────────────────────────────────

def load(filepath):
    df = pd.read_csv(filepath, dtype=str)   # load everything as string first
    print_section("RAW DATA SNAPSHOT")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  Columns: {list(df.columns)}")
    print(f"\n  Null counts:")
    for col in df.columns:
        n = df[col].isna().sum()
        if n > 0:
            print(f"    {col:<25} {n} nulls")
    return df.copy()


# ── Step 2: Fix Column Names ──────────────────────────────────

def fix_column_names(df):
    print_section("STEP 1: Column Names")
    original = list(df.columns)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    changed = [(o, n) for o, n in zip(original, df.columns) if o != n]
    if changed:
        log("Column names had spaces or uppercase",
            "Stripped whitespace and lowercased all column names",
            len(changed))
    else:
        print("  No column name issues found.")
    return df


# ── Step 3: Remove Duplicates ─────────────────────────────────

def remove_duplicates(df):
    print_section("STEP 2: Duplicates")
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        log("Exact duplicate rows found",
            f"Dropped {removed} duplicate rows (kept first occurrence)",
            removed,
            "E023 (Deepak Tiwari) and E001 (Arjun Sharma) were duplicated")
    else:
        print("  No duplicate rows found.")
    return df


# ── Step 4: Clean Name Column ─────────────────────────────────

def clean_names(df):
    print_section("STEP 3: Name Column")
    before = df["name"].copy()
    df["name"] = df["name"].str.strip().str.title()
    changed = (before != df["name"]).sum()
    if changed:
        log("Names had inconsistent casing or extra whitespace",
            "Stripped whitespace and applied Title Case to all names",
            int(changed),
            "'  Anita Desai  ' → 'Anita Desai' | 'RAHUL VERMA' → 'Rahul Verma'")
    return df


# ── Step 5: Clean Gender Column ───────────────────────────────

def clean_gender(df):
    print_section("STEP 4: Gender Column")
    mapping = {
        "male": "Male", "m": "Male",
        "female": "Female", "f": "Female",
    }
    before = df["gender"].copy()
    df["gender"] = df["gender"].str.strip().str.lower().map(mapping)
    nulls_after = df["gender"].isna().sum()
    changed = (before.str.strip().str.lower() != df["gender"].str.lower()).sum()
    log("Gender had inconsistent values: Male/M/male/FEMALE/F/female",
        "Standardised all to 'Male' or 'Female' using a mapping dictionary",
        int(changed),
        "'M' → 'Male' | 'FEMALE' → 'Female' | 'male' → 'Male'")
    if nulls_after:
        log("Unmapped gender values became NaN after standardisation",
            f"Left as NaN — {nulls_after} row(s) need manual review",
            int(nulls_after))
    return df


# ── Step 6: Clean Department Column ──────────────────────────

def clean_department(df):
    print_section("STEP 5: Department Column")
    before = df["department"].copy()
    df["department"] = df["department"].str.strip().str.title()
    changed = (before != df["department"]).sum()
    if changed:
        log("Department had inconsistent casing: engineering/HR/finance",
            "Applied Title Case to all department values",
            int(changed),
            "'engineering' → 'Engineering' | 'hr' → 'Hr'")
    # Fix "Hr" → "HR"
    df["department"] = df["department"].str.replace("^Hr$", "HR", regex=True)
    return df


# ── Step 7: Clean Salary Column ──────────────────────────────

def clean_salary(df):
    print_section("STEP 6: Salary Column")

    def parse_salary(val):
        if pd.isna(val):
            return np.nan
        val = str(val).strip()
        val = val.replace("₹", "").replace(",", "").replace(" ", "").upper()
        if val.endswith("INR"):
            val = val[:-3]
        if val.endswith("K"):
            try:
                return float(val[:-1]) * 1000
            except ValueError:
                return np.nan
        # Handle broken formatting like "1,10,000" → already stripped commas
        try:
            result = float(val)
            return result
        except ValueError:
            return np.nan

    df["salary"] = df["salary"].apply(parse_salary)

    # Flag impossible salaries
    negative = df["salary"] < 0
    too_low  = (df["salary"] > 0) & (df["salary"] < 10000)

    if negative.any():
        df.loc[negative, "salary"] = np.nan
        log("Negative salary values found",
            "Set to NaN — cannot be valid; needs manual correction",
            int(negative.sum()),
            "E013: salary was -5000")

    if too_low.any():
        df.loc[too_low, "salary"] = np.nan
        log("Salary values below ₹10,000 (likely input error)",
            "Set to NaN — e.g. '₹65,000' entered as '₹65' missing zeros",
            int(too_low.sum()),
            "E004: salary was ₹65 → likely ₹65,000")

    log("Salary had mixed formats: ₹85000 / 90000 INR / 75K / ₹1,10,000",
        "Stripped currency symbols, commas, and 'INR'. Converted 'K' suffix × 1000",
        "all rows",
        "'75K' → 75000 | '₹85,000' → 85000 | '90000 INR' → 90000")

    df["salary"] = df["salary"].astype(float)
    return df


# ── Step 8: Clean Age Column ──────────────────────────────────

def clean_age(df):
    print_section("STEP 7: Age Column")
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    impossible = (df["age"] < 18) | (df["age"] > 70)
    count = impossible.sum()
    if count:
        df.loc[impossible, "age"] = np.nan
        log("Impossible age values found (< 18 or > 70)",
            "Set to NaN — likely data entry errors",
            int(count),
            "E008: age=250 | E028: age=999 | E018: age=N/A")
    return df


# ── Step 9: Standardise Dates ─────────────────────────────────

def clean_dates(df):
    print_section("STEP 8: Joining Date Column")

    formats = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y",
               "%d %B %Y", "%d %b %Y"]

    def parse_date(val):
        if pd.isna(val):
            return pd.NaT
        val = str(val).strip()
        # Remove ordinal suffixes: 22nd → 22, 15th → 15, 25th → 25
        val = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", val)
        for fmt in formats:
            try:
                return datetime.strptime(val, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return pd.NaT

    df["joining_date"] = df["joining_date"].apply(parse_date)
    failed = df["joining_date"].isna().sum()
    log("Joining date had mixed formats: YYYY-MM-DD / DD/MM/YYYY / 22nd June 2020",
        "Parsed all formats and standardised to ISO format: YYYY-MM-DD",
        "all rows",
        "'22nd June 2020' → '2020-06-22' | '15/04/2019' → '2019-04-15'")
    if failed:
        log(f"{failed} date value(s) could not be parsed",
            "Set to NaN — needs manual correction",
            int(failed))
    return df


# ── Step 10: Fill Missing Values ──────────────────────────────

def handle_missing(df):
    print_section("STEP 9: Missing Values")

    # Performance rating — fill with median per department
    med = df.groupby("department")["performance_rating"].transform(
        lambda x: x.astype(float).median()
    )
    missing_perf = df["performance_rating"].isna().sum()
    df["performance_rating"] = df["performance_rating"].fillna(med)
    if missing_perf:
        log("performance_rating had missing values",
            "Filled with median rating of the same department",
            int(missing_perf),
            "E014 (Marketing) → filled with median Marketing rating")

    # Experience years — fill with 0 (new joinee assumption)
    df["experience_years"] = pd.to_numeric(df["experience_years"], errors="coerce")
    missing_exp2 = df["experience_years"].isna().sum()
    if missing_exp2:
        df["experience_years"] = df["experience_years"].fillna(0)
        log("experience_years had missing values",
            "Filled with 0 — likely new joinee with no prior experience",
            int(missing_exp2))

    # Age and salary — flag but leave as NaN (too risky to impute)
    remaining_nulls = df[["age", "salary"]].isna().sum()
    for col, count in remaining_nulls.items():
        if count:
            log(f"{col} has {count} values that could not be cleaned",
                "Left as NaN — imputing would introduce false precision. Flag for manual review.",
                int(count))

    return df


# ── Step 11: Fix Data Types ───────────────────────────────────

def fix_dtypes(df):
    print_section("STEP 10: Data Types")
    df["age"]               = pd.to_numeric(df["age"],               errors="coerce")
    df["salary"]            = pd.to_numeric(df["salary"],            errors="coerce")
    df["experience_years"]  = pd.to_numeric(df["experience_years"],  errors="coerce")
    df["performance_rating"]= pd.to_numeric(df["performance_rating"],errors="coerce")
    df["joining_date"]      = pd.to_datetime(df["joining_date"],     errors="coerce")
    log("All columns were loaded as strings (safe default)",
        "Cast age/salary/experience/rating to numeric; joining_date to datetime",
        "all rows")
    return df


# ── Step 12: Write Cleaning Log ───────────────────────────────

def write_log(df_before, df_after):
    lines = [
        "# Cleaning Log — Employee Dataset\n",
        f"**Input file:** `data/messy_employees.csv`  ",
        f"**Output file:** `data/clean_employees.csv`  ",
        f"**Date cleaned:** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Rows before:** {len(df_before)}  |  **Rows after:** {len(df_after)}\n",
        "---\n",
        "## Cleaning Decisions\n",
        "| # | Issue Found | Action Taken | Rows Affected | Example |\n",
        "|---|-------------|--------------|---------------|---------|\n",
    ]
    for i, e in enumerate(log_entries, 1):
        lines.append(
            f"| {i} | {e['issue']} | {e['action']} | {e['rows_affected']} | {e['example']} |\n"
        )

    lines += [
        "\n---\n",
        "## Final Data Quality Summary\n",
        f"| Column | Null Count | Data Type |\n",
        f"|--------|------------|----------|\n",
    ]
    for col in df_after.columns:
        nulls = df_after[col].isna().sum()
        dtype = str(df_after[col].dtype)
        lines.append(f"| `{col}` | {nulls} | {dtype} |\n")

    lines += [
        "\n---\n",
        "## Decisions That Need Human Review\n",
        "- Rows where `salary` is still NaN: verify with HR\n",
        "- Rows where `age` is still NaN: verify with employee records\n",
        "- `E004`: salary may have been ₹65,000 — set to NaN pending confirmation\n",
        "- `E013`: salary was -5000 — set to NaN pending confirmation\n",
    ]

    with open(LOG_FILE, "w") as f:
        f.writelines(lines)
    print(f"\n  Cleaning log saved to: {LOG_FILE}")


# ── Main ──────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Clean the Mess — Employee Dataset")
    print(f"  Input:  {INPUT_FILE}")
    print(f"  Output: {OUTPUT_FILE}")
    print("=" * 60)

    df_raw   = load(INPUT_FILE)
    df = df_raw.copy()
    df = fix_column_names(df)
    df = remove_duplicates(df)
    df = clean_names(df)
    df = clean_gender(df)
    df = clean_department(df)
    df = clean_salary(df)
    df = clean_age(df)
    df = clean_dates(df)
    df = handle_missing(df)
    df = fix_dtypes(df)

    df.to_csv(OUTPUT_FILE, index=False)
    write_log(df_raw, df)

    print_section("FINAL SUMMARY")
    print(f"  Rows before cleaning: {len(df_raw)}")
    print(f"  Rows after cleaning:  {len(df)}")
    print(f"  Duplicates removed:   {len(df_raw) - len(df)}")
    remaining_nulls = df.isna().sum().sum()
    print(f"  Remaining nulls:      {remaining_nulls} (see cleaning_log.md)")
    print(f"\n  Clean file saved:  {OUTPUT_FILE}")
    print(f"  Cleaning log:      {LOG_FILE}\n")


if __name__ == "__main__":
    main()
