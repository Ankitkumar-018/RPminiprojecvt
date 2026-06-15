# Cleaning Log — Employee Dataset
**Input file:** `data/messy_employees.csv`  **Output file:** `data/clean_employees.csv`  **Date cleaned:** 2026-06-15 11:36  **Rows before:** 31  |  **Rows after:** 30
---
## Cleaning Decisions
| # | Issue Found | Action Taken | Rows Affected | Example |
|---|-------------|--------------|---------------|---------|
| 1 | Exact duplicate rows found | Dropped 1 duplicate rows (kept first occurrence) | 1 | E023 (Deepak Tiwari) and E001 (Arjun Sharma) were duplicated |
| 2 | Names had inconsistent casing or extra whitespace | Stripped whitespace and applied Title Case to all names | 3 | '  Anita Desai  ' → 'Anita Desai' | 'RAHUL VERMA' → 'Rahul Verma' |
| 3 | Gender had inconsistent values: Male/M/male/FEMALE/F/female | Standardised all to 'Male' or 'Female' using a mapping dictionary | 4 | 'M' → 'Male' | 'FEMALE' → 'Female' | 'male' → 'Male' |
| 4 | Department had inconsistent casing: engineering/HR/finance | Applied Title Case to all department values | 12 | 'engineering' → 'Engineering' | 'hr' → 'Hr' |
| 5 | Negative salary values found | Set to NaN — cannot be valid; needs manual correction | 1 | E013: salary was -5000 |
| 6 | Salary had mixed formats: ₹85000 / 90000 INR / 75K / ₹1,10,000 | Stripped currency symbols, commas, and 'INR'. Converted 'K' suffix × 1000 | all rows | '75K' → 75000 | '₹85,000' → 85000 | '90000 INR' → 90000 |
| 7 | Impossible age values found (< 18 or > 70) | Set to NaN — likely data entry errors | 2 | E008: age=250 | E028: age=999 | E018: age=N/A |
| 8 | Joining date had mixed formats: YYYY-MM-DD / DD/MM/YYYY / 22nd June 2020 | Parsed all formats and standardised to ISO format: YYYY-MM-DD | all rows | '22nd June 2020' → '2020-06-22' | '15/04/2019' → '2019-04-15' |
| 9 | performance_rating had missing values | Filled with median rating of the same department | 1 | E014 (Marketing) → filled with median Marketing rating |
| 10 | experience_years had missing values | Filled with 0 — likely new joinee with no prior experience | 1 |  |
| 11 | age has 4 values that could not be cleaned | Left as NaN — imputing would introduce false precision. Flag for manual review. | 4 |  |
| 12 | salary has 1 values that could not be cleaned | Left as NaN — imputing would introduce false precision. Flag for manual review. | 1 |  |
| 13 | All columns were loaded as strings (safe default) | Cast age/salary/experience/rating to numeric; joining_date to datetime | all rows |  |

---
## Final Data Quality Summary
| Column | Null Count | Data Type |
|--------|------------|----------|
| `emp_id` | 0 | object |
| `name` | 0 | object |
| `age` | 4 | float64 |
| `gender` | 0 | object |
| `department` | 0 | object |
| `salary` | 1 | float64 |
| `joining_date` | 0 | datetime64[ns] |
| `city` | 0 | object |
| `experience_years` | 0 | float64 |
| `performance_rating` | 0 | float64 |

---
## Decisions That Need Human Review
- Rows where `salary` is still NaN: verify with HR
- Rows where `age` is still NaN: verify with employee records
- `E004`: salary may have been ₹65,000 — set to NaN pending confirmation
- `E013`: salary was -5000 — set to NaN pending confirmation
