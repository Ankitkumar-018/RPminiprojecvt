# Project 7: Single-Tool Agent

## What Is This?

An LLM **agent** that uses one external tool — a calculator and unit converter — to complete tasks it cannot reliably do on its own.

LLMs are notoriously bad at precise arithmetic. This agent solves that by letting Claude *decide* when to call the calculator tool, run it, get the real result, and then respond with confidence.

---

## What Skills You Will Learn

- What an "agent" is vs. a simple chatbot (agents take actions)
- How tool use / function calling works with the Claude API
- The **agent loop**: prompt → tool call → result → response
- How to define tools as JSON schemas
- How to safely evaluate math expressions in Python
- Understanding `stop_reason = "tool_use"` vs `"end_turn"`

---

## How the Agent Loop Works

```
User: "What is 2 to the power of 32?"
          │
          ▼
    Claude thinks: "I need the calculator for this"
          │
          ▼
    Claude calls:  calculator("2 ** 32")
          │
          ▼
    Tool runs:     Python eval → 4294967296
          │
          ▼
    Result fed back to Claude
          │
          ▼
    Claude responds: "2 to the power of 32 is 4,294,967,296."
```

Without the tool, Claude might say 4,294,967,296 — or it might say 4,294,967,294 — you can't be sure. With the tool, the answer is always exact.

---

## What the Tool Can Do

### Math Expressions
Any valid Python math expression:

| Expression | Result |
|------------|--------|
| `2 ** 32` | 4294967296 |
| `sqrt(1764)` | 42 |
| `sin(pi/6)` | 0.5 |
| `log2(1024)` | 10.0 |
| `floor(3.7)` | 3 |
| `abs(-99)` | 99 |

### Unit Conversions
Format: `conversion_name:value`

| Conversion | Example |
|------------|---------|
| `km_to_miles:5` | 3.1069 |
| `celsius_to_fahrenheit:100` | 212.0 |
| `usd_to_inr:100` | 8350.0 |
| `kg_to_pounds:70` | 154.3234 |
| `meters_to_feet:1` | 3.2808 |
| `liters_to_gallons:10` | 2.6417 |

---

## Folder Structure

```
07-single-tool-agent/
├── agent.py          ← Agent loop + tool definition + tool implementation
├── requirements.txt  ← anthropic SDK only
└── README.md
```

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 07-single-tool-agent
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set your API key

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Windows:**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

### Step 4 — Run in interactive mode (chat with the agent)

```bash
python agent.py
```

### Step 5 — Run in demo mode (see 9 preset examples automatically)

```bash
python agent.py demo
```

---

## Expected Output — Demo Mode

```
============================================================
  Single-Tool Agent — Demo Mode
  Tool: Calculator + Unit Converter
============================================================

────────────────────────────────────────────────────────────
User: What is 2 to the power of 32?

  [Tool called]  calculator('2 ** 32')
  [Tool result]  4294967296

Agent: 2 to the power of 32 is 4,294,967,296.
────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────
User: Convert 100 km to miles

  [Tool called]  calculator('km_to_miles:100')
  [Tool result]  62.1371

Agent: 100 kilometres is equal to approximately 62.14 miles.
────────────────────────────────────────────────────────────

────────────────────────────────────────────────────────────
User: I run 5km every day. How many miles is that per week?

  [Tool called]  calculator('5 * 7')
  [Tool result]  35

  [Tool called]  calculator('km_to_miles:35')
  [Tool result]  21.7480

Agent: Running 5 km every day means you run 35 km per week,
which is approximately 21.75 miles per week.
────────────────────────────────────────────────────────────
```

Notice in the last example: Claude called the tool **twice** in sequence — first to calculate the weekly total, then to convert. This is the agent autonomously planning multiple steps.

---

## How Tool Use Works (The Code)

### 1. Define the tool as a schema

```python
CALCULATOR_TOOL = {
    "name": "calculator",
    "description": "Evaluate a math expression...",
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "..."}
        },
        "required": ["expression"]
    }
}
```

### 2. Pass the tool to Claude

```python
response = client.messages.create(
    model=MODEL,
    tools=[CALCULATOR_TOOL],   ← tell Claude this tool exists
    messages=messages,
)
```

### 3. Check if Claude wants to use the tool

```python
if response.stop_reason == "tool_use":
    # Claude made a tool call
else:
    # Claude gave a final answer
```

### 4. Run the tool and feed results back

```python
tool_results.append({
    "type": "tool_result",
    "tool_use_id": tool_use.id,
    "content": result,        ← the actual computed value
})
messages.append({"role": "user", "content": tool_results})
```

### 5. Loop — Claude now generates the final response

---

## Try It Yourself — Extension Ideas

- Add a `web_search` tool (use the `requests` library with a free search API)
- Add a `weather` tool using the Open-Meteo API (free, no API key needed)
- Add a `python_runner` tool that executes arbitrary code snippets
- Change the model to `claude-opus-4-8` and compare how the agent reasons

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Missing API key | Set `ANTHROPIC_API_KEY` |
| `Agent loops forever` | Tool always returns an error | Fix the expression format |
| `eval` security concern | `eval()` runs arbitrary code | The `safe_globals` dict blocks all builtins — only math functions are allowed |
| `Unknown conversion` | Typo in unit name | Check the `UNIT_CONVERSIONS` dict in `agent.py` for valid names |
