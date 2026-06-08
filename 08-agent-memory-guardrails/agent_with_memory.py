"""
AFTER: Agent WITH Short-Term Memory
The full conversation history is passed with every API call.
The agent remembers everything said earlier in the session.
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = "You are a helpful assistant. Use the conversation history to give contextual answers."


def chat(history: list[dict], user_message: str) -> tuple[str, list[dict]]:
    """
    Send a message and get a reply. Returns the reply and the updated history.
    history is the full list of prior messages — this is what gives the agent memory.
    """
    history.append({"role": "user", "content": user_message})

    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        system=SYSTEM_PROMPT,
        messages=history          # ← entire history sent every time
    )

    reply = response.content[0].text.strip()
    history.append({"role": "assistant", "content": reply})

    return reply, history


def demo_mode():
    print("\n" + "=" * 60)
    print("  AFTER: Agent WITH Memory — Demo")
    print("  The full conversation history is sent every turn.")
    print("=" * 60)

    history = []
    demo_conversation = [
        "Hi! My name is Arjun and I am learning Python.",
        "What is my name?",
        "What programming language am I learning?",
        "Can you summarise what I told you so far?",
    ]

    for i, question in enumerate(demo_conversation, 1):
        print(f"\nTurn {i}")
        print(f"  User : {question}")
        reply, history = chat(history, question)
        print(f"  Agent: {reply}")
        print(f"  [History length: {len(history)} messages]")

    print("\n" + "=" * 60)
    print("  RESULT: The agent now remembers the full conversation.")
    print("=" * 60 + "\n")


def interactive_mode():
    print("\n" + "=" * 60)
    print("  Agent WITH Memory — Interactive Chat")
    print("  The agent remembers everything you say this session.")
    print("  Commands: 'history' = show memory | 'clear' = reset | 'quit' = exit")
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
                print("  [Memory cleared — starting fresh]\n")
                continue

            if user_input.lower() == "history":
                if not history:
                    print("  [No conversation history yet]\n")
                else:
                    print(f"\n  [Memory — {len(history)} messages stored]")
                    for msg in history:
                        role = "You  " if msg["role"] == "user" else "Agent"
                        print(f"    {role}: {msg['content'][:80]}{'...' if len(msg['content']) > 80 else ''}")
                    print()
                continue

            reply, history = chat(history, user_input)
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
