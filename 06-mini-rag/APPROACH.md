# Project 6: Mini-RAG — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a developer thinks through building a RAG system.

---

### Step 1 — Understand the Problem

**What exactly does this project need?**
- A bot that can answer questions about documents you give it
- It should say "I don't know" when the answer isn't in the documents — not make things up
- No heavy framework — built from scratch

**What problem does RAG solve?**
Claude was trained up to a certain date and doesn't know your private documents. RAG fixes both:
1. Feed your documents to the system
2. Retrieve the relevant parts for each question
3. Give Claude only those parts as context
4. Claude answers based only on what you gave it

---

### Step 2 — Questions to Ask Before Writing Code

- **Why not just send the full document to Claude every time?**
  → Documents can be very long. Claude has a context limit (tokens). Sending a 100-page PDF every message is slow and expensive. RAG sends only the 2–3 most relevant paragraphs.

- **How do I find the "relevant" parts of a document?**
  → Represent both the question and each document chunk as vectors (lists of numbers). Find the chunk whose vector is closest to the question vector. We use TF-IDF for this.

- **What is TF-IDF?**
  → Term Frequency × Inverse Document Frequency. Words that appear often in one chunk but rarely across all chunks are more "important" to that chunk. This lets us score each chunk's relevance to a query.

- **What is cosine similarity?**
  → A way to measure how similar two vectors are, regardless of their size. A score of 1 = identical direction, 0 = totally different.

- **What is chunking and why do we need it?**
  → Documents are split into smaller pieces (chunks). If a document is 50 pages, we don't want to search the whole thing as one block — we want to find the specific paragraph that answers the question.

- **Why overlap between chunks?**
  → If we cut exactly at 300 words, a key sentence might get split. 50-word overlap ensures sentences aren't cut at boundaries.

---

### Step 3 — Pseudo Code

```
START

  LOAD all .txt files from docs/ folder
  FOR each document:
    split into chunks of ~300 words with 50-word overlap
    store chunks as list of {source, chunk_id, text}

  BUILD TF-IDF INDEX:
    FOR each chunk:
      tokenize (lowercase, letters only)
      count term frequency (TF) per word
    FOR each word:
      count how many chunks contain it (document frequency DF)
    FOR each chunk:
      TF-IDF score for word = TF × log(N / DF)
      store as vector (dictionary of word → score)

  LOOP:
    query = get input from user

    VECTORIZE query:
      tokenize query
      compute TF-IDF for each query word

    FOR each chunk vector:
      score = cosine_similarity(query_vector, chunk_vector)

    top_k = top 3 chunks sorted by score

    IF top_k is empty or all scores are 0:
      PRINT "I don't have enough information"
      continue

    BUILD context string from top_k chunk texts

    SEND to Claude:
      system: "Answer ONLY from the context. Say I don't know if not in context."
      user: "Context: [context_string] \n\n Question: [query]"

    PRINT Claude's answer

END
```

---

### Step 4 — Think About the Retrieval vs Generation Separation

This is the most important design insight:

```
RAG has TWO completely separate jobs:

Job 1: RETRIEVAL (pure Python, no LLM)
  Query → TF-IDF → cosine similarity → top-k chunks
  This is fast, cheap, deterministic

Job 2: GENERATION (LLM)
  Context chunks + question → Claude → answer
  This is where the intelligence happens

Keep these two jobs separate in your code.
retriever code stays in one section, generator call in another.
```

---

### Step 5 — The Anti-Hallucination Prompt

This is the key prompt design decision:

```
BAD:
"Answer this question: What is overfitting?"
→ Claude uses its training knowledge → may hallucinate or add info not in your docs

GOOD:
System: "You are a Q&A assistant. Answer ONLY from the context provided.
         If the context does not contain the answer, say exactly:
         'I don't have enough information in my documents to answer this.'"
User: "Context: [chunk1 text] [chunk2 text]
       Question: What is overfitting?"
→ Claude is grounded to your documents only
```

---

### Step 6 — What Could Go Wrong?

| Risk | How to handle it |
|------|-----------------|
| Bot always says "I don't know" | Query words don't appear in docs — try different phrasing |
| Bot answers with outside knowledge | Strengthen system prompt: "NEVER use outside knowledge" |
| Slow on large document sets | TF-IDF works for < 200 docs; use embeddings + FAISS for more |
| Chunk cuts a key sentence | Increase overlap from 50 to 100 words |
| File encoding error | Open with `encoding='utf-8', errors='ignore'` |

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start coding.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — What documents will your RAG system know about?

```
My documents (list the files you will add to docs/):
1.
2.
3.

Topic this RAG bot will answer questions about:

```

---

### Step 2 — Why is RAG needed? (In your own words)

```
What problem does Claude have without your documents?


How does RAG fix it?


```

---

### Step 3 — Explain Chunking

**What is chunking and why do you need it?**

```
Write here:


```

**What happens if the chunk size is too small (e.g., 20 words)?**

```
Write here:

```

**What happens if the chunk size is too large (e.g., 5000 words)?**

```
Write here:

```

---

### Step 4 — Your Pseudo Code for the Retrieval Step

```
Write just the retrieval part (not the generation):




```

---

### Step 5 — Design the Anti-Hallucination Prompt

Write the system prompt you will use to prevent Claude from making things up:

```
System prompt:




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

**Test: Ask a question the documents don't cover. What did the bot say?**
```

```

**What is the difference between TF-IDF and real embeddings (like sentence-transformers)?**
```

```

**What would break if you didn't chunk the documents and sent each full document as one block?**
```

```
