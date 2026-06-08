"""
Structured-Output Workflow
Turns messy text (recipes or job postings) into validated JSON using Claude API.

Pipeline steps:
  1. Extract raw text from file
  2. Send to Claude with a strict JSON schema prompt
  3. Parse and validate the response
  4. Retry once if validation fails
  5. Save clean JSON output
"""

import os
import json
import re
import sys
import anthropic
from typing import Any

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"  # fast and cheap for structured extraction


# ── JSON Schemas (as plain dicts for prompt injection) ───────

RECIPE_SCHEMA = {
    "name": "string (recipe name)",
    "servings": "integer",
    "difficulty": "easy | medium | hard",
    "cook_time_minutes": "integer",
    "is_vegetarian": "boolean",
    "ingredients": [
        {"item": "string", "quantity": "string", "unit": "string or null"}
    ],
    "steps": ["string (each step as a sentence)"],
    "tags": ["string"]
}

JOB_SCHEMA = {
    "title": "string (job title)",
    "company": "string",
    "location": "string",
    "work_mode": "remote | hybrid | onsite",
    "employment_type": "full-time | contract | part-time",
    "experience_years_min": "integer or null",
    "experience_years_max": "integer or null",
    "salary_lpa_min": "number or null",
    "salary_lpa_max": "number or null",
    "required_skills": ["string"],
    "nice_to_have_skills": ["string"],
    "responsibilities": ["string"],
    "contact_email": "string or null"
}


def split_entries(text: str) -> list[str]:
    """Split a file with multiple entries separated by '--- ... ---' headers."""
    parts = re.split(r"---\s*.+?\s*---", text)
    return [p.strip() for p in parts if p.strip()]


def build_prompt(raw_text: str, schema: dict, entity_type: str) -> str:
    return f"""You are a data extraction assistant. Extract structured information from the {entity_type} text below.

Return ONLY valid JSON that matches this exact schema — no markdown, no explanation, just JSON:
{json.dumps(schema, indent=2)}

Rules:
- If a field cannot be determined from the text, use null
- For lists, return an empty list [] if nothing found
- difficulty must be exactly one of: easy, medium, hard
- work_mode must be exactly one of: remote, hybrid, onsite
- employment_type must be exactly one of: full-time, contract, part-time
- All numeric fields must be actual numbers (integers or floats), not strings

{entity_type.upper()} TEXT:
{raw_text}

JSON OUTPUT:"""


def call_claude(prompt: str) -> str:
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text.strip()


def extract_json(raw_response: str) -> Any:
    """Extract JSON even if Claude wraps it in markdown code fences."""
    # Remove ```json ... ``` fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_response, flags=re.MULTILINE)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
    return json.loads(cleaned.strip())


def validate(data: Any, schema_keys: list[str]) -> bool:
    """Basic validation: check all top-level keys from schema are present."""
    if not isinstance(data, dict):
        return False
    for key in schema_keys:
        if key not in data:
            print(f"  [Validation] Missing key: '{key}'")
            return False
    return True


def process_entry(raw_text: str, schema: dict, entity_type: str, index: int) -> dict | None:
    print(f"\n  Processing {entity_type} #{index + 1}...")
    prompt = build_prompt(raw_text, schema, entity_type)

    for attempt in range(1, 3):  # max 2 attempts
        try:
            raw = call_claude(prompt)
            data = extract_json(raw)
            schema_keys = list(schema.keys())
            if validate(data, schema_keys):
                print(f"  ✓ Parsed and validated on attempt {attempt}")
                return data
            else:
                print(f"  ✗ Validation failed on attempt {attempt}, retrying...")
        except json.JSONDecodeError as e:
            print(f"  ✗ JSON parse error on attempt {attempt}: {e}")
            if attempt == 2:
                print(f"  ✗ Giving up on this entry after 2 attempts")

    return None


def run_pipeline(input_file: str, entity_type: str):
    schema = RECIPE_SCHEMA if entity_type == "recipe" else JOB_SCHEMA

    print(f"\n{'='*60}")
    print(f"  Structured Output Pipeline")
    print(f"  File: {input_file}")
    print(f"  Type: {entity_type}")
    print(f"{'='*60}")

    with open(input_file, "r") as f:
        raw_text = f.read()

    entries = split_entries(raw_text)
    print(f"\nFound {len(entries)} entries to process.")

    results = []
    for i, entry in enumerate(entries):
        result = process_entry(entry, schema, entity_type, i)
        if result:
            results.append(result)

    output_file = f"output_{entity_type}s.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print(f"  Done! {len(results)}/{len(entries)} entries extracted successfully.")
    print(f"  Output saved to: {output_file}")
    print(f"{'='*60}\n")

    # Pretty print results
    print(json.dumps(results, indent=2))


def main():
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <recipe|job>")
        print("  python pipeline.py recipe   → parses sample_inputs/recipes.txt")
        print("  python pipeline.py job      → parses sample_inputs/job_postings.txt")
        sys.exit(1)

    entity_type = sys.argv[1].lower()
    if entity_type not in ("recipe", "job"):
        print("Error: type must be 'recipe' or 'job'")
        sys.exit(1)

    input_file = f"sample_inputs/{'recipes' if entity_type == 'recipe' else 'job_postings'}.txt"
    run_pipeline(input_file, entity_type)


if __name__ == "__main__":
    main()
