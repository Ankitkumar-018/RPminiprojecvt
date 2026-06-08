# Project 6: Mini-RAG Over Your Docs

## What Is This?

A **Retrieval-Augmented Generation (RAG)** system — the same architecture used inside ChatGPT's web browsing mode, Claude's document upload feature, and enterprise search tools — built from scratch without any framework.

You ask questions in plain English. The bot searches your documents, retrieves the most relevant chunks, and feeds them to Claude to generate an accurate answer. Crucially, if the answer isn't in the documents, **it says so instead of making things up**.

---

## What Skills You Will Learn

- What RAG is and why it exists (solves LLM hallucination + knowledge cutoff)
- How to chunk documents for retrieval
- TF-IDF (Term Frequency-Inverse Document Frequency) — a classic retrieval algorithm
- Cosine similarity for ranking results
- Prompt engineering for grounded Q&A (preventing hallucination)
- Building a complete pipeline from scratch — no LangChain, no vector database

---

## How RAG Works (The Pipeline)

```
Your Question
     │
     ▼
 Tokenize + TF-IDF vectorize the query
     │
     ▼
 Compare against all document chunks (cosine similarity)
     │
     ▼
 Retrieve top-3 most relevant chunks
     │
     ▼
 Build prompt: "Answer ONLY from this context: [chunks] \n Question: ..."
     │
     ▼
 Claude generates a grounded answer
     │
     ▼
 If context is empty → "I don't know"
```

---

## Why RAG? (The Problem It Solves)

| Problem | Without RAG | With RAG |
|---------|-------------|----------|
| Your private documents | Claude doesn't know them | Claude reads them |
| Hallucination | Claude invents facts | Claude cites only what's in the docs |
| Knowledge cutoff | Claude only knows up to training date | Works with any current doc |
| Cost | Sending full docs every time is expensive | Only relevant chunks are sent |

---

## Folder Structure

```
06-mini-rag/
├── rag.py               ← Full RAG system (load, chunk, index, retrieve, answer)
├── requirements.txt     ← anthropic SDK only
├── docs/                ← Your knowledge base (add any .txt files here)
│   ├── ml_basics.txt    ← Machine learning notes
│   ├── python_guide.txt ← Python programming guide
│   └── career_guide.txt ← Tech career and placement notes
└── README.md
```

---

## Requirements

- Python 3.10 or higher
- An Anthropic API key (free tier available at console.anthropic.com)
- No external ML libraries needed (TF-IDF built from scratch)

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 06-mini-rag
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

### Step 4 — Run the RAG bot

```bash
python rag.py
```

---

## Expected Output

### Startup
```
Loading documents...
Loaded 3 documents:
  - career_guide.txt
  - ml_basics.txt
  - python_guide.txt

Built 18 chunks (chunk size: 300 words, overlap: 50)
Building TF-IDF index...
Index ready.

============================================================
  Mini-RAG — Ask questions about your documents
  Type 'quit' to exit | Type 'sources' to list docs
============================================================
```

### Example Questions and Answers

```
You: What is overfitting?
  [Searching in: ml_basics.txt]

Bot: Overfitting happens when a model learns the training data too well,
including its noise, and performs poorly on new, unseen data. It has high
variance. Techniques to prevent overfitting include regularisation (L1/L2),
dropout, early stopping, and cross-validation.

---

You: How do I negotiate salary?
  [Searching in: career_guide.txt]

Bot: When negotiating salary, never reveal your expected salary first — let
them make an offer. Research the market rate on Glassdoor, Levels.fyi, and
LinkedIn Salary. Always negotiate, as 80% of offers have room to move up.
A common response is: "Based on my research and the market rate for this
role, I was expecting something in the range of X-Y LPA. Is there flexibility?"

---

You: What is the capital of France?
  [Searching in: ml_basics.txt, python_guide.txt, career_guide.txt]

Bot: I don't have enough information in my documents to answer this question.

---

You: What does list comprehension do in Python?
  [Searching in: python_guide.txt]

Bot: List comprehensions provide a concise way to create lists in Python.
For example: squares = [x**2 for x in range(10)] creates a list of squares.
You can also add conditions: even_squares = [x**2 for x in range(10) if x % 2 == 0].
Dict comprehensions work similarly: {word: len(word) for word in ["python", "java"]}.
```

---

## Key Design Decisions Explained

### Why TF-IDF instead of a vector database?

TF-IDF (Term Frequency × Inverse Document Frequency) is a classic algorithm that scores words by how important they are in a document relative to the whole corpus. It runs with zero external dependencies and works well on small document sets (< 100 docs).

For larger scale, you'd upgrade to dense embeddings (e.g., `sentence-transformers`) + a vector database (Pinecone, ChromaDB, FAISS).

### Why chunking with overlap?

Long documents are split into smaller chunks so the retriever can find specific sections. Overlap (50 words between chunks) prevents cutting a key sentence at a boundary.

### How hallucination is prevented

The system prompt tells Claude:
> "Only use information from the provided context. If the context does not contain enough information, say: I don't have enough information in my documents."

This is enforced by prompt design — no additional code needed.

---

## Add Your Own Documents

1. Create any `.txt` file in the `docs/` folder
2. Restart `python rag.py`
3. Ask questions about your document

The system picks up all `.txt` files automatically.

---

## Try It Yourself — Extension Ideas

- Add your own textbook chapter as a `.txt` file
- Change `TOP_K = 5` to retrieve more context
- Change `CHUNK_SIZE = 150` for finer-grained retrieval
- Upgrade from TF-IDF to real embeddings using `sentence-transformers`
- Add a `sources` list to each answer so users know which doc was used
- Try adding a PDF parser with `pypdf` to support PDF documents

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `AuthenticationError` | Wrong or missing API key | Set `ANTHROPIC_API_KEY` env variable |
| `No .txt files found` | `docs/` folder is empty or wrong path | Run from inside `06-mini-rag/` |
| Bot always says "I don't know" | Query words don't overlap with doc words | Try different phrasing or check doc content |
| `ModuleNotFoundError: anthropic` | SDK not installed | `pip install -r requirements.txt` |
