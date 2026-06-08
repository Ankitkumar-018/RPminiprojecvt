"""
BEFORE: Agent WITHOUT Memory
Each message is sent independently — the agent has no memory of previous turns.
Run this first to see the problem, then compare with agent_with_memory.py
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"


def ask(question: str) -> str:
    """Single-turn call — no history passed, no context retained."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system="You are a helpful assistant.",
        messages=[
            {"role": "user", "content": question}
        ]
    )
    return response.content[0].text.strip()


def main():
    print("\n" + "=" * 60)
    print("  BEFORE: Agent WITHOUT Memory")
    print("  Every message is sent in isolation.")
    print("  The agent forgets everything between turns.")
    print("=" * 60)

    demo_conversation = [
        "Hi! My name is Arjun and I am learning Python.",
        "What is my name?",
        "What programming language am I learning?",
        "Can you summarise what I told you so far?",
    ]

    for i, question in enumerate(demo_conversation, 1):
        print(f"\nTurn {i}")
        print(f"  User : {question}")
        answer = ask(question)
        print(f"  Agent: {answer}")

    print("\n" + "=" * 60)
    print("  PROBLEM: The agent cannot remember anything.")
    print("  It does not know your name or what you told it.")
    print("  See agent_with_memory.py for the fix.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
