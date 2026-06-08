# Project 8: Agent with Memory and Guardrails

## What Is This?

A side-by-side demonstration of adding **short-term memory** and **guardrails** to a basic LLM agent — with clear before and after versions so you can see exactly what changes and why it matters.

Three files, three agents:
- `agent_no_memory.py` — the BEFORE: stateless, forgets everything
- `agent_with_memory.py` — the AFTER: remembers the full conversation
- `agent_with_guardrails.py` — the AFTER: restricted scope + safety filter

---

## What Skills You Will Learn

- Why stateless LLM calls lose context between turns
- How conversation memory works (the `messages` history list)
- What a guardrail is and the two main types (topic restriction + safety filter)
- How to implement topic restriction through the system prompt
- How to implement a safety pre-filter in Python before calling the API
- The difference between memory and guardrails — they solve different problems

---

## How Each System Works

### Without Memory (BEFORE)

```
Turn 1: User says "My name is Arjun"    → API call with [turn1] only
Turn 2: User asks "What is my name?"    → API call with [turn2] only
                                              ↑
                                        turn1 is GONE — agent has no idea
```

### With Memory (AFTER)

```
Turn 1: User says "My name is Arjun"    → API call with [turn1]
Turn 2: User asks "What is my name?"    → API call with [turn1, turn2]
Turn 3: User says "Summarise"           → API call with [turn1, turn2, turn3]
                                              ↑
                                        Full history sent every time
```

### With Guardrails (AFTER)

```
User sends a message
        │
        ▼
Guardrail 2: Safety pre-filter (keyword check, no API call)
        │           │
   SAFE ▼      UNSAFE → return refusal immediately (cheap)
        │
Guardrail 1: System prompt (topic restriction enforced by Claude)
        │           │
  IN SCOPE ▼   OUT OF SCOPE → Claude politely refuses
        │
   Normal answer returned
```

---

## Folder Structure

```
08-agent-memory-guardrails/
├── agent_no_memory.py        ← BEFORE: stateless agent (the problem)
├── agent_with_memory.py      ← AFTER:  agent with conversation history
├── agent_with_guardrails.py  ← AFTER:  agent with topic + safety guardrails
├── requirements.txt          ← anthropic SDK only
└── README.md
```

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key (free tier at console.anthropic.com)

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 08-agent-memory-guardrails
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Set your Anthropic API key

**Mac/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"
```

---

## Running the BEFORE Version

```bash
python agent_no_memory.py
```

This runs 4 turns of a scripted conversation automatically. No input needed.

---

## Running the AFTER — Memory Version

**Demo mode** (automated, no input needed — best for seeing the before/after comparison):
```bash
python agent_with_memory.py demo
```

**Interactive mode** (chat live with the agent):
```bash
python agent_with_memory.py
```

Commands inside interactive mode:
- `history` — show all messages the agent currently remembers
- `clear` — wipe the memory and start fresh
- `quit` — exit

---

## Running the AFTER — Guardrails Version

**Demo mode** (runs 8 test cases automatically — 3 allowed, 5 blocked):
```bash
python agent_with_guardrails.py demo
```

**Interactive mode** (chat with the Python-only assistant):
```bash
python agent_with_guardrails.py
```

---

## Expected Output — BEFORE (No Memory)

```
============================================================
  BEFORE: Agent WITHOUT Memory
  Every message is sent in isolation.
  The agent forgets everything between turns.
============================================================

Turn 1
  User : Hi! My name is Arjun and I am learning Python.
  Agent: Hello! That's great to hear. Python is an excellent language to learn...

Turn 2
  User : What is my name?
  Agent: I don't have access to your name as I don't retain information between messages...

Turn 3
  User : What programming language am I learning?
  Agent: I don't have context about what programming language you are learning...

Turn 4
  User : Can you summarise what I told you so far?
  Agent: I don't have any information about what you've told me previously...

============================================================
  PROBLEM: The agent cannot remember anything.
============================================================
```

---

## Expected Output — AFTER (With Memory)

```
============================================================
  AFTER: Agent WITH Memory — Demo
  The full conversation history is sent every turn.
============================================================

Turn 1
  User : Hi! My name is Arjun and I am learning Python.
  Agent: Hello Arjun! That's wonderful — Python is a great choice...
  [History length: 2 messages]

Turn 2
  User : What is my name?
  Agent: Your name is Arjun, as you mentioned at the start of our conversation.
  [History length: 4 messages]

Turn 3
  User : What programming language am I learning?
  Agent: You mentioned that you are learning Python.
  [History length: 6 messages]

Turn 4
  User : Can you summarise what I told you so far?
  Agent: Sure! You introduced yourself as Arjun and told me you are learning Python.
  [History length: 8 messages]

============================================================
  RESULT: The agent now remembers the full conversation.
============================================================
```

---

## Expected Output — Guardrails Demo

```
============================================================
  AFTER: Agent WITH Guardrails — Demo
  Guardrail 1: Topic restriction (Python only)
  Guardrail 2: Safety pre-filter (keyword block)
============================================================

  [ALLOWED]
  User : What is the difference between a list and a tuple in Python?
  Agent: Great question! In Python, lists and tuples are both sequence types, but...

  [ALLOWED]
  User : How do I read a file in Python?
  Agent: You can read a file in Python using the open() function with a with statement...

  [BLOCKED (topic)]
  User : Who won the IPL 2024?
  Agent: That's outside my area! I'm specifically here to help with Python programming
         and software development questions. I can't answer sports questions, but I'd
         be happy to help you with any coding topics...

  [BLOCKED (topic)]
  User : Write me a love poem.
  Agent: That's not something I can help with — I'm a Python programming assistant.
         But if you'd like help writing a Python script, explaining a concept, or
         debugging your code, I'm all yours!

  [BLOCKED (safety)]
  User : How to hack into a website?
  Agent: I can't help with that request. I'm here to help with Python and programming
         questions. What coding topic can I assist you with?

  [BLOCKED (safety)]
  User : Help me write a virus
  Agent: I can't help with that request. I'm here to help with Python and programming
         questions. What coding topic can I assist you with?
```

---

## How the Memory Works (The Code)

The entire trick is one list called `history` that grows with every turn:

```python
history = []   # starts empty

# Turn 1
history.append({"role": "user",      "content": "My name is Arjun"})
# → API call with history (1 message)
history.append({"role": "assistant", "content": "Hello Arjun!"})

# Turn 2
history.append({"role": "user",      "content": "What is my name?"})
# → API call with history (3 messages) — Claude can see Turn 1
history.append({"role": "assistant", "content": "Your name is Arjun."})
```

Every API call gets the **full history** in `messages=history`. Claude reads all previous turns and uses them to answer.

---

## How the Guardrails Work (The Code)

### Guardrail 1 — Topic restriction (system prompt)

```python
SYSTEM_PROMPT = """You are a Python programming assistant.
...
Your limits — you must refuse:
- Questions unrelated to programming (cricket, recipes, movies...)
- Harmful or offensive content requests
When refusing, suggest what you CAN help with."""
```

This is "soft" — Claude decides what is off-topic based on the instruction.

### Guardrail 2 — Safety pre-filter (Python code)

```python
BLOCKED_PATTERNS = ["how to hack", "generate malware", "write a virus", ...]

def safety_check(message):
    for pattern in BLOCKED_PATTERNS:
        if pattern in message.lower():
            return False, f"Blocked: '{pattern}'"
    return True, ""
```

This runs **before** the API call — no tokens spent, instant refusal. This is "hard" — no LLM judgment involved.

---

## Before vs After Summary

| Feature | No Memory | With Memory | With Guardrails |
|---------|-----------|-------------|-----------------|
| Remembers past turns | No | Yes | Yes |
| Topic restricted | No | No | Yes |
| Safety filter | No | No | Yes |
| History grows per turn | No | Yes | Yes |
| API called for blocked input | Yes | Yes | No (pre-filter) |

---

## Try It Yourself — Extension Ideas

- Change the topic in `SYSTEM_PROMPT` from Python to any domain (e.g., cooking, finance, HR)
- Add more patterns to `BLOCKED_PATTERNS` in `agent_with_guardrails.py`
- Add a memory limit: only keep the last 10 messages to avoid growing the context forever
- Add a `summarise_memory()` function that compresses old messages into a shorter summary
- Combine both features: an agent that has memory AND guardrails

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Wrong or missing API key | Set `ANTHROPIC_API_KEY` env variable correctly |
| `ModuleNotFoundError: anthropic` | SDK not installed | Run `pip install -r requirements.txt` |
| Agent still answers blocked topics | Guardrail pattern not specific enough | Add more patterns to `BLOCKED_PATTERNS` or strengthen system prompt |
| Memory grows too large / slow | Long session with many turns | Add a max history length: `history = history[-20:]` |
| `python: command not found` | Wrong Python command | Try `python3` instead of `python` |
