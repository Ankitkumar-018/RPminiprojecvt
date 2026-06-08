# Project 4: AI Pair-Programmed Endpoint — Approach & Planning

---

## Part A: Filled Example
> Read this before you start. This is how a backend developer thinks through building an API.

---

### Step 1 — Understand the Problem

**What exactly does this project need?**
- One REST API endpoint (we built a full Task Manager with 6)
- Tests for that endpoint
- A written log of where the AI helped and where you corrected it

**What is a REST API?**
A REST API lets other programs talk to your code over HTTP. It uses:
- URLs to identify resources (`/tasks`, `/tasks/123`)
- HTTP methods to say what to do (`GET` = read, `POST` = create, `PATCH` = update, `DELETE` = delete)
- JSON to send and receive data

---

### Step 2 — Questions to Ask Before Writing Code

- **What resource am I building an API for?**
  → Tasks (a to-do item with title, priority, completion status)

- **What operations make sense for this resource?**
  → Create a task, list all tasks, get one task, update a task, delete a task

- **Where do I store the data?**
  → An in-memory Python dictionary for simplicity (no database setup needed)

- **How do I give each task a unique ID?**
  → `uuid.uuid4()` — generates a random unique ID, no database counter needed

- **What should happen if invalid data is sent?**
  → Return a 400 error with a clear message explaining what's wrong

- **What HTTP status codes should I use?**
  → 200 (success), 201 (created), 400 (bad input), 404 (not found)

- **What is Flask?**
  → A Python library that makes it easy to define URL routes and handle HTTP requests

---

### Step 3 — Pseudo Code

```
DEFINE Flask app
DEFINE tasks = {} as empty dictionary (our in-memory store)

DEFINE ROUTE GET /tasks:
  get optional query params: completed, priority
  results = all tasks from dictionary
  IF completed param exists:
    filter results to only completed/not-completed tasks
  IF priority param exists:
    filter results by that priority
  RETURN JSON list of results + count, status 200

DEFINE ROUTE POST /tasks:
  data = parse JSON from request body
  IF no data or title is missing or empty:
    RETURN error JSON, status 400
  IF priority is not one of low/medium/high:
    RETURN error JSON, status 400
  task = create new task with UUID, title, description, priority, completed=False, timestamps
  store task in tasks dict using task id as key
  RETURN task JSON, status 201

DEFINE ROUTE GET /tasks/<task_id>:
  task = look up task_id in tasks dict
  IF not found:
    RETURN error JSON, status 404
  RETURN task JSON, status 200

DEFINE ROUTE PATCH /tasks/<task_id>:
  task = look up task_id in tasks dict
  IF not found: RETURN 404
  data = parse JSON from request body
  IF title in data: update task title (validate not empty)
  IF priority in data: update task priority (validate value)
  IF completed in data: update task completed (validate it is bool not string)
  update task updated_at timestamp
  RETURN updated task JSON, status 200

DEFINE ROUTE DELETE /tasks/<task_id>:
  IF task_id not in tasks dict: RETURN 404
  delete tasks[task_id]
  RETURN success message, status 200
```

---

### Step 4 — Think About Route Order

Flask matches routes from top to bottom. This causes a subtle bug:

```
# WRONG ORDER — Flask treats "stats" as a task_id:
@app.route("/tasks/<task_id>")   ← defined first
@app.route("/tasks/stats")        ← never reached!

# CORRECT ORDER:
@app.route("/tasks/stats")        ← specific route first
@app.route("/tasks/<task_id>")    ← dynamic route second
```

Always define specific routes before dynamic (parameter) routes.

---

### Step 5 — Plan the Tests Before Writing Them

For each endpoint, think: what should pass? what should fail?

```
POST /tasks:
  ✓ valid title → 201
  ✗ missing title → 400
  ✗ empty title → 400
  ✗ invalid priority → 400
  ✗ no body → 400

GET /tasks/<id>:
  ✓ valid ID → 200
  ✗ wrong ID → 404

PATCH /tasks/<id>:
  ✓ update title → 200
  ✓ mark completed=True → 200
  ✗ completed="yes" (string not bool) → 400
  ✗ wrong ID → 404
```

Write these BEFORE writing the test code — it forces you to think about edge cases.

---

### Step 6 — Where to Use AI and What to Watch For

**Good to ask AI:**
- "Generate the Flask boilerplate for a CRUD API"
- "Write pytest fixtures for a Flask app"
- "What HTTP status code should I use for a created resource?"

**Watch for these bugs in AI output:**
- Type coercion: `bool("false")` is `True` in Python — AI often misses this
- Route ordering: AI may not warn about static vs dynamic route conflicts
- Missing input validation: AI often forgets to check for empty strings after `.strip()`
- Using `datetime.utcnow()` which is deprecated in Python 3.12+

---

---

## Part B: Your Turn — Blank Template
> Fill this in BEFORE you start coding.

**Name:** ___________________________
**Date:** ___________________________

---

### Step 1 — What resource will your API manage?

```
Resource name:
What fields does it have?:
  1.
  2.
  3.
```

---

### Step 2 — Design Your Endpoints

Fill in the table:

```
Method | URL                | What it does          | Success code
-------|--------------------|-----------------------|-------------
       | /                  |                       |
       | /                  |                       |
       | /  /<id>           |                       |
       | /  /<id>           |                       |
       | /  /<id>           |                       |
```

---

### Step 3 — Your Pseudo Code (pick ONE endpoint and write it)

```
ENDPOINT: _______________

Pseudo code:




```

---

### Step 4 — Input Validation

**What inputs will you validate and how?**

```
Field 1: _______
  - What's invalid?:
  - Error message to return:

Field 2: _______
  - What's invalid?:
  - Error message to return:
```

---

### Step 5 — Plan Your Tests

**Before writing test code, list what you will test (pass and fail cases):**

```
My endpoint: _______________

Tests that should PASS (✓):
1.
2.

Tests that should FAIL with error (✗):
1.
2.
3.
```

---

### Step 6 — AI Collaboration Log (fill as you build)

| What I asked AI | What AI suggested | Did I use it? | What I changed and why |
|-----------------|-------------------|---------------|------------------------|
| | | | |
| | | | |
| | | | |

---

### Step 7 — After finishing, reflect

**What bug did you find in AI-generated code?**
```

```

**What does HTTP status 201 mean and when do you use it?**
```

```

**What is the difference between GET and POST?**
```

```
