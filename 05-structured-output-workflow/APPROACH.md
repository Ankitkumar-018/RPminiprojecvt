# Project 5: Structured Output Workflow — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a developer thinks through an LLM pipeline.

---

### Step 1 — Understand the Problem

**What exactly does this project need?**
- Take messy, unstructured text (a casual recipe or job posting)
- Send it to an LLM with clear instructions
- Get back clean, structured JSON
- Validate that the JSON matches the expected schema
- Retry if the output is wrong

**Why is this hard without an LLM?**
- Traditional code (regex, string splitting) can parse structured formats
- But natural language is unpredictable — "serves 4" / "for 4 people" / "4 servings" all mean the same thing
- An LLM understands natural language and can normalise all these variations

---

### Step 2 — Questions to Ask Before Writing Code

- **What schema should the output follow?**
  → Define it as a Python dict first, then inject it into the prompt as JSON

- **How do I make Claude return only JSON and not explanation text?**
  → Say explicitly in the prompt: "Return ONLY valid JSON. No markdown, no explanation."

- **What if Claude wraps the output in code fences (```json ... ```)?**
  → Strip them with regex before parsing — this is common LLM behaviour

- **What if the JSON is valid but missing a required field?**
  → Validate all top-level keys after parsing. If any are missing, retry.

- **How many retries?**
  → 2 attempts is usually enough. After that, log the failure and move on.

- **How do I split a file with multiple recipes/jobs?**
  → Use a consistent separator in the file (`--- RECIPE 1 ---`) and split on it with regex.

---

### Step 3 — Pseudo Code

```
START

  DEFINE schema as a Python dict (the structure we want Claude to return)

  FUNCTION split_entries(text):
    use regex to split on "--- ... ---" separators
    return list of individual text blocks

  FUNCTION build_prompt(raw_text, schema, entity_type):
    return a string that says:
      "Extract structured data from this [entity_type].
       Return ONLY JSON matching this schema: [schema as JSON string]
       Text: [raw_text]"

  FUNCTION call_claude(prompt):
    send prompt to Claude API
    return response text

  FUNCTION extract_json(raw_response):
    strip markdown code fences if present (```json ... ```)
    parse and return JSON object

  FUNCTION validate(data, required_keys):
    FOR each key in required_keys:
      IF key not in data: return False
    return True

  FUNCTION process_entry(raw_text, schema, entity_type, index):
    FOR attempt in [1, 2]:
      prompt = build_prompt(raw_text, schema, entity_type)
      raw = call_claude(prompt)
      TRY:
        data = extract_json(raw)
        IF validate(data, schema.keys()):
          RETURN data
        ELSE:
          print "validation failed, retrying..."
      EXCEPT json.JSONDecodeError:
        print "JSON parse error, retrying..."
    RETURN None   ← give up after 2 attempts

  READ input file
  entries = split_entries(file text)

  results = []
  FOR each entry in entries:
    result = process_entry(entry, schema, entity_type, index)
    IF result is not None:
      append result to results

  SAVE results as JSON file
  PRINT results

END
```

---

### Step 4 — Think About the Prompt Design

The prompt is the most important part of this project. Think carefully:

```
BAD PROMPT:
"Extract the recipe information."
→ Claude will return whatever format it wants

GOOD PROMPT:
"Extract structured information from the recipe text below.
Return ONLY valid JSON matching this exact schema:
{
  "name": "string",
  "servings": "integer",
  ...
}
Rules:
- If a field is unknown, use null
- difficulty must be exactly: easy, medium, or hard
- Return only JSON, no explanation, no markdown

TEXT:
[paste the raw recipe here]"
→ Claude returns clean JSON every time
```

Being explicit about:
1. The exact output format (JSON only)
2. Allowed values for enum fields
3. What to do when data is missing (null)

...makes the output much more reliable.

---

### Step 5 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| Claude adds markdown fences | Strip with `re.sub(r"```json\s*", "", text)` |
| Claude returns prose explanation | Retry with stricter prompt: "Return ONLY JSON" |
| JSON parses but field is wrong type | Pydantic validation (extension idea) |
| API rate limit hit | Add `time.sleep(1)` between calls |
| `ANTHROPIC_API_KEY` not set | Check env var at start and fail early with a clear message |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start coding.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — What type of text will you parse?

```
I will parse: (recipe / job posting / other: _________)

Example of the messy input text I will work with:


```

---

### Step 2 — Design Your Schema

What fields do you want to extract? Fill in the table:

```
Field name        | Data type         | Required? | Notes
------------------|-------------------|-----------|-------
                  |                   |           |
                  |                   |           |
                  |                   |           |
                  |                   |           |
                  |                   |           |
```

---

### Step 3 — Write Your Prompt (Draft)

Write the prompt you will send to Claude:

```
Write your prompt here:




```

**What explicit rules did you add to prevent bad output?**

```
Rule 1:
Rule 2:
Rule 3:
```

---

### Step 4 — Your Pseudo Code

```
Write the pipeline steps in plain English:

Step 1:
Step 2:
Step 3:
Step 4:
Step 5:
Step 6:
```

---

### Step 5 — Questions You Had Before Starting

```
1.
2.
3.
```

---

### Step 6 — After finishing, reflect

**What did you have to add to the prompt to make the output reliable?**
```

```

**Did the retry logic ever trigger? What caused the failure?**
```

```

**What is the difference between prompt engineering and traditional programming?**
```

```
