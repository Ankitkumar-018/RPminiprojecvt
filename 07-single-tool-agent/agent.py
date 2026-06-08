"""
Single-Tool Agent — Calculator + Unit Converter
An LLM agent that uses a tool to perform calculations it cannot do reliably on its own.

The agent loop:
  1. User sends a question
  2. Claude decides if it needs the tool
  3. If yes: Claude calls the tool with arguments → tool runs → result fed back
  4. Claude generates final answer with the real computed result
  5. Repeat until Claude gives a final answer (no tool call)
"""

import os
import json
import math
import sys
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"


# ── Tool Definition ──────────────────────────────────────────
# This is what we tell Claude the tool can do (schema)

CALCULATOR_TOOL = {
    "name": "calculator",
    "description": (
        "Evaluate a mathematical expression and return the result. "
        "Supports: +, -, *, /, ** (power), sqrt(), log(), sin(), cos(), tan(), "
        "floor(), ceil(), round(), abs(), pi, e. "
        "Also converts units: e.g., 'km_to_miles:5', 'celsius_to_fahrenheit:100', "
        "'kg_to_pounds:70', 'usd_to_inr:100'."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": (
                    "A math expression like '2 ** 10', 'sqrt(144)', "
                    "or a unit conversion like 'celsius_to_fahrenheit:37'"
                )
            }
        },
        "required": ["expression"]
    }
}


# ── Tool Implementation ──────────────────────────────────────
# The actual Python function that runs when Claude calls the tool

UNIT_CONVERSIONS = {
    "km_to_miles":             lambda x: x * 0.621371,
    "miles_to_km":             lambda x: x * 1.60934,
    "celsius_to_fahrenheit":   lambda x: (x * 9/5) + 32,
    "fahrenheit_to_celsius":   lambda x: (x - 32) * 5/9,
    "kg_to_pounds":            lambda x: x * 2.20462,
    "pounds_to_kg":            lambda x: x / 2.20462,
    "meters_to_feet":          lambda x: x * 3.28084,
    "feet_to_meters":          lambda x: x / 3.28084,
    "usd_to_inr":              lambda x: x * 83.5,
    "inr_to_usd":              lambda x: x / 83.5,
    "liters_to_gallons":       lambda x: x * 0.264172,
    "gallons_to_liters":       lambda x: x / 0.264172,
}


def run_calculator(expression: str) -> str:
    expression = expression.strip()

    # Handle unit conversions (format: "conversion_name:value")
    if ":" in expression:
        parts = expression.split(":", 1)
        conversion_name = parts[0].strip().lower().replace(" ", "_")
        try:
            value = float(parts[1].strip())
        except ValueError:
            return f"Error: '{parts[1]}' is not a valid number"

        if conversion_name in UNIT_CONVERSIONS:
            result = UNIT_CONVERSIONS[conversion_name](value)
            return f"{result:.4f}"
        else:
            available = ", ".join(UNIT_CONVERSIONS.keys())
            return f"Error: Unknown conversion '{conversion_name}'. Available: {available}"

    # Handle math expressions
    safe_globals = {
        "__builtins__": {},
        "sqrt": math.sqrt,
        "log": math.log,
        "log2": math.log2,
        "log10": math.log10,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "floor": math.floor,
        "ceil": math.ceil,
        "round": round,
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
        "pow": pow,
    }
    try:
        result = eval(expression, safe_globals)  # noqa: S307
        if isinstance(result, float):
            return f"{result:.6f}".rstrip("0").rstrip(".")
        return str(result)
    except Exception as exc:
        return f"Error: {exc}"


# ── Agent Loop ───────────────────────────────────────────────

def run_agent(user_question: str, verbose: bool = True) -> str:
    messages = [{"role": "user", "content": user_question}]

    if verbose:
        print(f"\n{'─'*60}")
        print(f"User: {user_question}")

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=[CALCULATOR_TOOL],
            messages=messages,
        )

        # Check if Claude wants to use a tool
        if response.stop_reason == "tool_use":
            tool_uses = [b for b in response.content if b.type == "tool_use"]

            # Add Claude's response (with tool_use blocks) to message history
            messages.append({"role": "assistant", "content": response.content})

            # Run each tool and collect results
            tool_results = []
            for tool_use in tool_uses:
                expression = tool_use.input.get("expression", "")
                result = run_calculator(expression)

                if verbose:
                    print(f"\n  [Tool called]  calculator({expression!r})")
                    print(f"  [Tool result]  {result}")

                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": tool_use.id,
                    "content": result,
                })

            # Feed tool results back to Claude
            messages.append({"role": "user", "content": tool_results})

        else:
            # Claude gave a final answer (no more tool calls)
            final_answer = ""
            for block in response.content:
                if hasattr(block, "text"):
                    final_answer += block.text

            if verbose:
                print(f"\nAgent: {final_answer.strip()}")
                print(f"{'─'*60}\n")

            return final_answer.strip()


# ── Demo Mode ────────────────────────────────────────────────

DEMO_QUESTIONS = [
    "What is 2 to the power of 32?",
    "What is the square root of 1764?",
    "Convert 100 km to miles",
    "If I have 5000 USD, how much is that in Indian Rupees?",
    "What is sin(pi/6) + cos(pi/3)?",
    "I run 5km every day. How many miles is that per week?",
    "Convert 37 degrees Celsius (body temperature) to Fahrenheit",
    "What is log base 2 of 1024?",
    "If a rectangle has sides 12.5 and 8.3, what is its area and perimeter?",
]


def demo_mode():
    print("\n" + "="*60)
    print("  Single-Tool Agent — Demo Mode")
    print("  Tool: Calculator + Unit Converter")
    print("="*60)
    for q in DEMO_QUESTIONS:
        run_agent(q)


def interactive_mode():
    print("\n" + "="*60)
    print("  Single-Tool Agent — Interactive Mode")
    print("  I can calculate and convert units.")
    print("  Type 'quit' to exit.")
    print("="*60)
    while True:
        try:
            question = input("\nYou: ").strip()
            if not question:
                continue
            if question.lower() == "quit":
                print("Goodbye!")
                break
            run_agent(question)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"
    if mode == "demo":
        demo_mode()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
