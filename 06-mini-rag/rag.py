"""
Mini-RAG (Retrieval-Augmented Generation)
Q&A bot over a small set of documents — no frameworks, built from scratch.

How it works:
  1. Load documents from the docs/ folder
  2. Split each document into overlapping chunks
  3. Build a TF-IDF index over all chunks
  4. On each query:
     a. Find the most relevant chunks using cosine similarity
     b. Feed those chunks as context to Claude
     c. Claude answers based ONLY on the context
     d. If not enough info, Claude says so instead of hallucinating
"""

import os
import math
import re
import sys
from pathlib import Path
from collections import defaultdict
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
MODEL = "claude-haiku-4-5-20251001"

DOCS_DIR = "docs"
CHUNK_SIZE = 300        # words per chunk
CHUNK_OVERLAP = 50      # words overlap between chunks
TOP_K = 3               # how many chunks to retrieve


# ── Step 1: Load and chunk documents ────────────────────────

def load_documents(docs_dir: str) -> list[dict]:
    documents = []
    for path in Path(docs_dir).glob("*.txt"):
        text = path.read_text(encoding="utf-8")
        documents.append({"filename": path.name, "text": text})
    return documents


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start += chunk_size - overlap
    return chunks


def build_chunks(documents: list[dict]) -> list[dict]:
    all_chunks = []
    for doc in documents:
        chunks = chunk_text(doc["text"], CHUNK_SIZE, CHUNK_OVERLAP)
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["filename"],
                "chunk_id": i,
                "text": chunk,
            })
    return all_chunks


# ── Step 2: TF-IDF Index ─────────────────────────────────────

def tokenize(text: str) -> list[str]:
    return re.findall(r"\b[a-z]{2,}\b", text.lower())


def build_tfidf_index(chunks: list[dict]) -> dict:
    N = len(chunks)
    tf = []
    df = defaultdict(int)

    for chunk in chunks:
        tokens = tokenize(chunk["text"])
        token_count = defaultdict(int)
        for t in tokens:
            token_count[t] += 1
        total = len(tokens) or 1
        tf_scores = {t: count / total for t, count in token_count.items()}
        tf.append(tf_scores)
        for t in tf_scores:
            df[t] += 1

    tfidf = []
    for tf_scores in tf:
        scores = {}
        for t, score in tf_scores.items():
            idf = math.log(N / (df[t] + 1)) + 1
            scores[t] = score * idf
        tfidf.append(scores)

    return {"tfidf": tfidf, "df": df, "N": N}


def cosine_similarity(vec_a: dict, vec_b: dict) -> float:
    common = set(vec_a) & set(vec_b)
    if not common:
        return 0.0
    dot = sum(vec_a[t] * vec_b[t] for t in common)
    mag_a = math.sqrt(sum(v**2 for v in vec_a.values()))
    mag_b = math.sqrt(sum(v**2 for v in vec_b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def query_tfidf(query: str, index: dict, top_k: int) -> list[tuple[int, float]]:
    tokens = tokenize(query)
    N = index["N"]
    df = index["df"]
    total = len(tokens) or 1

    token_count = defaultdict(int)
    for t in tokens:
        token_count[t] += 1

    query_vec = {}
    for t, count in token_count.items():
        tf = count / total
        idf = math.log(N / (df.get(t, 0) + 1)) + 1
        query_vec[t] = tf * idf

    scores = []
    for i, chunk_vec in enumerate(index["tfidf"]):
        sim = cosine_similarity(query_vec, chunk_vec)
        scores.append((i, sim))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


# ── Step 3: Generate answer with Claude ──────────────────────

SYSTEM_PROMPT = """You are a helpful Q&A assistant. You answer questions based ONLY on the context provided.

Rules you must follow:
1. Only use information from the provided context sections to answer.
2. If the context does not contain enough information to answer the question, say exactly: "I don't have enough information in my documents to answer this question."
3. Never make up facts or use outside knowledge.
4. Quote or paraphrase from the context when relevant.
5. Keep your answers concise and clear."""


def answer_question(question: str, context_chunks: list[dict]) -> str:
    context_text = ""
    for i, chunk in enumerate(context_chunks, 1):
        context_text += f"\n[Source: {chunk['source']}]\n{chunk['text']}\n"

    prompt = f"""Context:
{context_text}

Question: {question}

Answer:"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=512,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip()


# ── Main: Interactive Q&A loop ───────────────────────────────

def build_rag_system():
    print("Loading documents...")
    documents = load_documents(DOCS_DIR)
    if not documents:
        print(f"No .txt files found in '{DOCS_DIR}/' folder.")
        sys.exit(1)

    print(f"Loaded {len(documents)} documents:")
    for d in documents:
        print(f"  - {d['filename']}")

    chunks = build_chunks(documents)
    print(f"\nBuilt {len(chunks)} chunks (chunk size: {CHUNK_SIZE} words, overlap: {CHUNK_OVERLAP})")

    print("Building TF-IDF index...")
    index = build_tfidf_index(chunks)
    print("Index ready.\n")

    return chunks, index


def interactive_mode(chunks, index):
    print("="*60)
    print("  Mini-RAG — Ask questions about your documents")
    print("  Type 'quit' to exit | Type 'sources' to list docs")
    print("="*60 + "\n")

    while True:
        try:
            question = input("You: ").strip()
            if not question:
                continue
            if question.lower() == "quit":
                print("Goodbye!")
                break
            if question.lower() == "sources":
                sources = set(c["source"] for c in chunks)
                print("  Documents in knowledge base:")
                for s in sorted(sources):
                    print(f"    - {s}")
                print()
                continue

            # Retrieve
            top_results = query_tfidf(question, index, TOP_K)
            retrieved = [chunks[i] for i, score in top_results if score > 0.0]

            if not retrieved:
                print("Bot: I don't have enough information in my documents to answer this question.\n")
                continue

            # Show which sources were used
            print(f"  [Searching in: {', '.join(set(c['source'] for c in retrieved))}]")

            # Generate
            answer = answer_question(question, retrieved)
            print(f"\nBot: {answer}\n")

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break


def main():
    chunks, index = build_rag_system()
    interactive_mode(chunks, index)


if __name__ == "__main__":
    main()
