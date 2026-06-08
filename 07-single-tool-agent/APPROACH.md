# Project 7: Single-Tool Agent — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a developer thinks through building an agent.

---

### Step 1 — Understand the Problem

**What exactly does this project need?**
- An LLM agent that uses one external tool (calculator + unit converter)
- Claude decides when to call the tool, calls it, gets the result, and uses it in the answer
- The tool does something Claude cannot reliably do on its own (precise arithmetic)

**What is an "agent" vs a regular chatbot?**
- Regular chatbot: User asks → Claude thinks → Claude answers (one step)
- Agent: User asks → Claude thinks → Claude calls a tool → tool runs → Claude uses result → Claude answers (multiple steps)

**Why does Claude need a calculator?**
LLMs are trained on text, not arithmetic circuits. Claude can reason about math but often makes arithmetic errors on exact calculations. A calculator is always correct. Combining both gives you the best of both worlds.

---

### Step 2 — Questions to Ask Before Writing Code

- **How does Claude "call" a Python function?**
  → Claude doesn't run Python. Instead, Claude returns a special response saying "I want to call tool X with argument Y". Your Python code reads that response, runs the actual function, and sends the result back.

- **How does my code know Claude wants to use a tool?**
  → Check `response.stop_reason == "tool_use"`. If it's `"end_turn"`, Claude is done.

- **What happens after the tool runs?**
  → Send the tool result back in a new message with role "user" and type "tool_result". Claude then reads it and generates the final answer.

- **What if the tool fails or returns an error?**
  → Return the error as the tool result — Claude will read it and handle it gracefully (e.g., "I tried to calculate that but got an error: division by zero").

- **Can Claude call the tool multiple times in one answer?**
  → Yes. The loop continues until `stop_reason == "end_turn"`. Claude may call the tool once, twice, or not at all depending on the question.

- **How do I safely run `eval()` for math?**
  → Pass a restricted `safe_globals` dict that only contains math functions. Never pass `__builtins__` — that would allow `__import__('os').system('rm -rf /')`.

---

### Step 3 — Pseudo Code (The Agent Loop)

```
START

  DEFINE tool schema (JSON schema telling Claude what the tool does and its input format)
  DEFINE run_calculator(expression) function in Python

  FUNCTION run_agent(question):

    messages = [{"role": "user", "content": question}]

    LOOP forever:

      response = call Claude API with:
        messages = messages
        tools = [calculator_tool_schema]

      IF response.stop_reason == "tool_use":

        add Claude's response to messages (it contains the tool_use request)

        FOR each tool_use block in response:
          expression = tool_use.input["expression"]
          result = run_calculator(expression)   ← actual Python runs here

          tool_result = {
            "type": "tool_result",
            "tool_use_id": tool_use.id,
            "content": result
          }

        add tool_result to messages as a new user message

        CONTINUE loop (go back to calling Claude)

      ELSE (stop_reason == "end_turn"):
        final_answer = extract text from response
        PRINT final_answer
        RETURN

END
```

---

### Step 4 — Visualise the Message Flow

For question "What is 2 to the power of 32?":

```
messages = [
  {role: "user", content: "What is 2 to the power of 32?"}
]
                    ↓ API call 1
Claude responds:
  stop_reason = "tool_use"
  content = [ToolUseBlock(name="calculator", input={"expression": "2 ** 32"})]

messages = [
  {role: "user",      content: "What is 2 to the power of 32?"},
  {role: "assistant", content: [ToolUseBlock(...)]},            ← add Claude's response
  {role: "user",      content: [{type: "tool_result",           ← add tool result
                                  tool_use_id: "...",
                                  content: "4294967296"}]}
]
                    ↓ API call 2
Claude responds:
  stop_reason = "end_turn"
  content = "2 to the power of 32 is 4,294,967,296."

DONE ✓
```

---

### Step 5 — Design the Tool Schema

Before coding, design what you want to tell Claude about the tool:

```
Name: calculator
Description: (what it can do — be specific so Claude uses it correctly)
  "Evaluate a math expression. Supports: +, -, *, /, **, sqrt(), log(), sin(), cos(),
   pi, e, floor(), ceil(), round(), abs().
   Also converts units: format 'conversion_name:value' e.g. 'km_to_miles:5'"

Input:
  expression (string, required) — the math expression or unit conversion to evaluate
```

---

### Step 6 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| Infinite loop | Claude keeps calling the tool — add a max_iterations counter |
| `eval` security risk | Use `safe_globals` dict — never pass raw `__builtins__` |
| Tool returns error | Return the error string — Claude handles it gracefully |
| Claude doesn't use the tool | Question may not need calculation — that's correct behaviour |
| Unit conversion unknown | Check against your conversion dict and return a helpful error |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start coding.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — What tool will your agent use?

```
Tool name:
What does it do:
Why can't Claude do this reliably on its own?:
```

---

### Step 2 — Design Your Tool Schema

```
Name:
Description:
Input parameter name:
Input parameter type:
Input parameter description:
```

---

### Step 3 — Your Pseudo Code for the Agent Loop

```
Write the loop in plain English steps:

Step 1:
Step 2:
Step 3:
Step 4:
Step 5:
```

---

### Step 4 — Draw the Message Flow

For the question "Convert 100 km to miles", draw what happens to the `messages` list:

```
messages = [
  Turn 1: ...
  Turn 2: ...
  Turn 3: ...
]
```

---

### Step 5 — What is stop_reason?

**When is `stop_reason == "tool_use"` and when is it `"end_turn"`?**

```
tool_use means:

end_turn means:
```

---

### Step 6 — Questions You Had Before Starting

```
1.
2.
3.
```

---

### Step 7 — After finishing, reflect

**Find a question where Claude calls the tool twice. What was the question?**
```

```

**Find a question where Claude does NOT call the tool. Why didn't it need to?**
```

```

**What is the difference between an agent and a chatbot?**
```

```
