# Project 4: AI Pair-Programmed REST API Endpoint

## What Is This?

A fully working **Task Manager REST API** built with Python and Flask, with 6 endpoints, 20 passing tests, and a written log documenting exactly where the AI helped and where human correction was needed.

This project teaches you both how to build an API and how to critically evaluate AI-generated code.

---

## What Skills You Will Learn

- REST API design (HTTP methods, status codes, JSON responses)
- Flask framework — routing, request parsing, error handling
- Input validation — rejecting bad data with clear error messages
- Writing unit tests with `pytest` and Flask's test client
- Thinking critically about AI-generated code and spotting bugs

---

## How the API Works

```
HTTP Request (curl / Postman / frontend)
        │
        ▼
   Flask route matches the URL + method
        │
        ▼
   Validate input (title required? priority valid? correct type?)
        │           │
        ▼           ▼
   Process      Return 400 error
   the request  with clear message
        │
        ▼
   Read/write in-memory task store (Python dict)
        │
        ▼
   Return JSON response with correct status code
   (200 OK / 201 Created / 404 Not Found)
```

---

## Folder Structure

```
04-ai-pair-programmed-endpoint/
├── app.py                    ← Flask API — all 6 endpoints
├── requirements.txt          ← Flask + pytest
├── ai_collaboration_log.md   ← Where AI helped and where it was wrong
├── tests/
│   └── test_tasks.py         ← 20 tests covering every endpoint and edge case
└── README.md
```

---

## API Design

### Base URL: `http://localhost:5000`

| Method | Endpoint | What It Does |
|--------|----------|--------------|
| GET | `/tasks` | List all tasks (filter by `?completed=true` or `?priority=high`) |
| POST | `/tasks` | Create a new task |
| GET | `/tasks/stats` | Summary: total, completed, pending, by priority |
| GET | `/tasks/<id>` | Get one specific task by ID |
| PATCH | `/tasks/<id>` | Update a task (title / description / priority / completed) |
| DELETE | `/tasks/<id>` | Delete a task |

### Task Object

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Study for exam",
  "description": "Cover chapters 3 to 7",
  "priority": "high",
  "completed": false,
  "created_at": "2025-06-04T10:30:00Z",
  "updated_at": "2025-06-04T10:30:00Z"
}
```

---

## Requirements

- Python 3.7 or higher
- pip (comes with Python)

---

## Setup — Step by Step

### Step 1 — Go to the project folder

```bash
cd 04-ai-pair-programmed-endpoint
```

### Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Start the API server

```bash
python app.py
```

You will see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Keep this terminal open. Open a **new terminal** for the next steps.

### Step 4 — Create a task

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Study Flask", "priority": "high"}'
```

### Step 5 — List all tasks

```bash
curl http://localhost:5000/tasks
```

### Step 6 — Filter tasks by priority

```bash
curl "http://localhost:5000/tasks?priority=high"
```

### Step 7 — Mark a task as completed (replace with your actual ID)

```bash
curl -X PATCH http://localhost:5000/tasks/YOUR-TASK-ID \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

### Step 8 — Get stats

```bash
curl http://localhost:5000/tasks/stats
```

### Step 9 — Delete a task

```bash
curl -X DELETE http://localhost:5000/tasks/YOUR-TASK-ID
```

---

## Expected Output Examples

### POST /tasks — Create a task
```json
{
  "id": "3f7a1c2d-...",
  "title": "Study Flask",
  "description": "",
  "priority": "high",
  "completed": false,
  "created_at": "2025-06-04T10:00:00Z",
  "updated_at": "2025-06-04T10:00:00Z"
}
```

### GET /tasks/stats
```json
{
  "total": 3,
  "completed": 1,
  "pending": 2,
  "by_priority": {
    "low": 0,
    "medium": 1,
    "high": 2
  }
}
```

### Error Response (400 Bad Request)
```json
{
  "error": "'title' is required and cannot be empty"
}
```

---

## How the Code Works

### Route definition in Flask

```python
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title", "").strip()
    if not title:
        return jsonify({"error": "'title' is required"}), 400
    ...
    return jsonify(task), 201   ← 201 = Created
```

### Why UUID for task IDs?

```python
import uuid
task["id"] = str(uuid.uuid4())
# → "550e8400-e29b-41d4-a716-446655440000"
```

UUIDs are random and globally unique — no database counter needed. Works even if you restart the server and create tasks again — IDs will never clash.

### Route ordering matters in Flask

```python
@app.route("/tasks/stats", methods=["GET"])   # ← must come FIRST
def get_stats(): ...

@app.route("/tasks/<task_id>", methods=["GET"])  # ← comes SECOND
def get_task(task_id): ...
```

If `/tasks/<task_id>` is defined first, Flask treats the word "stats" as a task ID and routes `/tasks/stats` to the wrong function. This was a bug found during human review — see `ai_collaboration_log.md`.

---

## How to Run Tests

### Run all 20 tests

```bash
pytest tests/
```

### Run with verbose output (see each test name)

```bash
pytest tests/ -v
```

### Expected test output

```
tests/test_tasks.py::test_list_tasks_empty PASSED
tests/test_tasks.py::test_create_task_success PASSED
tests/test_tasks.py::test_create_task_missing_title PASSED
tests/test_tasks.py::test_update_task_mark_completed PASSED
tests/test_tasks.py::test_delete_task_success PASSED
...
20 passed in 0.15s
```

---

## HTTP Status Codes Used

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PATCH, DELETE |
| 201 | Created | Successful POST (new task created) |
| 400 | Bad Request | Missing title, wrong priority, wrong type |
| 404 | Not Found | Task ID doesn't exist |

---

## AI Collaboration Summary

Read [ai_collaboration_log.md](ai_collaboration_log.md) for the full log.

**Two real bugs found in AI-generated code:**

1. **Type-safety bug** — AI used `bool(data["completed"])` which makes `bool("false") = True` in Python. Human fixed it to `isinstance(data["completed"], bool)`.
2. **Flask route ordering bug** — `/tasks/stats` must be defined before `/tasks/<task_id>` or "stats" gets treated as an ID. AI did not warn about this.

**Takeaway:** AI is excellent at boilerplate and structure. You must review it carefully for subtle type-handling bugs and framework-specific behaviour.

---

## Try It Yourself — Extension Ideas

- Add a `due_date` field to tasks with date validation
- Add `GET /tasks?search=keyword` to search by title
- Save tasks to a JSON file so they persist after restarting the server
- Connect it to a real SQLite database using `flask-sqlalchemy`
- Build a simple HTML + JavaScript frontend that calls these endpoints

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: flask` | Flask not installed | Run `pip install -r requirements.txt` |
| `Address already in use` | Port 5000 is already occupied | Stop the other process or change port to 5001 in `app.py` |
| `404 Not Found` on a valid ID | Server was restarted (data lives in memory) | Data resets on restart — create the task again |
| `curl: command not found` on Windows | curl not installed | Use Postman (free) or install curl via winget |
| `pytest: command not found` | pytest not installed | Run `pip install pytest` |
