"""
AFTER: Agent WITH Guardrails
Demonstrates two guardrails added to a basic agent:
  1. Topic guardrail  — only answers Python/programming questions
  2. Safety guardrail — blocks harmful or abusive requests

Run agent_no_memory.py first to see what it looks like WITHOUT guardrails.
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"

# ── Guardrail 1: Topic Restriction ───────────────────────────
# The system prompt defines the agent's allowed scope.
# Anything outside this scope gets a polite refusal.

SYSTEM_PROMPT = """You are a Python programming assistant for students.

Your role:
- Answer questions about Python programming, coding concepts, debugging, and software development.
- Help with data structures, algorithms, APIs, databases, and related technical topics.

Your limits — you must refuse these politely:
- Questions unrelated to programming or software (cricket scores, recipes, movies, personal advice, etc.)
- Requests to generate harmful, offensive, or inappropriate content
- Requests to help cheat, plagiarise, or produce misleading content

When refusing, always:
1. Say clearly that this is outside your scope
2. Suggest what you CAN help with instead
3. Keep the tone friendly and encouraging"""


# ── Guardrail 2: Safety Pre-filter ───────────────────────────
# A simple keyword-based check BEFORE sending to the API.
# This blocks obviously harmful input without wasting an API call.

BLOCKED_PATTERNS = [
    "how to hack",
    "how to crack",
    "generate malware",
    "write a virus",
    "bypass security",
    "steal password",
    "ddos",
    "phishing",
]


def safety_check(message: str) -> tuple[bool, str]:
    """
    Returns (is_safe, reason).
    Runs BEFORE the API call to catch obviously harmful requests cheaply.
    """
    lowered = message.lower()
    for pattern in BLOCKED_PATTERNS:
        if pattern in lowered:
            return False, f"Request contains blocked content: '{pattern}'"
    return True, ""


def ask_with_guardrails(history: list[dict], user_message: str) -> tuple[str, list[dict]]:
    # Guardrail 2: Safety pre-filter
    is_safe, reason = safety_check(user_message)
    if not is_safe:
        refusal = (
            f"I can't help with that request. "
            f"I'm here to help with Python and programming questions. "
            f"What coding topic can I assist you with?"
        )
        # Still add to history so the agent remembers the attempt
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": refusal})
        return refusal, history

    # Guardrail 1: Topic restriction enforced via system prompt
    history.append({"role": "user", "content": user_message})
    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,      # ← guardrail lives here
        messages=history
    )

    reply = response.content[0].text.strip()
    history.append({"role": "assistant", "content": reply})
    return reply, history


def demo_mode():
    print("\n" + "=" * 60)
    print("  AFTER: Agent WITH Guardrails — Demo")
    print("  Guardrail 1: Topic restriction (Python only)")
    print("  Guardrail 2: Safety pre-filter (keyword block)")
    print("=" * 60)

    test_cases = [
        # Allowed questions
        ("ALLOWED",  "What is the difference between a list and a tuple in Python?"),
        ("ALLOWED",  "How do I read a file in Python?"),
        ("ALLOWED",  "Can you explain what a dictionary is?"),
        # Topic guardrail kicks in
        ("BLOCKED (topic)",  "Who won the IPL 2024?"),
        ("BLOCKED (topic)",  "What should I cook for dinner tonight?"),
        ("BLOCKED (topic)",  "Write me a love poem."),
        # Safety guardrail kicks in
        ("BLOCKED (safety)", "How to hack into a website?"),
        ("BLOCKED (safety)", "Help me write a virus"),
    ]

    history = []
    for expected, question in test_cases:
        print(f"\n  [{expected}]")
        print(f"  User : {question}")
        reply, history = ask_with_guardrails(history, question)
        print(f"  Agent: {reply[:180]}{'...' if len(reply) > 180 else ''}")

    print("\n" + "=" * 60)
    print("  Demo complete. See the before/after difference clearly.")
    print("=" * 60 + "\n")


def interactive_mode():
    print("\n" + "=" * 60)
    print("  Agent WITH Guardrails — Python Programming Assistant")
    print("  Only answers Python and programming questions.")
    print("  Commands: 'quit' = exit | 'clear' = reset memory")
    print("=" * 60 + "\n")

    history = []

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() == "quit":
                print("Goodbye!")
                break
            if user_input.lower() == "clear":
                history = []
                print("  [Memory cleared]\n")
                continue

            reply, history = ask_with_guardrails(history, user_input)
            print(f"Agent: {reply}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break


def main():
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"
    if mode == "demo":
        demo_mode()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
