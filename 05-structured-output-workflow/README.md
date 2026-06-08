# Project 5: Structured-Output Workflow

## What Is This?

A multi-step LLM pipeline that takes **messy, unstructured text** (like a handwritten recipe or a casual job posting) and converts it into **clean, validated JSON**.

The output is guaranteed to match a schema — if Claude's response is malformed, the pipeline retries automatically.

---

## What Skills You Will Learn

- Prompting LLMs to return structured output
- Designing JSON schemas and injecting them into prompts
- Parsing and validating LLM responses
- Retry logic for unreliable outputs
- Building multi-step pipelines with the Claude API

---

## How the Pipeline Works

```
Raw text file
     │
     ▼
Split into individual entries (by --- separator)
     │
     ▼
For each entry:
  ┌─────────────────────────────┐
  │  Build prompt with schema   │
  │  Call Claude API            │
  │  Extract JSON from response │
  │  Validate required fields   │
  │  Retry once if invalid      │
  └─────────────────────────────┘
     │
     ▼
Save all results to output_recipes.json / output_jobs.json
     │
     ▼
Pretty-print results in terminal
```

---

## Folder Structure

```
05-structured-output-workflow/
├── pipeline.py                    ← Main pipeline (all logic here)
├── requirements.txt               ← anthropic SDK
├── sample_inputs/
│   ├── recipes.txt                ← 3 messy recipe descriptions
│   └── job_postings.txt           ← 3 messy job postings
└── README.md
```

After running, these files are created:
```
├── output_recipes.json            ← Clean structured recipe data
└── output_jobs.json               ← Clean structured job data
```

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key (free tier available at console.anthropic.com)

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 05-structured-output-workflow
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set your Anthropic API key

**On Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**On Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

> **How to get an API key:**
> 1. Go to https://console.anthropic.com
> 2. Sign up / Log in
> 3. Click "API Keys" in the sidebar
> 4. Create a new key and copy it

### Step 4 — Run the recipe pipeline

```bash
python pipeline.py recipe
```

### Step 5 — Run the job postings pipeline

```bash
python pipeline.py job
```

---

## Expected Output — Recipe Pipeline

Terminal output:
```
============================================================
  Structured Output Pipeline
  File: sample_inputs/recipes.txt
  Type: recipe
============================================================

Found 3 entries to process.

  Processing recipe #1...
  ✓ Parsed and validated on attempt 1

  Processing recipe #2...
  ✓ Parsed and validated on attempt 1

  Processing recipe #3...
  ✓ Parsed and validated on attempt 1

============================================================
  Done! 3/3 entries extracted successfully.
  Output saved to: output_recipes.json
============================================================
```

`output_recipes.json` contents:
```json
[
  {
    "name": "Grandma's Chicken Biryani",
    "servings": 4,
    "difficulty": "medium",
    "cook_time_minutes": 45,
    "is_vegetarian": false,
    "ingredients": [
      { "item": "basmati rice", "quantity": "500", "unit": "g" },
      { "item": "chicken", "quantity": "750", "unit": "g" },
      { "item": "onions", "quantity": "2", "unit": null },
      { "item": "yogurt", "quantity": "1", "unit": "cup" },
      { "item": "garlic cloves", "quantity": "4", "unit": null },
      { "item": "biryani masala", "quantity": "2", "unit": "tbsp" }
    ],
    "steps": [
      "Wash and soak rice for 30 minutes.",
      "Marinate chicken in yogurt and spices for 1 hour.",
      "Fry onions golden brown in ghee.",
      "Layer rice and chicken in a heavy pot.",
      "Seal with dough and cook on dum for 25 minutes on low flame.",
      "Serve hot."
    ],
    "tags": ["Indian", "non-vegetarian", "rice", "main course"]
  },
  ...
]
```

---

## Expected Output — Job Postings Pipeline

`output_jobs.json` contents:
```json
[
  {
    "title": "Backend Engineer",
    "company": "TechCorp",
    "location": "Bangalore",
    "work_mode": "hybrid",
    "employment_type": "full-time",
    "experience_years_min": 3,
    "experience_years_max": 5,
    "salary_lpa_min": 18,
    "salary_lpa_max": 25,
    "required_skills": ["Python", "REST APIs", "PostgreSQL", "Docker"],
    "nice_to_have_skills": ["Node.js", "MySQL", "AWS", "GCP"],
    "responsibilities": [
      "Design and build backend microservices",
      "Write clean code with tests",
      "Deploy on cloud infrastructure",
      "Conduct code reviews"
    ],
    "contact_email": "careers@techcorp.in"
  },
  ...
]
```

---

## What the Schema Enforces

### Recipe Schema

| Field | Type | Constraint |
|-------|------|-----------|
| `name` | string | Required |
| `servings` | integer | Required |
| `difficulty` | string | Must be: `easy`, `medium`, or `hard` |
| `cook_time_minutes` | integer | Required |
| `is_vegetarian` | boolean | Required |
| `ingredients` | list of objects | Each has `item`, `quantity`, `unit` |
| `steps` | list of strings | Each step is one sentence |
| `tags` | list of strings | Auto-inferred by Claude |

### Job Schema

| Field | Type | Constraint |
|-------|------|-----------|
| `title` | string | Required |
| `company` | string | Required |
| `location` | string | Required |
| `work_mode` | string | Must be: `remote`, `hybrid`, or `onsite` |
| `employment_type` | string | Must be: `full-time`, `contract`, or `part-time` |
| `experience_years_min/max` | integer or null | |
| `salary_lpa_min/max` | number or null | |
| `required_skills` | list | |
| `nice_to_have_skills` | list | |
| `responsibilities` | list | |
| `contact_email` | string or null | |

---

## Where the Retry Logic Kicks In

If Claude returns invalid JSON or a response missing required fields:
1. The pipeline logs which field failed
2. Sends the same prompt again (max 2 attempts)
3. If both fail, that entry is skipped with an error message

You can test this by intentionally breaking a prompt to see the retry.

---

## Try It Yourself — Extension Ideas

- Add your own text (copy-paste a recipe from a blog)
- Add a new entity type: e.g., `product` or `event`
- Add Pydantic for stricter type validation
- Build a simple web UI where users paste text and get JSON back
- Try with a different Claude model and compare output quality

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Missing or wrong API key | Set `ANTHROPIC_API_KEY` env variable |
| `RateLimitError` | Too many requests | Wait a few seconds and retry |
| `json.JSONDecodeError` | Claude returned non-JSON | Pipeline retries automatically; check prompt if it keeps failing |
| `ModuleNotFoundError: anthropic` | SDK not installed | Run `pip install -r requirements.txt` |
| `KeyError: ANTHROPIC_API_KEY` | Env var not set | Follow Step 3 in setup above |
